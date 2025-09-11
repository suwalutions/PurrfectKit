
from .cosine import ConsineSim
class KhaoManee:

    @classmethod
    def searching(cls, query_embed, sentence_embed, document, top_k):

        return ConsineSim.vector_search(query_embed, sentence_embed, document, top_k)
