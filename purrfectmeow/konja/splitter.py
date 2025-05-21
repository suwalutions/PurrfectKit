from typing import Optional
from langchain_text_splitters import TokenTextSplitter, CharacterTextSplitter
from functools import lru_cache

from purrfectmeow.taeng import Suphalaks
from purrfectmeow.kitty import kitty_logger

class Splitter:
    """
    A utility class for creating text splitters for token-based and character-based segmentation.

    Provides factory methods for generating `TokenTextSplitter` and `CharacterTextSplitter` instances,
    supporting OpenAI and HuggingFace tokenizers for flexible text preprocessing. This is particularly
    useful for handling long documents that need to be split into manageable chunks for tasks such as
    embedding generation, summarization, or semantic search.

    Attributes:
        DEFAULT_CHUNK_SIZE (int): Default chunk size (tokens or characters). Defaults to 500.
        DEFAULT_CHUNK_OVERLAP (int): Default chunk overlap. Defaults to 0.
        MAX_CHUNK_SIZE (int): Maximum chunk size to prevent memory issues. Defaults to 10,000.
        SUPPORTED_OPENAI_MODELS (set): Supported OpenAI model names for tiktoken tokenizer.

    Methods:
        create_token_splitter(model_name, chunk_size=None, chunk_overlap=None) -> TokenTextSplitter:
            Creates a token-based splitter using either an OpenAI or HuggingFace tokenizer based on the model name.
        create_character_splitter(separator='\n\n', chunk_size=None, chunk_overlap=None) -> CharacterTextSplitter:
            Creates a character-based splitter using a specified separator (e.g., paragraph or sentence).

    Internal Methods:
        _get_huggingface_tokenizer(model_name) -> tokenizer:
            Loads and caches a HuggingFace tokenizer for the specified model name.
        _validate_string_param(param, param_name, method) -> None:
            Validates that a string parameter is non-empty and non-whitespace.
        _validate_and_set_chunk_params(chunk_size, chunk_overlap, method) -> tuple[int, int]:
            Validates chunk size and overlap parameters, returning resolved values.
        _log_splitter_creation(method, params) -> None:
            Logs the creation of a splitter with the given parameters.
    """
    _logger = kitty_logger(__name__)
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 0
    SUPPORTED_OPENAI_MODELS = {
        "text-embedding-ada-002",
        "text-embedding-3-large",
        "text-embedding-3-small"
    }
    MAX_CHUNK_SIZE = 10000

    @staticmethod
    @lru_cache(maxsize=32)
    def _get_huggingface_tokenizer(model_name: str):
        """
        Load and cache a HuggingFace tokenizer for the specified model.

        This method retrieves a tokenizer using `Suphalaks.get_tokenizer` and caches
        the result for future use to improve performance.

        Args:
            model_name (str): The name or path of the model for which to load the tokenizer.

        Returns:
            PreTrainedTokenizer: A tokenizer instance corresponding to the given model.

        Raises:
            RuntimeError: If no tokenizer is found for the specified model name.
        """
        tokenizer = Suphalaks.get_tokenizer(model_name)
        if tokenizer is None:
            raise RuntimeError(f"No tokenizer found for model '{model_name}'")
        return tokenizer

    @classmethod
    def _validate_string_param(cls, param: str, param_name: str, method: str) -> None:
        """
        Validate that a given string parameter is non-empty and not just whitespace.

        Args:
            param (str): The parameter to validate.
            param_name (str): The name of the parameter (used in error messages).
            method (str): The name of the method invoking this validation (for logging).

        Raises:
            ValueError: If the parameter is empty or contains only whitespace.
        """
        if not param or not isinstance(param, str) or not param.strip():
            cls._logger.error(f"{param_name} must be a non-empty, non-whitespace string in {method}")
            raise ValueError(f"{param_name} must be a non-empty, non-whitespace string")

    @classmethod
    def _validate_and_set_chunk_params(
        cls, chunk_size: Optional[int], chunk_overlap: Optional[int], method: str
    ) -> tuple[int, int]:
        """
        Validate and resolve chunking parameters: chunk size and chunk overlap.

        If either parameter is `None`, default class values are used.
        Validation ensures values are within acceptable ranges.

        Args:
            chunk_size (Optional[int]): Desired size of each chunk.
            chunk_overlap (Optional[int]): Desired overlap between chunks.
            method (str): The name of the method invoking this validation (for logging).

        Returns:
            tuple[int, int]: Validated chunk size and chunk overlap.

        Raises:
            ValueError: If chunk size is non-positive, exceeds the maximum allowed,
                        or if chunk overlap is negative or greater than/equal to chunk size.
        """
        chunk_size = chunk_size if chunk_size is not None else cls.DEFAULT_CHUNK_SIZE
        chunk_overlap = chunk_overlap if chunk_overlap is not None else cls.DEFAULT_CHUNK_OVERLAP

        if chunk_size <= 0:
            cls._logger.error(f"Chunk size must be positive, got {chunk_size} in {method}")
            raise ValueError("Chunk size must be positive")
        if chunk_size > cls.MAX_CHUNK_SIZE:
            cls._logger.error(f"Chunk size ({chunk_size}) exceeds maximum ({cls.MAX_CHUNK_SIZE}) in {method}")
            raise ValueError(f"Chunk size exceeds maximum ({cls.MAX_CHUNK_SIZE})")
        if chunk_overlap < 0:
            cls._logger.error(f"Chunk overlap must be non-negative, got {chunk_overlap} in {method}")
            raise ValueError("Chunk overlap must be non-negative")
        if chunk_overlap >= chunk_size:
            cls._logger.error(f"Chunk overlap ({chunk_overlap}) must be less than chunk size ({chunk_size}) in {method}")
            raise ValueError("Chunk overlap must be less than chunk size")

        return chunk_size, chunk_overlap

    @classmethod
    def _log_splitter_creation(cls, method: str, params: dict) -> None:
        """
        Log the creation of a splitter with the provided parameters.

        Args:
            method (str): The name of the method that initiated the splitter creation.
            params (dict): A dictionary of parameters used in the splitter creation.
        """
        param_str = ", ".join(f"{k}={v}" for k, v in params.items())
        cls._logger.debug(f"Creating {method} with {param_str}")

    @classmethod
    def create_token_splitter(
        cls,
        model_name: str,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> TokenTextSplitter:
        """Create a TokenTextSplitter for the specified model.

        Args:
            model_name (str): Model name for the tokenizer (e.g., 'text-embedding-ada-002' or HuggingFace model ID).
            chunk_size (Optional[int]): Size of each chunk in tokens. Defaults to DEFAULT_CHUNK_SIZE.
            chunk_overlap (Optional[int]): Overlap between chunks in tokens. Defaults to DEFAULT_CHUNK_OVERLAP.

        Returns:
            TokenTextSplitter: A configured text splitter instance.

        Raises:
            ValueError: If model_name or chunk parameters are invalid.
            RuntimeError: If the tokenizer cannot be created.

        Example:
            >>> splitter = Splitter.create_token_splitter("text-embedding-ada-002", chunk_size=1000, chunk_overlap=100)
            >>> chunks = splitter.split_text("This is a sample text to split.")
        """
        cls._validate_string_param(model_name, "Model name", "create_token_splitter")
        chunk_size, chunk_overlap = cls._validate_and_set_chunk_params(chunk_size, chunk_overlap, "create_token_splitter")
        cls._log_splitter_creation("token splitter", {"model_name": model_name, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})

        try:
            if model_name in cls.SUPPORTED_OPENAI_MODELS:
                cls._logger.debug(f"Using OpenAI tokenizer for model '{model_name}'")
                return TokenTextSplitter.from_tiktoken_encoder(
                    model_name=model_name,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
            cls._logger.debug(f"Using HuggingFace tokenizer for model '{model_name}'")
            tokenizer = cls._get_huggingface_tokenizer(model_name)
            return TokenTextSplitter.from_huggingface_tokenizer(
                tokenizer=tokenizer,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        except (ValueError, ImportError) as e:
            cls._logger.exception(f"Failed to create splitter for model '{model_name}'")
            raise RuntimeError(f"Failed to create splitter for model '{model_name}': {str(e)}") from e

    @classmethod
    def create_character_splitter(
        cls,
        separator: str = "\n\n",
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> CharacterTextSplitter:
        """Create a CharacterTextSplitter with the specified separator.

        Args:
            separator (str): Separator to split text (e.g., '\n\n' for paragraphs). Defaults to '\n\n'.
            chunk_size (Optional[int]): Size of each chunk in characters. Defaults to DEFAULT_CHUNK_SIZE.
            chunk_overlap (Optional[int]): Overlap between chunks in characters. Defaults to DEFAULT_CHUNK_OVERLAP.

        Returns:
            CharacterTextSplitter: A configured character-based text splitter instance.

        Raises:
            ValueError: If separator or chunk parameters are invalid.

        Example:
            >>> splitter = Splitter.create_character_splitter(separator=".", chunk_size=200, chunk_overlap=20)
            >>> chunks = splitter.split_text("Sentence one. Sentence two.")
        """
        cls._validate_string_param(separator, "Separator", "create_character_splitter")
        chunk_size, chunk_overlap = cls._validate_and_set_chunk_params(chunk_size, chunk_overlap, "create_character_splitter")
        cls._log_splitter_creation("character splitter", {"separator": separator, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})

        return CharacterTextSplitter(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )