from abc import ABC, abstractmethod
from ..controller import controller

class baseGame(ABC):
    controller = controller()

    def __init__(self):
        self.resets = 0
        self.name = None
        self.started = False


    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def reset_game(self):
        pass

