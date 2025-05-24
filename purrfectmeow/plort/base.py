import numpy
from typing import List, Optional, Literal
from langchain_core.documents import Document

from purrfectmeow.plort.embedder import SimpleHFEmbedder
from purrfectmeow.plort.tokenization import SimpleTokenization
from purrfectmeow.plort.vectorstore import SimpleInMemoryVectorStore

class KhaoManee:
    """
    KhaoManee is a utility class for embedding documents and queries using a 
    specified embedding model and performing similarity search on embedded vectors.

    This class wraps functionalities from SimpleHFEmbedder and SimpleInMemoryVectorStore
    to provide easy access to embeddings and search results.

    Methods:
        get_embeddings(documents, model_name): Generate embeddings for one or more documents.
        get_query_embeddings(query, model_name): Generate embeddings for a query string.
        get_tokens(text, engine): Tokenizes the given text using the specified NLP engine.
        get_search(query_embedding, embeddings, documents, top_k): Perform similarity search to find the most relevant documents given a query embedding.
    """
    @staticmethod
    def get_embeddings(
        documents: Document, 
        model_name: Optional[str] = "intfloat/multilingual-e5-large-instruct"
    ):
        """
        Generate embeddings for the provided documents using a specified embedding model.

        Args:
            documents (Document): A Document object or a list of Document objects to embed.
            model_name (str, optional): The model identifier to use for embeddings.
                Defaults to "intfloat/multilingual-e5-large-instruct".

        Returns:
            numpy.ndarray: An array of embeddings representing the documents.

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
    ):
        """
        Generate an embedding vector for a query string using the specified embedding model.

        Args:
            query (str, optional): The input query text to embed. Defaults to "meow~".
            model_name (str, optional): The model identifier to use for embeddings.
                Defaults to "intfloat/multilingual-e5-large-instruct".

        Returns:
            numpy.ndarray: An embedding vector representing the query.

        Example:
            >>> query_embedding = KhaoManee.get_query_embeddings("Find cats")
            >>> print(query_embedding.shape)
        """
        return SimpleHFEmbedder.embed_query(query, model_name)
    
    @staticmethod
    def get_tokens(
        text: str,
        engine: Optional[Literal["spacy", "pythainlp", "huggingface"]] = "pythainlp"
        ):
        """
        Tokenizes the given text using the specified NLP engine.

        Args:
            text (str): The input text to tokenize.
            engine (Optional[Literal["spacy", "pythainlp", "huggingface"]], optional): 
                The tokenization engine to use. Must be one of:
                - "spacy": Uses spaCy tokenizer.
                - "pythainlp": Uses PyThaiNLP tokenizer (default).
                - "huggingface": Uses a HuggingFace tokenizer.

        Returns:
            List[str]: A list of tokens extracted from the input text.

        Raises:
            ValueError: If an unsupported engine name is provided.

        Example:
            >>> KhaoManee.get_tokens("ฉันรักภาษาไทย")
            ['ฉัน', 'รัก', 'ภาษา', 'ไทย']

            >>> KhaoManee.get_tokens("I love Python.", engine="spacy")
            ['I', 'love', 'Python', '.']
        """
        return SimpleTokenization.tokenize(text, engine)

    @staticmethod
    def get_search(
        query_embedding: numpy.ndarray,
        embeddings: List[numpy.ndarray],
        documents: List[Document],
        top_k: int = 5
    ):
        """
        Perform a similarity search to retrieve the top_k most relevant documents to the query.

        Args:
            query_embedding (numpy.ndarray): The embedding vector for the search query.
            embeddings (List[numpy.ndarray]): List of document embedding vectors.
            documents (List[Document]): List of Document objects corresponding to embeddings.
            top_k (int, optional): The number of top matching documents to return. Defaults to 5.

        Returns:
            List[Document]: The top_k documents most similar to the query.

        Example:
            >>> docs = [Document(page_content="Hello world"), Document(page_content="Bonjour monde")]
            >>> embeddings = KhaoManee.get_embeddings(docs)
            >>> query_emb = KhaoManee.get_query_embeddings("Hello")
            >>> top_docs = KhaoManee.get_search(query_emb, embeddings, docs, top_k=1)
            >>> print(top_docs[0].page_content)
        """
        return SimpleInMemoryVectorStore.search(
            query_embedding=query_embedding,
            vectors=list(embeddings),
            documents=documents,
            top_k=top_k
        )