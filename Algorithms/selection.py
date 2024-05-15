from random import uniform, choice, sample


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual based on fitness proportionate selection.
    """
    # Define a dictionary to map optimization types to fitness calculation functions
    optimization_map = {
        "max": lambda ind: ind.fitness,
        "min": lambda ind: 1 / ind.fitness
    }

    # Validate optimization type
    if population.optim not in optimization_map:
        raise ValueError("Invalid optimization type specified (must be 'max' or 'min').")

    # Calculate total fitness based on the selected optimization type
    total_fitness = sum(optimization_map[population.optim](individual) for individual in population)

    # Perform fitness proportionate selection
    r = uniform(0, total_fitness)
    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += optimization_map[population.optim](individual)
        if cumulative_fitness > r:
            return individual


def ts(population, n_participants=2):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        n_participants (int): Number of individuals participating in the tournament.

    Returns:
        Individual: selected individual.
    """
    optimization_map = {
        "max": lambda ind: ind.fitness,
        "min": lambda ind: 1 / ind.fitness
    }

    # Validate optimization type
    if population.optim not in optimization_map:
        raise ValueError("Invalid optimization type specified (must be 'max' or 'min').")

    # Tournament participants
    individuals = sample(list(population), n_participants)
    fitness_values = list(map(optimization_map[population.optim], individuals))

    # Select the individual with the better fitness based on the optimization type
    winner = individuals[fitness_values.index(max(fitness_values))]

    return winner
