from abc import ABC, abstractmethod
from ..controller import controller
from ..window import window
from ..image_handler import *
import os

class baseGame(ABC):
    controller = controller()
    display = window()

    def __init__(self):
        self.resets = 0
        self.name = None
        self.started = False
        self.referenceColorPixelStarter = None

    def clean_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def reset_game(self):
        pass

    def close(self):
        self.controller.fast_forward_off()
        self.display.close()

    @abstractmethod
    def select_starter(self, starter):
        pass
    
    @abstractmethod
    def menu_mode(self):
        pass

    @abstractmethod
    def starter_menu(self):
        pass

    @abstractmethod
    def starter_hunt(self, option):
        pass

    @abstractmethod
    def spin_mode(self):
        pass

    @abstractmethod
    def search_encounter(self):
        pass

    @abstractmethod
    def battle_started(self):
        pass

    @abstractmethod
    def get_referenceImage(self):
        pass
    
    @abstractmethod
    def static_encounter(self, option):
        pass
    
    @abstractmethod
    def legendary_menu(self):
        pass

    def get_colorPixel_reference(self, path,x,y):
        return color_pixel(path, x, y)
    
