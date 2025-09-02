from typing import List, Optional
import numpy

from .local import Local

class WichienMaat:
    DEFAULT_MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    
    @classmethod
    def embedding(cls, sentence: str | List[str], model_name: Optional[str] = None) -> numpy.ndarray:
        if model_name:
            return Local.model_encode(sentence, model_name)
        else:
            return Local.model_encode(sentence, cls.DEFAULT_MODEL_NAME)
