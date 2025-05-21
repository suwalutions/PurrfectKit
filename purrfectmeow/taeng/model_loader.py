import os
import threading
from pathlib import Path
from collections import OrderedDict
from transformers import AutoTokenizer, AutoModel, PreTrainedTokenizerBase, PreTrainedModel
from typing import Union

from purrfectmeow.kitty import kitty_logger

class LoadingModel:
    """
    Manages the loading, caching, and reuse of Hugging Face tokenizers and models.

    This class provides a thread-safe mechanism to:
    - Cache downloaded models/tokenizers to disk and in memory,
    - Set a custom cache path,
    - Preload frequently used tokenizers,
    - Automatically evict old entries based on a defined cache size limit.

    Methods:
        - set_path(path): Define a custom cache directory.
        - get_tokenizer(name): Load or retrieve a tokenizer from cache.
        - get_model(name): Load or retrieve a model from cache.

    Attributes:
        DEFAULT_CACHE_PATH (str): Default filesystem path for caching resources.
        DEFAULT_MAX_CACHE_SIZE (dict): Maximum in-memory cache size for tokenizers and models.
        PRELOADED_TOKENIZER_IDS (List[str]): Tokenizer identifiers to preload at startup.
    """
    DEFAULT_CACHE_PATH = 'models_hf/'
    DEFAULT_MAX_CACHE_SIZE = {'tokenizer': 10, 'model': 5}
    PRELOADED_TOKENIZER_IDS = [
        "intfloat/multilingual-e5-large-instruct",
        "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        "Lajavaness/bilingual-embedding-large",
        "BAAI/bge-m3",
        "Snowflake/snowflake-arctic-embed-l-v2.0",
    ]

    def __init__(self):
        """
        Initialize internal caches, threading locks, and logger. Creates the cache directory if it doesn't exist.
        """
        self._cache_dir = Path(self.DEFAULT_CACHE_PATH)
        self._cache_lock = threading.Lock()
        self._tokenizer_cache = OrderedDict()
        self._model_cache = OrderedDict()
        self._max_cache_size = self.DEFAULT_MAX_CACHE_SIZE
        self._is_tokenizer_preloaded = False
        self._logger = kitty_logger(__name__)
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def set_path(self, path: str) -> None:
        """
        Set a custom directory for storing cached tokenizers and models.

        This will reset existing in-memory caches and reload from the new path.

        Args:
            path (str): Path to the new cache directory.

        Raises:
            ValueError: If the provided path does not exist or is not a directory.
        """
        path_obj = Path(path).resolve()
        if not path_obj.is_dir():
            self._logger.error("Invalid cache path: %s", path)
            raise ValueError(f"Invalid cache path: `{path}` is not a directory")

        with self._cache_lock:
            self._cache_dir = path_obj
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            self._tokenizer_cache.clear()
            self._model_cache.clear()
            self._is_tokenizer_preloaded = False
            self._logger.info("Cache path set to: %s", path_obj)

    def _is_resource_cached(self, resource_dir: Path, resource_type: str) -> bool:
        """
        Check if the specified resource (tokenizer or model) is already cached locally.

        Args:
            resource_dir (Path): Directory path where the resource is expected to be cached.
            resource_type (str): Either 'tokenizer' or 'model'.

        Returns:
            bool: True if the resource exists in the local cache, False otherwise.
        """
        cache_file = 'tokenizer_config.json' if resource_type == 'tokenizer' else 'config.json'
        return (resource_dir / cache_file).exists()

    def _load_resource(self, resource_name: str, resource_type: str) -> Union[PreTrainedTokenizerBase, PreTrainedModel]:
        """
        Load a tokenizer or model either from local cache or the Hugging Face Hub.

        Args:
            resource_name (str): Hugging Face resource identifier.
            resource_type (str): Either 'tokenizer' or 'model'.

        Returns:
            Union[PreTrainedTokenizerBase, PreTrainedModel]: The loaded tokenizer or model.
        """
        resource_dir = self._cache_dir / resource_name.replace("/", "_")
        loader_class = AutoTokenizer if resource_type == 'tokenizer' else AutoModel

        if self._is_resource_cached(resource_dir, resource_type):
            try:
                self._logger.debug("Loading %s from cache: %s", resource_type, resource_dir)
                return loader_class.from_pretrained(resource_dir)
            except Exception as e:
                self._logger.warning("Cache load failed for %s: %s. Trying HF Hugging Face.", resource_dir, str(e))

        self._logger.debug("Downloading %s: %s", resource_type, resource_name)
        return loader_class.from_pretrained(resource_name, cache_dir=resource_dir)

    def _preload_tokenizers(self) -> None:
        """
        Preload and cache tokenizers defined in PRELOADED_TOKENIZER_IDS.

        Tokenizers are loaded into memory only once per session to reduce repeated loading.
        """

        if self._is_tokenizer_preloaded:
            return

        self._logger.info("Preloading tokenizers")
        for model_id in self.PRELOADED_TOKENIZER_IDS:
            try:
                tokenizer = self._load_resource(model_id, 'tokenizer')
                with self._cache_lock:
                    self._tokenizer_cache[model_id] = tokenizer
                    if len(self._tokenizer_cache) > self._max_cache_size['tokenizer']:
                        self._tokenizer_cache.popitem(last=False)
            except Exception as e:
                self._logger.warning("Failed to preload %s: %s", model_id, str(e))

        self._is_tokenizer_preloaded = True

    def get_tokenizer(self, tokenizer_name: str) -> PreTrainedTokenizerBase:
        """
        Retrieve a tokenizer by name. If available in memory cache, it is returned directly.
        Otherwise, it is loaded from disk or downloaded, then cached.

        Args:
            tokenizer_name (str): Hugging Face tokenizer identifier (e.g., "bert-base-uncased").

        Returns:
            PreTrainedTokenizerBase: The requested tokenizer.

        Raises:
            ValueError: If the tokenizer name is not a valid string or fails to load.
        """
        self._preload_tokenizers()

        if not isinstance(tokenizer_name, str):
            self._logger.error("Invalid tokenizer name: %s", tokenizer_name)
            raise ValueError(f"Invalid tokenizer name: `{tokenizer_name}`")

        with self._cache_lock:
            if tokenizer_name in self._tokenizer_cache:
                self._logger.debug("Using cached tokenizer: %s", tokenizer_name)
                self._tokenizer_cache.move_to_end(tokenizer_name)
                return self._tokenizer_cache[tokenizer_name]

        self._logger.info("Loading tokenizer: %s", tokenizer_name)
        try:
            tokenizer = self._load_resource(tokenizer_name, 'tokenizer')
            with self._cache_lock:
                self._tokenizer_cache[tokenizer_name] = tokenizer
                if len(self._tokenizer_cache) > self._max_cache_size['tokenizer']:
                    self._tokenizer_cache.popitem(last=False)
            return tokenizer
        except Exception as e:
            self._logger.error("Failed to load tokenizer %s: %s", tokenizer_name, str(e))
            raise ValueError(f"Cannot load tokenizer for `{tokenizer_name}`: {str(e)}")

    def get_model(self, model_name: str) -> PreTrainedModel:
        """
        Retrieve a model by name. If available in memory cache, it is returned directly.
        Otherwise, it is loaded from disk or downloaded, then cached.

        Args:
            model_name (str): Hugging Face model identifier (e.g., "bert-base-uncased").

        Returns:
            PreTrainedModel: The requested model.

        Raises:
            ValueError: If the model name is not a valid string or fails to load.
        """
        if not isinstance(model_name, str):
            self._logger.error("Invalid model name: %s", model_name)
            raise ValueError(f"Invalid model name: `{model_name}`")

        with self._cache_lock:
            if model_name in self._model_cache:
                self._logger.debug("Using cached model: %s", model_name)
                self._model_cache.move_to_end(model_name)
                return self._model_cache[model_name]

        self._logger.info("Loading model: %s", model_name)
        try:
            model = self._load_resource(model_name, 'model')
            with self._cache_lock:
                self._model_cache[model_name] = model
                if len(self._model_cache) > self._max_cache_size['model']:
                    self._model_cache.popitem(last=False)
            return model
        except Exception as e:
            self._logger.error("Failed to load model %s: %s", model_name, str(e))
            raise ValueError(f"Cannot load model for `{model_name}`: {str(e)}")