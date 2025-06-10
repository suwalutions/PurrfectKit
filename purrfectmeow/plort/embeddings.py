import numpy
from typing import Optional, List
from sentence_transformers import SentenceTransformer
from purrfectmeow.taeng.model_loader import LoadingModel

from purrfectmeow.kitty import kitty_logger

class SimpleEmbeddings:
    """
    A class for generating embeddings for documents and queries using SentenceTransformer models.

    Public Methods
    --------------
    embed_documents(documents, model_name)
        Embed a list of text documents into dense vector embeddings.
    embed_query(query, model_name)
        Embed a single query string into a dense vector embedding.

    Examples
    --------
    >>> SimpleEmbeddings.embed_documents(["สวัสดี", "คุณเป็นอย่างไรบ้าง"], model_name="intfloat/multilingual-e5-base")
    array([[...], [...]])

    >>> SimpleEmbeddings.embed_query("อากาศดีมาก", model_name="intfloat/multilingual-e5-base")
    array([...])
    """
    _kitty_logger = kitty_logger(__name__)

    @classmethod
    def _load_model(cls, model_name: Optional[str] = None) -> SentenceTransformer:
        """
        Load a pretrained SentenceTransformer model.
        
        Parameters
        ----------
        model_name : Optional[str]
            Name or path of the pretrained model to load.

        Returns
        -------
            SentenceTransformer: The loaded SentenceTransformer model.

        Notes
        -----
        This method `LoadingModel.get_st_model()` to load a SentenceTransformer.
        """
        cls._kitty_logger.debug(f"Loading model: {model_name}")
        model = LoadingModel.get_st_model(name=model_name)
        cls._kitty_logger.debug(f"Model '{model_name}' loaded successfully")
        return model

    @classmethod
    def embed_documents(
        cls,
        documents: List[str],
        model_name: Optional[str] = None
    ) -> numpy.ndarray:
        """
        Embed a list of documents into dense vector embeddings.

        Parameters
        ----------
        documents : List[str]
            A list of text documents to embed.
        model_name : Optional[str]
            Name or path of the pretrained model to use.

        Returns
        -------
        numpy.ndarray
            A 2D numpy array where each row is the embedding vector of a document.

        Notes
        -----
        This method encodes a batch of documents using SentenceTransformer's `encode` method.
        """
        model = cls._load_model(model_name)
        cls._kitty_logger.debug(f"Embedding {len(documents)} documents using model '{model_name}'")

        embeddings = model.encode(documents, convert_to_numpy=True)
        cls._kitty_logger.debug(f"Embeddings shape: {embeddings.shape}")

        return embeddings

    @classmethod
    def embed_query(
        cls,
        query: str,
        model_name: Optional[str] = None
    ) -> numpy.ndarray:
        """
        Embed a single query string into a dense vector embedding.

        Parameters
        ----------
        query : str
            The text query to embed.
        model_name : Optional[str]
            Name or path of the pretrained model to use.

        Returns
        -------
        numpy.ndarray
            A 1D numpy array representing the embedding vector of the query.

        Notes
        -----
        This method uses the SentenceTransformer `encode` method for a single input string.
        """
        model = cls._load_model(model_name)
        cls._kitty_logger.debug(f"Embedding query using model '{model_name}'")

        embedding = model.encode(query, convert_to_numpy=True)
        cls._kitty_logger.debug(f"Query embedding shape: {embedding.shape}")

        return embedding