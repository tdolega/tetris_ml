import time
import logging
import random
import os
import torch
import numpy as np
from multiprocessing import cpu_count

##### configuration #####

MAX_SCORE = 999999
USE_NEXT_PIECE = False

# pipes
INPUT_NAME = '/tmp/biai_output_' # game output, AI input
OUTPUT_NAME = '/tmp/biai_input_' # AI output, game input

# TETRIS_GAME_RUN_PATH = '../SFML_TETRIS/SFML_TETRIS'             # Marcin
# TETRIS_GAME_EXE_PATH = '../SFML_TETRIS/SFML_TETRIS/SFML_TETRIS' # Marcin
TETRIS_GAME_RUN_PATH = '../game/SFML_TETRIS'                                  # Tymek
TETRIS_GAME_EXE_PATH = '../game/SFML_TETRIS/cmake-build-release/SFML_TETRIS'  # Tymek

#####      ai       #####

# network
N_MIDDLE_SIZE = 4
N_OUTPUT_SIZE = 1
N_WEIGHTS_INIT_MAX = 1
N_WEIGHTS_INIT_MIN = -N_WEIGHTS_INIT_MAX
N_DEVICE = 'cpu'

MAX_EPOCHS = 100
RUNS_PER_CHILD = 6
WORKERS_AMOUNT = cpu_count()

# population
P_ELITISM = 0.25
P_MUTATION = 0.25
P_WEIGHTS_MUTATE_POWER = 0.1
P_SIZE = 100

#####               #####

LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(levelname)s> %(message)s"
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

# gamefield size
FIELD_WIDTH = 10
FIELD_UPPER_BUFFER = 4
FIELD_PLAYABLE_HEIGHT = 20
FIELD_HEIGHT = FIELD_PLAYABLE_HEIGHT + FIELD_UPPER_BUFFER
FIELD_LEN = FIELD_WIDTH * FIELD_HEIGHT
GAMEINFO_LEN = FIELD_LEN + 2 + 10 + 1 + 1

# game actions mapping
ACTIONS = {
    'left': 'a',
    'right': 'd',
    'rotate': 'w',
    'harddrop': 'q',
    'save': 'c',
    'restore': 'v',
    'reset': 'r',
    'stopDrawing': '[',
    'startDrawing': ']',
}

# tetromino id to name mapping
TETROMINO_NAMES = 'ILJSZTO'


#####               #####

# create absolute paths
TETRIS_GAME_RUN_PATH = os.path.join(os.path.dirname(__file__), TETRIS_GAME_RUN_PATH)
TETRIS_GAME_EXE_PATH = os.path.join(os.path.dirname(__file__), TETRIS_GAME_EXE_PATH)
