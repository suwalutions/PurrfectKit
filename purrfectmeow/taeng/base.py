from typing import BinaryIO
from transformers import PreTrainedTokenizerBase

from purrfectmeow.taeng.file_handler import HandleFile
from purrfectmeow.taeng.tokenizer import HFTokeniker

class Suphalaks:
    """
    A convenience class that wraps utility functions for tokenizer loading and file handling.

    This class serves as a simplified interface, making it easy to manage temporary files 
    and load tokenizers without needing to interact with the underlying utility classes directly.

    Methods:
        save_file(file: BinaryIO, file_name: str) -> str:

            Saves a binary file to a predefined temporary directory.

        remove_file(file_path: str) -> None:

            Deletes a file from the filesystem if it exists.

        get_tokenizer(model_name: str):
        
            Loads and returns a Hugging Face tokenizer instance, with caching support.

    Example usage:
        >>> from purrfectmeow import Suphalaks
        >>> tokenizer = Suphalaks.get_tokenizer("intfloat/multilingual-e5-large-instruct")
    """

    @staticmethod
    def save_file(file: BinaryIO, file_name: str) -> str:
        """
        Saves a binary file to a temporary directory.

        Args:
            file (BinaryIO): A binary file-like object to save.
            file_name (str): The name to assign to the saved file.

        Returns:
            str: The full path to the saved temporary file.

        Examples:
            >>> with open("example.txt", "rb") as f:
            ...     path = Suphalaks.save_file(f, "copy.txt")
        """
        return HandleFile.save_temp_file(file, file_name)
    
    @staticmethod
    def remove_file(file_path: str) -> None:
        """
        Removes a file from the filesystem.

        Args:
            file_path (str): The path of the file to be removed.

        Returns:
            None

        Examples:
            >>> Suphalaks.remove_file("tmp_dir/copy.txt")
        """
        HandleFile.remove_temp_file(file_path)

    @staticmethod
    def get_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
        """
        Loads a tokenizer from the Hugging Face Transformers library.

        Args:
            model_name (str): The name or path of the model for which to load the tokenizer.

        Returns:
            PreTrainedTokenizerBase: A tokenizer instance corresponding to the specified model.

        Raises:
            ValueError: If the model name is invalid or the tokenizer cannot be loaded.

        Examples:
            >>> tokenizer = Suphalaks.get_tokenizer("intfloat/multilingual-e5-large-instruct")
        """
        return HFTokeniker.get_tokenizer(model_name)