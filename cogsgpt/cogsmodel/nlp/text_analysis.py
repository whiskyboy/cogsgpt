import abc
import os
from typing import List

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from cogsgpt.args import ArgsType
from cogsgpt.cogsmodel import BaseModel


COGS_KEY = os.environ['COGS_KEY']
COGS_ENDPOINT = os.environ['COGS_ENDPOINT']


class BaseAnalysisModel(BaseModel, abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        ta_credential = AzureKeyCredential(COGS_KEY)
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=COGS_ENDPOINT,
            credential=ta_credential
        )
    
    @abc.abstractmethod
    def _analyze(self, text: str, language: str = "en") -> List:
        pass

    def run(self, *args, **kwargs) -> str:
        text = kwargs[ArgsType.TEXT.value]
        language = kwargs.get("language", "en")
        return str(self._analyze(text, language))


class KeyPhraseModel(BaseAnalysisModel):
    def _analyze(self, text: str, language: str = "en") -> List:
        response = self.text_analytics_client.extract_key_phrases(documents=[text], language=language)
        return response[0].key_phrases


class EntityLinkingModel(BaseAnalysisModel):
    def _analyze(self, text: str, language: str = "en") -> List:
        response = self.text_analytics_client.recognize_linked_entities(documents=[text], language=language)
        return [{
            "entity": entity.name,
            "url": entity.url,
            "data_source": entity.data_source,
            "matches": [{
                "text": match.text,
                "confidence_score": match.confidence_score
            } for match in entity.matches]
        } for entity in response[0].entities]


class EntityRecognitionModel(BaseAnalysisModel):
    def _analyze(self, text: str, language: str = "en") -> List:
        response = self.text_analytics_client.recognize_entities(documents=[text], language=language)
        return [{
            "entity": entity.text,
            "category": entity.category,
            "subcategory": entity.subcategory,
            "confidence_score": entity.confidence_score
        } for entity in response[0].entities]


class PIIModel(BaseAnalysisModel):
    def _analyze(self, text: str, language: str = "en") -> List:
        response = self.text_analytics_client.recognize_pii_entities(documents=[text], language=language)
        return [{
            "entity": entity.text,
            "category": entity.category,
            "confidence_score": entity.confidence_score
        } for entity in response[0].entities]


class SentimentClassiferModel(BaseAnalysisModel):
    def _analyze(self, text: str, language: str = "en") -> List:
        response = self.text_analytics_client.analyze_sentiment(documents=[text], language=language)
        return [{
            "sentence": sentence.text,
            "sentiment": sentence.sentiment,
        } for sentence in response[0].sentences]