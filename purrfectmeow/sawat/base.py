from typing import BinaryIO, Any, Callable

from purrfectmeow.taeng.file_handler import HandleFile
from purrfectmeow.sawat.markdown import Markdown
from purrfectmeow.sawat.ocr import OCR
from purrfectmeow.sawat.simple import Simple

class Malet:
    """
    Processes files using various loader methods for text extraction.

    Parameters
    ----------
    file : BinaryIO
        The binary file object to process.
    file_name : str
        The name of the file, used for temporary storage and processing.
    loader : str, optional
        The loader method to use for processing the file. Must be one of
        'MARKITDOWN', 'DOCLING', 'PYTESSERACT', 'EASYOCR', 'SURYAOCR',
        'PYMUPDF', 'PYMUPDF_AS_TXT', 'PANDAS_EXCEL', or 'PANDAS_CSV'.
        Defaults to 'PYMUPDF'.
    **kwargs : Any
        Additional keyword arguments to pass to the selected loader method.

    Returns
    -------
    str
        The processed content of the file as a string.

    Raises
    ------
    ValueError
        If the specified loader is not supported.

    Examples
    --------
    >>> from io import BytesIO
    >>> file = BytesIO(b"Sample content")
    >>> Malet.loader(file, "sample.pdf", loader="PYMUPDF")
    'Sample content'
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
        file_path = HandleFile.save_temp_file(file, file_name)
        try:
            if loader not in Malet._LOADER_METHODS:
                raise ValueError(f"Unsupported loader: {loader}")
            
            method = Malet._LOADER_METHODS[loader]
            return method(file_path, **kwargs)
        finally:
            HandleFile.remove_temp_file(file_path)