import os
import re
import time
import magic
import hashlib
import subprocess

from purrfectmeow.kitty import kitty_logger

class MetadataFile:
    """
    A class to extract and store metadata from a given file.

    Supports extraction of basic file system metadata (name, size, creation
    and modification dates, extension) as well as file type detection using
    the `magic` library. Additionally, it attempts to determine the total page
    count for PDF files using the `pdfinfo` tool, and defaults to 1 page for images.

    Attributes:
        file_path (str): Path to the target file.
        metadata (dict): Dictionary storing extracted metadata.

    Methods:
        get_metadata():
            Extract metadata from the file, return the stored metadata dictionary..
    """
    _logger = kitty_logger(__name__)

    def __init__(self, file_path):
        """
        Initialize MetadataFile with the path to a file.

        Args:
            file_path (str): The full path to the file to extract metadata from.
        """
        self.file_path = file_path
        self.metadata = {}

    def get_metadata(self):
        """
        Internal method to extract metadata from the file.

        This method collects:
            - File name
            - File size (in bytes)
            - File creation date and modification date (formatted as YYYY-MM-DD HH:MM:SS)
            - File extension (or "none" if no extension)
            - MIME type and description (using `magic` library)
            - Total pages:
                - For PDFs, uses `pdfinfo` to get the page count.
                - For images, defaults to 1.
                - For other file types, defaults to 1.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            RuntimeError: If metadata extraction fails for any other reason.

        Returns:
            dict: A dictionary containing extracted metadata.
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