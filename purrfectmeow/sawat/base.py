import os
from typing import BinaryIO, Any, Callable

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
        "PANDAS": Simple.convert_with_pandas,
        "ENCODING": Simple.convert_with_encoding
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
            Parses PDF, text file content using PyMuPDF.
        PANDAS : Callable
            Reads Spreadsheet, CSV files using pandas.
        ENCODING : Callable
            Reads files using endcoding uft-8.
        
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
        tmp_path = '.cache/tmp'
        os.makedirs(tmp_path, exist_ok=True)
        file_path = os.path.join(tmp_path, file_name)
        try:
            with open(file_path, "wb") as f:
                f.write(file.read())
            if loader not in Malet._LOADER_METHODS:
                raise ValueError(f"Unsupported loader: {loader}")
            
            method = Malet._LOADER_METHODS[loader]
            return method(file_path, **kwargs)
        finally:
            os.remove(file_path)