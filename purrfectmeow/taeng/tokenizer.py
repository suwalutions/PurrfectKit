import os
import re
import threading
from pathlib import Path
from collections import OrderedDict
from transformers import AutoTokenizer, PreTrainedTokenizerBase

from purrfectmeow.kitty import kitty_logger

class HFTokeniker:
    """
    A class to manage Hugging Face tokenizers with local caching and preloading support.

    This class allows efficient loading and reuse of Hugging Face tokenizers by caching
    them locally and maintaining a limited-size in-memory cache for quick access. It also
    supports preloading a predefined set of model tokenizers to speed up subsequent use.

    Attributes:
        HF_MODEL_PATH (str): Default path to store cached Hugging Face models.
        _cache_dir (Path): Directory path object pointing to the tokenizer cache location.
        _cache_lock (threading.Lock): Thread-safe lock for managing access to the tokenizer cache.
        _persistent_cache (OrderedDict): In-memory cache storing loaded tokenizers.
        _max_cache_size (int): Maximum number of tokenizers to hold in the in-memory cache.
        _is_initialized (bool): Flag to prevent repeated preloading of tokenizers.
        _preloaded_model_ids (List[str]): List of model names to preload on first use.
        _logger: Logger instance for logging events and errors.

    Methods:
        set_model_path(path: str) -> None:
            Set a custom directory path for tokenizer cache storage.

        get_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
            Retrieve a tokenizer by model name, loading from cache or Hugging Face Hub as needed.

    Internal Methods:
        _is_model_cached(model_dir: Path) -> bool:
            Check if the tokenizer is already cached locally.

        _preload_tokenizers() -> None:
            Preload tokenizers defined in `_preloaded_model_ids` into the in-memory cache.

        _load_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
            Load a tokenizer from the local cache or download it from the Hugging Face Hub.
    """
    HF_MODEL_PATH = 'models_hf/'
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

    _logger = kitty_logger(__name__)
    os.makedirs(HF_MODEL_PATH, exist_ok=True)

    @staticmethod
    def set_model_path(path: str) -> None:
        """
        Set the directory path for tokenizer cache storage.

        Args:
            path (str): Filesystem path to store or access cached tokenizers.

        Raises:
            ValueError: If the given path is not a valid directory.
        """
        path_obj = Path(path).resolve()
        if not path_obj.is_dir():
            HFTokeniker._logger.error("Invalid cache path: %s", path)
            raise ValueError(f"Invalid cache path: `{path}` is not a directory")

        with HFTokeniker._cache_lock:
            HFTokeniker._cache_dir = path_obj
            HFTokeniker._cache_dir.mkdir(parents=True, exist_ok=True)
            HFTokeniker._persistent_cache.clear()
            HFTokeniker._is_initialized = False
            HFTokeniker._logger.info("Cache path set to: %s", path_obj)

    @classmethod
    def _is_model_cached(cls, model_dir: Path) -> bool:
        """
        Check if the specified model directory contains a cached tokenizer.

        Args:
            model_dir (Path): Path to the model's cache directory.

        Returns:
            bool: True if the tokenizer is cached, False otherwise.
        """
        return (model_dir / "tokenizer_config.json").exists()

    @classmethod
    def _preload_tokenizers(cls) -> None:
        """
        Preload tokenizers listed in `_preloaded_model_ids` into the in-memory cache.

        Tokenizers are downloaded or loaded from the cache and stored in an LRU-style
        in-memory cache for fast access.
        """
        if cls._is_initialized:
            return

        cls._logger.info("Preloading tokenizers")
        for model_id in cls._preloaded_model_ids:
            if not re.match(r'^[\w.-]+/[\w.-]+$', model_id):
                cls._logger.warning("Invalid model ID: %s", model_id)
                continue
            try:
                tokenizer = cls._load_tokenizer(model_id)
                with cls._cache_lock:
                    cls._persistent_cache[model_id] = tokenizer
                    if len(cls._persistent_cache) > cls._max_cache_size:
                        cls._persistent_cache.popitem(last=False)
            except Exception as e:
                cls._logger.warning("Failed to preload %s: %s", model_id, str(e))

        cls._is_initialized = True

    @classmethod
    def _load_tokenizer(cls, model_name: str) -> PreTrainedTokenizerBase:
        """
        Load a tokenizer by name from cache or Hugging Face Hub.

        If the tokenizer exists in the local cache, it is loaded from disk.
        Otherwise, it is downloaded from the Hugging Face Hub and cached.

        Args:
            model_name (str): Model ID in the format 'org/model-name'.

        Returns:
            PreTrainedTokenizerBase: The loaded tokenizer instance.

        Raises:
            Exception: If loading fails from both cache and remote source.
        """
        model_dir = cls._cache_dir / model_name.replace("/", "_")
        if cls._is_model_cached(model_dir):
            try:
                cls._logger.debug("Loading from cache: %s", model_dir)
                return AutoTokenizer.from_pretrained(model_dir)
            except Exception as e:
                cls._logger.warning("Cache load failed for %s: %s. Trying HF Hub.", model_dir, str(e))

        cls._logger.debug("Downloading tokenizer: %s", model_name)
        return AutoTokenizer.from_pretrained(model_name, cache_dir=model_dir)

    @staticmethod
    def get_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
        """
        Retrieve a tokenizer for the specified Hugging Face model.

        The tokenizer is returned from the in-memory cache if available.
        Otherwise, it is loaded from disk or downloaded, and then cached.

        Args:
            model_name (str): The Hugging Face model ID, e.g., 'bert-base-uncased'.

        Returns:
            PreTrainedTokenizerBase: The tokenizer instance.

        Raises:
            ValueError: If the model name is invalid or tokenizer cannot be loaded.
        """
        HFTokeniker._preload_tokenizers()

        if not isinstance(model_name, str) or not re.match(r'^[\w-]+/[\w-]+$', model_name):
            HFTokeniker._logger.error("Invalid model name: %s", model_name)
            raise ValueError(f"Invalid model name: `{model_name}`")

        with HFTokeniker._cache_lock:
            if model_name in HFTokeniker._persistent_cache:
                HFTokeniker._logger.debug("Using cached tokenizer: %s", model_name)
                HFTokeniker._persistent_cache.move_to_end(model_name)
                return HFTokeniker._persistent_cache[model_name]

        HFTokeniker._logger.info("Loading tokenizer: %s", model_name)
        try:
            tokenizer = HFTokeniker._load_tokenizer(model_name)
            with HFTokeniker._cache_lock:
                HFTokeniker._persistent_cache[model_name] = tokenizer
                if len(HFTokeniker._persistent_cache) > HFTokeniker._max_cache_size:
                    HFTokeniker._persistent_cache.popitem(last=False)
            return tokenizer
        except Exception as e:
            HFTokeniker._logger.error("Failed to load tokenizer %s: %s", model_name, str(e))
            raise ValueError(f"Cannot load tokenizer for `{model_name}`: {str(e)}")
