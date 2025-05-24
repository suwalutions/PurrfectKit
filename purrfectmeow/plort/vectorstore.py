import numpy
from typing import List, Dict
from langchain_core.documents import Document
from sklearn.metrics.pairwise import cosine_similarity

from purrfectmeow.kitty import kitty_logger

class SimpleInMemoryVectorStore:
    """
    A simple in-memory vector store for performing similarity search on
    document embeddings using cosine similarity.

    This class provides a method to search for the most similar documents
    given a query embedding, by comparing it to a list of document embeddings.
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

        Args:
            query_embedding (numpy.ndarray): The embedding vector of the query.
            vectors (List[numpy.ndarray]): List of embedding vectors corresponding
                to the documents.
            documents (List[Document]): List of Document objects to search over.
            top_k (int, optional): The number of top similar documents to return.
                Defaults to 5.

        Returns:
            List[Dict[Document, float]]: A list of dictionaries, each containing
            a 'document' key with the Document object and a 'score' key with
            the cosine similarity score (float) between the query and the document.
            The list is sorted by descending similarity scores.

        Notes:
            - If the input vectors list is empty, returns an empty list.
            - Uses cosine similarity to measure similarity between embeddings.

        Example:
            >>> import numpy as np
            >>> from langchain_core.documents import Document
            >>> query_emb = np.array([0.1, 0.2, 0.3])
            >>> doc1 = Document(page_content="Doc 1 content")
            >>> doc2 = Document(page_content="Doc 2 content")
            >>> vectors = [np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.5, 0.6])]
            >>> docs = [doc1, doc2]
            >>> results = SimpleInMemoryVectorStore.search(query_emb, vectors, docs, top_k=1)
            >>> print(results)
            [{'score': 1.0, 'document': Document(page_content='Doc 1 content')}]
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