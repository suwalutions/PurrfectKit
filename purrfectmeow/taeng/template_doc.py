import uuid
import hashlib
from langchain_core.documents import Document

class DocTemplate:
    """
    A utility class for generating structured document chunks with metadata.

    This class provides a method to split text content into smaller chunks,
    compute hashes for each chunk, and encapsulate them into LangChain `Document`
    objects enriched with metadata, including chunk-specific and source-specific details.
    """

    @staticmethod
    def create_template(chunks: list[str], metadata: dict) -> Document:
        """
        Create a list of LangChain `Document` objects from text chunks and metadata.

        Each chunk is assigned a unique UUID, an MD5 hash, and positional metadata
        including the previous and next chunk hashes (if applicable). The resulting
        documents are useful for traceable, chunk-wise processing in language models
        or knowledge systems.

        Args:
            chunks (list[str]): List of string text chunks to convert into documents.
            metadata (dict): Dictionary containing metadata about the source of the content.
                             This will be embedded under the `source_info` key in each document.

        Returns:
            Document: A LangChain `Document` objects, each containing:
                - `page_content`: The text content of the chunk.
                - `metadata`: A dictionary with:
                    - `chunk_info`: Metadata about the chunk (number, id, hashes, size).
                    - `source_info`: The input metadata dictionary (name, size, dates, ext., type, desc, pages, hash).
        """

        docs = []
        chunk_hashes = [hashlib.md5(chunk.encode()).hexdigest() for chunk in chunks]

        for i, chunk in enumerate(chunks):
            chunk_number = i + 1
            chunk_id = uuid.uuid4().hex
            chunk_hash = chunk_hashes[i]

            chunk_info = {
                "chunk_number": chunk_number,
                "chunk_id": chunk_id,
                "chunk_hash": chunk_hash,
                "previous_chunk_hash": chunk_hashes[i - 1] if i > 0 else None,
                "next_chunk_hash": chunk_hashes[i + 1] if i < len(chunks) - 1 else None,
                "chunk_size": len(chunk),
            }

            doc_metadata = {
                "chunk_info": chunk_info,
                "source_info": metadata
            }

            doc = Document(
                page_content=chunk,
                metadata=doc_metadata
            )
            docs.append(doc)
        return docs