from dataclasses import dataclass

from pokemon.pokemon import Pokemon


STARTER_IDS = {252, 255, 258} 

POKEMON_NAMES = {
    252: "Treecko",
    255: "Torchic",
    258: "Mudkip",
    401: "Regirock",
    402: "Regice",
    403: "Registeel",
    405: "Groudon",
    406: "Rayquaza"
}


@dataclass(frozen=True)
class PokemonGen3(Pokemon):
    species_id: int
    pid: int
    sid: int
    tid: int

    @property
    def shiny_value(self) -> int:
        pid_high = (self.pid >> 16) & 0xFFFF
        pid_low = self.pid & 0xFFFF
        return self.tid ^ self.sid ^ pid_high ^ pid_low

    @property
    def is_shiny(self) -> bool:
        return self.shiny_value < 8

    @property
    def name(self) -> str:
        return POKEMON_NAMES.get(self.species_id, f"Pokémon #{self.species_id}")

    @property
    def is_starter(self) -> bool:
        return self.species_id in STARTER_IDS