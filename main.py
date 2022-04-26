from globalSetting import *
from analyze import getMetrics
from connector import getGameInfo, sendKeystrokes, startGame

if __name__ == "__main__":
    startGame()
    while True:
        currPiece, nextPiece, field = getGameInfo()
        metrics = getMetrics(field)
        
        randomAction = random.choice(list(ACTIONS.values()))
        sendKeystrokes(randomAction)

        time.sleep(1)
        logging.debug('='*30)
