from random import randint, choice, shuffle, uniform, random
from typing import List


def swap_mutator(individual: List[float], n_loops: int = 1) -> List[float]:
    """
    Mutates an individual by swapping elements in the chromosome.

    Args:
        individual (List[float]): The individual (chromosome) to be mutated.
        n_loops (int, optional): Number of swap operations to perform. Default is 1.

    Returns:
        List[float]: The mutated individual after swapping elements.
    """
    for _ in range(n_loops):
        length = len(individual) - 1
        index_1 = randint(0, length)
        index_2 = choice([randint(index_1, length), randint(0, index_1)])
        individual[index_1], individual[index_2] = individual[index_2], individual[index_1]
    return individual


def scramble_mutator(individual: List[float], max_subset_size: int = 5) -> List[float]:
    """
    Mutates an individual by scrambling a subset of its elements.

    Args:
        individual (List[float]): The individual (chromosome) to be mutated.
        max_subset_size (int, optional): Maximum size of the subset to be scrambled. Default is 5.

    Returns:
        List[float]: The mutated individual after scrambling a subset of elements.
    """
    length = len(individual) - 1
    index = randint(0, length)
    subset_end = min(index + max_subset_size, length + 1)
    subset = individual[index:subset_end]
    shuffle(subset)
    individual[index:subset_end] = subset
    return individual


def random_reset_mutator(individual: List[float], n_loops: int = 1) -> List[float]:
    """
    Mutates an individual by randomly resetting specific elements.

    Args:
        individual (List[float]): The individual (chromosome) to be mutated.
        n_loops (int, optional): Number of elements to reset (mutate). Default is 1.

    Returns:
        List[float]: The mutated individual after randomly resetting specified elements.
    """
    length = len(individual) - 1
    for _ in range(n_loops):
        index = randint(0, length)
        individual[index] = uniform(0, 2.999999)
    return individual


def custom_mutator(individual: List[float], mutation_rate: float = 0.5) -> List[float]:
    num_customers = len(individual)
    mutated_child = individual.copy()
    for i in range(1, num_customers):
        if random() < mutation_rate:
            if i < num_customers - 1:
                mutated_child[i], mutated_child[i + 1] = mutated_child[i + 1], mutated_child[i]
            if i == num_customers:
                mutated_child[num_customers], mutated_child[1] = mutated_child[1], mutated_child[num_customers]
    return mutated_child
