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
