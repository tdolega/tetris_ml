from globalSetting import *

# send keystrokes to game
def sendKeystrokes(keystrokes):
    outCon = open(outputName, "w")
    outCon.write(keystrokes + "\n")
    logging.debug('sent(%d): %s', len(keystrokes)+1, keystrokes)
    outCon.close()

# get game field and score from game
def getGameInfo():
    inCon = open(inputName, "rb")
    info = inCon.read()
    inCon.close()

    if(len(info) != GAMEINFO_LEN):
        logging.critical('field len %d != %d', len(field), GAMEINFO_LEN)
        exit(1)

    currPiece = info[FIELD_LEN + 0]
    nextPiece = info[FIELD_LEN + 1]
    field = np.frombuffer(info, np.uint8, FIELD_LEN)
    field.shape = (FIELD_HEIGHT, FIELD_WIDTH)

    # logging.debug('received(%d):\n  field: \n%s\n  currPiece: %s\n  nextPiece: %s', len(info), field, currPiece, nextPiece)
    return (currPiece, nextPiece, field)