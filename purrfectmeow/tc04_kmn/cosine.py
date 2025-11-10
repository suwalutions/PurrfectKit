import time

import numpy

from purrfectmeow.meow.chaus import SimilarityResult
from purrfectmeow.meow.felis import Document
from purrfectmeow.meow.kitty import kitty_logger


class CosineSim:
    _logger = kitty_logger(__name__)

    @classmethod
    def vector_search(
        cls,
        embed_query: numpy.ndarray,
        embed_sentence: numpy.ndarray | list[numpy.ndarray],
        documents: list[Document],
        top_k: int,
    ) -> list[SimilarityResult]:
        cls._logger.debug("Initializing vector search")
        start = time.time()
        try:
            from sklearn.metrics.pairwise import cosine_similarity

            sims = cosine_similarity([embed_query], embed_sentence)[0]
            top_indices = numpy.argsort(sims)[::-1][:top_k]

            results: list[SimilarityResult] = [
                SimilarityResult(score=float(sims[i]), document=documents[i]) for i in top_indices
            ]

            return results
        except Exception as e:
            cls._logger.exception(f"Failed to initialize vector search: {e}")
            raise
        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Vector search completed in {elapsed:.2f} seconds.")
