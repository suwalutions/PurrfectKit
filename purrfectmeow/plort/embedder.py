import torch
import numpy as np
from typing import List, Optional, Tuple
from langchain_core.documents import Document
from transformers import PreTrainedModel, PreTrainedTokenizer

from purrfectmeow.taeng import Suphalaks
from purrfectmeow.kitty import kitty_logger

class SimpleHFEmbedder:
    """
    A simple Hugging Face transformer-based embedder for converting documents or queries
    into dense vector embeddings using a pretrained model.

    This class wraps tokenizer and model loading management, and embedding
    computation including mean pooling over token embeddings. It supports embedding
    multiple documents or single queries and returns numpy arrays suitable for downstream
    tasks such as similarity search or classification.

    Attributes:
        _DEFAULT_MODEL_NAME (str): Default model identifier for embeddings if none provided.
        _logger (logging.Logger): Logger instance for debugging and info messages.

    Methods:
        embed_documents(documents, model_name=None) -> np.ndarray:
            Embed a list of `Document` objects into dense vectors.

        embed_query(query, model_name=None) -> np.ndarray:
            Embed a single query string into a dense vector.

        _get_tokenizer(model_name) -> PreTrainedTokenizer:
            Load the tokenizer corresponding to the specified model.

        _get_model(model_name) -> PreTrainedModel:
            Load the model on the specified device.

        _mean_pooling(model_output, attention_mask) -> torch.Tensor:
            Compute mean pooled embeddings from model output and attention mask.
    """
    _logger = kitty_logger(__name__)
    _DEFAULT_MODEL_NAME: str = "intfloat/multilingual-e5-large-instruct"

    @classmethod
    def embed_documents(
        cls,
        documents: List[Document], 
        model_name: Optional[str] = None, 
        device: Optional[str] = None
    ) -> np.ndarray:
        """
        Embed a list of Document objects into dense vector embeddings.

        Args:
            documents (List[Document]): A list of langchain Document instances to embed.
            model_name (Optional[str]): Name or path of the pretrained transformer model
                to use. Defaults to `SimpleHFEmbedder._DEFAULT_MODEL_NAME`.
            device (Optional[str]): Compute device to load the model on (e.g., 'cpu', 'cuda').
                Defaults to 'cuda' if available, else 'cpu'.

        Returns:
            np.ndarray: A 2D numpy array where each row is the embedding vector of a document.

        Example:
            >>> from langchain_core.documents import Document
            >>> docs = [Document(page_content="Hello world"), Document(page_content="Goodbye world")]
            >>> embeddings = SimpleHFEmbedder.embed_documents(docs)
            >>> embeddings.shape
            (2, 1024)  # assuming the model outputs 1024-dim embeddings
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
        device: Optional[str] = None
    ) -> np.ndarray:
        """
        Embed a single query string into a dense vector embedding.

        Args:
            query (str): The input query string to embed.
            model_name (Optional[str]): Name or path of the pretrained transformer model
                to use. Defaults to `SimpleHFEmbedder._DEFAULT_MODEL_NAME`.
            device (Optional[str]): Compute device to load the model on (e.g., 'cpu', 'cuda').
                Defaults to 'cuda' if available, else 'cpu'.

        Returns:
            np.ndarray: A 1D numpy array representing the embedding vector of the query.

        Example:
            >>> query = "What is the capital of France?"
            >>> embedding = SimpleHFEmbedder.embed_query(query)
            >>> embedding.shape
            (1024,)  # assuming the model outputs 1024-dim embeddings
        """
        cls._logger.debug(f"Embedding query: '{query[:50]}...'")
        doc = Document(page_content=query, metadata={})
        cls._logger.debug("Query embedding computed")
        return SimpleHFEmbedder.embed_documents([doc], model_name)[0]

    @classmethod
    def _get_tokenizer(cls, model_name: str) -> PreTrainedTokenizer:
        """
        Load the tokenizer for a given model name.

        Args:
            model_name (str): The pretrained model identifier.

        Returns:
            PreTrainedTokenizer: The tokenizer instance corresponding to the model.
        """
        cls._logger.debug(f"Loading tokenizer for model '{model_name}'")
        return Suphalaks.get_tokenizer(model_name)

    @classmethod
    def _get_model(
        cls,
        model_name: str, 
    ) -> PreTrainedModel:
        """
        Load the pretrained model on the specified device.

        Args:
            model_name (str): The pretrained model identifier.

        Returns:
            PreTrainedModel: The loaded model.
        """
        # device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        cls._logger.debug(f"Loading model '{model_name}'")
        model = Suphalaks.get_model(model_name)
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

        This averages token embeddings, ignoring padded tokens based on the attention mask.

        Args:
            model_output (Tuple[torch.Tensor]): Output tuple from the transformer model forward pass,
                where the first element contains token embeddings.
            attention_mask (torch.Tensor): Attention mask indicating valid tokens (1) vs padding (0).

        Returns:
            torch.Tensor: The mean pooled embedding tensor.
        """
        cls._logger.debug("Performing mean pooling on model outputs")
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        pooled = torch.sum(token_embeddings * input_mask_expanded, 1) / input_mask_expanded.sum(1)
        cls._logger.debug(f"Pooled embeddings shape: {pooled.shape}")
        return pooled