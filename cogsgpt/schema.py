from __future__ import annotations

from enum import Enum


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