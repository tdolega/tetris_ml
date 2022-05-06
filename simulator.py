from globalSetting import *
from connector import *
from analyze import getFitness

# how many rotations of tetromino we need to check
def rotatesToCheck(tetromino):
    match tetromino:
        case 'O':
            return 1
        case 'S' | 'Z' | 'I':
            return 2
        case _:
            return 4

# how many shift to left and right we need to check
def shiftsToCheck(tetromino):
    match tetromino:
        case 'I':
            return (5, 4)
        case _:
            return (4, 4)

# simulate all possible moves, and return best combination
bestScore = 0
bestMoves = ''
def getBestMoves():
    global bestScore, bestMoves
    bestScore = -10000 # todo: this is not nice
    bestMoves = ''

    currTetromino, nextTetromino, _ = getGameInfo() # todo: use nextTetromino
    shiftsLeft, shiftsRight = shiftsToCheck(currTetromino)

    sendKeystrokes(ACTIONS['save'])
    getGameInfo() # we need to do this useless read, to make game tick. This is not nice.
    for rotates in range(rotatesToCheck(currTetromino)):
        check(rotates, 0, 0)
        for sl in range(1, shiftsLeft + 1):
            check(rotates, sl, 0)
        for sr in range(1, shiftsRight + 1):
            check(rotates, 0, sr)

    logging.debug('best keystrokes: %s', bestMoves)
    return bestMoves

# simulate move, and update best score
def check(rotates, shiftsLeft, shiftsRight):
    keystrokes = ACTIONS['restore']              \
               + ACTIONS['rotate'] * rotates     \
               + ACTIONS['left']   * shiftsLeft  \
               + ACTIONS['right']  * shiftsRight \
               + ACTIONS['harddrop']

    sendKeystrokes(keystrokes)
    _, _, field = getGameInfo()
    score = getFitness(field)

    global bestScore, bestMoves
    if score > bestScore:
        bestScore = score
        bestMoves = keystrokes

    