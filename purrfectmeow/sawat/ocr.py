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
    A utility class for performing Optical Character Recognition (OCR) on image and PDF files.

    This class provides a unified interface to extract text using different OCR engines:
        - PyTesseract (Tesseract OCR)
        - EasyOCR
        - SuryaOCR (custom OCR pipeline using detection and recognition models)

    It supports input formats including PDFs and image files (PNG, JPG, JPEG), and automatically
    handles page-by-page processing for multi-page PDFs.

    Methods:
        convert_with_pytesseract(input_path: str) -> List[str]:
            Extracts text using the PyTesseract OCR engine for English and Thai.

        convert_with_easyocr(input_path: str) -> List[str]:
            Extracts text using the EasyOCR engine for English and Thai.

        convert_with_suryaocr(input_path: str) -> List[str]:
            Extracts text using the SuryaOCR system, which combines custom detection and recognition models.

    Internal Methods:
        _convert(input_path: str, converter: callable) -> str:
            Handles the core logic for converting input files into text using the provided converter.
            Supports both image and multi-page PDF input with logging and timing.
    """
    _logger = kitty_logger(__name__)
    @staticmethod
    def _convert(input_path: str, converter: callable) -> str:
        """
        Converts an image or PDF file to text using the provided OCR converter.

        Args:
            input_path (str): Path to the input file (PDF, PNG, JPG, or JPEG).
            converter (callable): A callable that processes an image and returns extracted text.

        Returns:
            str: The extracted text from all pages, joined with newlines.

        Notes:
            Logs the conversion start, success, and elapsed time.
            Ensures timing is logged even if an exception occurs.
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

        Args:
            input_path (str): Path to an image or PDF file.

        Returns:
            List[str]: Extracted text lines.
        """
        def tesseract_converter(img) -> str:
            return pytesseract.image_to_string(img, lang="tha+eng")

        return OCR._convert(input_path, tesseract_converter)

    @staticmethod
    def convert_with_easyocr(input_path: str) -> List[str]:
        """
        Perform OCR using EasyOCR.

        Args:
            input_path (str): Path to an image or PDF file.

        Returns:
            List[str]: Extracted text lines.
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

        Args:
            input_path (str): Path to an image or PDF file.

        Returns:
            List[str]: Extracted text lines.
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