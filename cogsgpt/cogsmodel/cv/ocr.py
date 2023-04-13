import os
from typing import Dict, List, Type

import azure.ai.vision as sdk
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.utils import ArgsType, FileSource, LanguageType, detect_file_source


COGS_KEY = os.environ['COGS_KEY']
COGS_ENDPOINT = os.environ['COGS_ENDPOINT']


class FormRecognizerModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=COGS_ENDPOINT,
            credential=AzureKeyCredential(COGS_KEY)
        )
        self.model_id = "prebuilt-read"

        self.supported_language = {
            LanguageType.English.value: "en",
            LanguageType.Chinese.value: "zh-Hans",
        }

    def _parse_result(self, analyze_result: Type) -> Dict:
        return {
            "content": analyze_result.content
        }

    def _analyze_document(self, document_file: str, language: str = "en") -> Dict:
        document_src = detect_file_source(document_file)
        if document_src == FileSource.LOCAL:
            with open(document_file, "rb") as f:
                poller = self.document_analysis_client.begin_analyze_document(
                    model_id=self.model_id, document=f, locale=language
                )
        elif document_src == FileSource.REMOTE:
            poller = self.document_analysis_client.begin_analyze_document_from_url(
                model_id=self.model_id, document_url=document_file, locale=language
            )
        else:
            raise ValueError(f"Invalid document source: {document_file}")

        result = poller.result()
        return self._parse_result(result)

    def run(self, *args, **kwargs) -> str:
        document_file = kwargs[ArgsType.IMAGE.value]
        language = kwargs.get("from_language", LanguageType.English.value)
        language = self.supported_language[language]
        return str(self._analyze_document(document_file, language))
