from random import randint, sample, choice, random
from typing import List, Tuple


def single_point_xo(parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Implementation of single point crossover.

    Args:
        parent1 (List[float]): First parent for crossover.
        parent2 (List[float]): Second parent for crossover.

    Returns:
        Tuple[List[float], List[float]]: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1) - 1)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    return offspring1, offspring2


def multi_point_xo(parent1: List[float], parent2: List[float], n: int = 2) -> Tuple[List[float], List[float]]:
    """
    Implementation of multipoint crossover.

    Args:
        parent1 (List[float]): First parent for crossover.
        parent2 (List[float]): Second parent for crossover.
        n (int): Number of crossover points.

    Returns:
        Tuple[List[float], List[float]]: Two offspring, resulting from the crossover.
    """
    offspring1 = parent1[:]
    offspring2 = parent2[:]
    length = len(parent1)
    xo_points = sorted(sample(range(1, length), n))
    for i in range(0, len(xo_points), 2):
        start = xo_points[i]
        end = xo_points[i + 1] if i + 1 < len(xo_points) else length
        offspring1[start:end], offspring2[start:end] = offspring2[start:end], offspring1[start:end]
    return offspring1, offspring2


def uniform_xo(parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Implementation of uniform crossover.

    Args:
        parent1 (List[float]): First parent for crossover.
        parent2 (List[float]): Second parent for crossover.

    Returns:
        Tuple[List[float], List[float]]: Two offspring, resulting from the crossover.
    """
    offspring1, offspring2 = parent1[:], parent2[:]
    for i in range(len(parent1)):
        offspring1[i] = choice([parent1[i], parent2[i]])
        offspring2[i] = parent1[i] if offspring1[i] == parent2[i] else parent2[i]
    return offspring1, offspring2


def pmx(parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
    """Partially Mapped Crossover (PMX) implementation."""
    point1 = randint(1, len(parent1) - 1)
    point2 = randint(point1 + 1, len(parent1))
    offspring1 = parent1[:]
    offspring2 = parent2[:]
    for i in range(point1, point2):
        offspring1[i], offspring2[i] = offspring2[i], offspring1[i]
    return offspring1, offspring2


def arithmetic_xo(parent1: List[float], parent2: List[float], alpha: float = 0.8) -> Tuple[List[float], List[float]]:
    """
    Perform arithmetic crossover (blend crossover) on two parents.

    Args:
        parent1 (List[float]): First parent chromosome.
        parent2 (List[float]): Second parent chromosome.
        alpha (float): Weighting factor for the crossover. Default is 0.5.

    Returns:
        Tuple[List[float], List[float]]: Two offspring after crossover.
    """
    offspring1 = parent1[:]
    offspring2 = parent2[:]
    for i in range(len(parent1)):
        value1 = alpha * parent1[i] + (1 - alpha) * parent2[i]
        value2 = alpha * parent2[i] + (1 - alpha) * parent1[i]
        offspring1[i] = value1
        offspring2[i] = value2
    return offspring1, offspring2


def sbx(parent1: List[float], parent2: List[float], eta_c: float = 10, p_c: float = 0.9,
        bounds: Tuple[float, float] = (0, 2.99)) -> Tuple[List[float], List[float]]:
    """
    Simulated Binary Crossover (SBX) for real-valued representations.

    Args:
        parent1 (List[float]): First parent solution.
        parent2 (List[float]): Second parent solution.
        eta_c (float): Distribution index, controls the shape of the probability distribution function.
        p_c (float): Crossover probability, determines the likelihood that crossover will be applied.
        bounds (Tuple[float, float]): Tuple of lower and upper bounds for each variable.

    Returns:
        Tuple[List[float], List[float]]: Two offspring solutions.
    """
    offspring1 = []
    offspring2 = []

    for x1, x2 in zip(parent1, parent2):
        if random() <= p_c:
            if random() <= 0.5:
                beta = (2 * random()) ** (1.0 / (eta_c + 1))
            else:
                beta = (1.0 / (2 * (1 - random()))) ** (1.0 / (eta_c + 1))

            y1 = 0.5 * (((1 + beta) * x1) + ((1 - beta) * x2))
            y2 = 0.5 * (((1 - beta) * x1) + ((1 + beta) * x2))

            y1 = max(bounds[0], min(y1, bounds[1]))
            y2 = max(bounds[0], min(y2, bounds[1]))

            offspring1.append(y1)
            offspring2.append(y2)
        else:
            offspring1.append(x1)
            offspring2.append(x2)

    return offspring1, offspring2
