import time
import random
from collections.abc import Callable
from emulator.mgba import MGBA
from game.rubySapphire import RubySapphireReader
from pokemon.gen3 import PokemonGen3
from utils.GbaController import GBAController
from hunter.base import BaseHunter

STARTER_IDS = {
    "Treecko": 252,
    "Torchic": 255,
    "Mudkip":  258,
}


class RubySapphireHunter(BaseHunter):

    def __init__(self, port: int = 8888, version: str = "ruby") -> None:
        self.bridge = MGBA(port=port)
        self.input = GBAController(self.bridge)
        self.game = RubySapphireReader(self.bridge)
        self.version = version

    # ------------------------------------------------------------------ #
    # Interfaz pública                                                     #
    # ------------------------------------------------------------------ #

    def hunt_starter(self, starter: str) -> None:
        self.bridge.connect()
        time.sleep(1)
        self._run_loop(lambda: self._starter_attempt(starter))
        self.bridge.disconnect()

    def hunt_legendary(self, legendary: str) -> None:
        dispatch = {
            "Groudon":   self._main_legendary_attempt,
            "Kyogre":    self._main_legendary_attempt,
            "Rayquaza":  lambda: self._static_encounter_attempt(500),
            "Regirock":  lambda: self._static_encounter_attempt(500),
            "Regice":    lambda: self._static_encounter_attempt(500),
            "Registeel": lambda: self._static_encounter_attempt(500),
            "Latios":    self._roaming_pokemon_attempt,
            "Latias":    self._roaming_pokemon_attempt,
        }
        self.bridge.connect()
        time.sleep(1)
        self._run_loop(dispatch[legendary])

    # ------------------------------------------------------------------ #
    # Mecánicas base                                                       #
    # ------------------------------------------------------------------ #

    def soft_reset(self):
        self.input.soft_reset()
        for _ in range(5):
            self.input.advance_frames(60)
            self.input.press_key("START")
        self.input.press_key("A")
        self.input.advance_frames(90)

    def load_state(self, state: int):
        self.input.load_state(state)

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
        self.input.advance_frames(random.randint(0, 1000))
        self.input.press_key("A")
        self.input.advance_frames(180)

    # ------------------------------------------------------------------ #
    # Intentos individuales (un reset → una lectura)                      #
    # ------------------------------------------------------------------ #

    def _starter_attempt(self, starter: str):
        self.soft_reset()
        time.sleep(random.uniform(0.1, 0.3))
        self.select_starter(starter)
        return self.game.read_starter_pokemon(STARTER_IDS[starter])

    def _main_legendary_attempt(self):
        self.soft_reset()
        time.sleep(random.uniform(0.1, 0.3))
        self.input.advance_frames(random.randint(0, 1000))
        self.input.press_key("LEFT")
        self.input.advance_frames(6)
        self.input.press_key("A")
        self.input.advance_frames(6)
        self.input.press_key("A")
        self.input.advance_frames(1300)
        return self.game.read_enemy_pokemon()

    def _roaming_pokemon_attempt(self):
        self.soft_reset()
        self.input.press_key("A")
        self.input.advance_frames(20)
        self.input.press_key("A")
        self.input.advance_frames(20)
        self.input.press_key("A")
        self.input.advance_frames(20)
        self.input.press_key("A")
        self.input.advance_frames(20)
        time.sleep(random.uniform(0.1, 0.3))
        self.input.advance_frames(random.randint(0, 1000))
        self.input.press_key("A")
        self.input.advance_frames(40)
        return self.game.read_roaming_pokemon()

    def _static_encounter_attempt(self, framess_to_hold: int):
        self.soft_reset()
        time.sleep(random.uniform(0.1, 0.3))
        self.input.advance_frames(random.randint(0, 1000))
        self.input.press_key("A")
        self.input.advance_frames(6)
        self.input.advance_frames(framess_to_hold)
        return self.game.read_enemy_pokemon()


    # ------------------------------------------------------------------ #
    # Loop genérico                                                        #
    # ------------------------------------------------------------------ #

    def _run_loop(self, attempt_fn: Callable[[], PokemonGen3]) -> None:
        is_shiny = False
        i = 1
        pid_count: dict[int, int] = {}

        while not is_shiny:
            try:
                pokemon = attempt_fn()
            except (TimeoutError, OSError) as e:
                print(f"\033[31mConnection error: {e}. Reconnecting...\033[0m")
                self.bridge.disconnect()
                self.bridge.connect()
                continue

            self._log_attempt(pokemon, i, pid_count)
            is_shiny = pokemon.is_shiny
            i += 1
