import time
from typing import Any

from sentence_transformers import SentenceTransformer

from purrfectmeow.meow.kitty import kitty_logger


class HuggingFace:
    _logger = kitty_logger(__name__)
    _MODEL_CACHE: dict[str, SentenceTransformer] = {}

    @classmethod
    def model_encode(
        cls,
        sentence: str | list[str],
        model_name: str,
    ) -> dict[str, Any]:
        cls._logger.debug("Initializing huggingface encode")
        start = time.time()
        try:
            if model_name not in cls._MODEL_CACHE:
                cls._logger.debug(f"Loading model: {model_name}")
                cls._MODEL_CACHE[model_name] = SentenceTransformer(model_name)
            else:
                cls._logger.debug(f"Using cached model: {model_name}")

            model = cls._MODEL_CACHE[model_name]

            cls._logger.debug("Encoding sentence(s)")
            embeddings = model.encode(sentence)

            cls._logger.debug("Encoding completed successfully")

            # Count tokens using the model's tokenizer
            tokenizer = model.tokenizer
            input_list = sentence if isinstance(sentence, list) else [sentence]
            total_tokens = sum(len(tokenizer.encode(text)) for text in input_list)

            if isinstance(sentence, str):
                return {"embeddings": [embeddings.tolist()], "total_tokens": total_tokens}

            return {"embeddings": embeddings.tolist(), "total_tokens": total_tokens}

        except Exception as e:
            cls._logger.exception(f"Failed to initialize Huggingface encode: {e}")
            raise

        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Huggingface encode completed in {elapsed:.2f} seconds.")
