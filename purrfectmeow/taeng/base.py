from typing import BinaryIO

from purrfectmeow.taeng.file_handler import HandleFile

class Suphalaks:
    @staticmethod
    def save_file(file: BinaryIO, file_name: str) -> str:
        """Saves a file to a temporay directory."""
        return HandleFile.save_temp_file(file, file_name)
    
    @staticmethod
    def remove_file(file_path: str) -> None:
        """"Removes a file from the filesystem."""
        HandleFile.remove_temp_file(file_path)