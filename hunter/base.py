from abc import ABC, abstractmethod


class BaseHunter(ABC):
    @abstractmethod
    def soft_reset(self):
        ...
    @abstractmethod
    def load_state(self, state: int):
        ...

    @abstractmethod
    def select_starter(self, starter_name: str):
        ...

    @abstractmethod
    def starter_hunter_loop(self, starter: str):
        ...

    @abstractmethod
    def main_legendary_hunter_loop(self):
        ...