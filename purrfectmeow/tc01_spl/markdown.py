import time
from collections.abc import Callable
from typing import Any

from purrfectmeow.meow.kitty import kitty_logger


class Markdown:
    _logger = kitty_logger(__name__)

    @classmethod
    def _convert(cls, file_path: str, converter: Callable[[str], Any], extractor: Callable[[Any], str]) -> str:
        cls._logger.debug(f"Starting conversion for '{file_path}'")
        start = time.time()
        try:
            raw_content: Any = converter(file_path)
            result: str = extractor(raw_content)

            cls._logger.debug(f"Succesfully converted '{file_path}'")

            return result

        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Conversion time spent '{elapsed:.2f}' seconds.")

    @classmethod
    def markitdown_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using MarkItDown for Conversion")

        from markitdown import MarkItDown

        mid = MarkItDown()

        return cls._convert(file_path, lambda path: mid.convert(path), lambda content: content.text_content)

    @classmethod
    def docling_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using Docling for Conversion")

        from docling.document_converter import DocumentConverter

        dcl = DocumentConverter()

        return cls._convert(
            file_path, lambda path: dcl.convert(path).document, lambda content: content.export_to_markdown()
        )

    @classmethod
    def pymupdf4llm_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using PyMuPDF4LLM for Conversion")
        cls._logger.debug(f"Starting conversion for '{file_path}'")
        start = time.time()

        import pymupdf4llm

        try:
            res: str = pymupdf4llm.to_markdown(file_path)
            cls._logger.debug(f"Succesfully converted '{file_path}'")

            return res
        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Conversion time spent '{elapsed:.2f}' seconds.")
