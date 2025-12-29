from typing import Any, BinaryIO

from .markdown import Markdown
from .ocr import Ocr
from .simple import Simple


class Suphalak:
    tmp_dir = ".cache/tmp"
    DEFAULT_LOADER = "PYMUPDF4LLM"

    _LOADERS: dict[str, dict[str, Any]] = {
        "MARKITDOWN": {
            "func": Markdown.markitdown_convert,
            "ext": ("csv", "docx", "md", "pdf", "pptx", "txt", "xls", "xlsx"),
        },
        "DOCLING": {
            "func": Markdown.docling_convert,
            "ext": ("csv", "docx", "jpg", "jpeg", "md", "pdf", "png", "pptx", "xlsx"),
        },
        "PYMUPDF4LLM": {
            "func": Markdown.pymupdf4llm_convert,
            "ext": ("docx", "pdf", "pptx", "txt", "xlsx"),
        },
        "PYTESSERACT": {
            "func": Ocr.pytesseract_convert,
            "ext": ("gif", "jpg", "jpeg", "pdf", "png"),
        },
        "EASYOCR": {
            "func": Ocr.easyocr_convert,
            "ext": ("gif", "jpg", "jpeg", "pdf", "png"),
        },
        "SURYAOCR": {
            "func": Ocr.suryaocr_convert,
            "ext": ("gif", "jpg", "jpeg", "pdf", "png"),
        },
        "DOCTR": {
            "func": Ocr.doctr_convert,
            "ext": ("gif", "jpg", "jpeg", "pdf", "png"),
        },
        "TYPHOONOCR": {
            "func": Ocr.typhoonocr_convert,
            "ext": ("gif", "jpg", "jpeg", "pdf", "png"),
        },
        "PYMUPDF": {
            "func": Simple.pymupdf_convert,
            "ext": ("docx", "md", "pdf", "pptx", "xlsx"),
        },
        "PANDAS": {
            "func": Simple.pandas_convert,
            "ext": ("csv", "xls", "xlsx"),
        },
        "ENCODING": {
            "func": Simple.encoding_convert,
            "ext": ("csv", "md", "txt"),
        },
    }

    @classmethod
    def _detect_loader(cls, file_ext: str) -> str:
        priority = [
            ("PANDAS", ("csv", "xls")),
            ("PYTESSERACT", ("jpg", "jpeg", "png", "gif")),
            ("PYMUPDF", ("pdf", "md")),
            ("PYMUPDF4LLM", ("txt", "xlsx", "pptx", "docx")),
        ]

        for loader, extensions in priority:
            if file_ext in extensions:
                return loader

        return cls.DEFAULT_LOADER

    @classmethod
    def reading(cls, file: BinaryIO, file_name: str, loader: str | None = None, **kwargs: Any) -> str:
        import os

        file_ext = file_name.split(".")[-1].lower()

        if not loader:
            loader = cls._detect_loader(file_ext)

        if loader not in cls._LOADERS:
            raise ValueError(f"Unsupported loader: '{loader}'")

        loader_conf = cls._LOADERS[loader]
        supported_ext = loader_conf["ext"]

        if file_ext not in supported_ext:
            raise TypeError(f"'{file_ext}' is not supported for '{loader}' loader.")

        os.makedirs(cls.tmp_dir, exist_ok=True)
        file_path = os.path.join(cls.tmp_dir, file_name)

        try:
            text: str
            with open(file_path, "wb") as f:
                f.write(file.read())

            text = loader_conf["func"](file_path, **kwargs)

            if (
                file_ext == "pdf"
                and (not text or not str(text).strip())
                and loader not in ("PYTESSERACT", "EASYOCR", "SURYAOCR", "DOCTR", "TYPHOONOCR")
            ):
                ocr_loader = cls._LOADERS["PYTESSERACT"]
                text = ocr_loader["func"](file_path, **kwargs)

            return text

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
