from tracemalloc import start
from emulator.mgba import MGBA
from game.rubySapphire import RubySapphireReader
from utils.GbaController import GBAController
from hunter.base import BaseHunter
import time
import random
STARTER_IDS = {
    "Treecko": 252,
    "Torchic": 255,
    "Mudkip": 258

}


class RubySapphireHunter(BaseHunter):
    def __init__(self, port: int = 8888) -> None:
        self.bridge = MGBA(port=port)
        self.input = GBAController(self.bridge)
        self.game = RubySapphireReader(self.bridge)

    def load_state(self, state: int):
        self.input.load_state(state)

    def soft_reset(self):
        self.input.soft_reset()
        for _ in range(5):
            self.input.advance_frames(60)
            self.input.press_key("START")
        self.input.press_key("A")
        self.input.advance_frames(90)   # cargar partida → en juego



    def select_starter(self, starter_name: str):
        self.input.press_key("A")
        if starter_name == "Treecko":
            self.input.press_key("LEFT")
        elif starter_name == "Mudkip":
            self.input.press_key("RIGHT")
        self.input.advance_frames(6)
        self.input.press_key("A")
        self.input.advance_frames(6)
        self.input.press_key("A")
        self.input.advance_frames(6)
        random_frames = random.randint(0, 300)
        self.input.advance_frames(random_frames)
        self.input.press_key("A")
        self.input.advance_frames(180)


    def starter_hunter_loop(self):
        self.bridge.connect()
        starter = input("Write the name of the starter you want to catch!")
        while starter != "Treecko" and starter != "Torchic" and starter != "Mudkip":
            starter = input("Try Again. Write it with the first letter in capital")


        time.sleep(1)
        is_shiny = False
        i = 1
        pid_count = {}
        while not is_shiny:
            try:
                self.soft_reset()
                r = random.uniform(0.1, 0.3)
                time.sleep(r)
                self.select_starter(starter)
                pokemon = self.game.read_pokemon(STARTER_IDS.get(starter))
            except (TimeoutError, OSError) as e:
                print(f"\033[31mConnection error: {e}. Reconnecting...\033[0m")
                self.bridge.disconnect()
                self.bridge.connect()
                continue
            is_shiny = pokemon.is_shiny
            pid_count[pokemon.pid] = pid_count.get(pokemon.pid, 0) + 1
            count = pid_count[pokemon.pid]
            if count == 1:
                seen_color = "\033[32m"    # verde
            elif count <= 3:
                seen_color = "\033[33m"    # amarillo
            else:
                seen_color = "\033[31m"    # rojo
            reset = "\033[0m"
            print(f"Pokemon {pokemon} is shiny? {is_shiny} Shiny Value {pokemon.shiny_value}. Try number {i}. PID 0x{pokemon.pid:08X} seen {seen_color}{count}x{reset}")

            i+=1

        self.bridge.disconnect()

            