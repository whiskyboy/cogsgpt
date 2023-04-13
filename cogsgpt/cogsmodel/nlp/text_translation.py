import os
import uuid

import requests

from cogsgpt.utils import ArgsType, LanguageType
from cogsgpt.cogsmodel import BaseModel


COGS_KEY = os.environ['COGS_KEY']
COGS_ENDPOINT = os.environ['COGS_ENDPOINT']
COGS_REGION = os.environ['COGS_REGION']


class TextTranslationModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.translate_endpoint = "https://api.cognitive.microsofttranslator.com/translate"
        self.headers = {
            'Ocp-Apim-Subscription-Key': COGS_KEY,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': COGS_REGION,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        self.supported_language = {
            LanguageType.English.value: "en",
            LanguageType.Chinese.value: "zh-Hans",
        }

    def _translate(self, text: str, from_language: str, to_language: str) -> str:
        body = [{
            'text': text
        }]
        params = {
            'api-version': '3.0',
            'from': from_language,
            'to': to_language
        }

        request = requests.post(self.translate_endpoint, headers=self.headers, params=params, json=body)
        response = request.json()
        return response[0]['translations'][0]['text']

    def run(self, *args, **kwargs) -> str:
        text = kwargs[ArgsType.TEXT.value]
        from_language = self.supported_language[kwargs["from_language"]]
        to_language = self.supported_language[kwargs["to_language"]]
        return self._translate(text, from_language, to_language)