from operator import attrgetter
from random import choice, random, uniform
from copy import copy


class Individual:
    # we always initialize
    def __init__(self, representation=None, size=None, valid_set=None, repetition=True):

        if representation is None:
            if repetition:
                # individual will be chosen from the valid_set with a specific size
                self.representation = [choice(valid_set) for i in range(size)]
            else:
                self.representation = [uniform(valid_set[0], valid_set[1]) for _ in range(size)]

        # if we pass an argument like Individual(my_path)
        else:
            self.representation = representation

        # fitness will be assigned to the individual
        self.fitness = self.get_fitness()

    # methods for the class
    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness function.")

    def get_neighbours(self):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f" Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):

        # population size
        self.size = size

        # defining the optimization problem as a minimization or maximization problem
        self.optim = optim

        self.individuals = []

        # appending the population with individuals
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    valid_set=kwargs["valid_set"],
                    repetition=kwargs["repetition"]
                )
            )

    def evolve(self, gens, xo_prob, mut_prob, select, xo, mutate, elitism):
        # gens = 100
        history = []
        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = copy(max(self.individuals, key=attrgetter('fitness')))
                elif self.optim == "min":
                    elite = copy(min(self.individuals, key=attrgetter('fitness')))

                new_pop.append(elite)

            while len(new_pop) < self.size:
                # selection
                parent1, parent2 = select(self), select(self)
                # xo with prob
                if random() < xo_prob:
                    offspring1, offspring2 = xo(parent1, parent2)
                # replication
                else:
                    offspring1, offspring2 = parent1.representation, parent2.representation
                # mutation with prob
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            self.individuals = new_pop
            if self.optim == "max":
                #print(f"Best individual of gen #{i + 1}: {max(self, key=attrgetter('fitness'))}")
                pass
            elif self.optim == "min":
                #print(f"Best individual of gen #{i + 1}: {min(self, key=attrgetter('fitness'))}")
                history.append((i+1, self.get_best_individual().fitness))
                pass
        return history

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def get_best_individual(self):
        if self.optim == "min":
            min = 1000000000
            for individual in self.individuals:
                fitness = individual.fitness
                if fitness < min:
                    min_individual = individual
                    min = fitness
            return min_individual
        elif self.optim == "max":
            max = 0
            for individual in self.individuals:
                fitness = individual.fitness
                if fitness > max:
                    max_individual = individual
                    max = fitness
            return max_individual
