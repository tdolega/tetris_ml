from globalSetting import *
from analyze import getMetrics
from connector import getGameInfo, sendKeystrokes

# main loop
while True:
    (currPiece, nextPiece, field) = getGameInfo()
    metrics = getMetrics(field)
    randomAction = random.choice(list(ACTIONS.values()))
    sendKeystrokes(randomAction)
    time.sleep(1)
    logging.debug('='*30)
