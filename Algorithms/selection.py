from random import uniform, choice, sample, random


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

def get_default_temperature(population):
    """Calculate a default temperature based on the range of fitness values in the population."""
    fitness_values = [individual.fitness for individual in population]
    fitness_min = min(fitness_values)
    fitness_max = max(fitness_values)
    temperature = (fitness_max - fitness_min) * 0.1  # 10% of fitness range
    return max(0.01, temperature)  # Ensure minimum temperature of 0.01


def boltzmann_selection(population, temperature=None):
    """Boltzmann selection implementation.

    Args:
        population (Population): The population we want to select from.
        temperature (float, optional): Temperature parameter for controlling selection pressure.
            If None, a default value will be calculated based on the range of fitness values.
            Defaults to None.

    Returns:
        Individual: Selected individual based on Boltzmann selection.
    """
    # Define a dictionary to map optimization types to fitness calculation functions
    optimization_map = {
        "max": lambda ind: ind.fitness,
        "min": lambda ind: -ind.fitness  # Negative fitness for minimization
    }

    # Validate optimization type
    if population.optim not in optimization_map:
        raise ValueError("Invalid optimization type specified (must be 'max' or 'min').")

    # Calculate Boltzmann weights
    if temperature is None:
        temperature = get_default_temperature(population)

    boltzmann_weights = []
    for individual in population:
        fitness_val = optimization_map[population.optim](individual)
        if fitness_val == 0:
            boltzmann_weights.append(0.0)
        else:
            boltzmann_weights.append(fitness_val / temperature)

    # Normalize weights to avoid numerical issues
    max_weight = max(boltzmann_weights)
    if max_weight > 0:
        boltzmann_weights = [weight - max_weight for weight in boltzmann_weights]

    # Calculate sum of Boltzmann weights
    total_weight = sum(boltzmann_weights)

    # Perform Boltzmann selection
    r = random() * total_weight
    cumulative_weight = 0
    for idx, individual in enumerate(population):
        cumulative_weight += boltzmann_weights[idx]
        if cumulative_weight > r:
            return individual
    # Fallback to return the last individual (in case of numerical issues)
    return population[-1]

def rank_based_selection(population, selection_pressure=1.5):
    """Rank-based selection implementation (Linear Ranking Selection).

    Args:
        population (Population): The population from which to select.
        selection_pressure (float, optional): Selection pressure parameter. Higher values increase
            the selection probability difference between the best and worst individuals.
            Defaults to 1.5.

    Returns:
        Individual: Selected individual based on Rank-Based Selection.
    """
    # Ensure selection pressure is greater than 0
    if selection_pressure <= 0:
        raise ValueError("Selection pressure must be greater than zero.")
    
    # Sort population based on fitness
    population.individuals.sort(key=lambda x: x.fitness)
    
    # Assign ranks
    ranks = list(range(1, len(population) + 1))
    
    # Calculate selection probabilities based on rank
    selection_probabilities = [((2 - selection_pressure) / len(population)) + 
                               (2 * rank * (selection_pressure - 1) / (len(population) * (len(population) - 1))) 
                               for rank in ranks]
    
    # Perform rank-based selection
    r = uniform(0, sum(selection_probabilities))
    cumulative_probability = 0
    for idx, individual in enumerate(population):
        cumulative_probability += selection_probabilities[idx]
        if cumulative_probability > r:
            return individual
    
    # Fallback to return the last individual (in case of numerical issues)
    return population[-1]

