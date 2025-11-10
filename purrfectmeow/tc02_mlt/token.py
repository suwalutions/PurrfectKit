import time

from langchain_text_splitters import TokenTextSplitter

from purrfectmeow.meow.kitty import kitty_logger


class TokenSplit:
    _logger = kitty_logger(__name__)

    _OPENAI_EMBED_MODEL = {"text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"}
    _OPENAI_HF_MODEL = {"Xenova/text-embedding-ada-002"}
    _HF_MODEL_DIR = ".cache/huggingface/hub/"

    @classmethod
    def splitter(cls, model_name: str, chunk_size: int, chunk_overlap: int) -> TokenTextSplitter:
        cls._logger.debug("Initializing token splitter")
        start = time.time()

        try:
            cls._logger.debug(f"Using OpenAI model tokenizer: {model_name}")
            if model_name in cls._OPENAI_EMBED_MODEL:
                splitter = TokenTextSplitter.from_tiktoken_encoder(
                    model_name=model_name, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
            else:
                cls._logger.debug(f"Using HuggingFace tokenizer: {model_name}")
                from transformers import AutoTokenizer, GPT2TokenizerFast

                if model_name in cls._OPENAI_HF_MODEL:
                    tokenizer = GPT2TokenizerFast.from_pretrained(model_name, cache_dir=cls._HF_MODEL_DIR)
                else:
                    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cls._HF_MODEL_DIR)
                splitter = TokenTextSplitter.from_huggingface_tokenizer(
                    tokenizer=tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )

            cls._logger.debug("Token splitter successfully initialized.")
            return splitter

        except Exception as e:
            cls._logger.exception(f"Failed to initialize token splitter: {e}")
            raise

        finally:
            elapsed = time.time() - start
            cls._logger.debug(f"Token splitting completed in {elapsed:.2f} seconds.")
