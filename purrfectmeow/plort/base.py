from typing import Optional, Literal, List
from langchain_core.documents import Document
import numpy

from purrfectmeow.plort.embedder import SimpleHFEmbedder
from purrfectmeow.plort.tokenization import SimpleTokenization

class KhaoManee:
    """
    A utility class for text embedding and tokenization.

    KhaoManee provides a high-level interface to internal modules handling:
    - Generating embeddings for documents or queries using Hugging Face models
    - Tokenizing text with support for multiple NLP engines

    This class is especially useful in retrieval-focused NLP pipelines such as 
    semantic search, document ranking, or lightweight Retrieval-Augmented Generation (RAG).

    Methods:
        get_embeddings(documents: Document, model_name: Optional[str]) -> numpy.ndarray
            Generate vector embeddings for one or more documents.

        get_query_embeddings(query: str, model_name: Optional[str]) -> numpy.ndarray
            Generate a vector embedding for a query string.

        get_tokens(text: str, engine: Optional[Literal["spacy", "pythainlp", "huggingface"]]) -> List[str]
            Tokenize input text using a specified NLP engine.

    Example:
        >>> from purrfectmeow import KhaoManee
        >>> docs = [Document(page_content="Hello world"), Document(page_content="Bonjour monde")]
        >>> embeddings = KhaoManee.get_embeddings(docs)
        >>> query_embedding = KhaoManee.get_query_embeddings("Hello")
    """

    @staticmethod
    def get_embeddings(
        documents: Document, 
        model_name: Optional[str] = "intfloat/multilingual-e5-large-instruct"
    ) -> numpy.ndarray:
        """
        Generate embeddings for the given documents using the specified model.

        Args:
            documents (Document or List[Document]): Document(s) to embed.
            model_name (Optional[str]): Hugging Face model name for embedding.
                Defaults to "intfloat/multilingual-e5-large-instruct".

        Returns:
            numpy.ndarray: Embeddings array representing the documents.

        Example:
            >>> docs = [Document(page_content="Hello world"), Document(page_content="Bonjour monde")]
            >>> embeddings = KhaoManee.get_embeddings(docs)
            >>> print(embeddings.shape)
        """
        return SimpleHFEmbedder.embed_documents(documents, model_name)

    @staticmethod
    def get_query_embeddings(
        query: Optional[str] = "meow~",
        model_name: Optional[str] = "intfloat/multilingual-e5-large-instruct"
    ) -> numpy.ndarray:
        """
        Generate an embedding vector for the input query text.

        Args:
            query (Optional[str]): Query string to embed. Defaults to "meow~".
            model_name (Optional[str]): Hugging Face model name for embedding.
                Defaults to "intfloat/multilingual-e5-large-instruct".

        Returns:
            numpy.ndarray: Embedding vector representing the query.

        Example:
            >>> query_embedding = KhaoManee.get_query_embeddings("Find cats")
            >>> print(query_embedding.shape)
        """
        return SimpleHFEmbedder.embed_query(query, model_name)

    @staticmethod
    def get_tokens(
        text: str,
        engine: Optional[Literal["spacy", "pythainlp", "huggingface"]] = "pythainlp"
    ) -> List[str]:
        """
        Tokenize the input text using the specified NLP engine.

        Args:
            text (str): Text to tokenize.
            engine (Optional[Literal["spacy", "pythainlp", "huggingface"]]): 
                Tokenization engine to use. Options:
                - "spacy": spaCy tokenizer
                - "pythainlp": PyThaiNLP tokenizer (default)
                - "huggingface": Hugging Face tokenizer

        Returns:
            List[str]: List of tokens extracted from the input text.

        Raises:
            ValueError: If an unsupported engine name is provided.

        Example:
            >>> KhaoManee.get_tokens("ฉันรักภาษาไทย")
            ['ฉัน', 'รัก', 'ภาษา', 'ไทย']

            >>> KhaoManee.get_tokens("I love Python.", engine="spacy")
            ['I', 'love', 'Python', '.']
        """
        return SimpleTokenization.tokenize(text, engine)