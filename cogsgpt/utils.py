from enum import Enum
import os
from typing import Optional
from urllib.parse import urlparse


class ArgsType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


class LanguageType(Enum):
    Chinese = "chinese"
    English = "english"


class FileSource(Enum):
    LOCAL = "local"
    REMOTE = "remote"


def detect_file_source(file_path: str) -> Optional[str]:
    # Check if the input is a local file path
    if os.path.isfile(file_path):
        return FileSource.LOCAL

    # Check if the input is a web URL
    parsed_url = urlparse(file_path)
    if parsed_url.scheme and parsed_url.netloc:
        return FileSource.REMOTE

    # If the input is neither a local file path nor a web URL, raise an exception
    raise ValueError("Input must be a local file path or a web URL")