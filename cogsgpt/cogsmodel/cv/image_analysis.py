import os
from typing import Dict, Optional

import azure.ai.vision as sdk
from cogsgpt.args import ArgsType

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.utils import FileSource, detect_file_source

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
            sdk.ImageAnalysisFeature.TEXT |
            sdk.ImageAnalysisFeature.TAGS
        )

    def analyze_image(self, image_file: str, language: str = "en") -> Optional[Dict]:
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

        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
            caption = ""
            if result.caption is not None:
                caption = result.caption.content

            tags = []
            if result.tags is not None:
                tags = [tag.name for tag in result.tags]

            objects = []
            if result.objects is not None:
                objects = [obj.name for obj in result.objects]

            text = []
            if result.text is not None:
                text = '\n'.join([line.content for line in result.text.lines])

            return {
                "caption": caption,
                "tags": tags,
                "objects": objects,
                "text": text
            }
        else:
            return {}

    def run(self, *args, **kwargs) -> Optional[Dict]:
        image_file = kwargs[ArgsType.IMAGE.value]
        language = kwargs.get("language", "en")
        return self.analyze_image(image_file, language)