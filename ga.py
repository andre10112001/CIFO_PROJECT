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

"""
Solution 1: Parameters {'pop_size': 10, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'ts', 
'xo': 'uniform_xo', 'mutate': 'custom_mutator'}, Average Fitness 5112

Solution 2: Parameters {'pop_size': 10, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'fps', 
'xo': 'multi_point_xo', 'mutate': 'custom_mutator'}, Average Fitness 5014

Solution 3: Parameters {'pop_size': 10, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'fps', 
'xo': 'uniform_xo', 'mutate': 'scramble_mutator'}, Average Fitness 4777

Solution 4: Parameters {'pop_size': 10, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'ts', 
'xo': 'uniform_xo', 'mutate': 'scramble_mutator'}, Average Fitness 4652

Solution 5: Parameters {'pop_size': 10, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'fps', 
'xo': 'uniform_xo', 'mutate': 'custom_mutator'}, Average Fitness 4501

Best representation ever: [1.5604348577135183, 1.9426594525742733, 1.9426594525742733, 1.9426594525742733, 
1.9426594525742733, 1.9426594525742733, 2.783167325590106, 2.783167325590106, 2.8561022316661893, 2.783167325590106, 
2.783167325590106, 2.783167325590106, 2.1808947787104938, 2.1808947787104938, 2.1808947787104938, 2.1808947787104938, 
2.1808947787104938, 1.4621338604973357, 1.3130105266083167, 1.3130105266083167, 1.3130105266083167, 
1.3130105266083167, 1.3130105266083167, 1.3130105266083167, 1.7377930150863488, 1.7377930150863488, 
2.774373736835426, 1.7377930150863488, 1.7377930150863488, 0.17906939466017277, 0.2733614146920273, 
0.00013989941867852186, 0.3256750533747002, 0.3256750533747002, 0.4000855168078291, 0.3256750533747002, 
0.4000855168078291, 0.4000855168078291, 0.4000855168078291, 0.4000855168078291, 2.3295692870886318, 
2.3030792817844294, 2.7336790935267037, 2.647570415329866, 0.7752821653865456, 0.7752821653865456, 
0.7772191473011201, 0.8658025346319859, 0.8658025346319859, 0.7772191473011201, 0.9404498217590195, 0.57623317473867, 
0.9404498217590195, 0.9404498217590195, 0.57623317473867, 0.674015280399356, 1.086770991702906, 1.086770991702906, 
1.086770991702906, 1.086770991702906, 1.3396353682049287, 1.086770991702906, 2.497588431658443, 2.3079025152599115, 
2.7764489779242547, 1.9245203725955509, 2.7764489779242547, 1.086770991702906, 2.3079025152599115, 
2.3079025152599115]

Best fitness ever: 3789 
Best load_1 ever: 758 
Best load_2 ever: 925 
Best load_3 ever: 724 
Path 1: [70, 31, 29, 30, 32, 33, 35, 34, 36, 37, 38, 39, 51, 54, 55, 44, 45, 46, 49, 47, 48, 50, 52, 53, 70] 
Path 2: [70, 56, 57, 58, 59, 61, 67, 18, 19, 20, 21, 22, 23, 60, 17, 0, 24, 25, 27, 28, 65, 1, 2, 3, 4, 5, 70] 
Path 3: [70, 12, 13, 14, 15, 16, 41, 63, 68, 69, 40, 62, 43, 42, 26, 64, 66, 6, 7, 9, 10, 11, 8, 70]

########################################################################################################################
#######################         increasing population size of the 5 solutions:       ###################################
########################################################################################################################

Solution 1: Parameters {'pop_size': 100, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'fps', 
'xo': 'multi_point_xo', 'mutate': 'scramble_mutator'}, Average Fitness 4285

Solution 2: Parameters {'pop_size': 100, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'fps', 
'xo': 'uniform_xo', 'mutate': 'scramble_mutator'}, Average Fitness 4187

Solution 3: Parameters {'pop_size': 100, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'ts', 
'xo': 'multi_point_xo', 'mutate': 'scramble_mutator'}, Average Fitness 3843

Solution 4: Parameters {'pop_size': 100, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'ts', 
'xo': 'uniform_xo', 'mutate': 'custom_mutator'}, Average Fitness 3787

Solution 5: Parameters {'pop_size': 100, 'gens': 500, 'xo_prob': 0.9, 'mut_prob': 0.15, 'select': 'ts', 
'xo': 'uniform_xo', 'mutate': 'scramble_mutator'}, Average Fitness 3431

Best representation ever: [0.977630419149109, 0.977630419149109, 0.977630419149109, 1.00675438065097, 
1.00675438065097, 1.00675438065097, 0.04083325429388835, 0.04083325429388835, 0.8597341812252587, 0.8597341812252587, 
0.8597341812252587, 0.8597341812252587, 0.36392890880831663, 0.20879197772276792, 0.20879197772276792, 
0.36392890880831663, 0.36392890880831663, 0.8089757928736642, 0.36392890880831663, 0.36392890880831663, 
1.6057103151082313, 1.6057103151082313, 1.6057103151082313, 1.5807258898167238, 0.48179529400836946, 
0.0029881501291359807, 0.5818211447343558, 0.03888499064966231, 0.4768053865284962, 2.6963716061337846, 
2.6963716061337846, 2.6963716061337846, 2.2658903486293207, 2.7311068659959323, 2.2658903486293207, 
2.7311068659959323, 2.3439134551824345, 2.7311068659959323, 1.4850136435493289, 1.4763022135333683, 
2.466655944214933, 2.428333109891813, 1.3004043029802186, 2.2566147122352125, 1.160299786973269, 1.1872177949794844, 
1.3451465212551161, 2.9280400767466297, 2.9502051999517858, 1.3451465212551161, 1.3451465212551161, 
2.9502051999517858, 2.124757937960456, 2.609493810778227, 2.989890020748347, 2.989890020748347, 2.989890020748347, 
0.937329577949209, 2.0906854184009376, 0.8687693930905355, 1.5363608662651185, 0.8687693930905355, 
2.5944510494681925, 2.9008293715751483, 1.7000056915932513, 0.7956149656698156, 1.97402140224253, 1.320613520972937, 
1.3579919449305202, 2.3443528961162556]

Best fitness ever: 3052
Best load_1 ever: 908
Best load_2 ever: 711
Best load_3 ever: 788
Path 1: [70, 25, 27, 6, 7, 13, 14, 12, 15, 16, 18, 19, 28, 24, 26, 65, 17, 8, 9, 10, 11, 59, 61, 57, 0, 1, 2, 70]
Path 2: [70, 3, 4, 5, 44, 45, 42, 67, 46, 49, 50, 68, 39, 38, 60, 23, 20, 21, 22, 64, 66, 70]
Path 3: [70, 58, 52, 43, 32, 34, 36, 69, 41, 40, 62, 53, 29, 30, 31, 33, 35, 37, 63, 47, 48, 51, 54, 55, 56, 70]
"""