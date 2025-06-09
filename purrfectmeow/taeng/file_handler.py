import os
from typing import BinaryIO

from purrfectmeow.kitty import kitty_logger

class HandleFile:
    """
    A utility class for handling file operations such as saving and removing files.

    Public Methods
    --------------
    save_temp_file(file, file_name)
        Save a binary file to a temporary directory.
    remove_temp_file(file_path)
        Remove a specified file from the filesystem if it exists.

    Examples
    --------
    >>> with open('example.txt', 'rb') as f:
    ...     file_path = HandleFile.save_temp_file(f, 'example.txt')
    >>> print(file_path)
    tmp_dir/example.txt
    >>> HandleFile.remove_temp_file('tmp_dir/example.txt')
    """
    _logger = kitty_logger(__name__)

    TMP_DIR = 'tmp_dir/'
    os.makedirs(TMP_DIR, exist_ok=True)
    _logger.debug(f"Temporary directory initialized at: {TMP_DIR}")
        
    @classmethod
    def save_temp_file(cls, file: BinaryIO, file_name: str) -> str:
        """
        Save a binary file to a temporary directory.

        Parameters
        ----------
        file : BinaryIO
            The binary file to be saved.

        file_name : str
            The name to use for the saved file.

        Returns
        -------
        str
            The path to the saved file.

        Raises
        ------
        Exception
            If there is an error during file saving.

        Notes
        -----
        This method saves the file to a predefined temporary directory (`tmp_dir/`).
        """
        file_path = os.path.join(cls.TMP_DIR, file_name)
        try:
            with open(file_path, 'wb') as f:
                data = file.read()
                f.write(data)
            cls._logger.debug(f"File saved: {file_path} ({len(data)} bytes)")
            return file_path
        except Exception as e:
            cls._logger.error(f"Failed to save file {file_name}: {e}", exc_info=True)
            raise
    
    @classmethod
    def remove_temp_file(cls, file_path: str) -> None:
        """
        Remove a specified file from the filesystem if it exists.

        Parameters
        ----------
        file_path : str
            The path of the file to be removed.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If there is an error during file removal.

        Notes
        -----
        - This method attempts to remove the file at the specified path. 
        - If the file does not exist, it logs a warning. 
        - If an error occurs during removal, it logs the error and raises an exception.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                cls._logger.debug(f"File removed: {file_path}")
            else:
                cls._logger.warning(f"Tried to remove non-existent file: {file_path}")
        except Exception as e:
            cls._logger.error(f"Failed to remove file {file_path}: {e}", exc_info=True)
            raise