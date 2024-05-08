# CIFO_PROJECT

In this project, we are solving an Asymmetric Capacitated Vehicle Routing Problem (ACVRP) using genetic algorithms. We have implemented several variations of solutions by modifying the selection process, mutation, and crossover techniques.

## Problem Description
The Asymmetric Capacitated Vehicle Routing Problem (ACVRP) involves optimizing the routing of vehicles to deliver goods from a depot to various customers while minimizing costs or maximizing efficiency. Key constraints include vehicle capacity limits and asymmetrical travel costs between locations.

## Genetic Algorithms
Genetic algorithms are a type of optimization algorithm inspired by the process of natural selection and genetics. They use a population of candidate solutions (individuals) that evolve over generations through selection, crossover (recombination), and mutation.

## Representation
In our problem, we are dealing with three trucks and 71 nodes to visit. Our representation involves a 70-element array (as the depot node does not need to be included in the solution representation), where each element is assigned a value between 0 and 2.99. The values between 0 and 1 correspond to truck 1, values between 1 and 2 correspond to truck 2, and values between 2 and 3 correspond to truck 3.

To determine the sequence of nodes for each truck's path, we sort the nodes in ascending order based on their assigned values in the array. This sorting process allows us to understand the sequence of nodes that each truck will visit.

To enhance clarity regarding this approach, please refer to the accompanying GIF demonstration (using an example with 8 nodes). 

![Representation Animation](Images/gif_2.gif)

## Genetic Algorithm Schema for Each Solution

### **Solution 1**
### Selection Method: Roulette Wheel Selection (TODO)
### Crossover Method: Single-Point Crossover (TODO)
### Mutation Method: Inversion Mutation (With a slight variation)

For the mutation method in Solution 1, we utilize a variation of the inversion mutation technique. Instead of inverting a contiguous subset of the individual's representation, we select two random values (genes) within the individual and swap their positions. This process is repeated `n` times, where `n` is a parameter of the mutation function.

This mutation approach introduces diversity into the population by randomly altering pairs of genes within individuals, potentially exploring new regions of the solution space.

![Mutation Animation](Images/gif_1.gif)

### Solution 2
- **TO DO**
### Solution 3
- **TO DO**
### Solution 4
- **TO DO**

