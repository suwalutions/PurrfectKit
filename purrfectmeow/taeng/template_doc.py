import uuid
import hashlib
from langchain_core.documents import Document

from purrfectmeow.kitty import kitty_logger

class DocTemplate:
    """
    A utility class for generating structured document chunks with metadata.

    This class provides a method to split text content into smaller chunks,
    compute hashes for each chunk, and encapsulate them into LangChain `Document`
    objects enriched with metadata, including chunk-specific and source-specific details.
    """
    _logger = kitty_logger(__name__)

    @classmethod
    def create_template(cls, chunks: list[str], metadata: dict) -> Document:
        """
        Create a list of LangChain `Document` objects from text chunks and metadata.

        Each chunk is assigned a unique UUID, an MD5 hash, and positional metadata
        including the previous and next chunk hashes (if applicable). The resulting
        documents are useful for traceable, chunk-wise processing in language models
        or knowledge systems.

        Args:
            chunks (list[str]): List of string text chunks to convert into documents.
            metadata (dict): Dictionary containing metadata about the source of the content.

        Returns:
            list[Document]: List of LangChain `Document` objects with structured metadata.

        Example:
            >>> chunks = ["Hello world.", "This is a test."]
            >>> metadata = {"source": "example.txt", "type": "text", "desc": "Sample file"}
            >>> docs = DocTemplate.create_template(chunks, metadata)
            >>> for doc in docs:
            >>>     print(doc.page_content)
            >>>     print(doc.metadata)
        """

        docs = []
        chunk_hashes = []

        for idx, chunk in enumerate(chunks):
            hash_val = hashlib.md5(chunk.encode()).hexdigest()
            chunk_hashes.append(hash_val)
            cls._logger.debug(f"[Chunk {idx+1}] MD5 hash: {hash_val}")

        for idx, chunk in enumerate(chunks):
            chunk_number = idx + 1
            chunk_id = uuid.uuid4().hex
            chunk_hash = chunk_hashes[idx]
            prev_hash = chunk_hashes[idx - 1] if idx > 0 else None
            next_hash = chunk_hashes[idx + 1] if idx < len(chunks) - 1 else None
            chunk_size = len(chunk)

            cls._logger.debug(
                f"[Chunk {chunk_number}] Creating document | ID: {chunk_id}, Size: {chunk_size}, "
                f"Prev: {prev_hash}, Current: {chunk_hash}, Next: {next_hash}"
            )

            chunk_info = {
                "chunk_number": chunk_number,
                "chunk_id": chunk_id,
                "chunk_hash": chunk_hash,
                "previous_chunk_hash": prev_hash,
                "next_chunk_hash": next_hash,
                "chunk_size": chunk_size,
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

        cls._logger.debug("Document creation complete.")
        return docs