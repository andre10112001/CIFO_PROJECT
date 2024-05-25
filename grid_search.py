import itertools
import statistics
from tqdm import tqdm
import time

class GridSearch:
    def __init__(self, run_func, **param_grid):
        self.run_func = run_func
        self.param_grid = param_grid
        self.n_runs = param_grid.pop('n_runs', 30)
        self.results = []
        self.times = []

    def get_total_combinations(self):
        # Calculate the total number of parameter combinations
        total_combinations = 1
        for values in self.param_grid.values():
            total_combinations *= len(values)
        return total_combinations

    def run(self):
        param_names = list(self.param_grid.keys())
        param_combinations = list(itertools.product(*self.param_grid.values()))
        total_combinations = len(param_combinations)

        print(f"Total combinations: {total_combinations}")

        for i, combination in enumerate(tqdm(param_combinations, desc="Grid Search Progress")):
            start_time = time.time()

            params = dict(zip(param_names, combination))
            readable_params = {k: (v.__name__ if callable(v) else v) for k, v in params.items()}
            print("______________________________________________________________________________")
            print(f"Running run_n_times with parameters: {readable_params}")
            results = self.run_func(n=self.n_runs, **params)
            # Calculate average fitness for this combination
            fitness_values = [result[1] for result in results]
            mean_fitness = statistics.mean(fitness_values)
            print()
            print(f"Average fitness for combination {i+1}: {mean_fitness}")

            self.results.append({
                'params': readable_params,
                'results': results,
                'average_fitness': mean_fitness
            })

            

            elapsed_time = time.time() - start_time
            self.times.append(elapsed_time)

            # Calculate dynamic average time and estimate remaining time
            avg_time_per_combination = sum(self.times) / len(self.times)
            remaining_combinations = total_combinations - (i + 1)
            estimated_remaining_time = remaining_combinations * avg_time_per_combination
            estimated_remaining_time_minutes = estimated_remaining_time / 60  # convert seconds to minutes

            tqdm.write(f"Estimated remaining time: {estimated_remaining_time_minutes:.2f} minutes")

        total_time_taken = sum(self.times)
        total_time_taken_minutes = total_time_taken / 60  # convert seconds to minutes
        print(f"Total time taken: {total_time_taken_minutes:.2f} minutes")

        return self.results
    
    def sort_results_by_fitness(self):
        self.results.sort(key=lambda x: x['average_fitness'], reverse=True)
