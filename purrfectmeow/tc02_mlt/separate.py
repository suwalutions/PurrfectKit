from __future__ import annotations

import time

from purrfectmeow.meow.kitty import kitty_logger


class SeparateSplit:
    _logger = kitty_logger(__name__)

    @classmethod
    def splitter(cls, chunk_separator: str) -> CharacterSeparator:
        cls._logger.debug("Initializing separate splitter")
        start = time.time()

        try:
            splitter = cls.CharacterSeparator(chunk_separator)

            cls._logger.debug("Separator splitter successfully initialized.")
            return splitter
        except Exception as e:
            cls._logger.exception(f"Failed to initialize separate splitter: {e}")
            raise
        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Separate splitting completed in {elapsed:.2f} seconds.")

    class CharacterSeparator:
        def __init__(self, separator: str):
            self.separator = separator

        def split_text(self, text: str) -> list[str]:
            chunks = [chunk + self.separator for chunk in text.split(self.separator)]
            chunks[-1] = chunks[-1].rstrip(self.separator)
            return chunks
