import time
from collections.abc import Callable
from typing import Any

from purrfectmeow.meow.kitty import kitty_logger


class Simple:
    _logger = kitty_logger(__name__)

    @classmethod
    def _convert(cls, file_path: str, converter: Callable[[str], Any]) -> str | Any:
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

        def reader(file_path: str) -> str:
            with open(file_path, encoding="utf-8") as f:
                return f.read()

        return cls._convert(file_path, lambda file_path: reader(file_path))

    @classmethod
    def pymupdf_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using PyMuPDF for Conversion")

        def reader(file_path: str) -> str:
            import pymupdf

            if file_path.endswith((".txt", ".md", ".json", ".html", ".xml")):
                return "".join(page.get_text() for page in pymupdf.open(file_path, filetype="txt"))
            else:
                return "".join(page.get_text() for page in pymupdf.open(file_path))

        return cls._convert(file_path, lambda file_path: reader(file_path))

    @classmethod
    def pandas_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using Pandas for Conversion")

        def reader(file_path: str) -> Any:
            import pandas

            if file_path.endswith((".xls", ".xlsx")):
                df_x: pandas.DataFrame = pandas.read_excel(file_path)
                return df_x.to_string(index=False)
            elif file_path.endswith(".csv"):
                df_c: pandas.DataFrame = pandas.read_csv(file_path)
                return df_c.to_string(index=False)
            elif file_path.endswith(".json"):
                df_j: pandas.DataFrame = pandas.read_json(file_path)
                return df_j.to_string(index=False)
            elif file_path.endswith(".html"):
                df_h: list[pandas.DataFrame] = pandas.read_html(file_path)
                return "".join(df.to_string(index=False) for df in df_h)
            elif file_path.endswith(".xml"):
                df_m: pandas.DataFrame = pandas.read_xml(file_path)
                return df_m.to_string(index=False)
            else:
                return ""

        return cls._convert(file_path, lambda file_path: reader(file_path))
