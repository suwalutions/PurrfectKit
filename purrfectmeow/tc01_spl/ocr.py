import time
from collections.abc import Callable
from typing import Any

from purrfectmeow.meow.kitty import kitty_logger


class Ocr:
    _logger = kitty_logger(__name__)
    _image_type = [
        ".apng",
        ".png",
        ".avif",
        ".gif",
        ".jpg",
        ".jpeg",
        ".jfif",
        ".pjpeg",
        ".pjp",
        ".png",
        ".svg",
        ".webp",
        ".bmp",
        ".ico",
        ".cur",
        ".tif",
        ".tiff",
    ]

    @classmethod
    def _convert(cls, file_path: str, converter: Callable[[str], Any]) -> str:
        cls._logger.debug(f"Starting conversion for '{file_path}'")
        start = time.time()

        try:
            content = []
            match file_path.lower():
                case path if path.endswith(".pdf"):
                    from pdf2image import convert_from_path

                    images = convert_from_path(file_path, fmt="png")
                    for idx, image in enumerate(images):
                        try:
                            text = converter(image)
                            cls._logger.debug(f"Text: {text}")
                            content.append(text)
                            cls._logger.debug(f"Page {idx + 1} processed")
                        except Exception as e:
                            cls._logger.exception(f"Page {idx + 1} failed: {e}")
                            raise
                case path if path.endswith(tuple(cls._image_type)):
                    from PIL import Image

                    image = Image.open(file_path)
                    try:
                        text = converter(image)
                        cls._logger.debug(f"Text: {text}")
                        content.append(text)
                        cls._logger.debug("Page 1 processed")
                    except Exception as e:
                        cls._logger.debug(f"Page 1 failed: {e}")
                        raise

            cls._logger.debug(f"Successfully converted '{file_path}'")
            return "\n".join(content)

        finally:
            elasped = time.time() - start
            cls._logger.debug(f"Conversion time spent '{elasped:.2f}' seconds.")

    @classmethod
    def pytesseract_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using PyTesseract for Conversion")

        def converter(image: str) -> Any:
            import pytesseract

            return pytesseract.image_to_string(image, lang="tha+eng")

        return cls._convert(file_path, converter)

    @classmethod
    def easyocr_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using EasyOCR for Conversion")

        def converter(image: str) -> Any:
            import easyocr
            import numpy

            reader = easyocr.Reader(["th", "en"], gpu=False)
            res = reader.readtext(numpy.array(image))
            return "\n".join(text for _, text, _ in res)

        return cls._convert(file_path, converter)

    @classmethod
    def suryaocr_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using SuryaOCR for Conversion")

        def converter(image: str) -> Any:
            from surya.detection import DetectionPredictor
            from surya.recognition import RecognitionPredictor

            rec_pred = RecognitionPredictor()
            det_pred = DetectionPredictor()

            prediction = rec_pred(
                [image],
                det_predictor=det_pred,
                detection_batch_size=1,
                recognition_batch_size=1,
            )
            return "\n".join(line.text for line in prediction[0].text_lines)

        return cls._convert(file_path, converter)

    @classmethod
    def doctr_convert(cls, file_path: str) -> str:
        cls._logger.debug("Using docTR for Conversion")

        def converter(image: Any) -> Any:
            import os
            import tempfile

            from doctr.io import DocumentFile
            from doctr.models import ocr_predictor

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                image.save(tmp.name)
                tmp_path = tmp.name

            model = ocr_predictor(pretrained=True)
            doc = DocumentFile.from_images(tmp_path)
            result = model(doc)
            data = result.export()
            combined_text = "\n".join(
                word["value"]
                for page in data["pages"]
                for block in page.get("blocks", [])
                for line in block.get("lines", [])
                for word in line.get("words", [])
                if "value" in word
            )
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return combined_text

        return cls._convert(file_path, converter)

    @classmethod
    def typhoonocr_convert(cls, file_path: str, **kwargs: Any) -> str:
        cls._logger.debug("Using Typhoon OCR for Conversion")

        def converter(image: Any) -> Any:
            import os
            import re
            import tempfile

            from typhoon_ocr import ocr_document

            base_url = kwargs.get("base_url") or os.getenv("OLLAMA_SERVER") or "http://localhost:11434/v1"
            if not base_url.endswith("/v1"):
                base_url += "/v1"
            api_key = kwargs.get("api_key") or "ollama"
            model = kwargs.get("model") or kwargs.get("model_name") or "scb10x/typhoon-ocr1.5-3b"

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                image.save(tmp.name)
                tmp_path = tmp.name

            text = ocr_document(tmp_path, base_url=base_url, api_key=api_key, model=model)

            if model.startswith("gemma3"):
                text = re.sub(r"^```[a-zA-Z0-9_]*\n|```$", "", text).strip()

            os.remove(tmp_path)

            return text

        return cls._convert(file_path, converter)
