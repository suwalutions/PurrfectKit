import time
from typing import Callable

from purrfectmeow.meow.kitty import kitty_logger

class Simple:

    _logger = kitty_logger(__name__)

    @classmethod
    def _convert(cls, file_path: str, converter: Callable) -> str:
        cls._logger.debug(f"Starting conversion for '{file_path}'")
        start = time.time()

        try:
            res = converter(file_path)
            
            cls._logger.debug(f"Successfully converted '{file_path}'")
            return res

        finally:
            elasped = time.time() - start
            cls._logger.debug(f"Conversion time spent '{elasped:.2f}' seconds.")

    @classmethod
    def encoding_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using Encoding for Conversion")

        def reader(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return cls._convert(file_path, lambda file_path: reader(file_path))

    @classmethod
    def pymupdf_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using PyMuPDF for Conversion")

        def reader(file_path):
            import pymupdf

            if file_path.endswith(('.txt', '.md', '.json', '.html', '.xml')):
                return "".join(page.get_text() for page in pymupdf.open(file_path, filetype="txt"))
            else:
                return "".join(page.get_text() for page in pymupdf.open(file_path))
        return cls._convert(file_path, lambda file_path: reader(file_path))

    @classmethod
    def pandas_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using Pandas for Conversion")

        def reader(file_path):
            import pandas

            if file_path.endswith(('.xls', '.xlsx')):
                return pandas.read_excel(file_path).to_string(index=False)
            elif file_path.endswith('.csv'):
                return pandas.read_csv(file_path).to_string(index=False)
            elif file_path.endswith('.json'):
                return pandas.read_json(file_path).to_string(index=False)
            elif file_path.endswith('.html'):
                return pandas.read_html(file_path)
            elif file_path.endswith('.xml'):
                return pandas.read_xml(file_path).to_string(index=False)
        return cls._convert(file_path, lambda file_path: reader(file_path))
