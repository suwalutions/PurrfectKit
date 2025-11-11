from typing import TypedDict

from purrfectmeow.meow.felis import Document


class SimilarityResult(TypedDict, total=False):
    score: float | str
    document: Document
