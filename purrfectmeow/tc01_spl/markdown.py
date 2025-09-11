import time
from typing import Callable

from purrfectmeow.meow.kitty import kitty_logger

class Markdown:
    
    _logger = kitty_logger(__name__)

    @classmethod
    def _convert(cls, file_path: str, converter: Callable, extractor: Callable) -> str:
        cls._logger.debug(f"Starting conversion for '{file_path}'")
        start = time.time()
        try:
            content = converter.convert(file_path)
            result = extractor(content)

            cls._logger.debug(f"Succesfully converted '{file_path}'")

            return result
        
        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Conversion time spent '{elapsed:.2f}' seconds.")

    @classmethod
    def markitdown_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using MarkItDown for Conversion")

        from markitdown import MarkItDown
        
        return cls._convert(file_path, MarkItDown(), lambda content: content.text_content)

    @classmethod
    def docling_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using Docling for Conversion")
        
        from docling.document_converter import DocumentConverter

        return cls._convert(file_path, DocumentConverter(), lambda content: content.document.export_to_markdown())

    @classmethod
    def pymupdf4llm_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using PyMuPDF4LLM for Conversion")
        cls._logger.debug(f"Starting conversion for '{file_path}'")
        start = time.time()

        import pymupdf4llm

        try:
            res = pymupdf4llm.to_markdown(file_path)
            cls._logger.debug(f"Succesfully converted '{file_path}'")

            return res
        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Conversion time spent '{elapsed:.2f}' seconds.")
