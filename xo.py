from random import randint


def single_point_xo(parent1, parent2):
    """Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    #print(f"parent1:{parent1}")
    #print(f"parent2:{parent2}")
    xo_point = randint(1, len(parent1)-1)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    #print(f"offspring1: {offspring1}")
    #print(f"offspring2: {offspring2}")
    return offspring1, offspring2