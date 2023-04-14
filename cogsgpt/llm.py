import os

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI


OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "")
OPENAI_MODEL_VERSION = os.environ.get("OPENAI_MODEL_VERSION", "")


class LLMManager():
    def __init__(self) -> None:
        if OPENAI_API_TYPE == "azure":
            self._LLM = AzureChatOpenAI(
                deployment_name=OPENAI_MODEL_NAME,
                openai_api_type=OPENAI_API_TYPE,
                openai_api_base=OPENAI_API_BASE,
                openai_api_version=OPENAI_MODEL_VERSION,
                openai_api_key=OPENAI_API_KEY,
            )
        elif OPENAI_API_TYPE == "openai":
            self._LLM = ChatOpenAI(
                model_name=OPENAI_MODEL_NAME,
                openai_api_key=OPENAI_API_KEY,
            )
        else:
            raise ValueError(f"OPENAI_API_TYPE must be either 'azure' or 'openai', but got {OPENAI_API_TYPE}")

    @property
    def LLM(self) -> ChatOpenAI:
        return self._LLM

llm_manager = LLMManager()