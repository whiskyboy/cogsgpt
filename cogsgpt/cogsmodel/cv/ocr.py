import os
from typing import Optional
import azure.ai.vision as sdk

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

    def recognize_text(self, image_file: str, language: str = "en") -> Optional[str]:
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
            return '\n'.join([line.content for line in result.text.lines])
        else:
            return ''

    def run(self, *args, **kwargs) -> Optional[str]:
        image_file = kwargs[ArgsType.IMAGE.value]
        return self.recognize_text(image_file)
