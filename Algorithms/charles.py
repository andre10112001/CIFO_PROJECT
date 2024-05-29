from operator import attrgetter
from random import choice, random, uniform
from copy import copy
from typing import List, Any, Tuple, Callable


class Individual:
    def __init__(self, representation: List[Any] = None, size: int = None, valid_set: List[Any] = None,
                 repetition: bool = True) -> None:
        if representation is None:
            if repetition:
                self.representation = [choice(valid_set) for _ in range(size)]
            else:
                self.representation = [uniform(valid_set[0], valid_set[1]) for _ in range(size)]
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_fitness(self) -> float:
        raise Exception("You need to monkey patch the fitness function.")

    def get_neighbours(self) -> List['Individual']:
        raise Exception("You need to monkey patch the neighbourhood function.")

    def __len__(self) -> int:
        return len(self.representation)

    def __getitem__(self, position: int) -> Any:
        return self.representation[position]

    def __setitem__(self, position: int, value: Any) -> None:
        self.representation[position] = value

    def __repr__(self) -> str:
        return f" Fitness: {self.fitness}"


class Population:
    def __init__(self, size: int, optim: str, **kwargs: Any) -> None:
        self.size = size
        self.optim = optim
        self.individuals = [
            Individual(size=kwargs["sol_size"], valid_set=kwargs["valid_set"], repetition=kwargs["repetition"]) for _ in
            range(size)]

    def evolve(self, gens: int, xo_prob: float, mut_prob: float, select: Callable, xo: Callable, mutate: Callable,
               elitism: bool) -> List[Tuple[int, float]]:
        history = []
        for i in range(gens):
            new_pop = []
            if elitism:
                elite = copy(
                    max(self.individuals, key=attrgetter('fitness')) if self.optim == "max" else min(self.individuals,
                                                                                                     key=attrgetter(
                                                                                                         'fitness')))
                new_pop.append(elite)
            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                offspring1, offspring2 = (
                    xo(parent1, parent2) if random() < xo_prob else (parent1.representation, parent2.representation))
                offspring1 = mutate(offspring1) if random() < mut_prob else offspring1
                offspring2 = mutate(offspring2) if random() < mut_prob else offspring2
                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))
            self.individuals = new_pop
            if self.optim == "min":
                history.append((i + 1, self.get_best_individual().fitness))
        return history

    def __len__(self) -> int:
        return len(self.individuals)

    def __getitem__(self, position: int) -> Individual:
        return self.individuals[position]

    def get_best_individual(self) -> Individual:
        return min(self.individuals, key=attrgetter('fitness')) if self.optim == "min" else max(self.individuals,
                                                                                                key=attrgetter(
                                                                                                    'fitness'))
