from abc import ABC, abstractmethod


class BaseProvider(ABC):

    SUPPORTED_TASKS = set()

    def __init__(self, name: str):
        self.name = name

    def supports(self, task: str) -> bool:
        """Check whether this provider supports a task."""
        return task in self.SUPPORTED_TASKS

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def execute(self, task: str, **kwargs):
        pass
