import os
import time
from typing import Any

from purrfectmeow.meow.kitty import kitty_logger


class OpenAI:
    _logger = kitty_logger(__name__)

    MAX_TOKENS_OPENAI = 300_000

    @classmethod
    def model_encode(
        cls, sentence: str | list[str], model_name: str, base_url: str, api_key: str, **kwargs: Any
    ) -> dict[str, Any]:
        cls._logger.debug("Initializing OpenAI encode")
        start = time.time()
        try:
            if api_key:
                key = api_key
            else:
                key = os.environ.get("OPENAI_API_KEY") or ""

            import tiktoken
            from openai import OpenAI

            tokenizer = tiktoken.get_encoding("cl100k_base")
            client = OpenAI(base_url=base_url, api_key=key)

            all_embeddings = []
            total_tokens = 0
            current_batch: list[str] = []
            current_tokens = 0
            batch_count = 0

            def submit_batch(batch: list[str]) -> None:
                nonlocal total_tokens, all_embeddings, batch_count
                batch_count += 1
                cls._logger.debug(
                    f"Submitting OpenAI batch {batch_count} with {len(batch)} texts ({current_tokens} tokens)"
                )
                try:
                    response = client.embeddings.create(input=batch, model=model_name)
                    all_embeddings.extend([item.embedding for item in response.data])
                    total_tokens += response.usage.total_tokens
                    cls._logger.debug(
                        f"OpenAI batch {batch_count} succeeded - tokens used: {response.usage.total_tokens}"
                    )
                except Exception as e:
                    cls._logger.error(f"OpenAI model '{model_name}' failed to create embeddings: {e}")
                    raise

            for text in sentence:
                token_count = len(tokenizer.encode(text))
                if current_tokens + token_count > cls.MAX_TOKENS_OPENAI:
                    cls._logger.debug(
                        f"Token limit reached ({current_tokens}/{cls.MAX_TOKENS_OPENAI}), submitting batch"
                    )
                    submit_batch(current_batch)
                    current_batch = []
                    current_tokens = 0

                current_batch.append(text)
                current_tokens += token_count

            if current_batch:
                submit_batch(current_batch)

            cls._logger.debug("Openai encode successfully initialized.")
            return {"embeddings": all_embeddings, "total_tokens": total_tokens}

        except Exception as e:
            cls._logger.exception(f"Failed to initialize OpenAI encode: {e}")
            raise

        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"OpenAI encode completed in {elapsed:.2f} seconds.")
