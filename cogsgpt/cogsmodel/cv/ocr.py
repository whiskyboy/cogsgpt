from enum import Enum
import os
from typing import Dict, List, Type

import azure.ai.vision as sdk
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.utils import FileSource, detect_file_source
from cogsgpt.args import ArgsType

COGS_KEY = os.environ['COGS_KEY']
COGS_ENDPOINT = os.environ['COGS_ENDPOINT']


class OCRModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.service_options = sdk.VisionServiceOptions(COGS_ENDPOINT, COGS_KEY)
        self.analysis_options = sdk.ImageAnalysisOptions()
        self.analysis_options.features = sdk.ImageAnalysisFeature.TEXT

    def _recognize_text(self, image_file: str, language: str = "en") -> List:
        image_src = detect_file_source(image_file)
        if image_src == FileSource.LOCAL:
            vision_source = sdk.VisionSource(filename=image_file)
        elif image_src == FileSource.REMOTE:
            vision_source = sdk.VisionSource(url=image_file)
        else:
            raise ValueError(f"Invalid image source: {image_file}")

        self.analysis_options.language = language

        image_analyzer = sdk.ImageAnalyzer(self.service_options, vision_source, self.analysis_options)
        result = image_analyzer.analyze()

        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.text is not None:
            return [line.content for line in result.text.lines]
        else:
            return []

    def run(self, *args, **kwargs) -> str:
        image_file = kwargs[ArgsType.IMAGE.value]
        language = kwargs.get("language", "en")
        return str(self._recognize_text(image_file, language))


# TODO: add more model ids for form recognizer
class FormRecognizerModelId(Enum):
    PREBUILT_READ = "prebuilt-read"


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
