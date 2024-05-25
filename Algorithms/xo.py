from random import randint, sample, choice, random


def single_point_xo(parent1, parent2):
    """
    Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1) - 1)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    return offspring1, offspring2


def multi_point_xo(parent1, parent2, n=2):
    """
    Implementation of multipoint crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.
        n (int): Number of crossover points.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = parent1[:]
    offspring2 = parent2[:]

    length = len(parent1)

    xo_points = sorted(sample(range(1, length), n))

    for i in range(0, len(xo_points), 2):
        start = xo_points[i]
        if i + 1 < len(xo_points):
            end = xo_points[i + 1]
        else:
            end = length

        offspring1[start:end], offspring2[start:end] = offspring2[start:end], offspring1[start:end]

    return offspring1, offspring2


def uniform_xo(parent1, parent2):
    """
    Implementation of uniform crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    offspring1, offspring2 = parent1[:], parent2[:]

    for i in range(len(parent1)):
        offspring1[i] = choice([parent1[i], parent2[i]])
        offspring2[i] = parent1[i] if offspring1[i] == parent2[i] else parent2[i]

    return offspring1, offspring2


def pmx(parent1, parent2):
    # Step 1: Select crossover points
    point1 = randint(1, len(parent1) - 1)
    point2 = randint(point1 + 1, len(parent1))

    # Step 2: Create offspring
    offspring1 = parent1[:]
    offspring2 = parent2[:]

    # Step 3: Exchange segments
    for i in range(point1, point2):
        # Swap segments corresponding to the same truck assignment
        offspring1[i], offspring2[i] = offspring2[i], offspring1[i]


    return offspring1, offspring2