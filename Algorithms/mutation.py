from random import randint, choice, shuffle, uniform


def swap_mutator(individual, n_loops=1):
    """
    Mutates an individual by swapping elements in the chromosome.

        This function randomly selects pairs of indices within the chromosome and swaps
        the elements at those indices. The number of swaps performed is determined by
        the `n_loops` parameter.

        Args:
            individual (list): The individual (chromosome) to be mutated.
            n_loops (int, optional): Number of swap operations to perform. Default is 1.

        Returns:
            list: The mutated individual after swapping elements.
    """
    for i in range(n_loops):
        length = len(individual) - 1

        index_1 = randint(0, length)
        index_2 = choice([randint(index_1, length), randint(0, index_1)])

        individual[index_1], individual[index_2] = individual[index_2], individual[index_1]

    return individual


def scramble_mutator(individual, max_subset_size=5):
    """
    Mutates an individual by scrambling a subset of its elements.

    This function randomly selects a subset of elements from the chromosome
    `individual` starting from a random index. It then shuffles the selected
    subset in place, resulting in a scrambled sequence of elements within the
    chromosome.

    Args:
        individual (list): The individual (chromosome) to be mutated.
        max_subset_size (int, optional): Maximum size of the subset to be scrambled.
            Default is 5.

    Returns:
        list: The mutated individual after scrambling a subset of elements.
    """
    length = len(individual) - 1

    index = randint(0, length)
    subset_end = min(index + max_subset_size, length + 1)
    subset = individual[index:subset_end]

    shuffle(subset)

    individual[index:subset_end] = subset

    return individual


def random_reset_mutator(individual, n_loops=1):
    """
    Mutates an individual by randomly resetting specific elements.

    This function randomly selects elements within the chromosome `individual`
    and assigns them new random values within a specified range [0, 2.999999].
    The number of elements to reset is determined by the `n_loops` parameter.

    Args:
        individual (list): The individual (chromosome) to be mutated.
        n_loops (int, optional): Number of elements to reset (mutate). Default is 1.

    Returns:
        list: The mutated individual after randomly resetting specified elements.
    """
    length = len(individual) - 1

    for _ in range(n_loops):
        index = randint(0, length)

        individual[index] = uniform(0, 2.999999)

    return individual
