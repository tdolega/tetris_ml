from globalSetting import *
from analyze import getScore

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

def keystrokesStr(rotates, shiftsLeft, shiftsRight):
    return ACTIONS['rotate'] * rotates     \
         + ACTIONS['left']   * shiftsLeft  \
         + ACTIONS['right']  * shiftsRight \
         + ACTIONS['harddrop']

def allKeystrokesCombinations(tetromino):
    shiftsLeft, shiftsRight = shiftsToCheck(tetromino)
    for rotates in range(rotatesToCheck(tetromino)):
        yield keystrokesStr(rotates, 0, 0)
        for sl in range(1, shiftsLeft + 1):
            yield keystrokesStr(rotates, sl, 0)
        for sr in range(1, shiftsRight + 1):
            yield keystrokesStr(rotates, 0, sr)

class Simulator:
    def __init__(self, conn, child_model):
        self.conn = conn
        self.child_model = child_model

    # simulate all possible moves, and return best combination
    def getBestMoves(self, currTetromino, nextTetromino = None):
        self.bestScore = np.NINF
        self.bestMoves = ''
    
        self.conn.sendKeystrokes(ACTIONS['save'] + ACTIONS['stopDrawing'])
        _, _, _, pointsBefore, _ = self.conn.getGameInfo()

        if USE_NEXT_PIECE and nextTetromino:
            for currKeystrokes in allKeystrokesCombinations(currTetromino):
                for nextKeystrokes in allKeystrokesCombinations(nextTetromino):
                    self.check(currKeystrokes, nextKeystrokes)
        else:
            for keystrokes in allKeystrokesCombinations(currTetromino):
                self.check(keystrokes, pointsBefore)

        self.conn.sendKeystrokes(ACTIONS['restore'] + ACTIONS['startDrawing'])
        self.conn.getGameInfo()

        if len(self.bestMoves) == 0: # every move is losing
            return ACTIONS['harddrop']
            
        return self.bestMoves

    def check(self, currKeystrokes, pointsBefore = 0, nextKeystrokes = ''):
        self.conn.sendKeystrokes(ACTIONS['restore'] + currKeystrokes + nextKeystrokes)
        _, _, field, pointsAfter, isGameOver = self.conn.getGameInfo()
        if isGameOver:
            return
        pointsDiff = pointsAfter - pointsBefore
        score = getScore(self.child_model, field, pointsDiff)

        if score > self.bestScore:
            self.bestScore = score
            self.bestMoves = currKeystrokes