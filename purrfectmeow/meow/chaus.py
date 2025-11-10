from typing import TypedDict

from .felis import Document


class FileMetadata(TypedDict, total=False):
    file_name: str
    file_size: int
    file_created_date: str
    file_modified_date: str
    file_extension: str
    file_type: str
    description: str
    total_pages: int | str
    file_md5: str


class SimilarityResult(TypedDict, total=False):
    score: float | str
    document: Document
