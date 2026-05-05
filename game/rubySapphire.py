from emulator.mgba import MGBA
from pokemon.gen3 import PokemonGen3

STARTER_PID_ADDRESS = 0x03004360
TID_ADDRESS         = 0x03004364
SID_ADDRESS         = 0x03004366

ENEMY_PARTY_ADDRESS = 0x030045C0

# All 24 permutations of [1,2,3,4] mapping data slot → subgroup (G=1 A=2 E=3 M=4)
_BLOCK_ORDERS = [
    [1,2,3,4],[1,2,4,3],[1,3,2,4],[1,3,4,2],[1,4,2,3],[1,4,3,2],
    [2,1,3,4],[2,1,4,3],[2,3,1,4],[2,3,4,1],[2,4,1,3],[2,4,3,1],
    [3,1,2,4],[3,1,4,2],[3,2,1,4],[3,2,4,1],[3,4,1,2],[3,4,2,1],
    [4,1,2,3],[4,1,3,2],[4,2,1,3],[4,2,3,1],[4,3,1,2],[4,3,2,1],
]


class RubySapphireReader():
    def __init__(self, bridge: MGBA):
        self._bridge = bridge

    def read_starter_pokemon(self, species_id: int) -> PokemonGen3:
        pid = self._bridge.read_u32(STARTER_PID_ADDRESS)
        tid = self._bridge.read_u16(TID_ADDRESS)
        sid = self._bridge.read_u16(SID_ADDRESS)
        return PokemonGen3(species_id, pid, sid, tid)

    def read_enemy_pokemon(self) -> PokemonGen3:
        return self._decode_pokemon(ENEMY_PARTY_ADDRESS)

    def _decode_pokemon(self, base: int) -> PokemonGen3:
        pid  = self._bridge.read_u32(base + 0x00)
        otid = self._bridge.read_u32(base + 0x04)
        key  = pid ^ otid

        # Read and decrypt the 12 data words (3 words × 4 subgroups)
        block = [
            self._bridge.read_u32(base + 0x20 + i * 4) ^ key
            for i in range(12)
        ]

        # Assign words to subgroups G/A/E/M (indices 0-3) by block order
        order = _BLOCK_ORDERS[pid % 24]
        g: list[list[int] | None] = [None] * 4
        for i in range(4):
            start = i * 3
            g[order[i] - 1] = [block[start], block[start + 1], block[start + 2]]

        # Growth block (g[0]): species in lower 16 bits of first word
        assert g[0] is not None
        species = g[0][0] & 0xFFFF

        tid = otid & 0xFFFF
        sid = (otid >> 16) & 0xFFFF

        return PokemonGen3(species, pid, sid, tid)
