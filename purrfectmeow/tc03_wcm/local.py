import time
from typing import Any

import numpy

from purrfectmeow.meow.kitty import kitty_logger


class Local:
    _logger = kitty_logger(__name__)
    _HF_MODEL_DIR = ".cache/huggingface/hub/"

    @classmethod
    def model_encode(cls, sentence: str | list[str], model_name: str, **kwargs: Any) -> numpy.ndarray:
        cls._logger.debug("Initializing local model encode")
        start = time.time()
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(
                model_name,
                cache_folder=cls._HF_MODEL_DIR,
                # local_files_only=True
            )

            embed = model.encode(sentence, convert_to_numpy=True)

            cls._logger.debug("Local model encode successfully initialized.")
            return embed
        except Exception as e:
            cls._logger.exception(f"Failed to initialize local model encode: {e}")
            raise
        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Local model encode completed in {elapsed:.2f} seconds.")
