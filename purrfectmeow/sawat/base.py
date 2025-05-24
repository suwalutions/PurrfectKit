from typing import BinaryIO, Any, Callable

from purrfectmeow.taeng import Suphalaks
from purrfectmeow.sawat.markdown import Markdown
from purrfectmeow.sawat.ocr import OCR
from purrfectmeow.sawat.simple import Simple

class Malet:
    """
    Unified interface for extracting text from a wide variety of document formats.

    Named after the elegant Malet breed of Thai cats, this class provides a 
    graceful abstraction to read text content from files such as PDFs, spreadsheets, images, and URLs. 
    It dispatches extraction tasks to specialized backends based on the loader specified.

    Supported loaders:
        - 'MARKITDOWN': Convert documents or URLs to Markdown using MarkItDown.
        - 'DOCLING': Convert documents or URLs to Markdown using Docling.
        - 'PYTESSERACT': Extract text from images or PDFs using Tesseract OCR.
        - 'EASYOCR': Extract text using EasyOCR with Thai and English support.
        - 'SURYAOCR': Extract structured text using SuryaOCR (detection + recognition).
        - 'PYMUPDF': Extract text from PDFs using PyMuPDF.
        - 'PYMUPDF_AS_TXT': Extract raw text from PDFs using PyMuPDF in text-only mode.
        - 'PANDAS_EXCEL': Read and convert Excel spreadsheets to plain text using pandas.
        - 'PANDAS_CSV': Read and convert CSV files to plain text using pandas.

    Methods:
        loader(file: BinaryIO, file_name: str, loader: str, **kwargs) -> str:
            Extract text from the given file using the specified loader backend.

    Examples:
        >>> from purrfectmeow import Malet
        >>> with open("example.pdf", "rb") as f:
        ...     text = Malet.loader(f, "example.pdf", loader="PYMUPDF")
    """
    
    _LOADER_METHODS: dict[str, Callable[[str], str]] = {
        "MARKITDOWN": Markdown.convert_with_markitdown,
        "DOCLING": Markdown.convert_with_docling,
        "PYTESSERACT": OCR.convert_with_pytesseract,
        "EASYOCR": OCR.convert_with_easyocr,
        "SURYAOCR": OCR.convert_with_suryaocr,
        "PYMUPDF": Simple.convert_with_pymupdf,
        "PYMUPDF_AS_TXT": Simple.convert_with_pymupdf_as_txt,
        "PANDAS_EXCEL": Simple.convert_with_pandas_excel,
        "PANDAS_CSV": Simple.convert_with_pandas_csv,
    }

    @staticmethod
    def loader(file: BinaryIO, file_name: str, loader: str = "PYMUPDF", **kwargs: Any) -> str:
        """
        Load and extract text from a file using the specified loader.

        Args:
            file (BinaryIO): File-like object opened in binary mode.
            file_name (str): Name of the file (used for saving and reference).
            loader (str, optional): Loader type to use for extraction. Defaults to "PYMUPDF".
            **kwargs (Any): Additional keyword arguments passed to the loader.

        Returns:
            str: Extracted text content.

        Raises:
            FileNotFoundError: If the file does not exist or cannot be accessed.
            ValueError: If the specified loader is invalid or unsupported.

        Examples:
            >>> with open("example.pdf", "rb") as f:
            ...     text = Malet.loader(f, "example.pdf", loader="PYMUPDF")
            >>> print(text[:200])  # Print first 200 characters
        """
        file_path = Suphalaks.save_file(file, file_name)
        try:
            if loader not in Malet._LOADER_METHODS:
                raise ValueError(f"Unsupported loader: {loader}")
            
            method = Malet._LOADER_METHODS[loader]
            return method(file_path, **kwargs)
        finally:
            Suphalaks.remove_file(file_path)