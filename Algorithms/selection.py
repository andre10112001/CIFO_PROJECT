from random import uniform


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    if population.optim == "max":
        total_fitness = sum([i.fitness for i in population])
        r = uniform(0, total_fitness)
        position = 0
        for individual in population:
            position += individual.fitness
            if position > r:
                return individual
    elif population.optim == "min":
        # Minimization case (fitness-proportional selection)
        # Calculate total fitness
        total_fitness = sum([1 / i.fitness for i in population])  # Inverse fitness for minimization

        # Generate a random number between 0 and the total fitness
        r = uniform(0, total_fitness)

        # Perform roulette wheel selection
        cumulative_inverse_fitness = 0
        for individual in population:
            cumulative_inverse_fitness += 1 / individual.fitness  # Use inverse fitness for selection
            if cumulative_inverse_fitness > r:
                return individual
    else:
        raise Exception(f"Optimization not specified (max/min)")