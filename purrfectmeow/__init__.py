"""Thai Cat breed classes mapped to NLP techniques.

This module exports classes representing thai cat breeds, each associated with an NLP technique.
Mappings:
    - Kornja: Content Chunking (breaking text into manageable segments)
    - WichienMaat: Semantic Search (understanding query intent)
    - KhaoManee: Embedding & Storage (converting text to vectors and storing)
    - Malet: Text Extraction (isolating specific data from text)
    - Suphalaks: Internal use
"""

from purrfectmeow.konja import Kornja
from purrfectmeow.meeze import WichienMaat
from purrfectmeow.plort import KhaoManee
from purrfectmeow.sawat import Malet
from purrfectmeow.taeng import Suphalaks

__all__ = [
    "Kornja",
    "WichienMaat",
    "KhaoManee",
    "Malet",
    "Suphalaks",
]

NLP_MAPPINGS = {
    "Kornja": "Content Chunking",
    "WichienMaat": "Semantic Search",
    "KhaoManee": "Embedding & Storage",
    "Malet": "Text Extraction",
    "Suphalaks": "Internal use",
}