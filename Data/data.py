"""
ACVRP Data Processing Script

This script reads and processes data from a specific file format used for the Asymmetric Capacitated Vehicle Routing Problem (ACVRP).

The file format includes the following sections:
- Head Section: Contains metadata about the problem instance, such as name, comment, type, dimension, etc.
- Edge Weight Section: Specifies the distance matrix between locations.
- Demand Section: Specifies the demand (load) for each location.
- Depot Section: Specifies the depot location.

The processed data is converted into numpy arrays for further analysis and modeling.
"""

# Imports
import numpy as np


# Read content inside the file
with open('Data/A071-03f.dat', 'r') as file:
    data_content = file.read()

# Split the content into lines
lines = data_content.splitlines()

# Getting the head part of the file
head = lines[:9]
name = head[0].split(" : ")[1]
comment = head[1].split(" : ")[1]
problem_type = head[2].split(" : ")[1]
dimension = int(head[3].split(" : ")[1])
edge_weight_type = head[4].split(" : ")[1]
edge_weight_format = head[5].split(" : ")[1]
display_data_type = head[6].split(" : ")[1]
capacity = int(head[7].split(" : ")[1])
vehicles = int(head[8].split(" : ")[1])

# Getting the matrix in the EDGE_WEIGHT_SECTION
edge_weight_section = lines[10:(71+10)]
matrix = []

for line in edge_weight_section:
    values_list = line.split()
    for index, value in enumerate(values_list):
        values_list[index] = int(value)
    matrix.append(values_list)

np_edge_weight_section = np.array(matrix)


# Getting the matrix in the DEMAND_SECTION
demand_section = lines[71+10+1:71+10+71]

demand_list = []
for line in demand_section:
    values_list = line.split()
    for index, value in enumerate(values_list):
        values_list[index] = int(value)
    demand_list.append(values_list)

np_demand_section = np.array(demand_list)

# Getting the depot_section
depot_section = lines[-2]