import os

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI

from cogsgpt.utils import singleton


# Required Env Vars
OPENAI_API_TYPE = os.environ["OPENAI_API_TYPE"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Required for Azure
if OPENAI_API_TYPE == "azure":
    OPENAI_API_BASE = os.environ["OPENAI_API_BASE"]


@singleton
class LLMManager():
    def __init__(self,
                 model_name: str = "",
                 deployment_name: str = "",
                 deployment_version: str = "",
                 **kwargs
                 ) -> None:
        if OPENAI_API_TYPE == "azure":
            self._LLM = AzureChatOpenAI(
                openai_api_type=OPENAI_API_TYPE,
                openai_api_base=OPENAI_API_BASE,
                openai_api_key=OPENAI_API_KEY,
                deployment_name=deployment_name,
                openai_api_version=deployment_version,
                **kwargs
            )
        elif OPENAI_API_TYPE == "openai":
            self._LLM = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                model_name=model_name,
                **kwargs
            )
        else:
            raise ValueError(f"OPENAI_API_TYPE must be either 'azure' or 'openai', but got {OPENAI_API_TYPE}")

    @property
    def LLM(self) -> ChatOpenAI:
        return self._LLM