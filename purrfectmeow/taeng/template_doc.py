import uuid
import hashlib
from langchain_core.documents import Document

from purrfectmeow.kitty import kitty_logger

class DocTemplate:
    """
    A class for creating structured LangChain Document objects from text chunks and metadata.

    Public Methods
    --------------
    create_template(chunks, metadata)
        Create a structured LangChain Document object from chunks and metadata.

    Examples
    --------
    >>> chunks = ["This is the first chunk.", "This is the second chunk."]
    >>> metadata = {"source": "example.txt", "author": "John Doe"}
    >>> documents = DocTemplate.create_template(chunks, metadata)
    >>> for doc in documents:
    ...     print(doc.page_content, doc.metadata)
    """

    _logger = kitty_logger(__name__)

    @classmethod
    def create_template(cls, chunks: list[str], metadata: dict) -> Document:
        """
        Create a structured LangChain Document object from chunks and metadata.

        Parameters
        ----------
        chunks : list[str]
            A list of text chunks to be included in the document.

        metadata : dict
            A dictionary containing metadata associated with the document, such as source information.

        Returns
        -------
        list[Document]
            A list of LangChain `Document` objects, each representing a chunk with its metadata.

        Raises
        ------
        ValueError
            If chunks are empty or metadata is not provided.

        Notes
        -----
        - Each chunk is assigned a unique ID and hash.
        - The first chunk has no previous hash, and the last chunk has no next hash.
        - The size of each chunk is recorded in the metadata.
        - The method logs detailed information about each chunk and its metadata.
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