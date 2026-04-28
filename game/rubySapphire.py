from emulator.mgba import MGBA
from pokemon.gen3 import PokemonGen3

PID_ADDRESS = 0x03004360
TID_ADDRESS = 0x03004364
SID_ADDRESS = 0x03004366

class RubySapphireReader():
    def __init__(self, bridge: MGBA):
        self._bridge = bridge

    def read_pokemon(self, species_id: int) -> PokemonGen3:
        pid = self._bridge.read_u32(PID_ADDRESS)
        tid = self._bridge.read_u16(TID_ADDRESS)
        sid = self._bridge.read_u16(SID_ADDRESS)

        return PokemonGen3(species_id, pid, sid, tid)
