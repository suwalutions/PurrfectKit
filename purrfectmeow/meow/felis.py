from typing import Any, Dict, List, Union

class Document:
    def __init__(self, page_content: str, metadata: Dict[str, Any]):
        self.page_content = page_content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"{self.__class__.__name__}(content={self.page_content!r}, metadata={self.metadata!r})"

    def __getitem__(self, key):
        if key == "page_content":
            return self.page_content
        elif key == "metadata":
            return self.metadata
        else:
            raise KeyError(f"{key} is not a valid key. Use 'page_content' or 'metadata'.")

    def to_dict(self):
        return {
            "page_content": self.page_content,
            "metadata": self.metadata
        }

class DocTemplate:
    @staticmethod
    def create_template(chunks: List[str], metadata: Dict[str, Any]) -> List[Document]:
        docs = []
        chunk_hashes = []

        import uuid
        import hashlib

        for idx, chunk in enumerate(chunks):
            hash_val = hashlib.md5(chunk.encode()).hexdigest()
            chunk_hashes.append(hash_val)

        for idx, chunk in enumerate(chunks):
            chunk_number = idx + 1
            chunk_id = uuid.uuid4().hex
            chunk_hash = chunk_hashes[idx]
            prev_hash = chunk_hashes[idx - 1] if idx > 0 else None
            next_hash = chunk_hashes[idx + 1] if idx < len(chunks) - 1 else None
            chunk_size = len(chunk)

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

        return docs

class MetaFile:
    @staticmethod
    def get_metadata(file: str) -> Dict[str, Union[str, int]]:
        return MetaFile._get_metadata_from_path(file)

    @staticmethod
    def _get_metadata_from_path(file_path: str) -> Dict[str, Union[str, int]]:
        metadata = {}
        
        import os
        import re
        import time
        import magic
        import hashlib
        import subprocess
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist")

            stats = os.stat(file_path)
            metadata["file_name"] = os.path.basename(file_path)
            metadata["file_size"] = stats.st_size
            metadata["file_created_date"] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(stats.st_ctime)
            )
            metadata["file_modified_date"] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime)
            )
            metadata["file_extension"] = os.path.splitext(file_path)[1] or "none"

            try:
                mime = magic.Magic(mime=True)
                metadata["file_type"] = mime.from_file(file_path)
                metadata["description"] = magic.from_file(file_path)
            except Exception as e:
                metadata["file_type"] = "unknown"
                metadata["description"] = f"Could not determine file type: {str(e)}"

            if metadata["file_type"].startswith("image/"):
                metadata["total_pages"] = 1
            elif metadata["file_type"].startswith("application/pdf"):
                try:
                    result = subprocess.run(
                        ['pdfinfo', file_path],
                        stdout=subprocess.PIPE,
                        text=True,
                        check=True
                    )
                    pages_match = re.search(r"Pages:\s*(\d+)", result.stdout)
                    if pages_match:
                        metadata["total_pages"] = int(pages_match.group(1))
                    else:
                        metadata["total_pages"] = "Unknown (could not parse page count)"
                except (subprocess.CalledProcessError, FileNotFoundError):
                    metadata["total_pages"] = "Unknown (pdfinfo not installed or failed)"
            else:
                metadata["total_pages"] = 1

            with open(file_path, "rb") as f:
                hash_md5 = hashlib.md5()
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                metadata["file_md5"] = hash_md5.hexdigest()

            return metadata

        except Exception as e:
            raise RuntimeError(f"Failed to extract metadata: {str(e)}")
