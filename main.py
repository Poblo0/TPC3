import src.game as game
import os
import argparse
import importlib

# 1. Configuración del analizador de argumentos
parser = argparse.ArgumentParser(description="Ejecución de partidas con oponentes dinámicos.")
parser.add_argument(
    "player1",
    help="Nombre del archivo de la sumisión para el jugador 1 en /submissions (sin .py)"
)
parser.add_argument(
    "player2",
    nargs="?",
    default="xd",
    help="Nombre del archivo de la sumisión para el jugador 2 en /submissions (sin .py)"
)
args = parser.parse_args()

# 2. Carga dinámica de los módulos seleccionados
try:
    # Carga del módulo para el jugador 1
    module_path1 = f"submissions.{args.player1}"
    player1_module = importlib.import_module(module_path1)
    Player1 = player1_module.Submission
except ImportError:
    print(f"Error: No se pudo encontrar el módulo '{args.player1}' en la carpeta submissions.")
    exit()
except AttributeError:
    print(f"Error: El módulo '{args.player1}' no tiene una clase 'Submission'.")
    exit()

try:
    # Carga del módulo para el jugador 2
    module_path2 = f"submissions.{args.player2}"
    player2_module = importlib.import_module(module_path2)
    Player2 = player2_module.Submission
except ImportError:
    print(f"Error: No se pudo encontrar el módulo '{args.player2}' en la carpeta submissions.")
    exit()
except AttributeError:
    print(f"Error: El módulo '{args.player2}' no tiene una clase 'Submission'.")
    exit()

# 3. Lógica del bucle de juego
round_num = 0
while os.path.isfile(f"./levels/level_{round_num}.txt"):
    game.set_up(f"./levels/level_{round_num}.txt", Player1(), Player2())
    game.loop()
    round_num += 1

print("Final scores:", game.team_points)
