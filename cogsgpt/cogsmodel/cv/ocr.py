from enum import Enum
import os
from typing import Dict, List, Type

import azure.ai.vision as sdk
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from cogsgpt.args import ArgsType
from cogsgpt.cogsmodel import BaseModel
from cogsgpt.utils import FileSource, detect_file_source


COGS_KEY = os.environ['COGS_KEY']
COGS_ENDPOINT = os.environ['COGS_ENDPOINT']


# TODO: add more model ids for form recognizer
class FormRecognizerModelId(Enum):
    PREBUILT_READ = "prebuilt-read"
    PREBUILT_LAYOUT = "prebuilt-layout"


class FormRecognizerModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=COGS_ENDPOINT,
            credential=AzureKeyCredential(COGS_KEY)
        )
        self.result_parser = {
            FormRecognizerModelId.PREBUILT_READ.value: self._parse_prebuilt_read_result
        }

    def _parse_prebuilt_read_result(self, analyze_result: Type) -> Dict:
        return {
            "content": analyze_result.content
        }

    def _parse_prebuilt_layout_result(self, analyze_result: Type) -> Dict:
        return {
            "content": analyze_result.content
        }

    def _analyze_document(self, document_file: str, model_id: str = FormRecognizerModelId.PREBUILT_READ.value) -> Dict:
        document_src = detect_file_source(document_file)
        if document_src == FileSource.LOCAL:
            with open(document_file, "rb") as f:
                poller = self.document_analysis_client.begin_analyze_document(
                    model_id, document=f
                )
        elif document_src == FileSource.REMOTE:
            poller = self.document_analysis_client.begin_analyze_document_from_url(
                model_id, document_url=document_file
            )
        else:
            raise ValueError(f"Invalid document source: {document_file}")

        result = poller.result()
        return self.result_parser[model_id](result)

    def run(self, *args, **kwargs) -> str:
        document_file = kwargs[ArgsType.IMAGE.value]
        model_id = kwargs.get("model_id", FormRecognizerModelId.PREBUILT_READ.value)
        return str(self._analyze_document(document_file, model_id))
