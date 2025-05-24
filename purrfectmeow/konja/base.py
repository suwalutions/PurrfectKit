from typing import List, Optional, Literal

from purrfectmeow.konja.splitter import Splitter

class Kornja:
    """
    A flexible utility class for chunking text into smaller segments using token-based or separator-based strategies.

    This class provides a static method chunking that allows dynamic configuration of text splitting behavior.
    It supports both:
    - Token-based splitting via OpenAI or HuggingFace tokenizers.
    - Separator-based splitting using a specified string separator.

    This class acts as a high-level interface to the lower-level Splitter class, offering a simplified API for 
    preparing text for use in NLP pipelines such as embeddings, semantic search, or summarization.

    Methods:
        chunking(
            text: str,
            splitter: Optional[Literal["token", "separator"]] = "token",
            ``**kwargs``
        ) -> List[str]:
            Splits the input text into chunks using the specified splitter type. Additional configuration options such as
            model_name (for token-based), separator (for separator-based), chunk_size, and chunk_overlap (for token-based)
            can be passed via keyword arguments.
    """

    @staticmethod
    def chunking(
        text: str,
        splitter: Optional[Literal["token", "separator"]] = "token",
        **kwargs
    ) -> List[str]:
        """Chunk text into segments using a token-based or separator-based splitter.

        Args:
            text (str): The input text to be chunked.
            splitter (Optional[Literal["token", "separator"]]): The type of splitter to use. Defaults to "token".
            ``**kwargs``: Additional parameters, including:
                - model_name (str, optional): Model name for token-based splitter (required if splitter="token").
                - separator (str, optional): Separator for character-based splitter (required if splitter="character").
                - chunk_size (Optional[int], optional): Size of each chunk in tokens (for token splitter only).
                - chunk_overlap (Optional[int], optional): Overlap between chunks in tokens (for token splitter only).

        Returns:
            List[str]: A list of text chunks.

        Raises:
            ValueError: If splitter is invalid or required kwargs (model_name, separator) are missing/invalid.
            RuntimeError: If the splitter cannot be created or text splitting fails.

        Examples:
            >>> # Token-based splitting with custom model
            >>> chunks = Kornja.chunking(text, model_name="intfloat/multilingual-e5-large-instruct")
            >>> # Uses splitter="token" with specified model

            >>> # Separator-based splitting with custom separator
            >>> text = "Sentence one. Sentence two. Sentence three."
            >>> chunks = Kornja.chunking(text, splitter="separator", separator=".")
            >>> # Splits on '.' without chunk size or overlap
        """
        match splitter:
            case "token":
                model_name = kwargs.get("model_name", "text-embedding-ada-002")
                chunk_size = kwargs.get("chunk_size", 500)
                chunk_overlap = kwargs.get("chunk_overlap", 0)

                if not model_name or not isinstance(model_name, str) or not model_name.strip():
                    raise ValueError("model_name must be a non-empty string for token splitter")
                sptr = Splitter.create_token_splitter(model_name, chunk_size, chunk_overlap)

            case "separator":
                separator = kwargs.get("separator", "\n\n")
                
                if not separator or not isinstance(separator, str) or not separator.strip():
                    raise ValueError("separator must be a non-empty string for separator splitter")
                sptr = Splitter.create_separator_splitter(separator)
                
            case _:
                raise ValueError(f"Invalid splitter type: {splitter}. Must be 'token' or 'separator'.")

        chunks = sptr.split_text(text)
        return chunks