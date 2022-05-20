from globalSetting import *
from analyze import N_INPUT_SIZE

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
        if lastPopulation is None:
            self.models = [Network() for _ in range(size)]
        else:
            self.lastModels = lastPopulation.models
            self.lastFitnesses = lastPopulation.fitnesses
            self.models = []
            self.crossover()
            self.mutate()
        self.fitnesses = np.zeros(self.size)

    def crossover(self):
        logging.info('Crossover')
        sum_fitnesses = np.sum(self.lastFitnesses)
        probs = [self.lastFitnesses[i] / sum_fitnesses for i in range(self.size)]

        # Sorting descending NNs according to their fitnesses
        sort_indices = np.argsort(probs)[::-1]
        for i in range(self.size):
            if i < self.size * P_ELITISM:
                # Add the top performing childs
                model_c = self.lastModels[sort_indices[i]]
            else:
                a, b = np.random.choice(self.size, size=2, p=probs, replace=False)

                model_a, model_b = self.lastModels[a], self.lastModels[b]
                model_c = Network()

                for inputIdx in range(N_INPUT_SIZE):
                    randomModel = np.random.choice([model_a, model_b])
                    model_c.middle.weight.data[0][inputIdx] = randomModel.middle.weight.data[0][inputIdx]
                for inputIdx in range(N_MIDDLE_SIZE):
                    randomModel = np.random.choice([model_a, model_b])
                    model_c.output.weight.data[0][inputIdx] = randomModel.output.weight.data[0][inputIdx]

            self.models.append(model_c)

    def mutate(self):
        logging.info('Mutating')
        for model in self.models:
            # Mutating weights by adding Gaussian noises
            for i in range(N_INPUT_SIZE):
                if np.random.random() > P_MUTATION:
                    continue

                with torch.no_grad():
                    noise = torch.randn(1).mul_(P_WEIGHTS_MUTATE_POWER).to(N_DEVICE)
                    model.middle.weight.data[0][i].add_(noise[0])

            for i in range(N_MIDDLE_SIZE):
                if np.random.random() > P_MUTATION:
                    continue

                with torch.no_grad():
                    noise = torch.randn(1).mul_(P_WEIGHTS_MUTATE_POWER).to(N_DEVICE)
                    model.output.weight.data[0][i].add_(noise[0])
