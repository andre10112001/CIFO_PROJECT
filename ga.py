from Algorithms.selection import fps, ts, boltzmann_selection, rank_based_selection
from Algorithms.xo import single_point_xo, multi_point_xo, pmx, uniform_xo, arithmetic_xo, sbx
from Algorithms.mutation import swap_mutator, scramble_mutator, random_reset_mutator, custom_mutator
from Algorithms.charles import Individual
from Data.data import np_edge_weight_section, np_demand_section, capacity
from utils import get_load, get_path, see_paths, run_n_times, plot_evolution_history, plot_fitness_boxplots
from grid_search import GridSearch

distance_matrix = np_edge_weight_section.copy()
demand_list = np_demand_section.copy()


def get_fitness(self):
    path_1, path_2, path_3 = get_path(self)
    total_distance = 0
    for path in [path_1, path_2, path_3]:
        for index in range(len(path) - 1):
            total_distance += distance_matrix[path[index]][path[index + 1]]
    fitness = total_distance
    load_1, load_2, load_3 = get_load(path_1, path_2, path_3)
    if (load_1 > capacity) or (load_2 > capacity) or (load_3 > capacity):
        fitness = fitness * 10000
    return fitness


def get_neighbours(self):
    pass


if __name__ == "__main__":
    # Monkey patching
    Individual.get_fitness = get_fitness
    Individual.get_neighbours = get_neighbours

    # Define the parameter grid
    param_grid = {
        'pop_size': [100],
        'gens': [500],
        'xo_prob': [0.9],
        'mut_prob': [0.15],
        'select': [fps, ts],
        'xo': [multi_point_xo, uniform_xo],
        'mutate': [scramble_mutator, custom_mutator],
        'n_runs': 30  # Add the number of runs
    }

    # Instantiate GridSearch with the parameter grid and the external run_n_times function
    grid = GridSearch(run_n_times, **param_grid)

    # Run the grid search
    grid.run()

    # Sort the combinations based on the average fitness
    grid.sort_results_by_fitness()

    top_5_results = grid.results[-5:]

    results_list = []
    # Plot the history of the top 5 combinatinos
    i = 1
    for result in top_5_results:
        plot_evolution_history(result["results"], title=f"Solution {i}")
        results_list.append(result["results"])
        i += 1

    # Plot the results for the top 5 combinations
    plot_fitness_boxplots(*results_list)

    # Print the soluctions and the corresponding parameters
    i = 1
    for combination in top_5_results:
        print(f"Solution {i}: Parameters {combination['params']}, Average Fitness {combination['average_fitness']}")
        i += 1

    # Extract the best ever solution obtained by the top 5 combinations
    min_fitness = 1_000_000
    for dict in top_5_results:
        results = dict["results"]
        for element in results:
            best_representation = element[0]
            best_fitness = element[1]
            load_1 = element[2]
            load_2 = element[3]
            load_3 = element[4]
            history = element[5]
            if best_fitness < min_fitness:
                min_fitness = best_fitness
                best_result_ever = element

    print(f"Best representation ever: {best_result_ever[0]}")
    print(f"Best fitness ever: {best_result_ever[1]}")
    print(f"Best load_1 ever: {best_result_ever[2]}")
    print(f"Best load_2 ever: {best_result_ever[3]}")
    print(f"Best load_3 ever: {best_result_ever[4]}")

    path_1, path_2, path_3 = see_paths(best_result_ever[0])
    print("Path 1:", path_1)
    print("Path 2:", path_2)
    print("Path 3:", path_3)
