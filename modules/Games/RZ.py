import time
from modules.Games.baseGame import baseGame

class RZ(baseGame):
    def __init__(self, Zafiro):
        super().__init__()
        
        if Zafiro: self.name = "Pokemon Zafiro"
        else: self.name = "Pokemon Rubi"

        self.isZafiro = Zafiro


    def start_game(self):
        self.started = True
        
        self.controller.press_start()
        time.sleep(1)
        self.controller.press_start()
        time.sleep(1)
        self.controller.press_start()
        time.sleep(1)
        self.controller.press_a()
        time.sleep(0.5)

    def reset_game(self):
        self.resets += 1
        self.controller.press_reset()