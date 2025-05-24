import threading
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from collections import OrderedDict

from purrfectmeow.kitty import kitty_logger

class LoadingModel:
    """
    A class responsible for managing the loading, caching, and preloading of Hugging Face models and tokenizers.

    This class uses a shared class-level in-memory cache and file-based cache to avoid redundant downloads of models
    and tokenizers from Hugging Face. It supports concurrent access and automatic eviction of older items based on a 
    maximum cache size.

    Class Attributes:
        DEFAULT_CACHE_PATH (str): Default directory path for caching models and tokenizers.
        DEFAULT_MAX_CACHE_SIZE (int): Default maximum number of items allowed in the cache.
        PRELOADED_TOKENIZER_IDS (list): A list of tokenizer model IDs to preload at class initialization.
        _cache_dir (Path): The directory on disk where resources are cached.
        _cache (OrderedDict): Class-level in-memory LRU cache for models and tokenizers.
        _cache_lock (threading.Lock): Thread lock for safe concurrent access to the cache.
        _max_cache_size (int): Maximum number of entries allowed in the cache.

    Class Methods:
        get_tokenizer(name: str) -> AutoTokenizer:
            Retrieves a tokenizer from the cache or downloads it.
        
        get_model(name: str) -> AutoModel:
            Retrieves a model from the cache or downloads it.
        
        set_path(path: str) -> None:
            Changes the cache directory path and clears the current in-memory cache.

    Internal Methods:
        _is_resource_cached(resource_dir: Path, is_tokenizer: bool) -> bool:
            Checks whether the resource is already cached on disk.
        
        _load_resource(name: str, is_tokenizer: bool):
            Loads the tokenizer or model from cache or downloads it if not available.
        
        _get_resource(name: str, is_tokenizer: bool):
            Retrieves or loads a resource, and updates the LRU cache.
        
        _preload_tokenizers() -> None:
            Preloads a list of commonly-used tokenizers.
    """
    _logger = kitty_logger(__name__)

    DEFAULT_CACHE_PATH = 'models_hf/'
    DEFAULT_MAX_CACHE_SIZE = 10
    PRELOADED_TOKENIZER_IDS = [
        "intfloat/multilingual-e5-large-instruct",
        # "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        # "Lajavaness/bilingual-embedding-large",
        # "BAAI/bge-m3",
        # "Snowflake/snowflake-arctic-embed-l-v2.0",
    ]

    _cache_dir = Path(DEFAULT_CACHE_PATH)
    _cache = OrderedDict()
    _cache_lock = threading.Lock()
    _max_cache_size = DEFAULT_MAX_CACHE_SIZE

    def __init__(self):
        self.__class__._cache_dir.mkdir(parents=True, exist_ok=True)
        self.__class__._logger.debug("Initialized LoadingModel with cache directory: %s", self._cache_dir)
        self.__class__._preload_tokenizers()

    @classmethod
    def _is_resource_cached(cls, resource_dir: Path, is_tokenizer: bool) -> bool:
        """
        Checks whether a given tokenizer or model is already cached locally on disk.

        Args:
            resource_dir (Path): Path to the local cache directory for the resource.
            is_tokenizer (bool): Whether the resource is a tokenizer (True) or model (False).

        Returns:
            bool: True if the resource is cached; False otherwise.
        """
        cache_file = 'tokenizer_config.json' if is_tokenizer else 'config.json'
        cached = (resource_dir / cache_file).exists()
        cls._logger.debug("Checking cache for %s at %s: %s",
                          "tokenizer" if is_tokenizer else "model", resource_dir, "found" if cached else "not found")
        return cached

    @classmethod
    def _load_resource(cls, name: str, is_tokenizer: bool):
        """
        Loads a Hugging Face model or tokenizer from local disk if cached, or downloads and caches it.

        Args:
            name (str): The Hugging Face identifier for the model or tokenizer.
            is_tokenizer (bool): True if loading a tokenizer, False if loading a model.

        Returns:
            Any: The loaded tokenizer or model object.

        Raises:
            ValueError: If loading fails due to network or cache issues.
        """
        resource_type = "tokenizer" if is_tokenizer else "model"
        resource_dir = cls._cache_dir / name.replace("/", "_")
        loader = AutoTokenizer if is_tokenizer else AutoModel
        cls._logger.debug("Loading %s: %s", resource_type, name)

        try:
            if cls._is_resource_cached(resource_dir, is_tokenizer):
                cls._logger.debug("Loading %s from local cache: %s", resource_type, resource_dir)
                return loader.from_pretrained(resource_dir)
            cls._logger.debug("Downloading %s from Hugging Face: %s", resource_type, name)
            return loader.from_pretrained(name, cache_dir=resource_dir)
        except Exception as e:
            cls._logger.error("Failed to load %s %s: %s", resource_type, name, str(e))
            raise ValueError(f"Cannot load {resource_type} for `{name}`: {str(e)}")

    @classmethod
    def _get_resource(cls, name: str, is_tokenizer: bool):
        """
        Retrieves a Hugging Face model or tokenizer from the class-level in-memory cache,
        or loads and caches it if not already present.

        Args:
            name (str): Hugging Face identifier for the model or tokenizer.
            is_tokenizer (bool): True if the resource is a tokenizer, False if it is a model.

        Returns:
            Any: The loaded and cached tokenizer or model.

        Raises:
            ValueError: If the provided name is not a string or loading fails.
        """
        if not isinstance(name, str):
            cls._logger.error("Invalid %s name: %s", "tokenizer" if is_tokenizer else "model", name)
            raise ValueError(f"Invalid {'tokenizer' if is_tokenizer else 'model'} name: `{name}`")

        resource_type = "tokenizer" if is_tokenizer else "model"
        key = (resource_type, name)
        with cls._cache_lock:
            if key in cls._cache:
                cls._logger.debug("Cache hit for %s: %s", resource_type, name)
                cls._cache.move_to_end(key)
                return cls._cache[key]

            cls._logger.debug("Cache miss for %s: %s, loading resource", resource_type, name)
            resource = cls._load_resource(name, is_tokenizer)
            cls._cache[key] = resource
            if len(cls._cache) > cls._max_cache_size:
                evicted_key = cls._cache.popitem(last=False)
                cls._logger.debug("Evicted %s from cache due to size limit: %s", evicted_key[0], evicted_key[1])
            cls._logger.debug("Successfully cached %s: %s", resource_type, name)
            return resource

    @classmethod
    def _preload_tokenizers(cls) -> None:
        """
        Preloads a predefined set of tokenizers into the cache for faster access.

        Logs any failures but does not raise exceptions to prevent preload errors from stopping execution.
        """
        cls._logger.debug("Starting preloading of tokenizers")
        for model_id in cls.PRELOADED_TOKENIZER_IDS:
            try:
                cls._get_resource(model_id, is_tokenizer=True)
                cls._logger.debug("Successfully preloaded tokenizer: %s", model_id)
            except Exception as e:
                cls._logger.warning("Failed to preload tokenizer %s: %s", model_id, str(e))

    @classmethod
    def get_tokenizer(cls, name: str) -> AutoTokenizer:
        """
        Class method to retrieve or load a tokenizer by its Hugging Face model identifier.

        This method uses a shared class-level cache to avoid redundant downloads or loads,
        ensuring efficient reuse across all instances or class-level calls.

        Args:
            name (str): The Hugging Face tokenizer identifier.

        Returns:
            AutoTokenizer: The loaded tokenizer object, either from cache or Hugging Face.

        Raises:
            ValueError: If the name is invalid or loading fails.
        """
        tokenizer = cls._get_resource(name, is_tokenizer=True)
        cls._logger.debug("Completed loading tokenizer: %s", name)
        return tokenizer

    @classmethod
    def get_model(cls, name: str) -> AutoModel:
        """
        Class method to retrieve or load a model by its Hugging Face model identifier.

        This method uses a shared class-level cache to avoid redundant downloads or loads,
        ensuring efficient reuse across all instances or class-level calls.

        Args:
            name (str): The Hugging Face model identifier.

        Returns:
            AutoModel: The loaded model object, either from cache or Hugging Face.

        Raises:
            ValueError: If the name is invalid or loading fails.
        """
        model = cls._get_resource(name, is_tokenizer=False)
        cls._logger.debug("Completed loading model: %s", name)
        return model