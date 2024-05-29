from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity
from Algorithms.charles import Population
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Callable

distance_matrix = np_edge_weight_section.copy()
demand_list = np_demand_section.copy()


def get_path(individual: 'Individual') -> Tuple[List[int], List[int], List[int]]:
    """
    Generate paths for the individual based on their representation.

    Args:
        individual (Individual): The individual whose paths are to be generated.

    Returns:
        Tuple[List[int], List[int], List[int]]: Three lists representing paths.
    """
    path_1, path_2, path_3 = [dimension - 1], [dimension - 1], [dimension - 1]
    indexed_values = list(enumerate(individual.representation))
    indexed_values.sort(key=lambda x: x[1])
    for index, value in indexed_values:
        if value < 1:
            path_1.append(index)
        elif value < 2:
            path_2.append(index)
        else:
            path_3.append(index)
    path_1.append(dimension - 1)
    path_2.append(dimension - 1)
    path_3.append(dimension - 1)
    return path_1, path_2, path_3


def get_load(path_1: List[int], path_2: List[int], path_3: List[int]) -> Tuple[int, int, int]:
    """
    Calculate the load for each path based on the demand list.

    Args:
        path_1 (List[int]): The first path.
        path_2 (List[int]): The second path.
        path_3 (List[int]): The third path.

    Returns:
        Tuple[int, int, int]: Loads for each path.
    """
    load_1, load_2, load_3 = 0, 0, 0
    for node in path_1:
        for element in demand_list:
            if element[0] == (node + 1):
                load_1 += element[1]
    for node in path_2:
        for element in demand_list:
            if element[0] == (node + 1):
                load_2 += element[1]
    for node in path_3:
        for element in demand_list:
            if element[0] == (node + 1):
                load_3 += element[1]
    return load_1, load_2, load_3


def see_paths(values: List[float]) -> Tuple[List[int], List[int], List[int]]:
    """
    Generate and sort paths based on the values in the individual's representation.

    Args:
        values (List[float]): The values from the individual's representation.

    Returns:
        Tuple[List[int], List[int], List[int]]: Three lists representing paths.
    """
    path_1, path_2, path_3 = [], [], []
    for index, value in enumerate(values):
        if value < 1:
            path_1.append(index)
        elif 1 <= value < 2:
            path_2.append(index)
        else:
            path_3.append(index)
    path_1.sort(key=lambda idx: values[idx])
    path_2.sort(key=lambda idx: values[idx])
    path_3.sort(key=lambda idx: values[idx])
    path_1.insert(0, dimension - 1)
    path_2.insert(0, dimension - 1)
    path_3.insert(0, dimension - 1)
    path_1.append(dimension - 1)
    path_2.append(dimension - 1)
    path_3.append(dimension - 1)
    return path_1, path_2, path_3


def run_n_times(
        pop_size: int, gens: int, xo_prob: float, mut_prob: float, select: Callable, xo: Callable, mutate: Callable,
        n: int = 30
) -> List[Tuple[List[float], float, int, int, int, List[Tuple[int, float]]]]:
    """
    Run the evolutionary algorithm multiple times and collect results.

    Args:
        pop_size (int): Population size.
        gens (int): Number of generations.
        xo_prob (float): Crossover probability.
        mut_prob (float): Mutation probability.
        select (Callable): Selection function.
        xo (Callable): Crossover function.
        mutate (Callable): Mutation function.
        n (int, optional): Number of runs. Default is 30.

    Returns:
        List[Tuple[List[float], float, int, int, int, List[Tuple[int, float]]]]: List of results from each run.
    """
    results = []
    for _ in tqdm(range(n)):
        P = Population(pop_size, "min", sol_size=dimension - 1, valid_set=[0, 2.999999], repetition=False)
        history = P.evolve(gens=gens, xo_prob=xo_prob, mut_prob=mut_prob, select=select, xo=xo, mutate=mutate,
                           elitism=True)
        min_individual = P.get_best_individual()
        representation = min_individual.representation
        fitness = min_individual.fitness
        path_1, path_2, path_3 = see_paths(representation)
        load_1, load_2, load_3 = get_load(path_1, path_2, path_3)
        result = (representation, fitness, load_1, load_2, load_3, history)
        results.append(result)
    return results


def plot_evolution_history(
        results: List[Tuple[List[float], float, int, int, int, List[Tuple[int, float]]]], title: str
) -> None:
    """
    Plot the evolution history of fitness values over generations.

    Args:
        results (List[Tuple[List[float], float, int, int, int, List[Tuple[int, float]]]]): Results from multiple runs.
        title (str): Title for the plot.
    """
    plt.figure(figsize=(10, 6))
    all_generations, all_best_fitness_values = [], []
    for i, result in enumerate(results):
        generations, best_fitness_values = [], []
        history = result[5]
        for gen, fitness in history:
            generations.append(gen)
            best_fitness_values.append(fitness)
        all_generations.append(generations)
        all_best_fitness_values.append(best_fitness_values)
        color = plt.cm.viridis(i / len(results))
        alpha = 0.2
        plt.plot(generations, best_fitness_values, label=f'Run {i + 1}', color=color, alpha=alpha, linewidth=1)
    max_generations = max(len(generations) for generations in all_generations)
    mean_fitness_values = np.zeros(max_generations)
    num_runs = len(all_best_fitness_values)
    for i in range(max_generations):
        sum_fitness = sum(all_best_fitness_values[j][i] for j in range(num_runs) if i < len(all_best_fitness_values[j]))
        mean_fitness_values[i] = sum_fitness / num_runs if num_runs > 0 else 0
    plt.plot(range(1, max_generations + 1), mean_fitness_values, label='Mean Fitness', color='red', linewidth=2)
    plt.title('Evolution of Best Fitness Over Generations (Multiple Runs)' + title)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True)
    plt.show()


def plot_fitness_boxplots(*results: List[Tuple[List[float], float, int, int, int, List[Tuple[int, float]]]]) -> None:
    """
    Plot boxplots comparing fitness distributions of different solutions.

    Args:
        *results (List[Tuple[List[float], float, int, int, int, List[Tuple[int, float]]]]): Results from different solutions.
    """
    data = []
    for result in results:
        solution_fitness = [element[1] for element in result]
        data.append(solution_fitness)
    labels = [f'Solution {i + 1}' for i in range(len(results))]
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels, patch_artist=True, notch=True, vert=False)
    plt.title('Fitness Distribution Comparison between Solutions')
    plt.xlabel('Fitness')
    plt.ylabel('Solution')
    plt.grid(True)
    plt.show()
