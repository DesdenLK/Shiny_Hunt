from abc import ABC, abstractmethod

class Emulator(ABC):
    @abstractmethod
    def connect(self) -> bool:
        ...

    def disconnect(self) -> None:
        ...

    def read_u8(self, _address: int) -> int:
        ...

    def read_u16(self, _address: int) -> int:
        ...

    def read_u32(self, _address: int) -> int:
        ...
