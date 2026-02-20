from typing import Any

import yaml

from .huggingface import HuggingFace
from .ollama import Ollama
from .openai import OpenAI


class WichienMaat:
    @classmethod
    def embedding(cls, sentence: str | list[str], model_name: str | None = None, **kwargs: Any) -> dict[str, Any]:
        ollama_url = kwargs.get("ollama_url") or kwargs.get("ollama_server") or kwargs.get("ollama_host") or ""
        base_url = kwargs.get("openai_base_url") or kwargs.get("base_url") or ""
        api_key = kwargs.get("openai_api_key") or kwargs.get("api_key") or ""

        with open("purrfectmeow/meow/felidae/models.yaml") as f:
            _CFG = yaml.safe_load(f)

        hf_models = set(_CFG["huggingface"]["models"])
        hf_default = _CFG["huggingface"]["default"]

        ollama_models = set(_CFG["ollama"]["models"])
        ollama_default = _CFG["ollama"]["default"]

        openai_models = set(_CFG["openai"]["models"])
        openai_default = _CFG["openai"]["default"]

        match model_name:
            case _ if model_name is not None and model_name in hf_models:
                return HuggingFace.model_encode(sentence, model_name)

            case _ if model_name is not None and model_name in ollama_models:
                return Ollama.model_encode(sentence, model_name, ollama_url)

            case _ if model_name is not None and model_name in openai_models:
                if api_key:
                    return OpenAI.model_encode(sentence, model_name, base_url, api_key)
                elif ollama_url:
                    return Ollama.model_encode(sentence, model_name, ollama_url)
                else:
                    return HuggingFace.model_encode(sentence, model_name)

            case None:
                if api_key:
                    return OpenAI.model_encode(sentence, openai_default, base_url, api_key)

                elif ollama_url:
                    return Ollama.model_encode(sentence, ollama_default, ollama_url)

                return HuggingFace.model_encode(sentence, hf_default)

            case _:
                return HuggingFace.model_encode(sentence, model_name or hf_default)
