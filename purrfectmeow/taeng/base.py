from typing import BinaryIO
from transformers import PreTrainedTokenizerBase, PreTrainedModel

from purrfectmeow.taeng.file_handler import HandleFile
from purrfectmeow.taeng.model_loader import LoadingModel

class Suphalaks:
    """
    A utility class for simplified file handling and Hugging Face model/tokenizer loading.

    This class abstracts away repetitive tasks such as saving and removing temporary files, 
    and loading tokenizers or models via Hugging Face's `transformers` library. It serves 
    as a wrapper around lower-level utility classes, making the codebase more concise and 
    easier to maintain.

    Methods:
        save_file(file: BinaryIO, file_name: str) -> str
            Saves a binary file to a temporary location.

        remove_file(file_path: str) -> None
            Deletes the specified file from the filesystem.

        get_model(model_name: str) -> PreTrainedModel
            Loads and returns a pretrained model from Hugging Face.
            Defaults to "intfloat/multilingual-e5-large-instruct".

        get_tokenizer(model_name: str) -> PreTrainedTokenizerBase
            Loads and returns a pretrained tokenizer from Hugging Face.
            Defaults to "intfloat/multilingual-e5-large-instruct".

    Example:
        >>> from purrfectmeow import Suphalaks
        >>> tokenizer = Suphalaks.get_tokenizer()
        >>> model = Suphalaks.get_model()
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
    def get_model(model_name: str = "intfloat/multilingual-e5-large-instruct") -> PreTrainedModel:
        """
        Loads a pretrained model from Hugging Face's model hub.

        Args:
            model_name (str): Name or path of the pretrained model.

        Returns:
            PreTrainedModel: Loaded Hugging Face model instance.

        Raises:
            ValueError: If the model name is invalid or loading fails.

        Example:
            >>> model = Suphalaks.get_model("bert-base-uncased")
        """
        return LoadingModel().get_model(model_name)

    @staticmethod
    def get_tokenizer(model_name: str = "intfloat/multilingual-e5-large-instruct") -> PreTrainedTokenizerBase:
        """
        Loads a tokenizer from the Hugging Face Transformers library.

        Args:
            model_name (str): Name or path of the tokenizer to load.

        Returns:
            PreTrainedTokenizerBase: Tokenizer instance associated with the model.

        Raises:
            ValueError: If the tokenizer cannot be loaded.

        Example:
            >>> tokenizer = Suphalaks.get_tokenizer("bert-base-uncased")
        """
        return LoadingModel().get_tokenizer(model_name)