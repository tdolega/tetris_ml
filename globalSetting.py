##### configuration #####

# pipes
inputName = '/tmp/biai_output' # game output, AI input
outputName = '/tmp/biai_input' # AI output, game input

TETRIS_GAME_RUN_PATH = '../game/SFML_TETRIS'
TETRIS_GAME_EXE_PATH = '../game/SFML_TETRIS/cmake-build-debug/SFML_TETRIS'
TETRIS_GAME_PARAMS = ['p']

#####      ai       #####

# network
N_INPUT_SIZE = 9
N_OUTPUT_SIZE = 1
N_WEIGHTS_INIT_MAX = 1
N_WEIGHTS_INIT_MIN = -N_WEIGHTS_INIT_MAX
N_DEVICE = 'cpu'

# population
P_ELITISM = 0.25
P_MUTATION = 0.25

#####               #####

import time
import logging
import random
import os
import numpy as np

LOG_FORMAT = "%(levelname)s> %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

# gamefield size
FIELD_WIDTH = 10
FIELD_UPPER_BUFFER = 4
FIELD_PLAYABLE_HEIGHT = 20
FIELD_HEIGHT = FIELD_PLAYABLE_HEIGHT + FIELD_UPPER_BUFFER
FIELD_LEN = FIELD_WIDTH * FIELD_HEIGHT
GAMEINFO_LEN = FIELD_LEN + 2

# game actions mapping
ACTIONS = {
    'left': 'a',
    'right': 'd',
    'rotate': 'r',
}

PIECE_NAMES = 'ILJSZTO'


#####               #####

# fix paths
TETRIS_GAME_RUN_PATH = os.path.join(os.path.dirname(__file__), TETRIS_GAME_RUN_PATH)
TETRIS_GAME_EXE_PATH = os.path.join(os.path.dirname(__file__), TETRIS_GAME_EXE_PATH)