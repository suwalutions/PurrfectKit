import time
import pymupdf
import pandas

from purrfectmeow.kitty import kitty_logger

class Simple:
    """
    Utility class for extracting text content from various file formats.

    Public Methods
    --------------
    convert_with_pymupdf(input_path)
        Extract text from files perserving layout via PyMuPDF
    convert_with_pandas(input_path)
        Convert Spreadsheet, CSV files to a formatted text table.
    convert_with_encoding(input_path)
        Convert files to with encoding UTF-8.
    
    Examples
    --------
    >>> Simple.convert_with_pymupdf("sample.pdf")
    >>> Simple.convert_with_pandas("spreadsheet.xls")
    >>> Simple.convert_with_encoding("readme.md")
    """
    _logger = kitty_logger(__name__)
    
    @staticmethod
    def _convert(input_path: str, converter: callable) -> str:
        """
        Helper method to convert a file to text using a provided converter function.

        Parameters
        ----------
        input_path : str
            Path to the input file.
        converter : callable
            A function that takes the input path and returns the converted text.

        Returns
        -------
        str
            Extracted text from the input file.

        Raises
        ------
        Exception
            Any exception raised by the converter function will propagate.

        Notes
        -----
        The method is designed to be flexible and reusable for different types of file conversions.
        """
        Simple._logger.debug(f"Starting conversion for '{input_path}'")
        start = time.time()
        try:
            result = converter(input_path)
            Simple._logger.debug(f"Successfully converted '{input_path}'.")
            return result
        finally:
            elapsed = time.time() - start
            Simple._logger.debug(f"Conversion time spent `{elapsed:.2f}` seconds.")
    
    @staticmethod
    def convert_with_pymupdf(input_path: str) -> str:
        """
        Perform text conversion using PyMuPDF

        Parameters
        ----------
        input_path : str
            Path to the input file.

        Returns
        ------
        str
            Extracted text from the input file.

        Notes
        -----
        - This method ...
        - ...
        """
        def pymupdf_open(path):
            if path.endswith(('.txt', '.md')):
                return "".join(page.get_text() for page in pymupdf.open(path, filetype="txt"))
            else:
                return "".join(page.get_text() for page in pymupdf.open(path))
        return Simple._convert(
            input_path,
            lambda path: pymupdf_open(path)
        )
    
    @staticmethod
    def convert_with_pandas(input_path: str) -> str:
        """
        Perform Spreadsheet, CSV conversion using pandas.

        Parameters
        ----------
        input_path : str
            Path to the input file.

        Returns
        ------
        str
            Extracted text from the input file.

        Notes
        -----
        - The method ...
        - ...
        """
        def pandas_read(path):
            if path.endswith(('.xls', '.xlsx')):
                return pandas.read_excel(path).to_string(index=False)
            elif path.endswith('.csv'):
                return pandas.read_csv(path).to_string(index=False)
        return Simple._convert(
            input_path,
            lambda path: pandas_read(path)
        )
    
    @staticmethod
    def convert_with_encoding(input_path: str) -> str:
        """
        Perform conversion using UTF-8 encoding.

        Parameters
        ----------
        input_path : str
            Path to the input file.

        Returns
        ------
        str
            Extracted text from the input file.

        Notes
        -----
        - This method assumes the input file is UTF-8 encoded.
        - Useful for handling `.md`, `.txt` or similar structure text files.
        """
        def encoding_read(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
            
        return Simple._convert(
            input_path,
            lambda path: encoding_read(path)
        )