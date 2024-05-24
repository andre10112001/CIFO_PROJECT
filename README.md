# CIFO_PROJECT

In this project, we are solving an Asymmetric Capacitated Vehicle Routing Problem (ACVRP) using genetic algorithms. We have implemented several variations of solutions by modifying the selection process, mutation, and crossover techniques.

***

## Problem Description
The Asymmetric Capacitated Vehicle Routing Problem (ACVRP) involves optimizing the routing of vehicles to deliver goods from a depot to various customers while minimizing costs or maximizing efficiency. Key constraints include vehicle capacity limits and asymmetrical travel costs between locations.

***

## Genetic Algorithms
Genetic algorithms are a type of optimization algorithm inspired by the process of natural selection and genetics. They use a population of candidate solutions (individuals) that evolve over generations through selection, crossover (recombination), and mutation.

***

## Representation
In our problem, we are dealing with three trucks and 71 nodes to visit. Our representation involves a 70-element array (as the depot node does not need to be included in the solution representation), where each element is assigned a value between 0 and 2.99. The values between 0 and 1 correspond to truck 1, values between 1 and 2 correspond to truck 2, and values between 2 and 3 correspond to truck 3.

To determine the sequence of nodes for each truck's path, we sort the nodes in ascending order based on their assigned values in the array. This sorting process allows us to understand the sequence of nodes that each truck will visit.

To enhance clarity regarding this approach, please refer to the accompanying GIF demonstration (using an example with 9 nodes where the 9th node is the depot node). 

![Representation Animation](Images/gif_2.gif)

The representation concept used in this project was inspired by the research presented in the article titled "A Genetic Algorithm for the Asymmetric Capacitated Vehicle Routing Problem" (available at this link).

***

## Fitness

The fitness of our solution is determined by the total distance traveled by the three trucks from the moment they depart the depot until they complete their routes. It's crucial to mention that if any truck exceeds its capacity limit, we apply a penalty to the solution. This penalty involves multiplying the fitness value by 10,000.

In summary, our fitness metric evaluates the combined travel distance of all trucks, with a penalty imposed if any truck exceeds its capacity threshold. This approach ensures that our solution adheres to both distance efficiency and capacity constraints.

***

## Genetic Algorithm Schema for Each Solution

### **Solution 1** 
(gens=1000, xo_prob=0.9, mut_prob=0.15, select=fps,xo=single_point_xo, mutate=variable_inversion_operator, elitism=True)
- **Selection Method:** Roulette Wheel Selection with Fitness Inversion
  - Higher fitness (lower total distance) results in a lower value (after inversion), increasing the probability of selection.
  
- **Crossover Method:** Single-Point Crossover
  - Basic crossover technique involving splitting two parent solutions at a random point and swapping sections to create new offspring.
  
- **Mutation Method:** Inversion Mutation with Random Gene Swaps
  - Instead of inverting contiguous subsets, two random genes within an individual are swapped `n` times to introduce diversity.

![Mutation Animation](Images/gif_1.gif)

### Solution 2
- **TO DO**
### Solution 3
- **TO DO**
### Solution 4
- **TO DO**

## Selection Operators

### fps (Fitness Proportionate)
TODO

### ts (Tourname Selection)
TODO

## Crossover operations

### single_point_xo (Single Point Crossover)
Single point crossover is a genetic algorithm technique where two parent solutions exchange segments at a randomly chosen point to create two new offspring, promoting genetic diversity. This method helps explore new solutions by combining different parts of the parents' genetic information.

The following gif demonstrates a cycle of single point crossover:
![single_point_xo Animation](Images/spxo.gif)

