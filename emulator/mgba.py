import socket
from emulator.base import Emulator
import logging
import time

logger = logging.getLogger(__name__)


class MGBA(Emulator):
    """
    Se comunica con mGBA a través del script Lua que corre dentro del emulador.
    
    Protocolo:
        Python  →  "R32:02024284\n"
        mGBA    →  "1234567890\n"
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8888, timeout: float = 60.0):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock: socket.socket | None = None
        self._recv_buf: bytes = b""

    # ------------------------------------------------------------------ #
    # EmulatorBridge interface
    # ------------------------------------------------------------------ #

    def connect(self, retries: int = 5, delay: float = 1.0) -> bool:
        for attempt in range(1, retries + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self._timeout)
                sock.connect((self._host, self._port))
                self._sock = sock
                logger.info("Conectado a mGBA en %s:%d", self._host, self._port)
                return True
            except (ConnectionRefusedError, OSError) as e:
                logger.warning(
                    "Intento %d/%d fallido: %s. ¿Está el script Lua cargado en mGBA?",
                    attempt, retries, e
                )
                if attempt < retries:
                    time.sleep(delay)

        logger.error("No se pudo conectar a mGBA tras %d intentos.", retries)
        return False

    def disconnect(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
            self._recv_buf = b""
            logger.info("Desconectado de mGBA.")

    def read_u8(self, address: int) -> int:
        return self._send_command("R8", address)

    def read_u16(self, address: int) -> int:
        return self._send_command("R16", address)

    def read_u32(self, address: int) -> int:
        return self._send_command("R32", address)

    def _send_command_raw(self, cmd: str) -> str:
        if not self._sock:
            raise RuntimeError("No conectado.")
        self._sock.sendall(f"{cmd}\n".encode())
        return self._recv_line().strip()

    @property
    def is_connected(self) -> bool:
        return self._sock is not None

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #

    def _send_command(self, cmd: str, address: int) -> int:
        if not self._sock:
            raise RuntimeError("No hay conexión con mGBA. Llama a connect() primero.")

        message = f"{cmd}:{address:08X}\n"
        try:
            self._sock.sendall(message.encode())
            response = self._recv_line()
            return int(response.strip())
        except (OSError, ValueError) as e:
            logger.error("Error leyendo memoria en 0x%08X: %s", address, e)
            self._sock = None  # marcar como desconectado
            raise


    def _recv_line(self) -> str:
        assert self._sock is not None
        try:
            while b"\n" not in self._recv_buf:
                chunk = self._sock.recv(64)
                if not chunk:
                    raise OSError("Conexión cerrada por mGBA.")
                self._recv_buf += chunk
        except (TimeoutError, OSError):
            self._sock = None
            self._recv_buf = b""
            raise
        line, self._recv_buf = self._recv_buf.split(b"\n", 1)
        return line.decode()