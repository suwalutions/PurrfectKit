import time
import pymupdf
import pandas

from purrfectmeow.kitty import kitty_logger

class Simple:
    """
    A utility class for extracting textual content from various file formats.

    This class provides static methods to convert content from:
        - PDF files using PyMuPDF
        - Excel files using pandas
        - CSV files using pandas

    Each conversion method logs the process, including timing and success status. The `_convert`
    helper method standardizes the logging and execution of all file conversion operations.

    Methods:
        convert_with_pymupdf(input_path: str) -> str:
            Extracts text from a PDF file using PyMuPDF's default `get_text()`.

        convert_with_pymupdf_as_txt(input_path: str) -> str:
            Extracts text from a PDF using PyMuPDF with `filetype="txt"` for raw output.

        convert_with_pandas_excel(input_path: str) -> str:
            Reads and converts the first sheet of an Excel file to a text string using pandas.

        convert_with_pandas_csv(input_path: str) -> str:
            Reads and converts a CSV file to a text string using pandas.

    Internal Methods:
        _convert(input_path: str, converter: callable) -> str:
            Wraps file conversion logic with timing and logging.
    """
    _logger = kitty_logger(__name__)
    @staticmethod
    def _convert(input_path: str, converter: callable) -> str:
        """
        Converts a file to text using the provided converter function.

        Args:
            input_path (str): Path to the input file (e.g., PDF, Excel, CSV).
            converter (callable): A callable that processes the file and returns extracted text.

        Returns:
            str: The extracted text from the file.

        Notes:
            Logs the conversion start, success, and elapsed time.
            Ensures timing is logged even if an exception occurs.
        """
        Simple._logger.debug(f"Starting conversion for '{input_path}'")
        start = time.time()
        try:
            result = converter(input_path)
            Simple._logger.info(f"Successfully converted '{input_path}'.")
            return result
        finally:
            elapsed = time.time() - start
            Simple._logger.debug(f"Conversion time spent `{elapsed:.2f}` seconds.")

    @staticmethod
    def convert_with_pymupdf(input_path: str) -> str:
        """Extracts text from a PDF file using PyMuPDF."""
        return Simple._convert(
            input_path,
            lambda path: "".join(page.get_text() for page in pymupdf.open(path))
        )

    @staticmethod
    def convert_with_pymupdf_as_txt(input_path: str) -> str:
        """Extracts raw text from a PDF using PyMuPDF with `filetype="txt"`."""
        return Simple._convert(
            input_path,
            lambda path: "".join(page.get_text() for page in pymupdf.open(path, filetype="txt"))
        )

    @staticmethod
    def convert_with_pandas_excel(input_path: str) -> str:
        """Extracts table data from an Excel file using pandas."""
        return Simple._convert(
            input_path,
            lambda path: pandas.read_excel(path).to_string(index=False)
        )

    @staticmethod
    def convert_with_pandas_csv(input_path: str) -> str:
        """Extracts table data from a CSV file using pandas."""
        return Simple._convert(
            input_path,
            lambda path: pandas.read_csv(path).to_string(index=False)
        )
