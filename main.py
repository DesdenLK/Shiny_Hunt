import argparse
from hunter.rubySapphireHunter import RubySapphireHunter

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8888)
args = parser.parse_args()

hunter = RubySapphireHunter(port=args.port)
hunter.main_legendary_hunter_loop()