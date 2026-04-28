from abc import ABC, abstractmethod


class Pokemon(ABC):
    species_id: int
    pid: int
    sid: int
    tid: int


    @property
    @abstractmethod
    def is_shiny(self) -> bool:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def is_starter(self) -> bool:
        ...


    def __str__(self) -> str:
        shiny_tag = " ✨ SHINY!" if self.is_shiny else ""
        return (
            f"{self.name} (#{self.species_id}) | "
            f"PID: 0x{self.pid:08X} | "
            f"TID: {self.tid} | SID: {self.sid}{shiny_tag}"
        )