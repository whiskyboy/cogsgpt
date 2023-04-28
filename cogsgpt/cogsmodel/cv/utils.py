from __future__ import annotations

from io import BytesIO
import os
from typing import List, Tuple
import requests
import tempfile

from PIL import Image, ImageDraw

from cogsgpt.schema import FileSource
from cogsgpt.utils import detect_file_source


def load_image(image_file: str) -> Image:
    image_src = detect_file_source(image_file)
    if image_src == FileSource.LOCAL:
        image = Image.open(image_file)
    elif image_src == FileSource.REMOTE:
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content))
    else:
        raise ValueError(f"Invalid image source: {image_file}")

    if image.mode in ('1', 'L', 'P', 'LA', 'PA'):
        # convert to RGB mode for low bit depth images
        image = image.convert('RGB')
    
    return image


def draw_rectangles(src_image_file: str, tgt_image_file: str | None = None,
                    rectangles: List[Tuple[int, int, int, int]] = [], texts: List[str] = [],
                    line_color: str = 'red', line_width: int = 2,
                    text_color: str = 'black', text_bg_color: str = 'white',
                    text_offset: Tuple[int, int] = (5, 5)) -> str:
    if len(texts) > 0:
        assert len(rectangles) == len(texts), "The size of rectangles and texts should be the same."

    image = load_image(src_image_file)
    
    draw = ImageDraw.Draw(image)
    for bbox, text in zip(rectangles, texts):
        draw.rectangle(bbox, outline=line_color, width=line_width)
        text_x, text_y = bbox[0] + text_offset[0], bbox[1] + text_offset[1]
        left, top, right, bottom = draw.textbbox((text_x, text_y), text)
        draw.rectangle((left-5, top-5, right+5, bottom+5), fill=text_bg_color)
        draw.text((text_x, text_y), text, fill=text_color)

    if tgt_image_file is None:
        src_image_suffix = os.path.splitext(src_image_file)[1]
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.' + src_image_suffix, delete=False) as tgt_image_file:
            image.save(tgt_image_file)

    return tgt_image_file.name


def crop_rectangle(src_image_file: str, tgt_image_file: str | None = None,
                   rectangle: Tuple[int, int, int, int] = ()) -> str:
    image = load_image(src_image_file)

    cropped_image = image.crop(rectangle)

    if tgt_image_file is None:
        src_image_suffix = os.path.splitext(src_image_file)[1]
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.' + src_image_suffix, delete=False) as tgt_image_file:
            cropped_image.save(tgt_image_file)

    return tgt_image_file.name