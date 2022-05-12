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

class Simulator:
    def __init__(self, conn, child_model):
        self.conn = conn
        self.child_model = child_model

    # simulate all possible moves, and return best combination
    def getBestMoves(self, currTetromino, nextTetromino): #TODO use nextTetromino
        self.bestScore = np.NINF
        self.bestMoves = ''
    
        self.conn.sendKeystrokes(ACTIONS['save'] + ACTIONS['stopDrawing'])
        self.conn.getGameInfo()

        shiftsLeft, shiftsRight = shiftsToCheck(currTetromino)
        for rotates in range(rotatesToCheck(currTetromino)):
            self.check(rotates, 0, 0)
            for sl in range(1, shiftsLeft + 1):
                self.check(rotates, sl, 0)
            for sr in range(1, shiftsRight + 1):
                self.check(rotates, 0, sr)

        self.conn.sendKeystrokes(ACTIONS['restore'] + ACTIONS['startDrawing'])
        self.conn.getGameInfo()

        return self.bestMoves

    # simulate move, and update best score
    def check(self, rotates, shiftsLeft, shiftsRight):
        keystrokes = ACTIONS['rotate'] * rotates     \
                + ACTIONS['left']   * shiftsLeft  \
                + ACTIONS['right']  * shiftsRight \
                + ACTIONS['harddrop']

        self.conn.sendKeystrokes(ACTIONS['restore'] + keystrokes)
        _, _, field, _, isGameOver = self.conn.getGameInfo()
        if isGameOver:
            return
            
        score = getScore(self.child_model, field)

        if score > self.bestScore:
            self.bestScore = score
            self.bestMoves = keystrokes
