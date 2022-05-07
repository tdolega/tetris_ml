import signal
from globalSetting import *
from simulator import getBestMoves
from connector import startGame, sendKeystrokes

def mainLoop():
    logging.info('='*30)
    
    bestMoves = getBestMoves()
    sendKeystrokes(bestMoves)

    time.sleep(.1)

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
