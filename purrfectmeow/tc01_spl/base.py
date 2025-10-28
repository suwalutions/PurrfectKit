from typing import Dict, Callable, BinaryIO, Any

from .markdown import Markdown
from .ocr import Ocr
from .simple import Simple

class Suphalak:

    tmp_dir = '.cache/tmp'

    _METHODS: Dict[str, Callable[[str], str]] = {
        "MARKITDOWN": Markdown.markitdown_convert,
        "DOCLING": Markdown.docling_convert,
        "PYMUPDF4LLM": Markdown.pymupdf4llm_convert,
        "PYTESSERACT": Ocr.pytesseract_convert,
        "EASYOCR": Ocr.easyocr_convert,
        "SURYAOCR": Ocr.suryaocr_convert,
        "DOCTR": Ocr.doctr_convert,
        "PYMUPDF": Simple.pymupdf_convert,
        "PANDAS": Simple.pandas_convert,
        "ENCODING": Simple.encoding_convert,
    }

    @classmethod
    def reading(cls, file: BinaryIO, file_name: str, loader: str, **kwargs: Any) -> str:
        file_ext = file_name.split(".")[-1]

        if loader == "ENCODING":
            if file_ext not in ("csv", "md", "txt"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "PANDAS":
            if file_ext not in ("csv", "xls", "xlsx"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "PYMUPDF":
            if file_ext not in ("docx", "md", "pdf", "pptx", "xlsx"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "DOCTR":
            if file_ext not in ("gif", "jpg", "pdf", "png"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "SURYAOCR":
            if file_ext not in ("gif", "jpg", "pdf", "png"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "EASYOCR":
            if file_ext not in ("gif", "jpg", "pdf", "png"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "PYTESSERACT":
            if file_ext not in ("gif", "jpg", "pdf", "png"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "PYMUPDF4LLM":
            if file_ext not in ("docx", "pdf", "pptx", "txt", "xlsx"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "DOCLING":
            if file_ext not in ("csv", "docx", "jpg", "md", "pdf", "png", "pptx", "xlsx"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        if loader == "MARKITDOWN":
            if file_ext not in ("csv", "docx", "md", "pdf", "pptx", "txt", "xls", "xlsx"):
                raise TypeError(f"'{file_ext}' does not supported for '{loader}' loader.")

        import os

        os.makedirs(cls.tmp_dir, exist_ok=True)
        file_path = os.path.join(cls.tmp_dir, file_name)
        
        try:
            with open(file_path, "wb") as f:
                f.write(file.read())
            if loader not in cls._METHODS:
                raise ValueError(f"Unsupported Loader: {loader}")

            return cls._METHODS[loader](file_path, **kwargs)
        finally:
            os.remove(file_path)
