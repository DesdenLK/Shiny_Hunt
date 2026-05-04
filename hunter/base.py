from abc import ABC, abstractmethod


class BaseHunter(ABC):

    @abstractmethod
    def soft_reset(self):
        ...

    @abstractmethod
    def load_state(self, state: int):
        ...

    @abstractmethod
    def hunt_starter(self, starter: str):
        ...

    @abstractmethod
    def hunt_legendary(self, legendary: str):
        ...

    def _log_attempt(self, pokemon, i: int, pid_count: dict) -> None:
        pid_count[pokemon.pid] = pid_count.get(pokemon.pid, 0) + 1
        count = pid_count[pokemon.pid]

        if count == 1:
            color = "\033[32m"
        elif count <= 3:
            color = "\033[33m"
        else:
            color = "\033[31m"

        print(
            f"Pokemon {pokemon} is shiny? {pokemon.is_shiny} "
            f"Shiny Value {pokemon.shiny_value}. Try number {i}. "
            f"PID 0x{pokemon.pid:08X} seen {color}{count}x\033[0m"
        )
