import numpy

from purrfectmeow.meow.chaus import SimilarityResult
from purrfectmeow.meow.felis import Document

from .cosine import CosineSim


class KhaoManee:
    @classmethod
    def searching(
        cls,
        query_embed: numpy.ndarray,
        sentence_embed: numpy.ndarray | list[numpy.ndarray],
        documents: list[Document],
        top_k: int,
    ) -> list[SimilarityResult]:
        return CosineSim.vector_search(query_embed, sentence_embed, documents, top_k)
