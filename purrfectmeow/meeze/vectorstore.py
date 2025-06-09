import numpy
from typing import List, Dict
from langchain_core.documents import Document
from sklearn.metrics.pairwise import cosine_similarity

from purrfectmeow.kitty import kitty_logger

class SimpleInMemoryVectorStore:
    """
    A simple in-memory vector store for performing similarity search.

    Public Methods
    --------------
    search(query_embedding, vectors, documents, top_k)
        Search for the top_k most similar documents to the query_embedding.

    Examples
    --------
    >>> query_emb = np.array([0.1, 0.2, 0.3])
    >>> doc1 = Document(page_content="Doc 1 content")
    >>> doc2 = Document(page_content="Doc 2 content")
    >>> vectors = [np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.5, 0.6])]
    >>> docs = [doc1, doc2]
    >>> results = SimpleInMemoryVectorStore.search(query_emb, vectors, docs, top_k=1)
    >>> print(results)
    [{'score': 1.0, 'document': Document(page_content='Doc 1 content')}]
    """
    _logger = kitty_logger(__name__)

    @classmethod
    def search(
        cls,
        query_embedding: numpy.ndarray,
        vectors: List[numpy.ndarray],
        documents: List[Document],
        top_k: int = 5
    ) -> List[Dict[Document, float]]:
        """
        Search for the top_k most similar documents to the query_embedding.

        Parameters
        ----------
        query_embedding : numpy.ndarray
            The embedding vector of the query.
        vectors : List[numpy.ndarray]
            List of embedding vectors corresponding to the documents.
        documents : List[Document]
            List of Document objects to search over.
        top_k : int
            The number of top similar documents to return.

        Returns
        -------
        List[Dict[Document, float]]
            A list of dict containing Document object and the cosine similarity score (float).

        Notes
        -----
        - This method uses cosine similarity to measure similarity between embeddings.
        - If the input vectors list is empty, returns an empty list.
        """
        if not vectors:
            cls._logger.debug("No vectors provided, returning empty result.")
            return []

        sims = cosine_similarity([query_embedding], vectors)[0]
        cls._logger.debug(f"Computed cosine similarities: {sims}")

        top_indices = numpy.argsort(sims)[::-1][:top_k]
        cls._logger.debug(
            f"Top {top_k} indices: {top_indices}, scores: {[sims[i] for i in top_indices]}"
        )
        results = [{
            "score": float(sims[i]),
            "document": documents[i]
        } for i in top_indices]

        cls._logger.debug(f"Returning top {len(results)} results: {results}")
        return results