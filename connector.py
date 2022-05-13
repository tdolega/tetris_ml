import subprocess
import signal

from globalSetting import *

class Connector:
    def __init__(self, idx):
        self.idx = str(idx)
        self.outputName = OUTPUT_NAME + self.idx
        self.inputName = INPUT_NAME + self.idx

    def startGame(self):
        logging.debug('starting game')
        self.processHandle = subprocess.Popen(
            cwd=TETRIS_GAME_RUN_PATH,
            executable=TETRIS_GAME_EXE_PATH,
            args=['p', self.idx],
            shell=True
        )

        logging.debug('waiting for game output pipe..')
        while not os.path.exists(self.outputName):
            time.sleep(.1)
        self.outCon = open(self.outputName, 'w')

        logging.debug('waiting for game input pipe..')
        while not os.path.exists(self.inputName):
            time.sleep(.1)
        self.inCon = open(self.inputName, 'rb')

    def kill(self):
        if self.processHandle:
            self.processHandle.kill()
        else:
            logging.error('killing game failed: cannot get process handle')

    # get game field and score from game
    def getGameInfo(self):
        # get info from the game
        info = self.inCon.readline()

        if(len(info) != GAMEINFO_LEN):
            logging.critical('field len %d != %d', len(info), GAMEINFO_LEN)
            exit(1)

        # unpack tetrominos
        currTetrominoIdx = info[FIELD_LEN + 0]
        nextTetrominoIdx = info[FIELD_LEN + 1]
        currTetromino = TETROMINO_NAMES[currTetrominoIdx]
        nextTetromino = TETROMINO_NAMES[nextTetrominoIdx]

        scoreString = info[FIELD_LEN + 2:FIELD_LEN + 12]
        score = int(scoreString)

        isGameOver = info[FIELD_LEN + 12] == ord('N')

        # unpack field
        field = np.frombuffer(info, np.uint8, FIELD_LEN)
        field.shape = (FIELD_HEIGHT, FIELD_WIDTH)

        logging.debug('received(%d):\n  field: \n%s\n  currTetromino: %s\n  nextTetromino: %s', len(info), field, currTetromino, nextTetromino)
        return (currTetromino, nextTetromino, field, score, isGameOver)

    def sendKeystrokes(self, keystrokes):
        written = self.outCon.write(keystrokes + '\n')
        self.outCon.flush()
        logging.debug('sent(%d): %s', written, keystrokes)

    def sendKeystrokesSlow(self, keystrokes):
        for i, key in enumerate(keystrokes):
            written = self.outCon.write(key + '\n')
            self.outCon.flush()
            logging.debug('sent(%d): %s', written, key)
            time.sleep(0.05)
            if i < len(keystrokes) - 1:
                self.getGameInfo()

def runAsUnixPgroup(func):
    os.setpgrp() # create new process group
    try:
        func()
    except Exception as e:
        logging.critical(e)        
    finally:
        os.killpg(0, signal.SIGKILL) # kill all game processes on error