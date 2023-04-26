from __future__ import annotations

import json
import os
import tempfile
import requests

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.schema import ArgsType, FileSource
from cogsgpt.utils import detect_file_source


class BackgroundRemover(BaseModel):
    def __init__(self) -> None:
        super().__init__()

        self.COGS_KEY = os.environ['COGS_KEY']
        self.COGS_ENDPOINT = f"{os.environ['COGS_ENDPOINT']}/computervision/imageanalysis:segment?api-version=2023-02-01-preview&mode=backgroundRemoval"

    def _remove_background(self, image_file: str) -> str:
        image_src = detect_file_source(image_file)
        if image_src == FileSource.LOCAL:
            headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': self.COGS_KEY
            }
            with open(image_file, 'rb') as image:
                body = image.read()
        elif image_src == FileSource.REMOTE:
            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.COGS_KEY
            }
            body = json.dumps({'url': image_file})
        else:
            raise ValueError(f"Invalid image source: {image_file}")

        response = requests.post(self.COGS_ENDPOINT, headers=headers, data=body)

        if response.status_code == 200:
            suffix = os.path.splitext(image_file)[1]
            with tempfile.NamedTemporaryFile(mode='w+b', suffix='.' + suffix, delete=False) as tgt_image_file:
                tgt_image_file.write(response.content)
                return tgt_image_file.name
        else:
            raise ValueError(f"Error: {response.status_code} {response.reason}")

    def run(self, *args, **kwargs) -> str:
        image_file = kwargs[ArgsType.IMAGE.value]
        return self._remove_background(image_file)
