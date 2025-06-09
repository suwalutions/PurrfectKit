import os
import re
import time
import magic
import hashlib
import subprocess
from typing import Dict

from purrfectmeow.kitty import kitty_logger

class MetadataFile:
    """
    A utility class for extracting metadata from files.

    Public Methods
    --------------
    get_metadata()
        Extracts metadata from the specified file and returns it as a dictionary.

    Example
    -------
    >>> metadata_extractor = MetadataFile('path/to/file.txt')
    >>> metadata = metadata_extractor.get_metadata()
    >>> print(metadata)
    {
        'file_name': 'file.txt',
        'file_size': 12345,
        'file_created_date': '2023-10-01 12:00:00',
        'file_modified_date': '2023-10-02 12:00:00',
        'file_extension': '.txt',
        'file_type': 'text/plain',
        'description': 'Text file',
        'total_pages': 1,
        'file_md5': 'd41d8cd98f00b204e9800998ecf8427e'
    }
    """
    _logger = kitty_logger(__name__)

    def __init__(self, file_path: str) -> None:
        """
        Initializes the MetadataFile instance with the specified file path.

        Parameters
        ----------
        file_path : str
            The path to the file for which metadata will be extracted.
        """
        self.file_path = file_path
        self.metadata = {}

    def get_metadata(self) -> Dict[str, str]:
        """
        Extracts metadata from the specified file.
        
        Returns
        -------
        Dict[str, str]
            A dictionary containing extracted metadata fields:
            - 'file_name': str
            - 'file_size': int
            - 'file_created_date': str
            - 'file_modified_date': str
            - 'file_extension': str
            - 'file_type': str
            - 'description': str
            - 'total_pages': int or str
            - 'file_md5': str

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        RuntimeError
            If metadata extraction fails due to unexpected error.

        Notes
        -----
        - This method uses `os.stat`, `magic`, `subprocess`, and `hashlib` to extract file details.
        - PDF page count is determined using `pdfinfo`; non-PDF files default to 1 page.
        - Falls back to safe defaults if type detection or page count extraction fails.
        """
        try:
            self._logger.debug(f"Starting metadata extraction for file: {self.file_path}")
            if not os.path.exists(self.file_path):
                self._logger.error(f"File not found: {self.file_path}")
                raise FileNotFoundError(f"File {self.file_path} does not exist")

            stats = os.stat(self.file_path)
            self.metadata["file_name"] = os.path.basename(self.file_path)
            self.metadata["file_size"] = stats.st_size
            self.metadata["file_created_date"] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(stats.st_ctime)
            )
            self.metadata["file_modified_date"] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime)
            )
            self.metadata["file_extension"] = os.path.splitext(self.file_path)[1] or "none"

            self._logger.debug(
                f"Basic metadata extracted: name={self.metadata['file_name']}, "
                f"size={self.metadata['file_size']}, created={self.metadata['file_created_date']}, "
                f"modified={self.metadata['file_modified_date']}, extension={self.metadata['file_extension']}"
            )

            try:
                mime = magic.Magic(mime=True)
                self.metadata["file_type"] = mime.from_file(self.file_path)
                self.metadata["description"] = magic.from_file(self.file_path)
                self._logger.debug(
                    f"File type detected: {self.metadata['file_type']}, description: {self.metadata['description']}"
                )
            except Exception as e:
                self.metadata["file_type"] = "unknown"
                self.metadata["description"] = f"Could not determine file type: {str(e)}"
                self._logger.warning(f"Failed to determine file type: {str(e)}")

            if self.metadata["file_type"].startswith("image/"):
                self.metadata["total_pages"] = 1
                self._logger.debug("File is an image, total_pages set to 1")
            elif self.metadata["file_type"].startswith("application/pdf"):
                try:
                    self._logger.debug("File is a PDF, attempting to get page count via pdfinfo")
                    result = subprocess.run(
                        ['pdfinfo', self.file_path], 
                        stdout=subprocess.PIPE, 
                        text=True, 
                        check=True
                    )
                    pages_match = re.search(r"Pages:\s*(\d+)", result.stdout)
                    if pages_match:
                        self.metadata["total_pages"] = int(pages_match.group(1))
                        self._logger.debug(f"PDF page count found: {self.metadata['total_pages']}")
                    else:
                        self.metadata["total_pages"] = "Unknown (could not parse page count)"
                        self._logger.warning("pdfinfo output did not contain page count")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    self.metadata["total_pages"] = "Unknown (pdfinfo not installed or failed)"
                    self._logger.warning(f"Failed to get PDF page count: {str(e)}")
            else:
                self.metadata["total_pages"] = 1
                self._logger.debug("File type unknown or not PDF/image, total_pages set to 1")

            with open(self.file_path, "rb") as f:
                hash_md5 = hashlib.md5()
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                self.metadata["file_md5"] = hash_md5.hexdigest()
            self._logger.debug(f"MD5 checksum calculated: {self.metadata['file_md5']}")

            self._logger.debug("Metadata extraction completed successfully")
            return self.metadata

        except Exception as e:
            self._logger.error(f"Failed to extract metadata: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to extract metadata: {str(e)}")