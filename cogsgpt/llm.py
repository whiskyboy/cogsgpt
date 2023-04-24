from __future__ import annotations

import os

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI

from cogsgpt.logger import logger


class LLMManager():
    def __init__(self,
                 model_name: str = "",
                 deployment_name: str = "",
                 deployment_version: str = "",
                 **kwargs
                 ) -> None:
        """
        LLMManager is a wrapper class for the OpenAI API. It allows you to easily switch between OpenAI and Azure OpenAI Service.

        Args:
            model_name (str, optional): The name of the OpenAI model. Defaults to "". If not specified, it will be read from the environment variable OPENAI_MODEL_NAME.
            deployment_name (str, optional): The name of the Azure deployment. Defaults to "". If not specified, it will be read from the environment variable OPENAI_DEPLOYMENT_NAME.
            deployment_version (str, optional): The version of the Azure deployment. Defaults to "". If not specified, it will be read from the environment variable OPENAI_DEPLOYMENT_VERSION.
            **kwargs: Additional keyword arguments to be passed to the OpenAI API.
        
        Raises:
            ValueError: If OPENAI_API_TYPE is not set to either "openai" or "azure".
        """
        # Required Env Vars
        OPENAI_API_TYPE = os.environ["OPENAI_API_TYPE"]
        OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

        # Required for Azure
        if OPENAI_API_TYPE == "azure":
            OPENAI_API_BASE = os.environ["OPENAI_API_BASE"]

        # Optional Env Vars
        if model_name == "":
            model_name = os.environ.get("OPENAI_MODEL_NAME", "")
        
        if deployment_name == "":
            deployment_name = os.environ.get("OPENAI_DEPLOYMENT_NAME", "")

        if deployment_version == "":
            deployment_version = os.environ.get("OPENAI_DEPLOYMENT_VERSION", "")

        if OPENAI_API_TYPE == "azure":
            logger.info(f"Using Azure deployment {deployment_name} (version {deployment_version})")
            self._LLM = AzureChatOpenAI(
                openai_api_type=OPENAI_API_TYPE,
                openai_api_base=OPENAI_API_BASE,
                openai_api_key=OPENAI_API_KEY,
                deployment_name=deployment_name,
                openai_api_version=deployment_version,
                **kwargs
            )
        elif OPENAI_API_TYPE == "openai":
            logger.info(f"Using OpenAI model {model_name}")
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