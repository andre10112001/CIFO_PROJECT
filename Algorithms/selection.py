from random import uniform, sample, random
from typing import Any, Callable, List


def fps(population: 'Population') -> 'Individual':
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual based on fitness proportionate selection.
    """
    optimization_map = {
        "max": lambda ind: ind.fitness,
        "min": lambda ind: 1 / ind.fitness
    }

    if population.optim not in optimization_map:
        raise ValueError("Invalid optimization type specified (must be 'max' or 'min').")

    total_fitness = sum(optimization_map[population.optim](individual) for individual in population)
    r = uniform(0, total_fitness)
    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += optimization_map[population.optim](individual)
        if cumulative_fitness > r:
            return individual


def ts(population: 'Population', n_participants: int = 2) -> 'Individual':
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        n_participants (int): Number of individuals participating in the tournament.

    Returns:
        Individual: Selected individual.
    """
    optimization_map = {
        "max": lambda ind: ind.fitness,
        "min": lambda ind: 1 / ind.fitness
    }

    if population.optim not in optimization_map:
        raise ValueError("Invalid optimization type specified (must be 'max' or 'min').")

    individuals = sample(list(population), n_participants)
    fitness_values = list(map(optimization_map[population.optim], individuals))
    winner = individuals[fitness_values.index(max(fitness_values))]
    return winner


def get_default_temperature(population: 'Population') -> float:
    """Calculate a default temperature based on the range of fitness values in the population."""
    fitness_values = [individual.fitness for individual in population]
    fitness_min = min(fitness_values)
    fitness_max = max(fitness_values)
    temperature = (fitness_max - fitness_min) * 0.1
    return max(0.01, temperature)


def boltzmann_selection(population: 'Population', temperature: float = None) -> 'Individual':
    """Boltzmann's selection implementation.

    Args:
        population (Population): The population we want to select from.
        temperature (float, optional): Temperature parameter for controlling selection pressure. Defaults to None.

    Returns:
        Individual: Selected individual based on Boltzmann selection.
    """
    optimization_map = {
        "max": lambda ind: ind.fitness,
        "min": lambda ind: -ind.fitness
    }

    if population.optim not in optimization_map:
        raise ValueError("Invalid optimization type specified (must be 'max' or 'min').")

    if temperature is None:
        temperature = get_default_temperature(population)

    boltzmann_weights = [optimization_map[population.optim](individual) / temperature for individual in population]
    max_weight = max(boltzmann_weights)
    boltzmann_weights = [weight - max_weight for weight in boltzmann_weights]
    total_weight = sum(boltzmann_weights)
    r = random() * total_weight
    cumulative_weight = 0
    for idx, individual in enumerate(population):
        cumulative_weight += boltzmann_weights[idx]
        if cumulative_weight > r:
            return individual
    return population[-1]


def rank_based_selection(population: 'Population', selection_pressure: float = 1.5) -> 'Individual':
    """Rank-based selection implementation (Linear Ranking Selection).

    Args:
        population (Population): The population from which to select.
        selection_pressure (float, optional): Selection pressure parameter. Defaults to 1.5.

    Returns:
        Individual: Selected individual based on Rank-Based Selection.
    """
    if selection_pressure <= 0:
        raise ValueError("Selection pressure must be greater than zero.")

    population.individuals.sort(key=lambda x: x.fitness)
    ranks = list(range(1, len(population) + 1))
    selection_probabilities = [((2 - selection_pressure) / len(population)) +
                               (2 * rank * (selection_pressure - 1) / (len(population) * (len(population) - 1)))
                               for rank in ranks]

    r = uniform(0, sum(selection_probabilities))
    cumulative_probability = 0
    for idx, individual in enumerate(population):
        cumulative_probability += selection_probabilities[idx]
        if cumulative_probability > r:
            return individual
    return population[-1]
