from typing import Optional, Literal, List
from langchain_core.documents import Document
import numpy

from purrfectmeow.plort.embedder import SimpleHFEmbedder
from purrfectmeow.plort.tokenization import SimpleTokenization

class KhaoManee:
    """
    A utility class for text embedding and tokenization.

    This class for encoding documents and query strings into dense vector using pre-trained transformer models, 
    as well as tokenizing text through various supported engines such as spaCy, PyThaiNLP, and Hugging Face. 
    It abstracts away the underlying complexity of embedding and tokenization processes.

    Public API
    ----------
    get_embeddings(documents, model_name)
        Generates embeddings and tokenizes text using various engines.
            
        Parameters
        ----------
        documents : Document
            The document(s) to generate embeddings for.
        model_name : str, optional
            The name of the model to use for embedding generation.

        Returns
        -------
        numpy.ndarray
            An array of embeddings for the input documents.

        Examples
        --------
        >>> from langchain_core.documents import Document
        >>> doc = Document(page_content="This is a test document.")
        >>> KhaoManee.get_embeddings(doc)
        array([[0.1, 0.2, ...], ...])
    
    get_query_embeddings(query, model_name)
        Generates embeddings for a query string using a specified model.

        Parameters
        ----------
        query : str, optional
            The query string to generate embeddings for. Defaults to 'meow~'.
        model_name : str, optional
            The name of the model to use for embedding generation. Defaults to
            'intfloat/multilingual-e5-large-instruct'.

        Returns
        -------
        numpy.ndarray
            An array of embeddings for the input query.

        Examples
        --------
        >>> KhaoManee.get_query_embeddings(query="What is this?")
        array([0.1, 0.2, ...])
    
    get_tokens(text, engine)
        Tokenizes input text using a specified tokenization engine.

        Parameters
        ----------
        text : str
            The input text to tokenize.
        engine : str, optional
            The tokenization engine to use. Must be one of 'spacy', 'pythainlp', or
            'huggingface'. Defaults to 'pythainlp'.

        Returns
        -------
        List[str]
            A list of tokens extracted from the input text.

        Raises
        ------
        ValueError
            If the specified engine is not one of 'spacy', 'pythainlp', or 'huggingface'.

        Examples
        --------
        >>> KhaoManee.get_tokens("Hello world", engine="pythainlp")
        ['Hello', 'world']
    """
    @staticmethod
    def get_embeddings(
        documents: Document, 
        model_name: Optional[str] = "intfloat/multilingual-e5-large-instruct"
    ) -> numpy.ndarray:
        return SimpleHFEmbedder.embed_documents(documents, model_name)

    @staticmethod
    def get_query_embeddings(
        query: Optional[str] = "meow~",
        model_name: Optional[str] = "intfloat/multilingual-e5-large-instruct"
    ) -> numpy.ndarray:
        return SimpleHFEmbedder.embed_query(query, model_name)

    @staticmethod
    def get_tokens(
        text: str,
        engine: Optional[Literal["spacy", "pythainlp", "huggingface"]] = "pythainlp"
    ) -> List[str]:
        return SimpleTokenization.tokenize(text, engine)