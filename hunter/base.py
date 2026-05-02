from abc import ABC, abstractmethod


class BaseHunter(ABC):
    @abstractmethod
    def load_state(self, state: int):
        ...

    @abstractmethod
    def select_starter(self, starter_name: str):
        ...