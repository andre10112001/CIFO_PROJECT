from Algorithms.selection import fps
from Algorithms.xo import single_point_xo
from Algorithms.mutation import swap_mutator
from Algorithms.charles import Population, Individual
from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity
from utils import get_load, get_path, see_paths

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


# Monkey patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

# Solution 1

""" P = Population(10, "min", sol_size=dimension-1, valid_set=[0, 2.999999], repetition=False)

P.evolve(gens=100, xo_prob=0.9, mut_prob=0.15, select=fps,
         xo=single_point_xo, mutate=swap_mutator, elitism=True)

min_individual = P.get_best_individual()

print(min_individual.fitness)

path_1, path_2, path_3 = see_paths(min_individual.representation)
load_1, load_2, load_3 = get_load(path_1, path_2, path_3)

print("Load 1:", load_1)
print("Path 1:", path_1)
print("Load 1:", load_2)
print("Path 2:", path_2)
print("Load 1:", load_3)
print("Path 3:", path_3) """

# Define a list to store the results
results = []

# Define the number of iterations (n)
n = 10  # Change this to the desired number of iterations

# Loop through the evolutionary process 'n' times
for _ in range(n):
    # Initialize and evolve the population
    P = Population(10, "min", sol_size=dimension - 1, valid_set=[0, 2.999999], repetition=False)
    P.evolve(gens=100, xo_prob=0.9, mut_prob=0.15, select=fps,
             xo=single_point_xo, mutate=swap_mutator, elitism=True)

    # Get the best individual after evolution
    min_individual = P.get_best_individual()

    # Extract representation, fitness, and paths/load information
    representation = min_individual.representation
    fitness = min_individual.fitness

    path_1, path_2, path_3 = see_paths(representation)
    load_1, load_2, load_3 = get_load(path_1, path_2, path_3)

    # Store the results in a tuple and append to the results list
    result = (representation, fitness, load_1, load_2, load_3)
    results.append(result)

# Print all results collected
for i, result in enumerate(results):
    print(f"Iteration {i + 1}:")
    # print("Representation:", result[0])
    print("Fitness:", result[1])
    print("Load 1:", result[2])
    print("Load 2:", result[3])
    print("Load 3:", result[4])
    print()

# Solution 2
# CODE HERE
