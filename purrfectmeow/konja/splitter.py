from typing import Optional, List
from functools import lru_cache
from langchain_text_splitters import TokenTextSplitter
from purrfectmeow.taeng.model_loader import LoadingModel

from purrfectmeow.kitty import kitty_logger

class Splitter:
    """
    A utility class for creating text splitters for token-based and separator-based segmentation.

    Attributes
    ----------
    DEFAULT_CHUNK_SIZE : int
    DEFAULT_CHUNK_OVERLAP : int
    MAX_CHUNK_SIZE : int
    SUPPORTED_OPENAI_MODELS : dict

    Public Methods
    --------------
    create_token_splitter(model_name, chunk_size, chunk_overlap)
        Creates a token-based splitter using either an OpenAI or HuggingFace tokenizer based on the model name.
    create_separator_splitter(separator)
        Creates a separator-based splitter using a specified separator (e.g., paragraph or sentence).

    Examples
    --------
    >>> splitter = Splitter.create_token_splitter("text-embedding-ada-002", chunk_size=256, chunk_overlap=32)
    >>> chunks = splitter.split_text("สวัสดีครับ นี่คือข้อความที่เราจะทำการแบ่งออกเป็นหลายตอน...")

    >>> separator_splitter = Splitter.create_separator_splitter("\n\n")
    >>> parts = separator_splitter.split_text("ย่อหน้าแรก\n\nย่อหน้าที่สอง\n\nย่อหน้าที่สาม")
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

    @classmethod
    @lru_cache(maxsize=32)
    def _get_huggingface_tokenizer(cls, model_name: str):
        """
        Load and cache a HuggingFace tokenizer for the specified model.

        Parameters
        ----------
        model_name : str
            The name or path of the model for which to load the tokenizer.

        Returns
        -------
        PreTrainedTokenizer
            A tokenizer instance corresponding to the given model.

        Raises
        ------
        RuntimeError
            If no tokenizer is found for the specified model name.

        Notes
        -----
        - This method helps improve performance when called repeatedly with the same model name.
        - Tokenizer is loaded through `LoadingModel.get_hf_tokenizer()` and cached using lru_cache.
        """
        cls._logger.debug(f"Loading HuggingFace tokenizer for model '{model_name}'")
        tokenizer = LoadingModel.get_hf_tokenizer(model_name)
        if tokenizer is None:
            cls._logger.error(f"No tokenizer found for model '{model_name}'")
            raise RuntimeError(f"No tokenizer found for model '{model_name}'")
        cls._logger.debug(f"Successfully loaded tokenizer for model '{model_name}'")
        return tokenizer

    @classmethod
    def _validate_string_param(cls, param: str, param_name: str, method: str) -> None:
        """
        Validate that a given string parameter is non-empty and not just whitespace.

        Parameters
        ----------
        param : str
            The parameter to validate.
        param_name : str
            The name of the parameter (used in error messages).
        method : str
            The name of the method invoking this validation (for logging).

        Raises
        ------
        ValueError
            If the parameter is empty or contains only whitespace.

        Notes
        -----
        This method pervents silent failures or misbehavior due to invalid string inputs.
        """
        cls._logger.debug(f"Validating parameter '{param_name}' in {method} with value: {param}")
        if not param or not isinstance(param, str) or not param.strip():
            cls._logger.error(f"{param_name} must be a non-empty, non-whitespace string in {method}")
            raise ValueError(f"{param_name} must be a non-empty, non-whitespace string")

    @classmethod
    def _validate_and_set_chunk_params(
        cls, chunk_size: Optional[int], chunk_overlap: Optional[int], method: str
    ) -> tuple[int, int]:
        """
        Validate and resolve chunking parameters: chunk size and chunk overlap.

        Parameters
        ----------
        chunk_size : Optional[int]
            Desired size of each chunk.
        chunk_overlap : Optional[int]
            Desired overlap between chunks.
        method : str
            The name of the method invoking this validation (for logging).

        Returns
        -------
        tuple[int, int]
            Validated chunk size and chunk overlap.

        Raises
        ------
        ValueError
            If chunk size is non-positive, exceeds the maximum allowed,
            or if chunk overlap is negative or greater than/equal to chunk size.

        Notes
        -----
        This method enforces limits on chunk sizing to prevent invalid behavior.
        """
        cls._logger.debug(f"Validating chunk parameters in {method}: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

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

        cls._logger.debug(f"Chunk parameters validated: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
        return chunk_size, chunk_overlap

    @classmethod
    def _log_splitter_creation(cls, method: str, params: dict) -> None:
        """
        Log the creation of a splitter with the provided parameters.

        Parameters
        ----------
        method : str
            The name of the method that initiated the splitter creation.
        params : dict
            A dictionary of parameters used in the splitter creation.

        Notes
        -----
        This method helps trace configuration used to create each splitter during debugging.
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
        """
        Create a TokenTextSplitter for the specified model.

        Parameters
        ----------
        model_name : str
            Model name for the tokenizer (e.g., 'text-embedding-ada-002' or HuggingFace model ID).
        chunk_size : Optional[int]
            Size of each chunk in tokens.
        chunk_overlap : Optional[int]
            Overlap between chunks in tokens.

        Returns
        -------
        TokenTextSplitter
            A configured text splitter instance.

        Raises
        ------
        ValueError
            If model_name or chunk parameters are invalid.
        RuntimeError
            If the tokenizer cannot be created.

        Notes
        -----
        This methods determines the appropirate tokenizer, and creates a token-based text splitter.
        """
        cls._logger.debug(f"Starting create_token_splitter with model_name='{model_name}', chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

        cls._validate_string_param(model_name, "Model name", "create_token_splitter")
        chunk_size, chunk_overlap = cls._validate_and_set_chunk_params(chunk_size, chunk_overlap, "create_token_splitter")
        cls._log_splitter_creation("token splitter", {"model_name": model_name, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})

        try:
            if model_name in cls.SUPPORTED_OPENAI_MODELS:
                cls._logger.debug(f"Using OpenAI tokenizer for model '{model_name}'")
                splitter = TokenTextSplitter.from_tiktoken_encoder(
                    model_name=model_name,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                cls._logger.debug("TokenTextSplitter created using OpenAI tokenizer")
                return splitter

            cls._logger.debug(f"Using HuggingFace tokenizer for model '{model_name}'")
            tokenizer = cls._get_huggingface_tokenizer(model_name)
            splitter = TokenTextSplitter.from_huggingface_tokenizer(
                tokenizer=tokenizer,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            cls._logger.debug("TokenTextSplitter created using HuggingFace tokenizer")
            return splitter
        
        except (ValueError, ImportError) as e:
            cls._logger.exception(f"Failed to create splitter for model '{model_name}'")
            raise RuntimeError(f"Failed to create splitter for model '{model_name}': {str(e)}") from e

    class KornjaSeparatorSplitter:
        def __init__(self, separator: str):
            """
            Initialize the separator-base splitter.

            Parameters
            ----------
            separator : str
                The delimiter used to split the text.

            Notes
            -----
            This method appends the separator back to each chunk.
            """
            Splitter._logger.debug(f"Initializing KornjaSeparatorSplitter with separator='{separator}'")
            self.separator = separator

        def split_text(self, text: str) -> List[str]:
            """
            Split the input text based on the specified separator.

            Parameters
            ----------
            text : str
                The input string to split.

            Returns
            -------
            List[str]

            Raises
            ------
            ValueError
                If the input is not a string.

            Notes
            -----
            This method retains the separator at the ennd.
            """
            if not isinstance(text, str):
                Splitter._logger.error("Text must be a string")
                raise ValueError("Text must be a string")
            
            chunks = [chunk + self.separator for chunk in text.split(self.separator)]
            Splitter._logger.debug(f"Split text into {len(chunks)} chunks before stripping last separator")
            chunks[-1] = chunks[-1].rstrip(self.separator)
            Splitter._logger.debug(f"Final chunk length after stripping: {len(chunks[-1])}")
            return chunks
        
    @classmethod
    def create_separator_splitter(
        cls,
        separator: str = "\n\n",
    ) -> KornjaSeparatorSplitter:
        """
        Create a KornjaSeparatorSplitter with the specified separator.

        Parameters
        ----------
        separator : str
            Separator to split text (e.g., '\\n\\n' for paragraphs).

        Returns
        -------
        KornjaSeparatorSplitter
            A configured separator-based text splitter instance.

        Raises
        ------
        ValueError
            If the separator is invalid.

        Notes
        -----
        This method is useful for custom logic like paragraph-level or sentence-level chunking without relying on token count.
        """
        cls._logger.debug(f"Starting create_separator_splitter with separator='{separator}'")
        cls._validate_string_param(separator, "Separator", "create_separator_splitter")
        cls._log_splitter_creation("separator splitter", {"separator": separator})

        splitter = cls.KornjaSeparatorSplitter(separator)
        cls._logger.debug("KornjaSeparatorSplitter instance created")
        return splitter