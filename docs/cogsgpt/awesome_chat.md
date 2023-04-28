Module cogsgpt.awesome_chat
===========================

Classes
-------

`CogsGPT(model_name: str = '', deployment_name: str = '', deployment_version: str = '', temperature: float = 0.7, request_timeout: int = 60, max_retries: int = 6, max_tokens: int | None = None, verbose: bool = False)`
:   The CogsGPT class is the main class for the CogsGPT library. It provides a simple interface to chat with Azure Cognitive Services.
    
    Args:
        model_name (str, optional): The name of the OpenAI model. Defaults to "". If not specified, it will be read from the environment variable OPENAI_MODEL_NAME.
        deployment_name (str, optional): The name of the Azure deployment. Defaults to "". If not specified, it will be read from the environment variable OPENAI_DEPLOYMENT_NAME.
        deployment_version (str, optional): The version of the Azure deployment. Defaults to "". If not specified, it will be read from the environment variable OPENAI_DEPLOYMENT_VERSION.
        temperature (float, optional): The temperature of the OpenAI model. Defaults to 0.7.
        request_timeout (int, optional): The timeout of the OpenAI model. Defaults to 60.
        max_retries (int, optional): The maximum number of retries of the OpenAI model. Defaults to 6.
        max_tokens (int | None, optional): The maximum number of tokens of the OpenAI model. Defaults to None.
        verbose (bool, optional): Whether to print verbose logs. Defaults to False.
    
    Examples:
        >>> from cogsgpt import CogsGPT
        >>> chatbot = CogsGPT()
        >>> chatbot.chat("What's the content of this image?")

    ### Methods

    `chat(self, human_input: str) ‑> str`
    :   This is the main method of CogsGPT class. It calls the following methods in order to generate a final response:
        1. parse_tasks: parse user input into a series of Azure Cognitive Service tasks
        2. execute_tasks: execute these Azure Cognitive Service tasks
        3. generate_response: generate final response from the results of Azure Cognitive Service tasks
        4. save_context: save user input and AI response to memory
        
        Args:
            human_input (str): User input.
        
        Returns:
            str: Final response.

    `execute_tasks(self, task_list: List[Dict]) ‑> List[Dict]`
    :   Execute a series of Azure Cognitive Service tasks.
        
        Args:
            task_list (List[Dict]): A list of Azure Cognitive Service tasks.
        
        Returns:
            List[Dict]: A list of Azure Cognitive Service tasks with results.

    `generate_response(self, human_input: str, task_result_list: List[Dict]) ‑> str`
    :   Generate final response from a series of Azure Cognitive Service results.
        
        Args:
            human_input (str): User input.
            task_result_list (List[Dict]): A list of Azure Cognitive Service tasks with results.
        
        Returns:
            str: Final response.

    `load_context(self) ‑> str`
    :   Load the conversation history from memory.
        
        Returns:
            str: The conversation history.

    `parse_tasks(self, human_input: str) ‑> List[Dict]`
    :   Parse user input into a series of Azure Cognitive Service tasks.
        
        Args:
            human_input (str): User input.
        
        Returns:
            List[Dict]: A list of Azure Cognitive Service tasks.

    `save_context(self, human_input: str, ai_response: str) ‑> None`
    :   Save user input and AI response to memory.
        
        Args:
            human_input (str): The user input.
            ai_response (str): The AI response.