from data import np_edge_weight_section, np_demand_section, capacity, vehicles

# print(np_edge_weight_section)

import numpy as np
from random import uniform

depot_index = 70
def get_path(representation):
    # Initialize paths
    path_1, path_2, path_3 = [depot_index], [depot_index], [depot_index]

    # Create a list of tuples (index, value) from the representation
    indexed_values = list(enumerate(representation))

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
    path_1.append(depot_index)
    path_2.append(depot_index)
    path_3.append(depot_index)
    return path_1, path_2, path_3

# Test example data
example_data = [0.1, 0.333, 1.1, 2.9, 1.2, 0.11]
print(get_path(example_data))
