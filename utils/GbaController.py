class GBAController():
    def __init__(self, bridge):
        self._bridge = bridge

    def press_key(self, key: str) -> None:
        self._bridge.send_command_raw(f"K:{key}")

    def load_state(self, slot: int) -> None:
        self._bridge.send_command_raw(f"LS:{slot}")

    def soft_reset(self) -> None:
        self._bridge.send_command_raw("SR")

    def advance_frames(self, n: int) -> None:
        self._bridge.send_command_raw(f"AF:{n}")
