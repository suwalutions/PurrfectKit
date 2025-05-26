from typing import BinaryIO, Dict, List, Any
from langchain_core.documents import Document
from transformers import PreTrainedTokenizerBase, PreTrainedModel

from purrfectmeow.taeng.file_handler import HandleFile
from purrfectmeow.taeng.file_metadata import MetadataFile
from purrfectmeow.taeng.model_loader import LoadingModel
from purrfectmeow.taeng.template_doc import DocTemplate

class Suphalaks:
    """
    Provides utilities for file handling, model loading, and document templating.

    Parameters
    ----------
    file : BinaryIO
        The binary file object to save.
    file_name : str
        The name of the file for temporary storage.

    Returns
    -------
    str
        The file path of the saved temporary file.

    Examples
    --------
    >>> from io import BytesIO
    >>> file = BytesIO(b"Sample content")
    >>> Suphalaks.save_file(file, "sample.txt")
    '/tmp/sample.txt'
    
    Removes a temporary file from the specified file path.

    Parameters
    ----------
    file_path : str
        The path of the temporary file to remove.

    Examples
    --------
    >>> Suphalaks.remove_file('/tmp/sample.txt')
    
    Loads a pre-trained model based on the specified model name.

    Parameters
    ----------
    model_name : str
        The name of the model to load. Defaults to
        'intfloat/multilingual-e5-large-instruct' if empty.

    Returns
    -------
    PreTrainedModel
        The loaded pre-trained model.

    Examples
    --------
    >>> model = Suphalaks.get_model("intfloat/multilingual-e5-large-instruct")
    
    Loads a tokenizer for a specified model.

    Parameters
    ----------
    model_name : str
        The name of the model for which to load the tokenizer. Defaults to
        'intfloat/multilingual-e5-large-instruct' if empty.

    Returns
    -------
    PreTrainedTokenizerBase
        The loaded tokenizer for the specified model.

    Examples
    --------
    >>> tokenizer = Suphalaks.get_tokenizer("intfloat/multilingual-e5-large-instruct")
    
    Extracts metadata from a file at the specified file path.

    Parameters
    ----------
    file_path : str
        The path to the file from which to extract metadata.

    Returns
    -------
    Dict
        A dictionary containing the file's metadata.

    Examples
    --------
    >>> metadata = Suphalaks.get_file_metadata('/tmp/sample.pdf')
    {'filename': 'sample.pdf', 'size': 1024}
    
    Creates a document template from text chunks and metadata.

    Parameters
    ----------
    chunks : List[str]
        A list of text chunks to include in the document. Defaults to an empty list.
    metadata : Dict[str, Any]
        A dictionary of metadata to associate with the document. Defaults to an empty
        dictionary.

    Returns
    -------
    Document
        A Document object created from the provided chunks and metadata.

    Examples
    --------
    >>> chunks = ["chunk1", "chunk2"]
    >>> metadata = {"source": "sample.pdf"}
    >>> doc = Suphalaks.document_template(chunks, metadata)
    """

    @staticmethod
    def save_file(file: BinaryIO, file_name: str) -> str:
        return HandleFile.save_temp_file(file, file_name)

    @staticmethod
    def remove_file(file_path: str) -> None:
        HandleFile.remove_temp_file(file_path)

    @staticmethod
    def get_model(model_name: str) -> PreTrainedModel:
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_model(model_name)

    @staticmethod
    def get_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_tokenizer(model_name)

    @staticmethod
    def get_file_metadata(file_path: str) -> Dict:
        return MetadataFile(file_path).get_metadata()

    @staticmethod
    def document_template(chunks: List[str], metadata: Dict[str, Any]) -> Document:
        chunks = chunks or []
        metadata = metadata or {}
        return DocTemplate.create_template(chunks, metadata)