# CIFO_PROJECT

In this project, we are solving an Asymmetric Capacitated Vehicle Routing Problem (ACVRP) using genetic algorithms. We have implemented several variations of solutions by modifying the selection process, mutation, and crossover techniques.

## Problem Description
The Asymmetric Capacitated Vehicle Routing Problem (ACVRP) involves optimizing the routing of vehicles to deliver goods from a depot to various customers while minimizing costs or maximizing efficiency. Key constraints include vehicle capacity limits and asymmetrical travel costs between locations.

## Genetic Algorithms
Genetic algorithms are a type of optimization algorithm inspired by the process of natural selection and genetics. They use a population of candidate solutions (individuals) that evolve over generations through selection, crossover (recombination), and mutation.

## Representation
In our problem, we are dealing with three trucks and 71 nodes to visit. Our representation involves a 70-element array (as the depot node does not need to be included in the solution representation), where each element is assigned a value between 0 and 2.99. The values between 0 and 1 correspond to truck 1, values between 1 and 2 correspond to truck 2, and values between 2 and 3 correspond to truck 3.

To determine the sequence of nodes for each truck's path, we sort the nodes in ascending order based on their assigned values in the array. This sorting process allows us to understand the sequence of nodes that each truck will visit.

To enhance clarity regarding this approach, please refer to the accompanying GIF demonstration (using an example with 9 nodes where the 9th node is the depot node). 

![Representation Animation](Images/gif_2.gif)

## Fitness

The fitness of our solution is determined by the total distance traveled by the three trucks from the moment they depart the depot until they complete their routes. It's crucial to mention that if any truck exceeds its capacity limit, we apply a penalty to the solution. This penalty involves multiplying the fitness value by 10,000.

In summary, our fitness metric evaluates the combined travel distance of all trucks, with a penalty imposed if any truck exceeds its capacity threshold. This approach ensures that our solution adheres to both distance efficiency and capacity constraints.

## Genetic Algorithm Schema for Each Solution

### **Solution 1**
### Selection Method: Roulette Wheel Selection
In our case, the selection process for crossover operates similarly to the maximization scenario, where higher fitness values correspond to a higher probability of selection. However, since our problem involves minimization (aiming to minimize the fitness function), we invert the fitness values. This means that we use the inverted fitness values for the roulette wheel selection mechanism.

To clarify, by inverting the fitness values, we essentially turn higher fitness (lower cost or distance in our case) into lower values and vice versa. This inverted fitness value is then utilized in the roulette wheel selection to guide the probability of selecting individuals for crossover, prioritizing solutions with lower fitness (cost) values. This adjustment ensures that our selection process aligns with the objective of minimizing the total distance traveled by the trucks.

### Crossover Method: Single-Point Crossover
The crossover operator used in this solution is a basic single-point crossover method. This technique involves taking two parent solutions, dividing them into sections at a random point, and then swapping these sections between the parents to create new offspring. It's important to note that this crossover method is implemented without any additional adjustments or modifications.
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

