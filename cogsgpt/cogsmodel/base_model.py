import abc


class BaseModel(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs) -> str:
        pass

