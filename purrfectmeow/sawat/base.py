from typing import BinaryIO, Any, Callable

from purrfectmeow.kitty import kitty_logger
from purrfectmeow.taeng import Suphalaks
from purrfectmeow.sawat.markdown import Markdown
from purrfectmeow.sawat.ocr import OCR
from purrfectmeow.sawat.simple import Simple

class Malet:
    """Text extraction class inspired by the Malet Thai cat breed.

    This class provides methods to extract text from various file types using specialized loaders.
    Supported file types include PDFs, images, spreadsheets, and Markdown files. Each loader is 
    optimized for a specific format or extraction technique.

    Attributes:
        supported_loaders (list): List of available loader names: \n
            - 'MARKITDOWN': MarkItDown for Markdown conversion\n
            - 'DOCLING': Docling for Markdown conversion\n
            - 'PYTESSERACT': Tesseract OCR for image text extraction\n
            - 'EASYOCR': EasyOCR for image text extraction\n
            - 'SURYAOCR': SuryaOCR for image text extraction\n
            - 'PYMUPDF': PyMuPDF for PDF text extraction\n
            - 'PYMUPDF_AS_TXT': Alternate PyMuPDF extraction as plain text\n
            - 'PANDAS_EXCEL': pandas for Excel file extraction\n
            - 'PANDAS_CSV': pandas for CSV file extraction\n

    Examples:
        >>> from purrfectmeow import Malet
        >>> docs = Malet.loader("example.pdf", "example.pdf", loader="PYMUPDF")
    """
    _logger = kitty_logger(__name__)
    _LOADER_METHODS: dict[str, tuple[Callable[[BinaryIO, str], str], str]] = {
        "MARKITDOWN": (Markdown.convert_with_markitdown, "MarkItDown Converter"),
        "DOCLING": (Markdown.convert_with_docling, "Docling converter"),
        "PYTESSERACT": (OCR.convert_with_pytesseract, "Tesseract converter"),
        "EASYOCR": (OCR.convert_with_easyocr, "EasyOCR converter"),
        "SURYAOCR": (OCR.convert_with_suryaocr, "SuryaOCR converter"),
        "PYMUPDF": (Simple.convert_with_pymupdf, "PyMuPDF converter"),
        "PYMUPDF_AS_TXT": (Simple.convert_with_pymupdf_as_txt, "PyMuPDF converter"),
        "PANDAS_EXCEL": (Simple.convert_with_pandas_excel, "Pandas converter"),
        "PANDAS_CSV": (Simple.convert_with_pandas_csv, "Pandas converter"),
    }

    @staticmethod
    def loader(file: BinaryIO, file_name: str, loader: str, **kwargs: Any) -> str:
        """Load and extract text from a file using the specified loader.

        Args:
            file (BinaryIO): A file-like object opened in binary mode.
            file_name (str): Name of the file for reference (used for context or metadata).
            loader (str): Loader type to use for extraction.
            **kwargs (Any): Additional keyword arguments passed to the loader.

        Returns:
            str: Extracted text content, or other data structure depending on the loader.

        Raises:
            FileNotFoundError: If the file does not exist or cannot be accessed.
            ValueError: If the specified loader is invalid or unsupported.

        Examples:
            >>> with open("example.pdf", "rb") as f:
            ...     text = Malet.loader(f, "example.pdf", loader="PYMUPDF")
            >>> print(text[:200])  # Prints first 200 characters of extracted text
        """
        Malet._logger.info(f"Loading file `{file_name}` with loader `{loader}`")
        file_path = Suphalaks.save_file(file, file_name)
        try:
            if loader not in Malet._LOADER_METHODS:
                Malet._logger.error(f"Unsupported loader: {loader}")
                raise ValueError(f"Unsupported loader: {loader}")
            
            method, converter_name = Malet._LOADER_METHODS[loader]
            Malet._logger.debug(f"Using {converter_name}...")
            return method(file_path)
        finally:
            Suphalaks.remove_file(file_path)