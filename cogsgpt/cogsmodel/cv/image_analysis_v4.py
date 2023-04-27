from __future__ import annotations

from abc import ABC, abstractmethod
import os
from typing import Dict

import azure.ai.vision as sdk

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.schema import ArgsType, FileSource
from cogsgpt.utils import detect_file_source
from cogsgpt.cogsmodel.cv.utils import draw_rectangles, crop_rectangle


class ImageAnalysisV4Model(BaseModel, ABC):
    def __init__(self) -> None:
        super().__init__()
        
        COGS_KEY = os.environ['COGS_KEY']
        COGS_ENDPOINT = os.environ['COGS_ENDPOINT']
        self.service_options = sdk.VisionServiceOptions(COGS_ENDPOINT, COGS_KEY)
        self.analysis_options = sdk.ImageAnalysisOptions()

    @abstractmethod
    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        pass

    def _analyze_image(self, image_file: str) -> Dict:
        image_src = detect_file_source(image_file)
        if image_src == FileSource.LOCAL:
            vision_source = sdk.VisionSource(filename=image_file)
        elif image_src == FileSource.REMOTE:
            vision_source = sdk.VisionSource(url=image_file)
        else:
            raise ValueError(f"Invalid image source: {image_file}")
        
        image_analyzer = sdk.ImageAnalyzer(self.service_options, vision_source, self.analysis_options)
        result = image_analyzer.analyze()

        return self._parse_result(image_file, result)

    def run(self, *args, **kwargs) -> str:
        image_file = kwargs[ArgsType.IMAGE.value]
        return str(self._analyze_image(image_file))


class ImageCaptionModel(ImageAnalysisV4Model):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.DENSE_CAPTIONS

    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.dense_captions is not None:
            return {
                "captions": [
                    {
                        "text": caption.content,
                        "confidence": f"{caption.confidence * 100:.2f}%",
                    } for caption in result.dense_captions]
            }
        else:
            return {}


class ObjectDetectionModel(ImageAnalysisV4Model):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.OBJECTS

    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.objects is not None:
            return {
                "objects": [
                    {
                        "object": obj.name,
                        "confidence": f"{obj.confidence * 100:.2f}%",
                    } for obj in result.objects],
                "image": draw_rectangles(image_file,
                                         rectangles=[(
                                            obj.bounding_box.x,
                                            obj.bounding_box.y,
                                            obj.bounding_box.x + obj.bounding_box.w,
                                            obj.bounding_box.y + obj.bounding_box.h) for obj in result.objects],
                                         texts=[f"{obj.name} ({obj.confidence * 100:.2f}%)" for obj in result.objects]),
            }
        else:
            return {}


class ImageTaggingModel(ImageAnalysisV4Model):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.TAGS

    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.tags is not None:
            return {
                "tags": [
                    {
                        "tag": tag.name,
                        "confidence": f"{tag.confidence * 100:.2f}%",
                    } for tag in result.tags],
            }
        else:
            return {}


class PeopleDetectionModel(ImageAnalysisV4Model):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.PEOPLE

    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.people is not None:
            return {
                "count": len(result.people),
                "image": draw_rectangles(image_file,
                                         rectangles=[(
                                            person.bounding_box.x,
                                            person.bounding_box.y,
                                            person.bounding_box.x + person.bounding_box.w,
                                            person.bounding_box.y + person.bounding_box.h) for person in result.people],
                                         texts=[f"{person.confidence * 100:.2f}%" for person in result.people]),
            }
        else:
            return {}


class SmartCropModel(ImageAnalysisV4Model):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.CROP_SUGGESTIONS

    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.crop_suggestions is not None:
            crop_result = result.crop_suggestions[0]
            return {
                "crop_ratio": crop_result.aspect_ratio,
                "image": crop_rectangle(image_file, rectangle=(
                    crop_result.bounding_box.x,
                    crop_result.bounding_box.y,
                    crop_result.bounding_box.x + crop_result.bounding_box.w,
                    crop_result.bounding_box.y + crop_result.bounding_box.h)),
            }
        else:
            return {}


class ImageTextModel(ImageAnalysisV4Model):
    def __init__(self) -> None:
        super().__init__()
        self.analysis_options.features = sdk.ImageAnalysisFeature.TEXT

    def _parse_result(self, image_file: str, result: sdk.ImageAnalysisResult) -> Dict:
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED and result.text is not None:
            return {
                "text": [line.content for line in result.text.lines],
            }
        else:
            return {}