##### configuration #####

# pipes
inputName = '/tmp/biai_output' # game output, AI input
outputName = '/tmp/biai_input' # AI output, game input

#####               #####

import time
import logging
import random
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

