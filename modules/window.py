import subprocess
import time


class window():
    def __init__(self, x=100, y=100, width=250, height=250):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.process = None
        self.window_id = None

    def __get_windowID(self):

        # Buscar el ID de la ventana asociada al PID usando wmctrl
        try:
            # Ejecutar wmctrl -lp y capturar la salida
            wmctrl_output = subprocess.check_output(['wmctrl', '-lp'], universal_newlines=True)
            
            # Filtrar el ID de la ventana asociada al PID
            window_id = None
            for line in wmctrl_output.splitlines():
                if str(self.process.pid) in line:  # Buscar el PID en cada línea
                    window_id = line.split()[0]  # Obtener el primer campo (el ID de la ventana)
                    break
            
            if window_id:
                self.window_id = window_id
            else:
                print(f"No se encontró ninguna ventana asociada con el PID {self.process.pid}.")
                
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar wmctrl: {e}")

    def display(self, rom_path):
        self.process = subprocess.Popen(["mgba-qt", rom_path])
        time.sleep(2)
        self.__get_windowID()
        subprocess.run(["wmctrl", "-ir", self.window_id, "-e", f"0,{self.x},{self.y},{self.width},{self.height}"])

    def close(self):
        # Cerrar la ventana
        subprocess.run(["wmctrl", "-ic", self.window_id])

    def move(self, x, y):
        # Mover la ventana
        self.x = x
        self.y = y
        subprocess.run(["wmctrl", "-ir", self.window_id, "-e", f"0,{x},{y},{self.width},{self.height}"])

    def resize(self, width, height):
        self.width = width
        self.height = height
        subprocess.run(["wmctrl", "-ir", self.window_id, "-e", f"0,{self.x},{self.y},{width},{height}"])

    def focus(self):
        # Dar foco a la ventana
        subprocess.run(["wmctrl", "-ia", self.window_id])


