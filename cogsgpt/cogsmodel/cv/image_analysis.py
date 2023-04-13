import os
from typing import Dict, List

import azure.ai.vision as sdk

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.utils import ArgsType, FileSource, LanguageType, detect_file_source


COGS_KEY = os.environ['COGS_KEY']
COGS_ENDPOINT = os.environ['COGS_ENDPOINT']


class ImageAnalysisModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.service_options = sdk.VisionServiceOptions(COGS_ENDPOINT, COGS_KEY)
        self.analysis_options = sdk.ImageAnalysisOptions()
        self.analysis_options.features = (
            sdk.ImageAnalysisFeature.CAPTION |
            sdk.ImageAnalysisFeature.OBJECTS |
            sdk.ImageAnalysisFeature.TAGS |
            sdk.ImageAnalysisFeature.TEXT
        )
        self.supported_language = {
            LanguageType.English.value: "en",
            LanguageType.Chinese.value: "zh-Hans",
        }

    def _parse_result(self, result: sdk.ImageAnalysisResult) -> Dict:
        result_dict = {}
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
            if result.caption is not None:
                result_dict["caption"] = result.caption.content
            if result.objects is not None:
                result_dict["objects"] = [obj.name for obj in result.objects]
            if result.tags is not None:
                result_dict["tags"] = [tag.name for tag in result.tags]
            if result.text is not None:
                result_dict["text"] = [line.content for line in result.text.lines]
        return result_dict

    def _analyze_image(self, image_file: str, language: str = "en") -> Dict:
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

        return self._parse_result(result)

    def run(self, *args, **kwargs) -> str:
        image_file = kwargs[ArgsType.IMAGE.value]
        language = kwargs.get("from_language", LanguageType.English.value)
        language = self.supported_language[language]
        return str(self._analyze_image(image_file, language))


class ImageCaptionModel(ImageAnalysisModel):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.CAPTION

    def _analyze_image(self, image_file: str, language: str = "en") -> str:
        result = super()._analyze_image(image_file, language)
        return result.get("caption", "")


class ObjectDetectionModel(ImageAnalysisModel):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.OBJECTS

    def _analyze_image(self, image_file: str, language: str = "en") -> List:
        result = super()._analyze_image(image_file, language)
        return result.get("objects", [])


class ImageTaggingModel(ImageAnalysisModel):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.TAGS

    def _analyze_image(self, image_file: str, language: str = "en") -> List:
        result = super()._analyze_image(image_file, language)
        return result.get("tags", [])


class ImageTextModel(ImageAnalysisModel):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.TEXT

    def _analyze_image(self, image_file: str, language: str = "en") -> List:
        result = super()._analyze_image(image_file, language)
        return result.get("text", [])
