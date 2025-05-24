import time
from markitdown import MarkItDown
from docling.document_converter import DocumentConverter

from purrfectmeow.kitty import kitty_logger

class Markdown:
    """
    A utility class for converting documents or URLs to Markdown format using third-party tools.

    This class provides static methods to facilitate Markdown conversion via:
        - MarkItDown: A lightweight converter for extracting text content.
        - Docling: A structured document converter supporting export to Markdown.

    The class abstracts away the conversion and extraction process, ensuring consistent logging,
    timing, and error handling across tools.

    Methods:
        convert_with_markitdown(input_path: str) -> str:
            Converts content using MarkItDown and returns the extracted Markdown.

        convert_with_docling(input_path: str) -> str:
            Converts content using Docling and returns the exported Markdown.

    Internal Methods:
        _convert(input_path: str, converter: callable, extractor: callable) -> str:
            Handles the shared logic of converting input and extracting Markdown, with logging.
    """
    _logger = kitty_logger(__name__)
    @staticmethod
    def _convert(input_path: str, converter: callable, extractor: callable) -> str:
        """
        Converts a file or URL to Markdown using the provided converter and extractor.

        Args:
            input_path (str): The path to the input file or URL to convert.
            converter (callable): A callable object that performs the conversion.
            extractor (callable): A callable that extracts Markdown content from the converted result.

        Returns:
            str: The extracted Markdown content as a string.

        Notes:
            Logs the conversion start, success, and elapsed time.
            Ensures timing is logged even if an exception occurs.
        """
        Markdown._logger.debug(f"Starting conversion for '{input_path}'")
        start = time.time()
        try:
            content = converter.convert(input_path)
            result = extractor(content)
            Markdown._logger.debug(f"Successfully converted '{input_path}'.")
            return result
        finally:
            elapsed = time.time() - start
            Markdown._logger.debug(f"Conversion time spent `{elapsed:.2f}` seconds.")

    @staticmethod
    def convert_with_markitdown(input_path: str) -> str:
        """
        Converts a file or URL to Markdown format using the MarkItDown converter.

        Args:
            input_path (str): The path to the input file or URL to convert.

        Returns:
            str: The Markdown content extracted from the input.

        Raises:
            Exception: If the conversion fails, with details logged.
        """
        return Markdown._convert(
            input_path,
            MarkItDown(),
            lambda content: content.text_content
        )

    @staticmethod
    def convert_with_docling(input_path: str) -> str:
        """
        Converts a file or URL to Markdown format using the Docling converter.

        Args:
            input_path (str): The path to the input file or URL to convert.

        Returns:
            str: The Markdown content exported from the converted document.

        Raises:
            Exception: If the conversion fails, with details logged.
        """
        return Markdown._convert(
            input_path,
            DocumentConverter(),
            lambda content: content.document.export_to_markdown()
        )