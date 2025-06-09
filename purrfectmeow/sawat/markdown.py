import time
from markitdown import MarkItDown
from docling.document_converter import DocumentConverter

from purrfectmeow.kitty import kitty_logger

class Markdown:
    """
    Utility class for converting documents or URLs to Markdown format using third-party tools.

    Public Methods
    --------------
    convert_with_markitdown(input_path)
        Extracts text using the MarkItdown.
    convert_with_docling(input_path)
        Extracts text using the Docling.

    Examples
    --------
    >>> text = Markdown.convert_with_markitdown("document.xlsx")
    >>> text = Markdown.convert_with_docling("document.docx")
    """
    _logger = kitty_logger(__name__)
    
    @staticmethod
    def _convert(input_path: str, converter: callable, extractor: callable) -> str:
        """
        Helper method to convert a file to text using a provided converter function.

        Parameters
        ----------
        input_path : str
            The path to the input file or URL to convert.
        converter : callable
            A callable object that performs the conversion.
        extractor : callable
            A callable that extracts Markdown content from the converted result.

        Returns
        -------
        str
            The extracted Markdown content as a string.

        Notes
        -----
        The method is designed to be flexible and reusable for different types of file conversions.
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

        Parameters
        ----------
        input_path : str
            The path to the input file or URL to convert.

        Returns
        -------
        str
            The Markdown content extracted from the input.

        Notes
        -----
        - This method uses the `MarkItDown` library to convert various document types.
        - It extracts Markdown using the `.text_content` attribute of the result.
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

        Parameters
        ----------
        input_path : str
            The path to the input file or URL to convert.

        Returns
        -------
        str
            The Markdown content extracted from the input.

        Notes
        -----
        - This method uses the `DocumentConverter` from the `docling` package.
        - It calls `.export_to_markdown()` on the `document` attribute of the result.
        """
        return Markdown._convert(
            input_path,
            DocumentConverter(),
            lambda content: content.document.export_to_markdown()
        )