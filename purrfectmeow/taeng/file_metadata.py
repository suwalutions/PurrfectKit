import os
import io
import re
import time
import magic
import hashlib
import subprocess
from typing import Dict, Union, BinaryIO

from purrfectmeow.kitty import kitty_logger

class MetadataFile:
    """
    A utility class for extracting metadata from files or file-like objects.

    This class supports both file paths (as strings) and in-memory file-like objects
    such as `io.BytesIO`. It extracts various metadata fields including file name,
    size, type, MD5 checksum, and more. For PDF files, it attempts to detect the
    total number of pages.

    Parameters
    ----------
    file : Union[str, io.BytesIO]
        The file to extract metadata from. Can be a file path (str) or a BytesIO object.

    Public Methods
    --------------
    get_metadata() -> Dict[str, str]
        Extracts metadata and returns it as a dictionary.

    Example
    -------
    >>> # Using file path
    >>> metadata_extractor = MetadataFile('path/to/file.pdf')
    >>> metadata = metadata_extractor.get_metadata()

    >>> # Using BytesIO object
    >>> from io import BytesIO
    >>> with open('path/to/file.pdf', 'rb') as f:
    ...     byte_data = BytesIO(f.read())
    >>> metadata_extractor = MetadataFile(byte_data)
    >>> metadata = metadata_extractor.get_metadata()

    Sample Output
    -------------
    {
        'file_name': 'file.pdf',
        'file_size': 12345,
        'file_created_date': '2023-10-01 12:00:00',
        'file_modified_date': '2023-10-02 12:00:00',
        'file_extension': '.pdf',
        'file_type': 'application/pdf',
        'description': 'PDF document, version 1.7',
        'total_pages': 5,
        'file_md5': 'd41d8cd98f00b204e9800998ecf8427e'
    }
    """
    _logger = kitty_logger(__name__)

    def __init__(self, file: Union[str, io.BytesIO]) -> None:
        """
        Initializes the MetadataFile instance with either a file path or a file-like object.

        Parameters
        ----------
        file : Union[str, io.BytesIO]
            The file to extract metadata from. Can be:
            - A string representing the file path on disk.
            - A BytesIO object representing an in-memory binary file.

        Raises
        ------
        TypeError
            If the provided `file` is neither a string nor a BytesIO object.
        """
        if isinstance(file, str):
            self.file_path = file
            self.file_obj = None
        elif isinstance(file, io.BytesIO):
            self.file_obj = file
            self.file_path = None
        else:
            raise TypeError("file must be a file path (str) or a BytesIO object")
        
        self.metadata = {}

    def get_metadata(self) -> Dict[str, str]:
        """
        Extracts metadata from the file.

        If a file path was provided during initialization, this delegates to
        `_get_metadata_from_path`. If a BytesIO object was provided, it delegates to
        `_get_metadata_from_bytes`.

        Returns
        -------
        Dict[str, str]
            A dictionary containing metadata such as:
            - 'file_name'
            - 'file_size'
            - 'file_created_date'
            - 'file_modified_date'
            - 'file_extension'
            - 'file_type'
            - 'description'
            - 'total_pages'
            - 'file_md5'

        Raises
        ------
        RuntimeError
            If metadata extraction fails.
        """
        if self.file_path:
            return self._get_metadata_from_path()
        else:
            return self._get_metadata_from_bytes()

    def _get_metadata_from_path(self) -> Dict[str, str]:
        """
        Extracts metadata from a file located on disk using its file path.

        This includes file size, creation/modification timestamps, MIME type,
        description, page count (for PDFs), and MD5 checksum.

        Returns
        -------
        Dict[str, str]
            A dictionary containing extracted metadata.

        Raises
        ------
        FileNotFoundError
            If the specified file path does not exist.
        RuntimeError
            If metadata extraction fails due to an unexpected error.
        """
        try:
            self._logger.debug("Starting metadata extraction for file path")
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
        
    def _get_metadata_from_bytes(self) -> Dict[str, str]:
        """
        Extracts metadata from a file-like object (BytesIO).

        Since file system metadata (e.g. timestamps) is unavailable for in-memory
        files, those fields will be set to 'N/A' or appropriate fallbacks.
        MIME type and MD5 checksum are inferred from the byte content.

        Returns
        -------
        Dict[str, str]
            A dictionary containing extracted metadata.

        Raises
        ------
        RuntimeError
            If metadata extraction fails due to an unexpected error.
        """
        try:
            self._logger.debug("Starting metadata extraction from BytesIO")
            self.file_obj.seek(0, os.SEEK_END)
            size = self.file_obj.tell()
            self.file_obj.seek(0)

            self.metadata["file_name"] = "uploaded_file"
            self.metadata["file_size"] = size
            self.metadata["file_created_date"] = "N/A"
            self.metadata["file_modified_date"] = "N/A"
            self.metadata["file_extension"] = "unknown"

            magic_obj = magic.Magic(mime=True)
            self.metadata["file_type"] = magic_obj.from_buffer(self.file_obj.read(2048))
            self.file_obj.seek(0)
            self.metadata["description"] = magic.from_buffer(self.file_obj.read(2048))
            self.file_obj.seek(0)

            self.metadata["total_pages"] = 1
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: self.file_obj.read(4096), b""):
                hash_md5.update(chunk)
            self.file_obj.seek(0)
            self.metadata["file_md5"] = hash_md5.hexdigest()

            return self.metadata

        except Exception as e:
            self._logger.error(f"Failed to extract metadata from BytesIO: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to extract metadata: {str(e)}")