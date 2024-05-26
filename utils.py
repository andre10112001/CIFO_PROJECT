from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity
from Algorithms.charles import Population
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


distance_matrix = np_edge_weight_section.copy()
demand_list = np_demand_section.copy()


def get_path(self):
    # Initialize paths
    path_1, path_2, path_3 = [dimension-1], [dimension-1], [dimension-1]

    # Create a list of tuples (index, value) from the representation
    indexed_values = list(enumerate(self.representation))

    # Sort the list of tuples based on the values (second element of each tuple)
    indexed_values.sort(key=lambda x: x[1])

    # Append indices to respective paths based on sorted values
    for index, value in indexed_values:
        if value < 1:
            path_1.append(index)
        elif value < 2:
            path_2.append(index)
        else:
            path_3.append(index)
        # Append depot node index at the end of each path
    path_1.append(dimension-1)
    path_2.append(dimension-1)
    path_3.append(dimension-1)

    return path_1, path_2, path_3

def get_load(path_1, path_2, path_3):
    load_1 = 0
    load_2 = 0
    load_3 = 0
    for node in path_1:
        for element in demand_list:
            if element[0] == (node + 1) :
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


def see_paths(values):
    path_1 = []
    path_2 = []
    path_3 = []

    for index, value in enumerate(values):
        if value < 1:
            path_1.append(index)
        elif 1 <= value < 2:
            path_2.append(index)
        elif 2 <= value <= 3:
            path_3.append(index)
    
    path_1.sort(key=lambda idx: values[idx])
    path_2.sort(key=lambda idx: values[idx])
    path_3.sort(key=lambda idx: values[idx])

    path_1.insert(0, dimension-1)
    path_2.insert(0, dimension-1)
    path_3.insert(0, dimension-1)

    path_1.append(dimension-1)
    path_2.append(dimension-1)
    path_3.append(dimension-1)
    
    return path_1, path_2, path_3

def run_n_times(pop_size, gens, xo_prob, mut_prob,
                select, xo, mutate, n = 30):
    # Define a list to store the results
    results = []

    # Loop through the evolutionary process 'n' times
    for _ in tqdm(range(n)):
        # Initialize and evolve the population
        P = Population(pop_size, "min", sol_size=dimension - 1, valid_set=[0, 2.999999], repetition=False)
        history = P.evolve(gens=gens, xo_prob=xo_prob, mut_prob=mut_prob, select=select,
                xo=xo, mutate=mutate, elitism=True)

        # Get the best individual after evolution
        min_individual = P.get_best_individual()

        # Extract representation, fitness, and paths/load information
        representation = min_individual.representation
        fitness = min_individual.fitness

        path_1, path_2, path_3 = see_paths(representation)
        load_1, load_2, load_3 = get_load(path_1, path_2, path_3)

        # Store the results in a tuple and append to the results list
        result = (representation, fitness, load_1, load_2, load_3, history)
        results.append(result)
    return results


import matplotlib.pyplot as plt
import numpy as np

def plot_evolution_history(results):
    plt.figure(figsize=(10, 6))
    
    all_generations = []
    all_best_fitness_values = []

    # Collect all best fitness values from all runs
    for i, result in enumerate(results):
        generations = []
        best_fitness_values = []

        # Extract generation number and best fitness value for each iteration in this result
        history = result[5]  # History is the 6th element in the result tuple
        for gen, fitness in history:
            generations.append(gen)
            best_fitness_values.append(fitness)
        
        all_generations.append(generations)
        all_best_fitness_values.append(best_fitness_values)

        # Plot individual run histories with different colors and transparency
        color = plt.cm.viridis(i / len(results))  # Use colormap to assign colors
        alpha = 0.2  # Set transparency level
        plt.plot(generations, best_fitness_values, label=f'Run {i + 1}', color=color, alpha=alpha, linewidth=1)

    # Compute mean best fitness values across all runs at each generation
    max_generations = max(len(generations) for generations in all_generations)
    mean_fitness_values = np.zeros(max_generations)
    num_runs = len(all_best_fitness_values)

    for i in range(max_generations):
        sum_fitness = sum(all_best_fitness_values[j][i] for j in range(num_runs) if i < len(all_best_fitness_values[j]))
        mean_fitness_values[i] = sum_fitness / num_runs if num_runs > 0 else 0

    # Plot the mean fitness line
    plt.plot(range(1, max_generations + 1), mean_fitness_values, label='Mean Fitness', color='red', linewidth=2)

    plt.title('Evolution of Best Fitness Over Generations (Multiple Runs)')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True)
    plt.show()

def plot_fitness_boxplots(*results):
    # Prepare data for boxplots
    data = []

    for i, result in enumerate(results):
        solution_fitness = [element[1] for element in result]
        data.append(solution_fitness)

    # Create labels based on solution names
    labels = [f'Solution {i + 1}' for i in range(len(results))]

    # Create boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels, patch_artist=True, notch=True, vert=False)

    # Customize plot appearance
    plt.title('Fitness Distribution Comparison between Solutions')
    plt.xlabel('Fitness')
    plt.ylabel('Solution')
    plt.grid(True)
    plt.show()




