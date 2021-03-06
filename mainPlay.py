from globalSetting import *
from ai import Network
from connector import Connector, runAsUnixPgroup
from simulator import Simulator

MODEL_FILENAME = 'models/' + 'model.bin' # delete first part (folder) if using provided model
displayMode=True

def play(model):
    conn = Connector(-1)
    conn.startGame(displayMode)
    sim = Simulator(conn, model)
    while True:
        currTetromino, nextTetromino, _, score, isGameOver = conn.getGameInfo()

        if isGameOver or score >= MAX_SCORE:
            logging.info('Ended with score: %s' % score)
            continue

        bestMoves = sim.getBestMoves(currTetromino, nextTetromino)

        # conn.sendKeystrokes(bestMoves)
        conn.sendKeystrokesSlow(bestMoves)

def main():
    modelState = torch.load(MODEL_FILENAME)
    model = Network()
    model.load_state_dict(modelState)
    play(model)

if __name__ == '__main__':
    runAsUnixPgroup(main)