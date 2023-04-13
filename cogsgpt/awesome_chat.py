import json
import logging
import os
from typing import Dict, List

from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseMessage
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI

from cogsgpt import awesome_prompts, ArgsType
from cogsgpt.cogsmodel import *

OPENAI_MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]
OPENAI_MODEL_VERSION = os.environ["OPENAI_MODEL_VERSION"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


TaskMap = {
    "image-caption": ImageCaptionModel,
    "object-detection": ObjectDetectionModel,
    "image-tagging": ImageTaggingModel,
    "OCR": ImageTextModel,
    "form-recognizer": FormRecognizerModel,
    "text2speech": Text2SpeechModel,
    "speech2text": Speech2TextModel,
    "key-phrase": KeyPhraseModel,
    "entity-linking": EntityLinkingModel,
    "entity-recognition": EntityRecognitionModel,
    "sentiment-analysis": SentimentAnalysisModel,
    "extract-summarize": ExtractSummarizeModel,
    "abstract-summarize": AbstractSummarizeModel,
    "personally-identifiable-information": PIIModel,
    "text-translation": TextTranslationModel,
}


class CogsGPT():
    def __init__(self) -> None:
        self.task_metas = json.load(open("./cogsgpt/task_metas.json", "r"))
        self.parse_task_examples = json.load(open("./cogsgpt/parse_task_examples.json", 'r'))
        self.generate_response_presteps = json.load(open("./cogsgpt/generate_response_presteps.json", 'r'))

        self.parse_task_prompt = self._create_parse_task_prompt()
        self.generate_response_prompt = self._create_generate_response_prompt()

        self.memory = ConversationBufferMemory(memory_key='history')

        self.chat_model = AzureChatOpenAI(
            deployment_name=OPENAI_MODEL_NAME,
            openai_api_version=OPENAI_MODEL_VERSION,
        )

    def _save_context(self, human_input: str, ai_response: str) -> None:
        self.memory.chat_memory.add_user_message(human_input)
        self.memory.chat_memory.add_ai_message(ai_response)

    def _load_context(self) -> str:
        return self.memory.load_memory_variables({})['history']

    def _create_parse_task_prompt(self) -> ChatPromptTemplate:
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=awesome_prompts.ParseTaskPrompts.SYSTEM_PROMPT,
                input_variables=awesome_prompts.ParseTaskPrompts.SYSTEM_PROMPT_VAR_LIST,
                template_format="jinja2"
            )
        )

        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=awesome_prompts.ParseTaskPrompts.USER_PROMPT,
                input_variables=awesome_prompts.ParseTaskPrompts.USER_PROMPT_VAR_LIST,
                template_format="jinja2"
            )
        )

        examples_message_prompts = []
        for example in self.parse_task_examples:
            role_message_prompt_template = AIMessagePromptTemplate if example["role"] == "assistant" else HumanMessagePromptTemplate
            examples_message_prompts.append(
                role_message_prompt_template(
                    prompt=PromptTemplate(
                        template=example["content"],
                        input_variables=[],
                        template_format="jinja2"
                    )
                )
            )

        return ChatPromptTemplate.from_messages([system_message_prompt, *examples_message_prompts, human_message_prompt])
    
    def _create_generate_response_prompt(self) -> ChatPromptTemplate:
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=awesome_prompts.GenerateResponsePrompts.SYSTEM_PROMPT,
                input_variables=awesome_prompts.GenerateResponsePrompts.SYSTEM_PROMPT_VAR_LIST,
                template_format="jinja2"
            )
        )
        
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=awesome_prompts.GenerateResponsePrompts.USER_PROMPT,
                input_variables=awesome_prompts.GenerateResponsePrompts.USER_PROMPT_VAR_LIST,
                template_format="jinja2"
            )
        )

        presteps_message_prompts = []
        for prestep in self.generate_response_presteps:
            role_message_prompt_template = AIMessagePromptTemplate if prestep["role"] == "assistant" else HumanMessagePromptTemplate
            presteps_message_prompts.append(
                role_message_prompt_template(
                    prompt=PromptTemplate(
                        template=prestep["content"],
                        input_variables=["input", "processes"],
                        template_format="jinja2"
                    )
                )
            )

        return ChatPromptTemplate.from_messages([system_message_prompt, *presteps_message_prompts, human_message_prompt])

    def _format_parse_task_prompt(self, human_input: str) -> List[BaseMessage]:
        history = self._load_context()
        return self.parse_task_prompt.format_prompt(
            history=history,
            input=human_input,
            args_type_list=[t.value for t in ArgsType],
            task_list=[t['task'] for t in self.task_metas],
            task_metas=self.task_metas
        ).to_messages()

    def _format_generate_response_prompt(self, human_input: str, task_list: List[Dict]) -> List[BaseMessage]:
        return self.generate_response_prompt.format_prompt(
            input=human_input,
            processes=task_list
        ).to_messages()

    def _parse_tasks(self, human_input: str) -> List[Dict]:
        messages = self._format_parse_task_prompt(human_input)
        logger.info(f"Parse task prompt: {messages}")
        response = self.chat_model(messages).content
        logger.info(f"Parse task response: {response}")
        return json.loads(response)

    def _collect_deps_results(self, task_args: Dict, task_list: List[Dict]) -> Dict:
        for arg_name, arg_value in task_args.items():
            if "<GENERATED>-" in arg_value:
                dep_id = int(arg_value.split("-")[1])
                task_args[arg_name] = task_list[dep_id].get("result", "")
        return task_args

    def _execute_tasks(self, task_list: List[Dict]) -> List[Dict]:
        for task in task_list:
            try:
                task_name = task["task"]
                if task_name not in TaskMap:
                    logger.warning(f"Task {task_name} not supported")
                else:
                    task_model = TaskMap[task_name]()
                    task["args"] = self._collect_deps_results(task["args"], task_list)
                    logger.info(f"Task {task_name} args: {task['args']}")
                    task["result"] = task_model.run(**task["args"])
                    logger.info(f"Task {task_name} result: {task['result']}")
            except Exception as e:
                logger.error(f"Task {task_name} execute failed: {e}")
        return task_list

    def _generate_response(self, human_input: str, task_result_list: List[Dict]) -> str:
        messages = self._format_generate_response_prompt(human_input, task_result_list)
        logger.info(f"Generate response prompt: {messages}")
        response = self.chat_model(messages).content
        logger.info(f"Generate response response: {response}")
        return response

    def chat(self, human_input: str) -> str:
        # 1. parse tasks
        task_list = self._parse_tasks(human_input)

        # 2. execute tasks
        task_result_list = self._execute_tasks(task_list)

        # 3. generate response
        response = self._generate_response(human_input, task_result_list)

        # 4. save human_input/response into memory
        self._save_context(human_input, response)

        return response