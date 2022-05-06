import signal
from globalSetting import *
from simulator import getBestMoves
from connector import startGame, sendKeystrokes

def mainLoop():
    bestMoves = getBestMoves()
    sendKeystrokes(bestMoves)

    time.sleep(.1)
    logging.debug('='*30)

if __name__ == "__main__":
    os.setpgrp() # create new process group
    try:
        startGame()
        while True:
            mainLoop()
    except Exception as e:
        logging.critical(e)        
    finally:
        os.killpg(0, signal.SIGKILL) # kill all game processes on error
