import os
import time
from typing import Any

from purrfectmeow.meow.kitty import kitty_logger


class Ollama:
    _logger = kitty_logger(__name__)

    @classmethod
    def model_encode(
        cls, sentence: str | list[str], model_name: str, ollama_url: str | None, **kwargs: Any
    ) -> dict[str, Any]:
        cls._logger.debug("Initializing ollama encode")
        start = time.time()
        try:
            from ollama import Client

            if ollama_url:
                host = ollama_url

            else:
                host = os.environ.get("OLLAMA_HOST") or "http://localhost:11434"

            client = Client(host=host)
            embed = client.embed(model=model_name, input=sentence)

            cls._logger.debug("Ollama encode successfully initialized.")
            return {"embeddings": embed.get("embeddings"), "total_tokens": embed.get("prompt_eval_count")}

        except Exception as e:
            cls._logger.exception(f"Failed to initialize Ollama encode: {e}")
            raise

        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Ollama encode completed in {elapsed:.2f} seconds.")
