import threading
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from collections import OrderedDict

from purrfectmeow.kitty import kitty_logger

class LoadingModel:
    """
    A class responsible for managing the loading, caching, and preloading of Hugging Face models and tokenizers.

    Attributes:
        DEFAULT_CACHE_PATH (str): Default directory path for caching models and tokenizers.
        DEFAULT_MAX_CACHE_SIZE (int): Default maximum cache size before eviction occurs.
        PRELOADED_TOKENIZER_IDS (list): A list of predefined tokenizer IDs to preload.
        _cache_dir (Path): Directory where models and tokenizers are cached.
        _cache (OrderedDict): In-memory cache for storing loaded models and tokenizers.
        _cache_lock (threading.Lock): Lock for synchronizing access to the cache.
        _max_cache_size (int): Maximum allowed cache size before evicting old items.

    Methods:
        set_path(self, path: str) -> None:
            Sets a new cache path and clears the current in-memory cache.
        
        get_tokenizer(self, name: str):
            Retrieves a tokenizer by its name from the cache or downloads it if not present.
        
        get_model(self, name: str):
            Retrieves a model by its name from the cache or downloads it if not present.

    Interna Methods:
        __init__(self):
            Initializes the class, setting up the cache directory, cache size, and logger, and preloads the tokenizers.
        
        _is_resource_cached(self, resource_dir: Path, is_tokenizer: bool) -> bool:
            Checks if the resource (model or tokenizer) is already cached in the specified directory.
        
        _load_resource(self, name: str, is_tokenizer: bool):
            Loads a model or tokenizer from the cache or downloads it from Hugging Face if not cached.
        
        _preload_tokenizers(self) -> None:
            Preloads a predefined list of tokenizers and logs the success or failure of each attempt.
        
        _get_resource(self, name: str, is_tokenizer: bool):
            Retrieves a model or tokenizer from the cache, or loads it if not present, and caches it.
    """
    _logger = kitty_logger(__name__)

    DEFAULT_CACHE_PATH = 'models_hf/'
    DEFAULT_MAX_CACHE_SIZE = 10
    PRELOADED_TOKENIZER_IDS = [
        "intfloat/multilingual-e5-large-instruct",
        "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        "Lajavaness/bilingual-embedding-large",
        "BAAI/bge-m3",
        "Snowflake/snowflake-arctic-embed-l-v2.0",
    ]

    def __init__(self):
        """Initializes the LoadingModel instance.

        Sets up the cache directory, in-memory cache, thread lock, logger, and preloads a set of predefined tokenizers.
        """
        self._cache_dir = Path(self.DEFAULT_CACHE_PATH)
        self._cache = OrderedDict()
        self._cache_lock = threading.Lock()
        self._max_cache_size = self.DEFAULT_MAX_CACHE_SIZE
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._logger.debug("Initialized LoadingModel with cache directory: %s", self._cache_dir)
        self._preload_tokenizers()

    def set_path(self, path: str) -> None:
        """Sets a new cache path and clears the in-memory cache.

        Args:
            path (str): The new path to be used for caching resources.

        Raises:
            ValueError: If the provided path is not a valid directory.
        """
        path_obj = Path(path).resolve()
        if not path_obj.is_dir():
            self._logger.error("Invalid cache path provided: %s is not a directory", path)
            raise ValueError(f"Invalid cache path: `{path}` is not a directory")
        with self._cache_lock:
            self._logger.debug("Setting new cache path: %s", path_obj)
            self._cache_dir = path_obj
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            self._cache.clear()
            self._logger.debug("Cleared in-memory cache due to path change")
            self._preload_tokenizers()

    def _is_resource_cached(self, resource_dir: Path, is_tokenizer: bool) -> bool:
        """Checks if a resource (tokenizer or model) is already cached locally.

        Args:
            resource_dir (Path): The path where the resource should be cached.
            is_tokenizer (bool): Whether the resource is a tokenizer (True) or model (False).

        Returns:
            bool: True if the resource is found in the cache, False otherwise.
        """
        cache_file = 'tokenizer_config.json' if is_tokenizer else 'config.json'
        cached = (resource_dir / cache_file).exists()
        self._logger.debug("Checking cache for %s at %s: %s", 
                          "tokenizer" if is_tokenizer else "model", resource_dir, "found" if cached else "not found")
        return cached

    def _load_resource(self, name: str, is_tokenizer: bool):
        """Loads a tokenizer or model from cache or downloads it from Hugging Face.

        Args:
            name (str): The Hugging Face model or tokenizer identifier.
            is_tokenizer (bool): Whether to load a tokenizer (True) or model (False).

        Returns:
            Any: The loaded tokenizer or model object.

        Raises:
            ValueError: If the resource cannot be loaded.
        """
        resource_type = "tokenizer" if is_tokenizer else "model"
        resource_dir = self._cache_dir / name.replace("/", "_")
        loader = AutoTokenizer if is_tokenizer else AutoModel
        self._logger.debug("Loading %s: %s", resource_type, name)
        
        try:
            if self._is_resource_cached(resource_dir, is_tokenizer):
                self._logger.debug("Loading %s from local cache: %s", resource_type, resource_dir)
                return loader.from_pretrained(resource_dir)
            self._logger.debug("Downloading %s from Hugging Face: %s", resource_type, name)
            return loader.from_pretrained(
                name, 
                cache_dir=resource_dir, 
                # trust_remote_code=True
            )
        except Exception as e:
            self._logger.error("Failed to load %s %s: %s", resource_type, name, str(e))
            raise ValueError(f"Cannot load {resource_type} for `{name}`: {str(e)}")

    def _preload_tokenizers(self) -> None:
        """Preloads a predefined list of tokenizers into the cache.

        Logs success or failure of each tokenizer load attempt.
        """
        self._logger.debug("Starting preloading of tokenizers")
        for model_id in self.PRELOADED_TOKENIZER_IDS:
            try:
                self._get_resource(model_id, is_tokenizer=True)
                self._logger.debug("Successfully preloaded tokenizer: %s", model_id)
            except Exception as e:
                self._logger.warning("Failed to preload tokenizer %s: %s", model_id, str(e))

    def _get_resource(self, name: str, is_tokenizer: bool):
        """Retrieves a resource from cache or loads it if not cached.

        Args:
            name (str): The Hugging Face model or tokenizer identifier.
            is_tokenizer (bool): Whether to retrieve a tokenizer (True) or model (False).

        Returns:
            Any: The tokenizer or model object.

        Raises:
            ValueError: If the name is not a string or resource fails to load.
        """
        if not isinstance(name, str):
            self._logger.error("Invalid %s name: %s", "tokenizer" if is_tokenizer else "model", name)
            raise ValueError(f"Invalid {'tokenizer' if is_tokenizer else 'model'} name: `{name}`")
        
        resource_type = "tokenizer" if is_tokenizer else "model"
        key = (resource_type, name)
        with self._cache_lock:
            if key in self._cache:
                self._logger.debug("Cache hit for %s: %s", resource_type, name)
                self._cache.move_to_end(key)
                return self._cache[key]
            
            self._logger.debug("Cache miss for %s: %s, loading resource", resource_type, name)
            resource = self._load_resource(name, is_tokenizer)
            self._cache[key] = resource
            if len(self._cache) > self._max_cache_size:
                evicted_key = self._cache.popitem(last=False)
                self._logger.debug("Evicted %s from cache due to size limit: %s", evicted_key[0], evicted_key[1])
            self._logger.debug("Successfully cached %s: %s", resource_type, name)
            return resource

    def get_tokenizer(self, name: str) -> AutoTokenizer:
        """Retrieves or loads a tokenizer by name and returns it.

        Args:
            name (str): The Hugging Face tokenizer identifier.

        Returns:
            AutoTokenizer: The tokenizer object.
        """
        pre_loaded = self._get_resource(name, is_tokenizer=True)
        self._logger.debug("Completed preloading tokenizer: %s", name)
        return pre_loaded

    def get_model(self, name: str) -> AutoModel:
        """Retrieves or loads a model by name and returns it.

        Args:
            name (str): The Hugging Face model identifier.

        Returns:
            AutoModel: The model object.
        """
        pre_loaded = self._get_resource(name, is_tokenizer=False)
        self._logger.debug("Completed preloading model: %s", name)
        return pre_loaded