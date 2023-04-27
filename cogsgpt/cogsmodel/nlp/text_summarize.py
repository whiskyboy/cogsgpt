from __future__ import annotations

import abc
import os

from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction, AbstractSummaryAction
from azure.core.credentials import AzureKeyCredential

from cogsgpt.schema import ArgsType, LanguageType
from cogsgpt.cogsmodel import BaseModel


class BaseSummarizeModel(BaseModel, abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        
        COGS_KEY = os.environ['COGS_KEY']
        COGS_ENDPOINT = os.environ['COGS_ENDPOINT']
        ta_credential = AzureKeyCredential(COGS_KEY)
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=COGS_ENDPOINT,
            credential=ta_credential
        )

        self.supported_language = {
            LanguageType.English.value: "en",
            LanguageType.Chinese.value: "zh-hans",
        }

    @abc.abstractmethod
    def _summarize(self, text: str, language: str = "en") -> str:
        pass

    def run(self, *args, **kwargs) -> str:
        text = kwargs[ArgsType.TEXT.value]
        language = kwargs.get(ArgsType.SRC_LANGUAGE.value, LanguageType.English.value)
        language = self.supported_language[language]
        return self._summarize(text, language)


class ExtractSummarizeModel(BaseSummarizeModel):
    def _summarize(self, text: str, language: str = "en") -> str:
        poller = self.text_analytics_client.begin_analyze_actions(
            documents=[text],
            actions=[ExtractSummaryAction()],
            language=language
        )
        document_result = list(poller.result())[0]
        extract_summary_result = document_result[0]

        return " ".join([sentence.text for sentence in extract_summary_result.sentences])


class AbstractSummarizeModel(BaseSummarizeModel):
    def _summarize(self, text: str, language: str = "en") -> str:
        poller = self.text_analytics_client.begin_analyze_actions(
            documents=[text],
            actions=[AbstractSummaryAction()],
            language=language
        )
        document_result = list(poller.result())[0]
        abstract_summary_result = document_result[0]

        return " ".join([summary.text for summary in abstract_summary_result.summaries])
