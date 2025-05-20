import os
from typing import BinaryIO

class HandleFile:
    TMP_DIR = 'tmp_dir/'
    os.makedirs(TMP_DIR, exist_ok=True)
        
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
        with open(file_path, 'wb') as f:
            f.write(file.read())
        return file_path
    
    @staticmethod
    def remove_temp_file(file_path: str) -> None:
        """
        Deletes a file from the filesystem if it exists.

        Args:
            file_path (str): The path of the file to delete.

        Returns:
            None
        """
        if os.path.exists(file_path):
            os.remove(file_path)