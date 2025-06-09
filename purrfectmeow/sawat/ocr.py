import os
import time
import numpy
import easyocr
import pytesseract
from typing import List
from PIL import Image
from pdf2image import convert_from_path
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

from purrfectmeow.kitty import kitty_logger

class OCR:
    """
    Utility class for performing Optical Character Recognition (OCR) on image and PDF files.

    Public Methods
    --------------
    convert_with_pytesseract(input_path)
        Extracts text using the PyTesseract OCR engine for English and Thai.
    convert_with_easyocr(input_path)
        Extracts text using the EasyOCR engine for English and Thai.
    convert_with_suryaocr(input_path)
        Extracts text using the SuryaOCR system, which combines custom detection and recognition models.

    Examples
    --------
    >>> text = OCR.convert_with_pytesseract("document.pdf")
    >>> text = OCR.convert_with_easyocr("image.jpg")
    >>> text = OCR.convert_with_suryaocr("scan.png")
    """
    _logger = kitty_logger(__name__)
    
    def _convert(input_path: str, converter: callable) -> str:
        """
        Helper method to convert a file to text using a provided converter function.

        Parameters
        ----------
        input_path : str
            Path to the input file.
        converter : callable
            A callable that processes an image and returns extracted text.

        Returns
        -------
        str
            The extracted text from all pages, joined with newlines.

        Raises
        ------
        FileNotFoundError
            If the input file does not exist.
        ValueError
            If the input file format is not supported.
        Exception
            If the converter function fails during processing.

        Notes
        -----
        The method is designed to be flexible and reusable for different types of file conversions.
        """
        OCR._logger.debug(f"Starting conversion for '{input_path}'")
        start = time.time()
        try:
            content = []
            match input_path.lower():
                case path if path.endswith(".pdf"):
                    images = convert_from_path(input_path, fmt="png")
                    for idx, image in enumerate(images):
                        try:
                            text = converter(image)
                            OCR._logger.debug(f"Text: {text}")
                            content.append(text)
                            OCR._logger.debug(f"Page {idx+1} processed.")
                        except Exception as e:
                            OCR._logger.exception(f"Page {idx+1} failed: {e}")
                            raise
                case path if path.endswith((".png", ".jpg", ".jpeg")):
                    image = Image.open(input_path)
                    text = converter(image)
                    content.append(text)
                    OCR._logger.debug("Page 1 processed.")
            OCR._logger.debug(f"Successfully converted '{input_path}'.")
            return "\n".join(content)
        finally:
            elapsed = time.time() - start
            OCR._logger.debug(f"Conversion time spent `{elapsed:.2f}` seconds.")

    @staticmethod
    def convert_with_pytesseract(input_path: str) -> List[str]:
        """
        Perform OCR using pytesseract.

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
        - This method uses the `pytesseract` library and supports both English and Thai languages.
        - It is best suited for well-scanned text images or PDFs with minimal noise.
        """
        def tesseract_converter(img) -> str:
            return pytesseract.image_to_string(img, lang="tha+eng")

        return OCR._convert(input_path, tesseract_converter)

    @staticmethod
    def convert_with_easyocr(input_path: str) -> List[str]:
        """
        Perform OCR using EasyOCR.

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
        - This method initializes the model only once per call.
        - EasyOCR works well with various fonts and image styles and supports multilingual OCR.
        """
        reader = easyocr.Reader(['th', 'en'], gpu=False)

        def easy_converter(img) -> str:
            results = reader.readtext(numpy.array(img))
            return "\n".join(text for _, text, _ in results)

        return OCR._convert(input_path, easy_converter)

    @staticmethod
    def convert_with_suryaocr(input_path: str) -> List[str]:
        """
        Perform OCR using SuryaOCR.

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
        - This method my be slower than other methods due to model complixity.
        - SuryaOCR combines custom-trained detection and recognition models, which makes it more accurate for domain-specific or noisy documents.
        """
        recognition_predictor = RecognitionPredictor()
        detection_predictor = DetectionPredictor()

        def surya_converter(img) -> str:
            prediction = recognition_predictor(
                [img],
                det_predictor=detection_predictor,
                detection_batch_size=1,
                recognition_batch_size=1,
            )
            return "\n".join(line.text for line in prediction[0].text_lines)

        return OCR._convert(input_path, surya_converter)