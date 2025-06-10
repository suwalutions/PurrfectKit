import numpy
from typing import List
from langchain_core.documents import Document

from purrfectmeow.meeze.vectorstore import SimpleInMemoryVectorStore

class WichienMaat:
    """
    A ligthweight and efficient vector-based semantic search utility for document retrieval.

    This class for performing similarity searches between a query embedding and a set of document embeddings. 
    Ideal for use cases involving small- to medium-scale semantic search applications, it abstracts
    the search logic while maintaining flexibility and interpretability of results.
    """
    @staticmethod
    def get_search(
        query_embedding: numpy.ndarray,
        embeddings: List[numpy.ndarray],
        documents: List[Document],
        top_k: int = 5
    ):
        """
        Performs similarity searches using embeddings and documents.

        Parameters
        ----------
        query_embedding : numpy.ndarray
            The embedding vector for the search query.
        embeddings : List[numpy.ndarray]
            A list of embedding vectors to search against.
        documents : List[Document]
            A list of Document objects corresponding to the embeddings.
        top_k : int, optional
            The number of top similar documents to return. Defaults to 5.

        Returns
        -------
        List[Document]
            A list of the top_k most similar documents based on the query embedding.

        Examples
        --------
        >>> import numpy as np
        >>> from langchain_core.documents import Document
        >>> query_emb = np.array([0.1, 0.2, 0.3])
        >>> embeddings = [np.array([0.1, 0.2, 0.4]), np.array([0.4, 0.5, 0.6])]
        >>> docs = [Document(page_content="Doc 1"), Document(page_content="Doc 2")]
        >>> WichienMaat.get_search(query_emb, embeddings, docs, top_k=2)
        [Document(page_content="Doc 1"), Document(page_content="Doc 2")]
        """
        return SimpleInMemoryVectorStore.search(
            query_embedding=query_embedding,
            vectors=list(embeddings),
            documents=documents,
            top_k=top_k
        )