from typing import BinaryIO, Dict, List, Any
from langchain_core.documents import Document
from transformers import PreTrainedTokenizerBase, PreTrainedModel

from purrfectmeow.taeng.file_handler import HandleFile
from purrfectmeow.taeng.file_metadata import MetadataFile
from purrfectmeow.taeng.model_loader import LoadingModel
from purrfectmeow.taeng.template_doc import DocTemplate

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

    @classmethod
    def save_file(cls, file: BinaryIO, file_name: str) -> str:
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
    
    @classmethod
    def remove_file(cls, file_path: str) -> None:
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

    @classmethod
    def get_model(cls, model_name: str) -> PreTrainedModel:
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
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_model(model_name)

    @classmethod
    def get_tokenizer(cls, model_name: str) -> PreTrainedTokenizerBase:
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
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_tokenizer(model_name)
    
    @classmethod
    def get_file_metadata(cls, file_path: str) -> Dict:
        """
        Extract metadata from a given file path.

        Args:
            file_path (str): The path to the file from which to extract metadata.

        Returns:
            Dict: A dictionary containing metadata information about the file.
        
        Example:
            >>> metadata = Suphalaks.get_file_metadata('/path/to/file.pdf')
        """
        return MetadataFile(file_path).get_metadata()

    @classmethod
    def get_document_template(cls, chunks: List[str], metadata: Dict[str, Any]) -> Document:
        """
        Generate a LangChain Document from text chunks and metadata.

        This static method serves as a wrapper around `DocTemplate.create_template`,
        transforming raw text chunks and associated metadata into a structured 
        `Document` object compatible with LangChain.

        Args:
            chunks (List[str]): A list of text chunks representing parts of the document.
            metadata (Dict[str, Any]): Metadata dictionary to embed within each document.

        Returns:
            Document: A LangChain Document composed of the provided chunks and metadata.

        Example:
            >>> chunks = ["you only", "live once"]
            >>> metadata = {"source": "file.txt"}
            >>> doc = Suphalaks.get_document_template(chunks, metadata)
        """
        chunks = chunks or []
        metadata = metadata or {}
        return DocTemplate.create_template(chunks, metadata)