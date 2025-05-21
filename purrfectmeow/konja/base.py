from typing import List, Optional, Literal

from purrfectmeow.kitty import kitty_logger
from purrfectmeow.konja.splitter import Splitter

class Kornja:
    """
    A flexible utility class for chunking text into smaller segments using token-based or character-based strategies.

    This class provides a static method chunking that allows dynamic configuration of text splitting behavior.
    It supports both:
    - Token-based splitting via OpenAI or HuggingFace tokenizers.
    - Character-based splitting using a specified string separator.

    This class acts as a high-level interface to the lower-level Splitter class, offering a simplified API for 
    preparing text for use in NLP pipelines such as embeddings, semantic search, or summarization.

    Methods:
        chunking(
            text: str,
            splitter: Optional[Literal["token", "character"]] = "token",
            chunk_size: Optional[int] = None,
            chunk_overlap: Optional[int] = None,
            ``**kwargs``
        ) -> List[str]:
            Splits the input text into chunks using the specified splitter type. Additional configuration options such as
            model_name (for token-based) or separator (for character-based) can be passed via keyword arguments.
    """
    _logger = kitty_logger(__name__)

    @staticmethod
    def chunking(
        text: str,
        splitter: Optional[Literal["token", "character"]] = "token",
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        **kwargs
    ) -> List[str]:
        """Chunk text into segments using a token-based or character-based splitter.

        Args:
            text (str): The input text to be chunked.
            splitter (Optional[Literal["token", "character"]]): The type of splitter to use. Defaults to "token".
            chunk_size (Optional[int]): Size of each chunk (tokens or characters). Defaults to None.
            chunk_overlap (Optional[int]): Overlap between chunks. Defaults to None.
            **kwargs: Additional parameters, including:
                - model_name (str, optional): Model name for token-based splitter (required if splitter="token").
                - separator (str, optional): Separator for character-based splitter (required if splitter="character").

        Returns:
            List[str]: A list of text chunks.

        Raises:
            ValueError: If splitter is invalid or required kwargs (model_name, separator) are missing/invalid.
            RuntimeError: If the splitter cannot be created or text splitting fails.

        Examples:
            >>> # Token-based splitting with default model
            >>> text = "This is a sample text to chunk into smaller pieces."
            >>> chunks = Kornja.chunking(text, chunk_size=10, chunk_overlap=2)
            >>> # Uses splitter="token" and model_name="text-embedding-ada-002"

            >>> # Token-based splitting with custom model
            >>> chunks = Kornja.chunking(text, model_name="intfloat/multilingual-e5-large-instruct")
            >>> # Uses splitter="token" with specified model

            >>> # Character-based splitting with custom separator
            >>> text = "Sentence one. Sentence two. Sentence three."
            >>> chunks = Kornja.chunking(text, splitter="character", separator=".", chunk_size=20, chunk_overlap=5)
            >>> # Splits on '.' with specified chunk size and overlap
        """
        Kornja._logger.info(
            f"Chunking text with splitter='{splitter}', chunk_size={chunk_size}, "
            f"chunk_overlap={chunk_overlap}, kwargs={kwargs}"
        )

        try:
            match splitter:
                case "token":
                    model_name = kwargs.get("model_name", "text-embedding-ada-002")
                    if not model_name or not isinstance(model_name, str) or not model_name.strip():
                        Kornja._logger.error("model_name must be a non-empty string for token splitter")
                        raise ValueError("model_name must be a non-empty string for token splitter")
                    sptr = Splitter.create_token_splitter(model_name, chunk_size, chunk_overlap)
                case "character":
                    separator = kwargs.get("separator", "\n\n")
                    if not separator or not isinstance(separator, str) or not separator.strip():
                        Kornja._logger.error("separator must be a non-empty string for character splitter")
                        raise ValueError("separator must be a non-empty string for character splitter")
                    sptr = Splitter.create_character_splitter(separator, chunk_size, chunk_overlap)
                case _:
                    Kornja._logger.error(f"Invalid splitter type: {splitter}")
                    raise ValueError(f"Invalid splitter type: {splitter}. Must be 'token' or 'character'.")

            chunks = sptr.split_text(text)
            Kornja._logger.debug(f"Generated {len(chunks)} chunks")
            return chunks
        except (ValueError, RuntimeError) as e:
            Kornja._logger.exception(f"Failed to chunk text with splitter '{splitter}'")
            raise RuntimeError(f"Failed to chunk text: {str(e)}") from e