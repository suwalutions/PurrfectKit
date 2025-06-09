import os
import re
import threading
from pathlib import Path
from collections import OrderedDict
from transformers import AutoTokenizer, PreTrainedTokenizerBase

from purrfectmeow.kitty import kitty_logger

class HFTokeniker:
    """
    Lightweight manager for Hugging Face tokenizers with in-memory caching.

    Attributes
    ----------
    HF_MODEL_PATH : str
        Local path for storing cached tokenizer models.

    Public Methods
    --------------
    set_model_path(path)
        Set a custom path for the Hugging Face model cache directory.
    get_tokenizer(model_name)
        Retrieve a Hugging Face tokenizer by model name, using an in-memory cache for efficiency.

    Examples
    --------
    >>> hft = HFTokenizer()
    >>> hft.set_model_path("/paht/to/your/cache")
    >>> tokenizer = htf.get_tokenizer("bert-base-uncased")
    >>> tokenizer("Hello, World")
    """
    _logger = kitty_logger(__name__)
    
    HF_MODEL_PATH: str = '.cache/models/'

    _cache_dir = Path(HF_MODEL_PATH)
    _cache_lock = threading.Lock()
    _persistent_cache = OrderedDict()
    _max_cache_size = 10
    _is_initialized = False

    _preloaded_model_ids = [
        "intfloat/multilingual-e5-large-instruct",
        "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        "Lajavaness/bilingual-embedding-large",
        "BAAI/bge-m3",
        "Snowflake/snowflake-arctic-embed-l-v2.0",
    ]

    os.makedirs(HF_MODEL_PATH, exist_ok=True)
    _logger.debug("Hugging Face model cache directory initialized at: %s", HF_MODEL_PATH)

    @classmethod
    def _is_model_cached(cls, model_dir: Path) -> bool:
        """
        Check if a Hugging Face model or tokenizer is cached in the specified directory.

        Parameters
        ----------
        model_dir : Path
            The directory where the model or tokenizer is expected to be cached.

        Returns
        -------
        bool
            True if the model or tokenizer is cached, False otherwise.

        Notes
        -----
        This method checks for the presencs of a `tokenizer_config.json` file insise the model directory,
        which is an indicator that the tokenizer files are cached locally.
        """
        cls._logger.debug("Checking cache for model: %s", model_dir)
        cache_tokenizer = (model_dir / "tokenizer_config.json").exists()
        cls._logger.debug("Cache status for %s: %s", model_dir, "found" if cache_tokenizer else "not found")
        return cache_tokenizer

    @classmethod
    def _preload_tokenizers(cls) -> None:
        """
        Preload a predefined list of Hugging Face tokenizers into the in-memory cache.

        Notes
        -----
        - This method ensures that commonly used tokenizers are loaded into memory at startup to reduce latency during actual use.
        - It skips loading if tokenizers have already been initialized (controlled by `_is_initialized`).
        - It validates model IDs with a regex to ensure they conform to expecetd format ('namespace/model').
        - Tokenizers are stored in thread-safe manner within `_persistent_cache`.
        - When the cache exceeds its maximum size, the oldest tokenizer entry is evicted to manage memory usage.
        """
        cls._logger.debug("Preloading tokenizers...")
        if cls._is_initialized:
            cls._logger.debug("Tokenizers already preloaded, skipping.")
            return

        for model_id in cls._preloaded_model_ids:
            if not re.match(r'^[\w.-]+/[\w.-]+$', model_id):
                cls._logger.warning("Invalid model ID format: %s", model_id)
                cls._logger.debug("Skipping invalid model ID: %s", model_id)
                continue
            try:
                cls._logger.debug("Preloading tokenizer for model: %s", model_id)
                tokenizer = cls._load_tokenizer(model_id)
               
                with cls._cache_lock:
                    cls._persistent_cache[model_id] = tokenizer
                    cls._logger.debug("Preloaded tokenizer: %s", model_id)

                    if len(cls._persistent_cache) > cls._max_cache_size:
                        cls._persistent_cache.popitem(last=False)
                        cls._logger.debug("Cache size exceeded, removed oldest tokenizer.")
                    else:
                        cls._logger.debug("Current cache size: %d", len(cls._persistent_cache))

            except Exception as e:
                cls._logger.warning("Failed to preload %s: %s", model_id, str(e))

        cls._is_initialized = True

    @classmethod
    def _load_tokenizer(cls, model_name: str) -> PreTrainedTokenizerBase:
        """
        Load a Hugging Face tokenizer by its model name, checking the cache first.

        Parameters
        ----------
        model_name : str
            The Hugging Face model ID, e.g., 'bert-base-uncased'.

        Returns
        -------
        PreTrainedTokenizerBase
            The loaded tokenizer instance.

        Notes
        -----
        - Attempts to load the tokenizer from a local cache directory first to avoid unnecessary downloads.
        - If the local cache is missing or corrupted, it falls back to downloading from the Hugging Face Hub.
        - The cache directory name replaces '/' with '_' to form a valid folder name.
        """
        cls._logger.debug("Loading tokenizer for model: %s", model_name)
        model_dir = cls._cache_dir / model_name.replace("/", "_")

        if cls._is_model_cached(model_dir):
            try:
                cls._logger.debug("Loading from cache: %s", model_dir)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                cls._logger.debug("Tokenizer loaded from cache: %s", model_name)
                return tokenizer
            
            except Exception as e:
                cls._logger.warning("Cache load failed for %s: %s. Trying HF Hub.", model_dir, str(e))
        
        cls._logger.debug("Downloading tokenizer from Hugging Face Hub: %s", model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_dir)
        cls._logger.debug("Tokenizer loaded successfully: %s", model_name)
        return tokenizer

    @staticmethod
    def set_model_path(path: str) -> None:
        """
        Set a custom directory for caching Hugging Face tokenizers.

        Parameters
        ----------
        path : str
            A path to store cache.

        Notes
        -----
        This method resets the internal cache and reinitializes the tokenizer configuration. Any previously cached tokenizers will be cleared.
        """
        HFTokeniker._logger.debug("Setting custom cache path: %s", path)
        path_obj = Path(path).resolve()

        with HFTokeniker._cache_lock:
            HFTokeniker._cache_dir = path_obj
            HFTokeniker._cache_dir.mkdir(parents=True, exist_ok=True)
            HFTokeniker._persistent_cache.clear()
            HFTokeniker._is_initialized = False
            HFTokeniker._logger.debug("Cache path set to: %s", path_obj)

    @staticmethod
    def get_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
        """
        Retrieve a Hugging Face tokenizer by model name, using an in-memory cache for efficiency.

        Parameters
        ----------
        model_name : str
            The Hugging Face model ID, e.g., 'bert-base-uncased'.

        Returns
        -------
        PreTrainedTokenizerBase
            The loaded tokenizer instance.

        Raises
        ------
        ValueError
            If the provided model name is not a valid string or if loading fails.

        Notes
        -----
        - Uses an internal cache to improve performance.
        - `model_name` must follow the 'namespace/model' patterns.
        - Raises `ValueError` if the tokenizer cannot be loaded.
        - This static method relies on internal helpers and cahces.
        """
        HFTokeniker._logger.debug("Getting tokenizer for model: %s", model_name)
        HFTokeniker._preload_tokenizers()

        if not isinstance(model_name, str) or not re.match(r'^[\w-]+/[\w-]+$', model_name):
            HFTokeniker._logger.error("Invalid model name: %s", model_name)
            raise ValueError(f"Invalid model name: `{model_name}`")

        with HFTokeniker._cache_lock:
            if model_name in HFTokeniker._persistent_cache:
                HFTokeniker._logger.debug("Using cached tokenizer: %s", model_name)
                HFTokeniker._persistent_cache.move_to_end(model_name)
                return HFTokeniker._persistent_cache[model_name]

        HFTokeniker._logger.debug("Loading tokenizer: %s", model_name)
        try:
            tokenizer = HFTokeniker._load_tokenizer(model_name)
            HFTokeniker._logger.debug("Tokenizer loaded successfully: %s", model_name)
            with HFTokeniker._cache_lock:
                HFTokeniker._persistent_cache[model_name] = tokenizer
                
                if len(HFTokeniker._persistent_cache) > HFTokeniker._max_cache_size:
                    HFTokeniker._persistent_cache.popitem(last=False)
            return tokenizer
        except Exception as e:
            HFTokeniker._logger.error("Failed to load tokenizer %s: %s", model_name, str(e))
            raise ValueError(f"Cannot load tokenizer for `{model_name}`: {str(e)}")