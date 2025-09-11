from typing import Any, List, Literal, Optional

from .token import TokenSplit
from .separate import SeparateSplit

class Malet:
    DEFAULT_MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 0
    DEFAULT_CHUNK_SEPARATOR = '\n\n'

    @staticmethod
    def _get_kwarg(kwargs: dict, keys: List[str], default: Any = None) -> Any:
        for key in keys:
            if key in kwargs:
                return kwargs[key]
        return default

    @classmethod
    def chunking(cls, text: str, chunk_method: Optional[Literal["token", "separate"]] = "token", **kwargs: Any) -> List[str]:
        match chunk_method:
            case "token":
                model_name = cls._get_kwarg(kwargs, ["model_name", "ModelName", "modelName"], cls.DEFAULT_MODEL_NAME)
                chunk_size = cls._get_kwarg(kwargs, ["chunk_size", "ChunkSize", "chunkSize"], cls.DEFAULT_CHUNK_SIZE)
                chunk_overlap = cls._get_kwarg(kwargs, ["chunk_overlap", "ChunkOverlap", "chunkOverlap"], cls.DEFAULT_CHUNK_OVERLAP)

                method = TokenSplit.splitter(model_name, chunk_size, chunk_overlap)
                return method.split_text(text)

            case "separate":
                chunk_separator = cls._get_kwarg(kwargs, ["chunk_separator", "ChunkSeparator", "chunkSeparator"], cls.DEFAULT_CHUNK_SEPARATOR)

                method = SeparateSplit.splitter(chunk_separator)
                return method.split_text(text)
