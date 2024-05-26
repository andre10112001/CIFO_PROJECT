from Algorithms.selection import fps, ts
from Algorithms.xo import single_point_xo, multi_point_xo, pmx, uniform_xo, arithmetic_xo, sbx
from Algorithms.mutation import swap_mutator, scramble_mutator, random_reset_mutator, custom_mutator
from Algorithms.charles import Population, Individual
from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity
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
        'pop_size': [10],
        'gens': [100],
        'xo_prob': [0.9],
        'mut_prob': [0.15],
        'select': [fps, ts],
        'xo': [single_point_xo, multi_point_xo, pmx, uniform_xo, arithmetic_xo, sbx],
        'mutate': [swap_mutator, scramble_mutator, random_reset_mutator, custom_mutator],
        'n_runs': 30  # Add the number of runs
    }

    # Instantiate GridSearch with the parameter grid and the external run_n_times function
    grid = GridSearch(run_n_times, **param_grid)

    # Run the grid search
    grid.run()

    # Sort the combinations based on the average fitness
    grid.sort_results_by_fitness()

    print()
    for result in grid.results:
        print("Params:", result['params'])
        #print("Results", result["results"])
        print("Average Fitness:", result['average_fitness'])

    # Extract the best solution from the result
    best_result = min(grid.results, key=lambda x: x['average_fitness'])

    # Extract representation from the best solution
    best_solution = best_result['results'][0]
    representation = best_solution[0]

    # Calculate paths and loads from the representation
    path_1, path_2, path_3 = see_paths(representation)
    load_1, load_2, load_3 = get_load(path_1, path_2, path_3)

    # Print paths and loads for each vehicle in the best solution
    print("Paths and Loads for Solution with Minimum Fitness:")
    print("Path 1:", path_1, "Load:", load_1)
    print("Path 2:", path_2, "Load:", load_2)
    print("Path 3:", path_3, "Load:", load_3)


    # OLD VERSION
    """
    ##################################################
    # Solution 1
    ##################################################

    # Run this solutions n times
    print("Running: SOLUTION 1")

    # results = ([run_1, run_2, ..., run_n])
    # run_i = [(best_representaion_i, best_fitness_i, load_i_1, load_i_2, load_i_3, history_i)]
    # history_i = [(gen_1, fitness_1), (gen_2, fitness_2), ..., (gen_l, fitness_l)]
    results_1 = run_n_times(pop_size=10, gens=100, xo_prob=0.9, mut_prob=0.15, select=fps, 
                        xo=single_point_xo, mutate=swap_mutator, n=30)

    ##################################################
    # Solution 2
    ##################################################
    print("Running: SOLUTION 2")

    results_2 = run_n_times(pop_size=10, gens=100, xo_prob=0.9, mut_prob=0.15, select=ts,
                        xo=single_point_xo, mutate=scramble_mutator, n=30)


    ##################################################
    # Solution 3
    ##################################################
    print("Running: SOLUTION 3")

    results_3 = run_n_times(pop_size=10, gens=100, xo_prob=0.9, mut_prob=0.15, select=fps, 
                        xo=single_point_xo, mutate=random_reset_mutator, n=30)

    ##################################################
    # PLOTS
    ##################################################

    # Plotting the history of each run of solution 1
    plot_evolution_history(results_1)

    # Plotting the history of each run of solution 2
    plot_evolution_history(results_2)

    # Plotting the history of each run of solution 3
    plot_evolution_history(results_3)

    # Boxplot for each solution
    plot_fitness_boxplots(results_1 , results_2, results_3)"""