import argparse
from hunter.rubySapphireHunter import RubySapphireHunter

GENERATIONS = {
    1: {
        "label": "Generación 3 (GBA)",
        "games": {
            1: {
                "label":        "Pokémon Ruby",
                "version":      "ruby",
                "hunter_class": RubySapphireHunter,
                "legendaries":  {1: "Groudon", 2: "Rayquaza", 3: "Regirock", 
                4: "Regice", 5: "Registeel", 6: "Latios"},
            },
            2: {
                "label":        "Pokémon Sapphire",
                "version":      "sapphire",
                "hunter_class": RubySapphireHunter,
                "legendaries":  {1: "Kyogre", 2: "Rayquaza", 3: "Regirock", 
                4: "Regice", 5: "Registeel", 6: "Latias"},
            },
        },
        "modes": {
            1: "Starter",
            2: "Legendario",
            3: "Wild Pokemon"
        },
        "starters": {
            1: "Treecko",
            2: "Torchic",
            3: "Mudkip",
        },
    },
}

BOLD  = "\033[1m"
CYAN  = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"
DIM   = "\033[2m"


def print_banner():
    print(f"\n{BOLD}{CYAN}{'='*40}")
    print("       ✦  SHINY HUNTER  ✦")
    print(f"{'='*40}{RESET}\n")


def pick_number(prompt: str, options: dict) -> int:
    for key, entry in options.items():
        label = entry["label"] if isinstance(entry, dict) else entry
        print(f"  {BOLD}{key}{RESET}. {label}")
    print()
    while True:
        try:
            choice = int(input(f"{prompt} (1-{len(options)}): ").strip())
            if choice in options:
                return choice
        except ValueError:
            pass
        print(f"  {DIM}Opción inválida. Ingresa un número entre 1 y {len(options)}.{RESET}")


def main(port: int):
    print_banner()

    print(f"{BOLD}Selecciona una generación:{RESET}\n")
    gen_key = pick_number("Generación", GENERATIONS)
    gen = GENERATIONS[gen_key]

    print(f"\n{BOLD}Selecciona un juego:{RESET}\n")
    game_key = pick_number("Juego", gen["games"])
    game = gen["games"][game_key]

    print(f"\n{BOLD}Selecciona el modo de caza:{RESET}\n")
    mode_key = pick_number("Modo", gen["modes"])
    mode = gen["modes"][mode_key]

    starter = None
    legendary = None

    if mode == "Starter":
        print(f"\n{BOLD}Selecciona el starter:{RESET}\n")
        starter_key = pick_number("Starter", gen["starters"])
        starter = gen["starters"][starter_key]
    elif mode == "Legendario":
        print(f"\n{BOLD}Selecciona el legendario:{RESET}\n")
        legendary_key = pick_number("Legendario", game["legendaries"])
        legendary = game["legendaries"][legendary_key]

    target = starter or legendary
    print(f"\n{GREEN}▶ {game['label']} — {mode} ({target}) (puerto {port}){RESET}\n")

    hunter = game["hunter_class"](port=port, version=game["version"])

    if mode == "Starter":
        hunter.hunt_starter(starter)
    elif mode == "Legendario":
        hunter.hunt_legendary(legendary)
    else:
        hunter.hunt_wild_pokemon()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()
    main(args.port)
