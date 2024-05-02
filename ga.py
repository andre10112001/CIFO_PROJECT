from Algorithms.selection import fps
from Algorithms.xo import single_point_xo
from Algorithms.mutation import mutation_operator
from Algorithms.charles import Population, Individual
from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity
from random import uniform, random
from operator import attrgetter
import copy

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
            if element[0] == node:
                load_1 += element[1]
    for node in path_2:
        for element in demand_list:
            if element[0] == node:
                load_2 += element[1]
    for node in path_3:
        for element in demand_list:
            if element[0] == node:
                load_3 += element[1]
    return load_1, load_2, load_3


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

gens = 100
for i in range(gens):
    new_pop = []
    while len(new_pop) < len(P):
        # selection
        parent1, parent2 = fps(P), fps(P)
        # xo with 0.5 prob
        if random() < 0.5:
            offspring1, offspring2 = single_point_xo(parent1, parent2)
        # replication
        else:
            offspring1, offspring2 = parent1.representation, parent2.representation
        # mutation with prob 0.5
        if random() < 0.5:
            offspring1 = mutation_operator(offspring1)
        if random() < 0.5:
            offspring2 = mutation_operator(offspring2)

        new_pop.append(Individual(representation=offspring1))
        new_pop.append(Individual(representation=offspring2))

    P.individuals = new_pop
    print(f"Best individual of gen #{i+1}: {max(P, key = attrgetter('fitness'))}")
    if (i + 1) == gens:
        P.print_solutions()