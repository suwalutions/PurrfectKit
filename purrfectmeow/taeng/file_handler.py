import os
from typing import BinaryIO

from purrfectmeow.kitty import kitty_logger

class HandleFile:
    """
    A utility class for handling temporary file operations.

    This class provides methods to save a binary file to a temporary directory
    and to remove it when no longer needed. The temporary directory is created
    automatically if it does not exist.

    Attributes:
        TMP_DIR (str): Path to the temporary directory where files are stored.

    Methods:
        save_temp_file(file: BinaryIO, file_name: str) -> str:
            Saves a binary file to the temporary directory and returns its path.

        remove_temp_file(file_path: str) -> None:
            Removes the specified file from the filesystem if it exists.
    """
    _logger = kitty_logger(__name__)

    TMP_DIR = 'tmp_dir/'
    os.makedirs(TMP_DIR, exist_ok=True)
    _logger.debug(f"Temporary directory initialized at: {TMP_DIR}")
        
    @classmethod
    def save_temp_file(cls, file: BinaryIO, file_name: str) -> str:
        """
        Saves an uploaded file to a temporary directory.

        Args:
            file (BinaryIO): A file-like object.
            file_name (str): Name of the file to be saved.

        Returns:
            str: Full path to the saved file.
        """
        file_path = os.path.join(cls.TMP_DIR, file_name)
        try:
            with open(file_path, 'wb') as f:
                data = file.read()
                f.write(data)
            cls._logger.info(f"File saved: {file_path} ({len(data)} bytes)")
            return file_path
        except Exception as e:
            cls._logger.error(f"Failed to save file {file_name}: {e}", exc_info=True)
            raise
    
    @classmethod
    def remove_temp_file(cls, file_path: str) -> None:
        """
        Deletes a file from the filesystem if it exists.

        Args:
            file_path (str): The path of the file to delete.

        Returns:
            None
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                cls._logger.info(f"File removed: {file_path}")
            else:
                cls._logger.warning(f"Tried to remove non-existent file: {file_path}")
        except Exception as e:
            cls._logger.error(f"Failed to remove file {file_path}: {e}", exc_info=True)
            raise