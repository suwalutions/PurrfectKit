import torch
import numpy
from typing import List, Optional, Tuple
from langchain_core.documents import Document
from transformers import PreTrainedModel, PreTrainedTokenizer

from purrfectmeow.taeng.model_loader import LoadingModel
from purrfectmeow.kitty import kitty_logger

class SimpleHFEmbedder:
    """
    A simple for converting documents or queries into dense vector embeddings.

    Public Methods
    --------------
    embed_documents(documents, model_name)
        Embed a list of `Document` objects into dense vectors.

    embed_query(query, model_name)
        Embed a single query string into a dense vector.

    Examples
    --------
    >>> docs = [Document(page_content="สวัสดี"), Document(page_content="คุณเป็นอย่างไรบ้าง")]
    >>> SimpleHFEmbedder.embed_documents(docs, model_name="intfloat/multilingual-e5-large-instruct")
    array([[...], [...]])

    >>> SimpleHFEmbedder.embed_query("สภาพอากาศเป็นอย่างไร", model_name="intfloat/multilingual-e5-large-instruct")
    array([...])
    """
    _logger = kitty_logger(__name__)

    _DEFAULT_MODEL_NAME: str = "intfloat/multilingual-e5-large-instruct"

    @classmethod
    def _get_tokenizer(cls, model_name: str) -> PreTrainedTokenizer:
        """
        Load the tokenizer for a given model name.

        Parameters
        ----------
        model_name : str
            The pretrained model identifier.

        Returns
        -------
        PreTrainedTokenizer
            The tokenizer instance corresponding to the model.

        Notes
        -----
        This method uses `Loading.get_hf_tokenizer()` to retrieve the tokenizer.
        """
        cls._logger.debug(f"Loading tokenizer for model '{model_name}'")
        return LoadingModel.get_hf_tokenizer(model_name)

    @classmethod
    def _get_model(
        cls,
        model_name: str, 
    ) -> PreTrainedModel:
        """
        Load the pretrained model on the specified device.

        Parameters
        ----------
        model_name : str
            The pretrained model identifier.

        Returns
        -------
        PreTrainedModel
            The loaded model.

        Notes
        -----
        This method uses `Loading.get_hf_model()` to retrieve the model.
        """
        # device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        cls._logger.debug(f"Loading model '{model_name}'")
        model = LoadingModel.get_hf_model(model_name)
        # model.to(device)
        return model

    @classmethod
    def _mean_pooling(
        cls,
        model_output: Tuple[torch.Tensor], 
        attention_mask: torch.Tensor
    ) -> torch.Tensor:
        """
        Apply mean pooling to the token embeddings from the model output.

        Parameters
        ----------
        model_output : Tuple[torch.Tensor]
            Output tuple from the transformer model forward pass.
        attention_mask : torch.Tensor
            Attention mask indicating valid tokens (1) vs padding (0).

        Returns
        -------
        torch.Tensor
            The mean pooled embedding tensor.

        Notes
        -----
        This method computes the weighted average of token embeddings.
        """
        cls._logger.debug("Performing mean pooling on model outputs")
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        pooled = torch.sum(token_embeddings * input_mask_expanded, 1) / input_mask_expanded.sum(1)
        cls._logger.debug(f"Pooled embeddings shape: {pooled.shape}")
        return pooled

    @classmethod
    def embed_documents(
        cls,
        documents: List[Document], 
        model_name: Optional[str] = None, 
        device: Optional[str] = None
    ) -> numpy.ndarray:
        """
        Embed a list of Document objects into dense vector embeddings.

        Parameters
        ----------
        documents : List[Document]
            A list of langchain Document instances to embed.
        model_name : Optional[str]
            Name or path of the pretrained transformer model to use.
        device : Optional[str]
            Compute device to load the model on (e.g., 'cpu', 'cuda').

        Returns
        -------
        numpy.ndarray
            A 2D numpy array where each row is the embedding vector of a document.

        Notes
        -----
        This method tokenizes the document content.
        """
        model_name = model_name or SimpleHFEmbedder._DEFAULT_MODEL_NAME
        cls._logger.debug(f"Embedding documents using model '{model_name}'")

        tokenizer = SimpleHFEmbedder._get_tokenizer(model_name)
        cls._logger.debug("Tokenizer loaded successfully")

        model = SimpleHFEmbedder._get_model(model_name)
        cls._logger.debug(f"Model loaded on device '{device}'")

        texts: List[str] = [doc.page_content for doc in documents]
        cls._logger.debug(f"Number of documents to embed: {len(texts)}")

        with torch.no_grad():
            encoded = tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(device)
            cls._logger.debug(f"Tokenized inputs: input_ids shape {encoded['input_ids'].shape}")

            output = model(**encoded)
            cls._logger.debug("Model forward pass complete")

        embeddings = SimpleHFEmbedder._mean_pooling(output, encoded['attention_mask'])
        cls._logger.debug(f"Embeddings computed with shape {embeddings.shape}")

        return embeddings.cpu().numpy()

    @classmethod
    def embed_query(
        cls,
        query: str, 
        model_name: Optional[str] = None,
    ) -> numpy.ndarray:
        """
        Embed a single query string into a dense vector embedding.

        Parameters
        ----------
        query : str
            The input query string to embed.
        model_name : Optional[str]
            Name or path of the pretrained transformer model to use.

        Returns
        -------
        numpy.ndarray
            A 1D numpy array representing the embedding vector of the query.

        Notes
        -----
        This method wraps the query.
        """
        cls._logger.debug(f"Embedding query: '{query[:50]}...'")
        doc = Document(page_content=query, metadata={})
        cls._logger.debug("Query embedding computed")
        return SimpleHFEmbedder.embed_documents([doc], model_name)[0]