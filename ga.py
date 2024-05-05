from Algorithms.selection import fps
from Algorithms.xo import single_point_xo
from Algorithms.mutation import variable_inversion_operator
from Algorithms.charles import Population, Individual
from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity
from utils import get_load, get_path, see_paths

distance_matrix = np_edge_weight_section.copy()
demand_list = np_demand_section.copy()


def get_fitness(self):
    path_1, path_2, path_3 = get_path(self)
    total_distance = 0
    for path in [path_1, path_2, path_3]:
        for index in range(len(path)-1):
            total_distance += distance_matrix[path[index]][path[index+1]]
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

P = Population(10, "min", sol_size=dimension-1, valid_set=[0, 2.999999], repetition=False)

P.evolve(gens=100, xo_prob=0.9, mut_prob=0.15, select=fps,
         xo=single_point_xo, mutate=variable_inversion_operator, elitism=True)

min_individual = P.get_best_individual()

print(min_individual.fitness)

path_1, path_2, path_3 = see_paths(min_individual.representation)

print("Path 1:", path_1)
print("Path 2:", path_2)
print("Path 3:", path_3)