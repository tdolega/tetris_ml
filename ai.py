from globalSetting import *
from analyze import N_INPUT_SIZE
import math

class Network(torch.nn.Module):
    def __init__(self, output_w=None):
        super(Network, self).__init__()
        if output_w:
            logging.critical('`ouput_w` defined, but shouldn\'t. Bailing out')
            exit(2)

        self.middle = torch.nn.Linear(N_INPUT_SIZE, N_MIDDLE_SIZE, bias=False).to(N_DEVICE)
        self.output = torch.nn.Linear(N_MIDDLE_SIZE, N_OUTPUT_SIZE, bias=False).to(N_DEVICE)
        self.middle.weight.requires_grad_(False)
        self.output.weight.requires_grad_(False)
        torch.nn.init.uniform_(self.middle.weight, a=N_WEIGHTS_INIT_MIN, b=N_WEIGHTS_INIT_MAX)
        torch.nn.init.uniform_(self.output.weight, a=N_WEIGHTS_INIT_MIN, b=N_WEIGHTS_INIT_MAX)

    def activate(self, values):
        with torch.no_grad():
            values = torch.from_numpy(values).float().to(N_DEVICE)
            middle = self.middle(values)
            out = self.output(middle)
            return out

class Population:
    def __init__(self, size, lastPopulation=None):
        self.size = size
        self.fitnesses = np.zeros(self.size)
        if lastPopulation is None:
            self.models = [Network() for _ in range(size)]
        else:
            self.lastModels = lastPopulation.models
            self.lastFitnesses = lastPopulation.fitnesses
            self.models = []
            self.crossover()
            self.mutate()

    def crossover(self):
        logging.info('Crossover')
        fitnessSum = np.sum(self.lastFitnesses)
        probabilities = [self.lastFitnesses[i] / fitnessSum for i in range(self.size)]

        sortedProbabilities = np.argsort(probabilities)[::-1]
        boundary = math.floor(self.size * P_ELITISM)
        for i in range(boundary):
            modelNext = self.lastModels[sortedProbabilities[i]]
            self.models.append(modelNext)
        for i in range(boundary, self.size):
            randA, randB = np.random.choice(self.size, size=2, p=probabilities, replace=False)
            modelA, modelB = self.lastModels[randA], self.lastModels[randB]
            modelNext = Network()

            for inputIdx in range(N_INPUT_SIZE):
                randomModel = np.random.choice([modelA, modelB])
                modelNext.middle.weight.data[0][inputIdx] = randomModel.middle.weight.data[0][inputIdx]
            for inputIdx in range(N_MIDDLE_SIZE):
                randomModel = np.random.choice([modelA, modelB])
                modelNext.output.weight.data[0][inputIdx] = randomModel.output.weight.data[0][inputIdx]

            self.models.append(modelNext)

    def _mutateSingle(self, weight):
        if np.random.random() > P_MUTATION:
            return

        with torch.no_grad():
            noise = torch.randn(1).mul_(P_WEIGHTS_MUTATE_POWER).to(N_DEVICE)
            weight.add_(noise[0])

    def mutate(self):
        logging.info('Mutating')
        for model in self.models:
            for i in range(N_INPUT_SIZE):
                self._mutateSingle(model.middle.weight.data[0][i])
            for i in range(N_MIDDLE_SIZE):
                self._mutateSingle(model.output.weight.data[0][i])
