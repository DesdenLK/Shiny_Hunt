from tracemalloc import start
from emulator.mgba import MGBA
from game.rubySapphire import RubySapphireReader
from utils.GbaController import GBAController
from hunter.base import BaseHunter
import time

STARTER_IDS = {
    "Treecko": 252,
    "Torchic": 255,
    "Mudkip": 258

}


class RubySapphireHunter(BaseHunter):
    def __init__(self) -> None:
        self.bridge = MGBA()
        self.input = GBAController(self.bridge)
        self.game = RubySapphireReader(self.bridge)

    def load_state(self, state: int):
        self.input.load_state(state)

    def select_starter(self, starter_name: str):
        time.sleep(2)
        if starter_name == "Treecko":
            self.input.press_key("LEFT")
        elif starter_name == "Mudkip":
            self.input.press_key("RIGHT")
        time.sleep(0.1)
        self.input.press_key("A")
        time.sleep(0.1)
        self.input.press_key("A")
        time.sleep(0.1)
        self.input.press_key("A")


    def starter_hunter_loop(self):
        self.bridge.connect()
        starter = input("Write the name of the starter you want to catch!")
        while starter != "Treecko" and starter != "Torchic" and starter != "Mudkip":
            starter = input("Try Again. Write it with the first letter in capital")


        time.sleep(10)
        is_shiny = False
        i = 1
        while not is_shiny:
            self.load_state(1)
            self.select_starter(starter)
            pokemon = self.game.read_pokemon(STARTER_IDS.get(starter))
            is_shiny = pokemon.is_shiny
            print(f"Pokemon {pokemon} is shiny? {is_shiny} Shiny Value {pokemon.shiny_value}. Try number {i}")
            
            i+=1

            
            