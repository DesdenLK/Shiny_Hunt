import time
from modules.window import window
from modules.Games.RZ import RZ


def main():
    game = RZ(False)
    display = window()
    display.display("./roms/Rubi/Pokemon-Rubi.gba")
    time.sleep(2)
    display.move(400,200)
    time.sleep(5)
    display.focus()
    game.start_game()
    game.reset_game()

    time.sleep(5)
    display.close()

if __name__ == "__main__":
    main()

