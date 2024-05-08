from Data.data import dimension, np_edge_weight_section, np_demand_section, capacity

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


