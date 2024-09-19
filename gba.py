import time
import os
from modules.window import window
from modules.Games.Rubi import Rubi
import pyfiglet
from colorama import Fore, Back, Style

def clean_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    game = None
    print(Fore.YELLOW + pyfiglet.figlet_format("Auto Shiny Hunt", font="slant") + Fore.RESET)
    print("1. Pokemon Zafiro")
    print("2. Pokemon Rubi")
    print("3. Salir")
    print("Seleccione un juego:")
    option = int(input())
    
    if option < 3: game = Rubi()

    clean_terminal()
    game.menu_mode()

def main():
    clean_terminal()
    print_menu()

if __name__ == "__main__":
    main()

