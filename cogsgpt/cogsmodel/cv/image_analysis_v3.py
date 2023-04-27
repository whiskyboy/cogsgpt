from __future__ import annotations

from abc import ABC, abstractmethod
import os
from typing import Dict

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes, Details, ImageAnalysis
from msrest.authentication import CognitiveServicesCredentials

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.schema import ArgsType, FileSource
from cogsgpt.utils import detect_file_source
from cogsgpt.cogsmodel.cv.utils import draw_rectangles


class ImageAnalysisV3Model(BaseModel, ABC):
    def __init__(self) -> None:
        super().__init__()
        
        COGS_KEY = os.environ['COGS_KEY']
        COGS_ENDPOINT = os.environ['COGS_ENDPOINT']
        self.client = ComputerVisionClient(COGS_ENDPOINT, CognitiveServicesCredentials(COGS_KEY))
        self.image_features = []
        self.image_details = []

    @abstractmethod
    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        pass

    def _analyze_image(self, image_file: str) -> Dict:
        image_src = detect_file_source(image_file)
        if image_src == FileSource.LOCAL:
            result = self.client.analyze_image_in_stream(open(image_file, "rb"),
                                                         visual_features=self.image_features,
                                                         details=self.image_details)
        elif image_src == FileSource.REMOTE:
            result = self.client.analyze_image(image_file,
                                               visual_features=self.image_features,
                                               details=self.image_details)
        else:
            raise ValueError(f"Invalid image source: {image_file}")
        
        return self._parse_result(image_file, result)

    def run(self, *args, **kwargs) -> str:
        image_file = kwargs[ArgsType.IMAGE.value]
        return str(self._analyze_image(image_file))


class ImageCategorizeModel(ImageAnalysisV3Model):
    def __init__(self) -> None:
        super().__init__()
        self.image_features = [VisualFeatureTypes.categories]
        # self.image_details = [Details.celebrities, Details.landmarks]
        self.image_details = [Details.landmarks]

    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        if len(result.categories) > 0:
            categories = []
            for category in result.categories:
                res = {
                    "name": category.name,
                    "confidence": f"{category.score * 100:.2f}%",
                }
                if category.detail is not None:
                    if category.detail.celebrities is not None:
                        res["celebrities"] = [f"{celebrity.name}" for celebrity in category.detail.celebrities]
                    if category.detail.landmarks is not None:
                        res["landmarks"] = [f"{landmark.name}" for landmark in category.detail.landmarks]
                categories.append(res)
            return {
                "categories": categories,
            }
        else:
            return {}


class BrandDetectionModel(ImageAnalysisV3Model):
    def __init__(self) -> None:
        super().__init__()
        self.image_features = [VisualFeatureTypes.brands]

    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        if len(result.brands) > 0:
            return {
                "brands": [
                    {
                        "name": brand.name,
                        "confidence": f"{brand.confidence * 100:.2f}%",
                    } for brand in result.brands],
                "image": draw_rectangles(image_file,
                                         rectangles=[(
                                            brand.rectangle.x,
                                            brand.rectangle.y,
                                            brand.rectangle.x + brand.rectangle.w,
                                            brand.rectangle.y + brand.rectangle.h) for brand in result.brands],
                                         texts=[f"{brand.name} ({brand.confidence * 100:.2f}%)" for brand in result.brands]),
            }
        else:
            return {}


class FaceDetectionModel(ImageAnalysisV3Model):
    def __init__(self) -> None:
        super().__init__()
        self.image_features = [VisualFeatureTypes.faces]

    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        if len(result.faces) > 0:
            return {
                "count": len(result.faces),
                "image": draw_rectangles(image_file,
                                         rectangles=[(
                                            face.face_rectangle.left,
                                            face.face_rectangle.top,
                                            face.face_rectangle.left + face.face_rectangle.width,
                                            face.face_rectangle.top + face.face_rectangle.height) for face in result.faces]),
            }
        else:
            return {}


class AdultContentDetectionModel(ImageAnalysisV3Model):
    def __init__(self) -> None:
        super().__init__()
        self.image_features = [VisualFeatureTypes.adult]

    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        return {
            "adult": {
                "is_adult_content": result.adult.is_adult_content,
                "is_racy_content": result.adult.is_racy_content,
                "is_gory_content": result.adult.is_gory_content,
                "adult_score": f"{result.adult.adult_score * 100:.2f}%",
                "racy_score": f"{result.adult.racy_score * 100:.2f}%",
                "gory_score": f"{result.adult.gore_score * 100:.2f}%",
            },
        }


class ColorSchemeDetectionModel(ImageAnalysisV3Model):
    def __init__(self) -> None:
        super().__init__()
        self.image_features = [VisualFeatureTypes.color]

    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        return {
            "color": {
                "dominant_colors": result.color.dominant_colors,
                "dominant_foreground_color": result.color.dominant_color_foreground,
                "dominant_background_color": result.color.dominant_color_background,
                "accent_color": result.color.accent_color,
                "is_bw_img": result.color.is_bw_img,
            },
        }


class ImageTypeDetectionModel(ImageAnalysisV3Model):
    def __init__(self) -> None:
        super().__init__()
        self.image_features = [VisualFeatureTypes.image_type]

    def _parse_result(self, image_file: str, result: ImageAnalysis) -> Dict:
        return {
            "image_type": {
                "is_clip_art": result.image_type.clip_art_type > 1,
                "is_line_drawing": result.image_type.line_drawing_type == 1,
            },
        }