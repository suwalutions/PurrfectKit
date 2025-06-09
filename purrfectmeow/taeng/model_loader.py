import threading
from pathlib import Path
from collections import OrderedDict
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

from purrfectmeow.kitty import kitty_logger

class LoadingModel:
    """
    A utility class for loading and caching Hugging Face tokenizers and models.

    Public Methods
    --------------
    get_hf_tokenizer(name)
        Retrieve or load a Hugging Face tokenizer by its identifier.
    get_hf_model(name)
        Retrieve or load a Hugging Face model by its identifier.
    get_st_model(name)
        Retrieve or load a SentenceTransformer model by its identifier.

    Example
    -------
    >>> loader = LoadingModel()
    >>> tokenizer = loader.get_hf_tokenizer("bert-base-uncased")
    >>> model = loader.get_hf_model("bert-base-uncased")
    >>> st_model = loader.get_st_model("sentence-transformers/all-MiniLM-L6-v2")
    """
    _logger = kitty_logger(__name__)

    DEFAULT_CACHE_PATH = '.cache/models/'
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
        """
        Initialize by creating the cache directory and preloading tokenizers
        """
        self.__class__._cache_dir.mkdir(parents=True, exist_ok=True)
        self.__class__._logger.debug("Initialized LoadingModel with cache directory: %s", self._cache_dir)
        self.__class__._preload_tokenizers()

    @classmethod
    def _is_resource_cached(cls, resource_dir: Path, is_tokenizer: bool) -> bool:
        """
        Check if the resource (tokenizer or model) is cached locally.

        Parameters
        ----------
        resource_dir : Path
            The directory where the resource is cached.

        is_tokenizer : bool
            True if checking for a tokenizer, False for a model.

        Returns
        -------
        bool: True if the resource is cached, False otherwise.

        Notes
        -----
        This method checks for a specific config file to verify the presence of the cached resource.
        """
        cache_file = 'tokenizer_config.json' if is_tokenizer else 'config.json'
        cached = (resource_dir / cache_file).exists()
        cls._logger.debug("Checking cache for %s at %s: %s", "tokenizer" if is_tokenizer else "model", resource_dir, "found" if cached else "not found")
        return cached

    @classmethod
    def _load_resource(cls, name: str, is_tokenizer: bool) -> AutoTokenizer | AutoModel:
        """
        Load a tokenizer or model from Hugging Face or local cache.

        Parameters
        ----------
        name : str
            The Hugging Face model or tokenizer identifier.

        is_tokenizer : bool
            True if loading a tokenizer, False for a model.

        Returns
        -------
        AutoTokenizer or AutoModel: The loaded resource object.

        Raises
        ------
        ValueError: If the resource cannot be loaded or is invalid.

        Notes
        -----
        This method attemps to load from local cache first, otherwise downloading from Hugging Face
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
    def _get_resource(cls, name: str, is_tokenizer: bool) -> AutoTokenizer | AutoModel:
        """
        Retrieve or load a tokenizer or model by its Hugging Face identifier.

        Parameters
        ----------
        name : str
            The Hugging Face model or tokenizer identifier.

        is_tokenizer : bool
            True if retrieving a tokenizer, False for a model.

        Returns
        -------
        AutoTokenizer or AutoModel: The loaded resource object.

        Raises
        ------
        ValueError: If the name is invalid or loading fails.

        Notes
        -----
        This method uses an LRU cache mechanism to manage memory usage efficiently.
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
        Preload a set of predefined tokenizers to optimize performance.

        Notes
        -----
        This method is typically called during initialization to reduce latency for common tokenizers.
        """
        cls._logger.debug("Starting preloading of tokenizers")
        for model_id in cls.PRELOADED_TOKENIZER_IDS:
            try:
                cls._get_resource(model_id, is_tokenizer=True)
                cls._logger.debug("Successfully preloaded tokenizer: %s", model_id)
            except Exception as e:
                cls._logger.warning("Failed to preload tokenizer %s: %s", model_id, str(e))

    @classmethod
    def get_hf_tokenizer(cls, name: str) -> AutoTokenizer:
        """
        Class method to retrieve or load a tokenizer by its Hugging Face model identifier.

        Parameters
        ----------
        name : str
            The Hugging Face tokenizer identifier.

        Returns
        -------
        AutoTokenizer: The loaded tokenizer object, either from cache or Hugging Face.

        Notes
        -----
        This method uses the internal caching mechanism to reduce redundant loading.
        """
        tokenizer = cls._get_resource(name, is_tokenizer=True)
        cls._logger.debug("Completed loading tokenizer: %s", name)
        return tokenizer

    @classmethod
    def get_hf_model(cls, name: str) -> AutoModel:
        """
        Class method to retrieve or load a Hugging Face model by its identifier.

        Parameters
        ----------
        name : str
            The Hugging Face model identifier.

        Returns
        -------
        AutoModel: The loaded model object, either from cache or Hugging Face.

        Notes
        -----
        This method uses the internal caching mechanism to manage memory and reuse models.
        """
        model = cls._get_resource(name, is_tokenizer=False)
        cls._logger.debug("Completed loading model: %s", name)
        return model
    
    @classmethod
    def get_st_model(cls, name: str) -> SentenceTransformer:
        """
        Class method to retrieve or load a SentenceTransformer model by its identifier.
        
        Parameters
        ----------
        name : str
            The SentenceTransformer model identifier.

        Returns
        -------
        SentenceTransformer: The loaded SentenceTransformer model object, either from cache or local.

        Notes
        -----
        This method loads models from local cache, and raise an error if model isn't already cached.
        """
        cls._logger.debug(f"Loading SentenceTransformer model: %s", name)
        model = SentenceTransformer(
            model_name_or_path=name, 
            cache_folder=cls._cache_dir, 
            local_files_only=True
        )
        return model