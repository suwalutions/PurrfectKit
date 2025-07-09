from io import BytesIO
from typing import Dict, List, Any, Union
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from transformers import PreTrainedTokenizerBase, PreTrainedModel

from purrfectmeow.taeng.template_doc import DocTemplate
from purrfectmeow.taeng.model_loader import LoadingModel
from purrfectmeow.taeng.file_metadata import MetadataFile

class Suphalaks:
    """
    A class for handling files, loading models, and creating document templates.

    This class consolidates methods from `LoadingModel`, `DocTemplate` and `MetadataFile`
    to perform common operations such as saving/removing files, retrieving models and tokenizers, 
    extracting file metadata, and creating structured LangChain document templates.
    """

    @staticmethod
    def get_tokenizer(model_name: str = None) -> PreTrainedTokenizerBase:
        """
        Retrieve a Hugging Face tokenizer by model name.

        Parameters
        ----------
        model_name : str, optional
            The name of the model. If None, a default is used.

        Returns
        -------
        PreTrainedTokenizerBase
            The tokenizer corresponding to the specified model.

        Examples
        --------
        >>> tokenizer = Suphalaks.get_tokenizer('bert-base-uncased')
        """
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_hf_tokenizer(model_name)

    @staticmethod
    def get_model_hf(model_name: str = None) -> PreTrainedModel:
        """
        Retrieve a Hugging Face model by model name.

        Parameters
        ----------
        model_name : str, optional
            The name of the model. If None, a default is used.

        Returns
        -------
        PreTrainedModel
            The loaded Hugging Face model.

        Examples
        --------
        >>> model = Suphalaks.get_model_hf('bert-base-uncased')
        """
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_hf_model(model_name)
    
    @staticmethod
    def get_model_st(model_name: str = None) -> SentenceTransformer:
        """
        Retrieve a SentenceTransformer model by model name.

        Parameters
        ----------
        model_name : str, optional
            The name of the model. If None, a default is used.

        Returns
        -------
        SentenceTransformer
            The loaded SentenceTransformer model.

        Examples
        --------
        >>> st_model = Suphalaks.get_model_st('all-MiniLM-L6-v2')
        """
        model_name = model_name or "intfloat/multilingual-e5-large-instruct"
        return LoadingModel.get_st_model(model_name)

    @staticmethod
    def get_file_metadata(file: Union[str, BytesIO]) -> Dict:
        """
        Extract metadata from a file, supporting both file paths and in-memory file-like objects.

        Parameters
        ----------
        file : Union[str, BytesIO]
            The file to extract metadata from. Can be:
            - A string path to a file on disk.
            - A BytesIO object representing an in-memory file.

        Returns
        -------
        Dict
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

        Examples
        --------
        >>> metadata = Suphalaks.get_file_metadata('tmp_dir/example.txt')
        >>> with open('tmp_dir/example.txt', 'rb') as f:
        ...     metadata = Suphalaks.get_file_metadata(f.read())
        """
        return MetadataFile(file).get_metadata()

    @staticmethod
    def document_template(chunks: List[str], metadata: Dict[str, Any]) -> Document:
        """
        Create a structured LangChain Document object from chunks and metadata.

        Parameters
        ----------
        chunks : List[str]
            A list of text chunks.
        metadata : Dict[str, Any]
            A dictionary containing metadata associated with the document.

        Returns
        -------
        Document
            A structured LangChain `Document` object.

        Examples
        --------
        >>> chunks = ["This is the first chunk.", "This is the second chunk."]
        >>> metadata = {"source": "example.txt", "author": "John Doe"}
        >>> document = Suphalaks.document_template(chunks, metadata)
        >>> print(document.page_content, document.metadata)
        """
        chunks = chunks or []
        metadata = metadata or {}
        return DocTemplate.create_template(chunks, metadata)