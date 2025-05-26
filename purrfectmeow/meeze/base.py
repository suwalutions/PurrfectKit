import numpy
from typing import List
from langchain_core.documents import Document

from purrfectmeow.meeze.vectorstore import SimpleInMemoryVectorStore

class WichienMaat:
    """
    A utility class for performing similarity search over embedded documents.

    WichienMaat provides a simple interface to retrieve the most relevant documents 
    given a query embedding by leveraging an in-memory vector store.

    This class is especially useful in NLP pipelines involving semantic search, 
    document retrieval, or ranking based on vector similarity.

    Methods:
        get_search(query_embedding: numpy.ndarray, embeddings: List[numpy.ndarray], documents: List[Document], top_k: int) -> List[Document]
            Retrieve the top-k documents most similar to the query embedding.

    Example:
        >>> from purrfectmeow import WichienMaat
        >>> docs = [Document(page_content="Hello world"), Document(page_content="Bonjour monde")]
        >>> embeddings = KhaoManee.get_embeddings(docs)
        >>> query_emb = KhaoManee.get_query_embeddings("Hello")
        >>> top_docs = WichienMaat.get_search(query_emb, embeddings, docs, top_k=1)
        >>> print(top_docs[0].page_content)
    """
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