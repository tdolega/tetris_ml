import pickle
from multiprocessing import Pool
from datetime import datetime
import operator

from globalSetting import *
from ai import Population
from simulator import Simulator
from connector import Connector, runAsUnixPgroup
from analyze import METRICS_NAMES

def training(epoch, child_index, child_model):
    scores = []

    conn = Connector(child_index)
    conn.startGame()

    sim = Simulator(conn, child_model)

    run = 0
    while True:
        currTetromino, nextTetromino, _, score, isGameOver = conn.getGameInfo()

        if isGameOver or score >= MAX_SCORE:
            scores.append(score)
            conn.sendKeystrokes(ACTIONS['reset'])
            run += 1
            if run < RUNS_PER_CHILD:
                continue
            break

        bestMoves = sim.getBestMoves(currTetromino)
        conn.sendKeystrokes(bestMoves)

    conn.kill()

    fitness = np.average(scores)
    fitnessDiff = 100*((max(scores) - min(scores)) / fitness) if fitness else 0
    logging.info("epoch %2d child %2d -> fitness %6d ± %d%%" % (epoch, child_index, fitness, fitnessDiff))

    return fitness

def train():
    population = None
    maxFitnessEver = 0

    epoch = 0
    pool = Pool(WORKERS_AMOUNT)

    tTrainingStart = datetime.now()

    while epoch < MAX_EPOCHS:
        tEpochStart = datetime.now()

        if population is None:
            if epoch == 0:
                population = Population(P_SIZE)
            else:
                with open('checkpoints/%s.pkl' % (epoch - 1), 'rb') as f:
                    population = pickle.load(f)
        else:
            population = Population(P_SIZE, population)

        fitnesses, models = zip(*sorted(zip(population.fitnesses, population.models), reverse=True, key=operator.itemgetter(0)))
        population.fitnesses = np.asarray(fitnesses)
        population.models = list(models)

        workers = []
        for i in range(P_SIZE):
            worker = pool.apply_async(training, (epoch, i, population.models[i]))
            workers.append(worker)
        for i, worker in enumerate(workers):
            population.fitnesses[i] = worker.get()

        maxFitness = np.max(population.fitnesses)
        epochTook = datetime.now() - tEpochStart
        trainingTook = datetime.now() - tTrainingStart

        logging.info('#' * 50)
        logging.info('Epoch %2d summary:', epoch)
        logging.info(' took %s (%s)', str(epochTook).split(".")[0], str(trainingTook).split(".")[0])
        logging.info(' fitness:')
        logging.info('  max:  %d' % maxFitness)
        logging.info('  mean: %d' % np.mean(population.fitnesses))
        logging.info(' best weights:')
        bestModelIdx = np.argmax(population.fitnesses)
        bestModelWeights = population.models[bestModelIdx].output.weight.data.tolist()[0]
        for i, weight in enumerate(bestModelWeights):
            logging.info('  %s: %f' % (METRICS_NAMES[i], np.round(weight, 2)))
        logging.info('#' * 50)

        # make checkpoint
        with open('checkpoints/%s.pkl' % epoch, 'wb') as f:
            pickle.dump(population, f)

        if maxFitness >= maxFitnessEver:
            maxFitnessEver = maxFitness
            # save best model
            torch.save(population.models[bestModelIdx].state_dict(), 'models/%d' % maxFitness)

        epoch += 1

    pool.join()
    pool.close()

if __name__ == '__main__':
    runAsUnixPgroup(train)