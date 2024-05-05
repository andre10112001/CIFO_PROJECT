from random import randint

def variable_inversion_operator(individual, n_loops = 1):
    for i in range(n_loops):
        index_1 = randint(0, len(individual) - 1)
        index_2 = randint(0, len(individual) - 1)
        while index_1 == index_2:
            index_2 = randint(0, len(individual) - 1)
        individual[index_1], individual[index_2] = individual[index_2], individual[index_1]
    return individual