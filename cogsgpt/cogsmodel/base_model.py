import abc
from typing import Optional


class BaseModel(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs) -> Optional[str]:
        pass

