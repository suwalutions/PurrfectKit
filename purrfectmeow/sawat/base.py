from typing import BinaryIO, Any, Callable
from purrfectmeow.taeng.file_handler import HandleFile

from purrfectmeow.sawat.markdown import Markdown
from purrfectmeow.sawat.ocr import OCR
from purrfectmeow.sawat.simple import Simple

class Malet:
    """
    A class provides a static interface to load and convert files into text.

    This class consolidates methods from `Markdown`, `OCR`, and `Simple` to perform
    extracting text from various file formats using a range of loader backends such as 
    Markdown converters, OCR engines, and simple data parsers.
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
    def loader(
        file: BinaryIO, 
        file_name: str, 
        loader: str = "PYMUPDF", 
        **kwargs: Any
    ) -> str:
        """
        Load and convert a binary file using the specifed loader backend.

        Parameters
        ----------
        file: BinaryIO
            The binary file to be converted.
        file_name: str
            The name to use for the file.
        loader: str
            The loader backend
        **kwargs
            Any arguments needed for the loader.

        Supported Loaders
        -----------------
        MARKITDOWN : Callable
            Converts Markdown using the Markitdown engine.
        DOCLING : Callable
            Converts Markdown using the Docling engine.
        PYTESSERACT : Callable
            Extracts text from images or PDFs using Tesseract OCR.
        EASYOCR : Callable
            Extracts text using the EasyOCR engine.
        SURYAOCR : Callable
            Extracts text using the SuryaOCR engine.
        PYMUPDF : Callable
            Parses PDF content using PyMuPDF.
        PYMUPDF_AS_TXT : Callable
            Extracts plain text from PDFs using PyMuPDF as text.
        PANDAS_EXCEL : Callable
            Reads Excel files using pandas.
        PANDAS_CSV : Callable
            Reads CSV files using pandas.
        
        Returns
        -------
        str
            The extracted text.

        Examples
        --------
        >>> with open("example.pdf", "rb") as f:
        ...     text = Malet.loader(f, "example.pdf", loader="PYMUPDF")
        >>> print(text)
        """
        file_path = HandleFile.save_temp_file(file, file_name)
        try:
            if loader not in Malet._LOADER_METHODS:
                raise ValueError(f"Unsupported loader: {loader}")
            
            method = Malet._LOADER_METHODS[loader]
            return method(file_path, **kwargs)
        finally:
            HandleFile.remove_temp_file(file_path)