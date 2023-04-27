from __future__ import annotations

import os
import uuid

import requests

from cogsgpt.schema import ArgsType, LanguageType
from cogsgpt.cogsmodel import BaseModel


class TextTranslationModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()

        COGS_KEY = os.environ['COGS_KEY']
        COGS_REGION = os.environ['COGS_REGION']
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

    def _translate(self, text: str, src_language: str, tgt_language: str) -> str:
        body = [{
            'text': text
        }]
        params = {
            'api-version': '3.0',
            'from': src_language,
            'to': tgt_language
        }

        request = requests.post(self.translate_endpoint, headers=self.headers, params=params, json=body)
        response = request.json()
        return response[0]['translations'][0]['text']

    def run(self, *args, **kwargs) -> str:
        text = kwargs[ArgsType.TEXT.value]
        src_language = self.supported_language[kwargs[ArgsType.SRC_LANGUAGE.value]]
        tgt_language = self.supported_language[kwargs[ArgsType.TGT_LANGUAGE.value]]
        return self._translate(text, src_language, tgt_language)