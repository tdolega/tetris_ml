import subprocess
from globalSetting import *

# send keystrokes to game
def sendKeystrokes(keystrokes):
    outCon = open(outputName, 'w')
    outCon.write(keystrokes)
    outCon.close()
    logging.debug('sent(%d): %s', len(keystrokes), keystrokes)

# get game field and score from game
def getGameInfo():
    # get info from the game
    inCon = open(inputName, "rb")
    info = inCon.read()
    inCon.close()

    if(len(info) != GAMEINFO_LEN):
        logging.critical('field len %d != %d', len(field), GAMEINFO_LEN)
        exit(1)

    # unpack tetrominos
    currTetrominoIdx = info[FIELD_LEN + 0]
    nextTetrominoIdx = info[FIELD_LEN + 1]
    currTetromino = TETROMINO_NAMES[currTetrominoIdx]
    nextTetromino = TETROMINO_NAMES[nextTetrominoIdx]

    # unpack field
    field = np.frombuffer(info, np.uint8, FIELD_LEN)
    field.shape = (FIELD_HEIGHT, FIELD_WIDTH)

    logging.debug('received(%d):\n  field: \n%s\n  currTetromino: %s\n  nextTetromino: %s', len(info), field, currTetromino, nextTetromino)
    return (currTetromino, nextTetromino, field)

def startGame():
    logging.debug('starting game')
    subprocess.Popen(
        executable=TETRIS_GAME_EXE_PATH,
        args=TETRIS_GAME_PARAMS,
        cwd=TETRIS_GAME_RUN_PATH,
    )

    logging.debug('waiting for game input pipe..')
    while not os.path.exists(inputName):
        time.sleep(.1)
    logging.debug('waiting for game output pipe..')
    while not os.path.exists(outputName):
        time.sleep(.1)
