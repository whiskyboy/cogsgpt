Module cogsgpt.llm
==================

Classes
-------

`LLMManager(model_name: str = '', deployment_name: str = '', deployment_version: str = '', **kwargs)`
:   LLMManager is a wrapper class for the OpenAI API. It allows you to easily switch between OpenAI and Azure OpenAI Service.
    
    Args:
        model_name (str, optional): The name of the OpenAI model. Defaults to "". If not specified, it will be read from the environment variable OPENAI_MODEL_NAME.
        deployment_name (str, optional): The name of the Azure deployment. Defaults to "". If not specified, it will be read from the environment variable OPENAI_DEPLOYMENT_NAME.
        deployment_version (str, optional): The version of the Azure deployment. Defaults to "". If not specified, it will be read from the environment variable OPENAI_DEPLOYMENT_VERSION.
        **kwargs: Additional keyword arguments to be passed to the OpenAI API.
    
    Raises:
        ValueError: If OPENAI_API_TYPE is not set to either "openai" or "azure".

    ### Instance variables

    `LLM: langchain.chat_models.openai.ChatOpenAI`
    :