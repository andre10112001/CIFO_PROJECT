from random import randint, sample, choice, random
import random


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

def arithmetic_xo(parent1, parent2, alpha=0.8):
    """
    Perform arithmetic crossover (blend crossover) on two parents.

    Parameters:
    - parent1 (list): First parent chromosome.
    - parent2 (list): Second parent chromosome.
    - alpha (float): Weighting factor for the crossover. Default is 0.5.

    Returns:
    - offspring1 (list): First offspring after crossover.
    - offspring2 (list): Second offspring after crossover.
    """
    # Create copies of parents
    offspring1 = parent1[:]
    offspring2 = parent2[:]

    # Perform crossover for each gene
    for i in range(len(parent1)):
        # Calculate new values for offspring
        value1 = alpha * parent1[i] + (1 - alpha) * parent2[i]
        value2 = alpha * parent2[i] + (1 - alpha) * parent1[i]

        # Assign new values to offspring
        offspring1[i] = value1
        offspring2[i] = value2

    return offspring1, offspring2


def sbx(parent1, parent2, eta_c=10, p_c=0.9, bounds=(0, 2.99)):
    """
    Simulated Binary Crossover (SBX) for real-valued representations.

    Args:
    - parent1 (list): First parent solution.
    - parent2 (list): Second parent solution.
    - eta_c (float): Distribution index, controls the shape of the probability distribution function.
    - p_c (float): Crossover probability, determines the likelihood that crossover will be applied.
    - bounds (tuple): Tuple of lower and upper bounds for each variable.

    Returns:
    - offspring1 (list): First offspring solution.
    - offspring2 (list): Second offspring solution.
    """
    offspring1 = []
    offspring2 = []
    
    for x1, x2 in zip(parent1, parent2):
        if random.random() <= p_c:
            if random.random() <= 0.5:
                # Exploring away from parents
                beta = (2 * random.random()) ** (1.0 / (eta_c + 1))
            else:
                # Exploring towards parents
                beta = (1.0 / (2 * (1 - random.random()))) ** (1.0 / (eta_c + 1))
            
            # Calculate offspring values
            y1 = 0.5 * (((1 + beta) * x1) + ((1 - beta) * x2))
            y2 = 0.5 * (((1 - beta) * x1) + ((1 + beta) * x2))
            
            # Ensure offspring are within bounds
            y1 = max(bounds[0], min(y1, bounds[1]))
            y2 = max(bounds[0], min(y2, bounds[1]))
            
            # Append offspring to the list
            offspring1.append(y1)
            offspring2.append(y2)
        else:
            # If no crossover, offspring are copies of parents
            offspring1.append(x1)
            offspring2.append(x2)
    
    return offspring1, offspring2
