from typing import List, Optional
import spacy
from spacy.language import Language
from tokenizers import Tokenizer
from pythainlp.tokenize import word_tokenize

from purrfectmeow.taeng.model_loader import LoadingModel
from purrfectmeow.kitty import kitty_logger

class SimpleTokenization:
    """
    A simple tokenization utility class for processing Thai text using different tokenization engines.

    This class supports the following tokenization engines:
        - spaCy (using a blank Thai model)
        - PyThaiNLP (newmm tokenizer)
        - HuggingFace tokenizer (requires tokenizer path)

    Attributes:
        _DEFAULT_MODEL_NAME (str): The default model name used for HuggingFace tokenizer.

    Methods:
        tokenize(text: str, engine: str = "spacy", huggingface_tokenizer_path: Optional[str] = None) -> List[str]:
            Tokenizes the given text using the specified engine.
    """
    _logger = kitty_logger(__name__)
    _DEFAULT_MODEL_NAME: str = "intfloat/multilingual-e5-large-instruct"

    _spacy_nlp: Optional[Language] = None
    _huggingface_tokenizer: Optional[Tokenizer] = LoadingModel.get_tokenizer(_DEFAULT_MODEL_NAME)

    @classmethod
    def _load_spacy(cls) -> Language:
        """
        Load and return a blank spaCy NLP model for Thai language.

        Returns:
            spacy.Language: A blank Thai language pipeline.
        """
        if cls._spacy_nlp is None:
            cls._logger.debug("Loading blank spaCy model for Thai...")
            cls._spacy_nlp = spacy.blank("th")
        else:
            cls._logger.debug("spaCy model already loaded.")
        return cls._spacy_nlp

    @classmethod
    def _load_huggingface(cls, tokenizer_path: str) -> Tokenizer:
        """
        Load and return a HuggingFace tokenizer from a specified path.

        Args:
            tokenizer_path (str): The path to the tokenizer JSON file.

        Returns:
            Tokenizer: A HuggingFace tokenizer instance.

        Raises:
            ValueError: If the path is not provided or tokenizer loading fails.
        """
        if cls._huggingface_tokenizer is None:
            cls._logger.debug(f"Loading HuggingFace tokenizer from: {tokenizer_path}")
            cls._huggingface_tokenizer = Tokenizer.from_file(tokenizer_path)
        else:
            cls._logger.debug("HuggingFace tokenizer already loaded.")
        return cls._huggingface_tokenizer

    @classmethod
    def tokenize(
        cls,
        text: str,
        engine: str = "spacy",
        huggingface_tokenizer_path: Optional[str] = None
    ) -> List[str]:
        """
        Tokenizes the input text using the specified engine.

        Args:
            text (str): The text to tokenize.
            engine (str): Tokenization engine to use. One of "spacy", "pythainlp", or "huggingface".
            huggingface_tokenizer_path (str, optional): Required for the "huggingface" engine if tokenizer is not already loaded.

        Returns:
            List[str]: A list of tokenized words or subwords.

        Raises:
            ValueError: If an unknown engine is specified or required parameters are missing.

        Example:
            >>> SimpleTokenization.tokenize("ฉันรักแมว", engine="pythainlp")
            ['ฉัน', 'รัก', 'แมว']
        """
        cls._logger.debug(f"Tokenizing text with engine: {engine}")
        cls._logger.debug(f"Input text: {text}")

        match engine:
            case "spacy":
                nlp = cls._load_spacy()
                tokens = [token.text for token in nlp(text)]
            case "pythainlp":
                tokens = word_tokenize(text, engine="newmm", join_broken_num=True)
            case "huggingface":
                if cls._huggingface_tokenizer is None:
                    if huggingface_tokenizer_path is None:
                        cls._logger.error("No path provided for HuggingFace tokenizer.")
                        raise ValueError("Provide 'huggingface_tokenizer_path' to load tokenizer for huggingface engine.")
                    cls._load_huggingface(huggingface_tokenizer_path)
                tokens = cls._huggingface_tokenizer.encode(text).tokens
            case _:
                cls._logger.error(f"Unknown tokenizer engine: {engine}")
                raise ValueError(f"Unknown tokenizer engine: {engine}")
        
        cls._logger.debug(f"Tokens: {tokens}")
        return tokens
