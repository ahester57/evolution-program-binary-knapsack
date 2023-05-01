# ahester57

import asyncio
import copy
import numpy as np
import sys
import time

from collections import deque
from typing import Callable

import binary_knapsack.test_functions.binary_knapsack as binary_knapsack
from binary_knapsack.chromosome import Chromosome
from binary_knapsack.population import Population
from binary_knapsack.selection_mechanism.mechanism import SelectionMechanism
from binary_knapsack.selection_mechanism.proportional import Proportional


class GA:
    """
    A class for a genetic algorithm (GA).

    Attributes:
        dims (int, optional): Dimensions of chromosome vector. Represents the number of items to choose from.
        max_item_weight (float, optional): Upper bound for weight.
        profit_correlation_factor (float, optional): Constant used in generation of weakly correlated data sets.
        capacity (float, optional): Capacity of the knapsack.
        pop_size (int): Population size. Defaults to 30.
        p_c (float): Probability of crossover. In range [0, 1].
        p_m (float): Probability of mutation. In range [0, 1].
        t_max (int): Maximum iterations/generations.
        random (np.random.Generator): The random number generator.
        population (Population): Collection of current generation's individual chromosomes.
        fitness_function (Callable): The "fitness function" or "objective function."
        maximize (bool): (False)[minimize]; (True)[maximize]. Default True.
        Select_Mechanism (SelectionMechanism): The selected selection mechanism. Default Proportional.
        selection_parameters (dict): The selected selection mechanism parameters.
    """
    def __init__(
        self,
        dims:int=20,
        max_item_weight:float=10.0,
        profit_correlation_factor:float=5.0,
        capacity:float=40.0,
        pop_size:int=300,
        p_c:float=0.65,
        p_m:float=0.05,
        t_max:int=50,
        rand_seed:int=None,
        fitness_function:Callable=binary_knapsack.fn,
        maximize:bool=True,
        Select_Mechanism:SelectionMechanism=Proportional,
        selection_parameters:dict={}
    ) -> None:
        """
        Initialize the parameters for a genetic algorithm.

        Args:
            dims (int, optional): Dimensions of chromosome vector. Represents the number of items to choose from. Defaults to 20.
            max_item_weight (float, optional): Upper bound for weight. Defaults to 10.0.
            profit_correlation_factor (float, optional): Constant used in generation of weakly correlated data sets. Defaults to 5.
            capacity (float, optional): Capacity of the knapsack. Defaults to 40.0.
            pop_size (int, optional): Population size. Defaults to 30.
            p_c (float, optional): Probability of crossover. In range [0, 1]. Defaults to 0.65.
            p_m (float, optional): Probability of mutation. In range [0, 1]. Defaults to 0.05.
            t_max (int, optional): Maximum iterations/generations. Defaults to 50.
            rand_seed(int, optional): Seed for random number generator.
            fitness_function (Callable, optional): Function of \vec{x}. Returns (float). default sum([x**2 for x in alleles]).
            maximize (bool, optional): (False)[minimize]; (True)[maximize]. Default True.
            Select_Mechanism (SelectionMechanism): The selected selection mechanism. Default Proportional.
            selection_parameters (dict, optional): The selected selection mechanism parameters.
        """
        assert dims > 0 and type(dims) is int
        assert pop_size > 0 and pop_size % 2 == 0
        assert p_c >= 0 and p_c <= 1
        assert p_m >= 0 and p_m <= 1
        assert t_max > 0
        assert fitness_function is not None and callable(fitness_function)
        assert maximize in (False, True)
        self.dims = int(dims)
        self._bitstring_length = None
        self.max_item_weight = float(max_item_weight)
        self.profit_correlation_factor = float(profit_correlation_factor)
        self.capacity = float(capacity)
        self.pop_size = int(pop_size)
        self.p_c = float(p_c)
        self.p_m = float(p_m)
        self.t_max = int(t_max)
        self.t = 0
        self.test_data_set = None
        self.population = None
        self.best_of_run = None
        self.fitness_function = fitness_function
        self.maximize = maximize
        self.Select_Mechanism : SelectionMechanism = Select_Mechanism
        self.selection_parameters = selection_parameters
        self.random = None
        self.seed_random(rand_seed)

    async def simulate(self) -> Chromosome:
        """Simulate the genetic algorithm with configured parameters."""
        self.initialize_test_data_set()
        self.initialize_population()
        self.evaluate_population()
        deque((self.iterate() for _ in np.arange(self.t_max)), maxlen=0) # execute generator
        print(self.best_of_run)
        return self.best_of_run

    def iterate(self) -> None:
        """Perform one iteration of the simulation."""
        self.t = self.t + 1
        if self.t > self.t_max:
            return
        # print('creating')
        self.population = self.create_next_population()
        # print('evaluating')
        self.evaluate_population()
        if self.t % 10 == 0 or self.t == self.t_max:
            self.print_stats()
        if self.population.is_converged:
            print(f'Population Converged at t={self.t}. Terminating')
            self.print_stats()
            self.t = self.t_max


    def create_next_population(self) -> Population:
        """Perform selection, crossover, and mutation on the population.

        Returns:
            Population: The proposed next generation of the population.
        """
        return Population(self.bitwise_gene_mutation(
                            self.bitwise_single_point_crossover(
                                self.selection_mechanism())))

    def selection_mechanism(self) -> list[Chromosome]:
        """Perform selection on the population.

        Returns:
            list of Chromosome: A new population after a round of selection.
        """
        assert self.population.is_evaluated
        # print('selecting')
        try:
            mechanism : SelectionMechanism = self.Select_Mechanism(self.random, tuple(c.fitness_score for c in self.population.members), self.population.sum_of_fitnesses, self.maximize, **self.selection_parameters)
        except NotImplementedError:
            print('Provided Select_Mechanism not supported.')
            sys.exit(1)
        return [copy.deepcopy(self.population.members[i]) for i in mechanism.next_population()]

    def bitwise_single_point_crossover(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform single cut-point crossover on the population using self.p_c as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of single cut-point crossover.
        """
        # print('crossing')
        next_gen = []
        randomness = self.random.uniform(0, 1, size=int(self.pop_size/2))
        for i in np.arange(0, self.pop_size, step=2):
            p1 : Chromosome = population[i]
            p2 : Chromosome = population[i+1]
            if randomness[int(i/2)] < self.p_c:
                # crossover, perform single-point crossover
                cut_point = self.random.integers(1, self.dims)
                p1_split = np.split(p1.bitstring, [cut_point])
                p2_split = np.split(p2.bitstring, [cut_point])
                # print('crossing')
                p1.bitstring = np.concatenate((p1_split[0], p2_split[1]))
                p2.bitstring = np.concatenate((p2_split[0], p1_split[1]))
            next_gen.append(p1)
            next_gen.append(p2)
        return next_gen

    def bitwise_gene_mutation(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform gene-wise mutation on the population using self.p_m as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of gene-wise mutation.
        """
        # print('mutating')
        next_gen = []
        randomness = self.random.uniform(0, 1, size=self.bitstring_length*self.pop_size)
        for j, c in enumerate(population):
            bitstring = c.bitstring
            mutated = False
            offset = j * self.bitstring_length
            for i, a in enumerate(bitstring):
                if randomness[offset + i] < self.p_m:
                    # mutation
                    # print('mutating', i)
                    bitstring[i] = np.abs(a - 1)
                    mutated = True
            if mutated:
                c.bitstring = bitstring
            next_gen.append(c)
        return next_gen

    def evaluate_population(self) -> None:
        """Evaluate an entire iteration/generation's population.
        
        Track fitness scores using a tuple containing (index, fitness_score).
        """
        self.population.evaluate(self.test_data_set, self.fitness_function)
        if self.maximize:
            if self.best_of_run is None or self.population.high_score.fitness_score > self.best_of_run.fitness_score:
                self.best_of_run = copy.deepcopy(self.population.high_score)
        else:
            if self.best_of_run is None or self.population.low_score.fitness_score < self.best_of_run.fitness_score:
                self.best_of_run = copy.deepcopy(self.population.low_score)

    def initialize_test_data_set(self) -> None:
        """Initialize a population for the GA within configured parameters."""
        weights = np.random.uniform(1, self.max_item_weight, size=self.dims)
        profit_variances = np.random.uniform(-self.profit_correlation_factor, self.profit_correlation_factor, size=self.dims)
        # If profit ends up below 0, set to 0 and consider it actual garbage.
        profits = [np.max((0, weights[i] + profit_variances[i])) for i in range(self.dims)]
        self.test_data_set = np.dstack((profits, weights))[0]
        print('Profits\t\tWeights')
        print(self.test_data_set)

    def initialize_population(self) -> None:
        """
        Initialize a population for the GA within configured parameters.
        
        This can only happen when there is no current population.
        """
        if self.population is not None:
            raise RuntimeError('Population already initialized')
        self.population = Population(
            tuple(
                Chromosome(self.random, self.dims)
                for _ in np.arange(self.pop_size)
            )
        )

    def seed_random(self, given_seed:int=None) -> None:
        """
        Initialize the random seed using a made-up via hand-waving function.
        
        This can only happen when there is no current random generator.

        Args:
            given_seed (int, optional): Seed for random number generator
        """
        if self.random is not None:
            raise RuntimeError('Random already seeded')
        seed = None
        if given_seed is not None:
            seed = int(given_seed)
            self.random = np.random.default_rng(seed)
        else:
            np.random.seed(int(time.time()))
            # seed random using datetime, then export the result of that to re-seed
            seed = np.random.randint(1, 123456789)
            self.random = np.random.default_rng(seed)
        print(f'Seeded random with {seed}')

    def print_stats(self) -> None:
        print(f'----------- Gen. {self.t} ---------------')
        print(f'High  Fitness: {self.population.high_score}\n')
        print(f'Low   Fitness: {self.population.low_score}\n')
        print(f'Avg   Fitness: {self.population.average_fitness}\n')
        print(f'Best-of-Run  : {self.best_of_run} at t={self.best_of_run_generation}')

    @property
    def best_of_run(self) -> Chromosome:
        return self._best_of_run[0]

    @property
    def best_of_run_generation(self) -> int:
        return self._best_of_run[1]

    @best_of_run.setter
    def best_of_run(self, value:Chromosome) -> None:
        assert value is None or type(value) is Chromosome
        self._best_of_run = value, self.t

    @property
    def population(self) -> Population:
        return self._population

    @population.setter
    def population(self, value:Population) -> None:
        assert (value is None and self.pop_size is not None) or len(value.members) == self.pop_size
        self._population = value

    @property
    def bitstring_length(self) -> np.uint8:
        """L"""
        if self._bitstring_length is not None:
            return self._bitstring_length
        self._bitstring_length = self.dims
        return self._bitstring_length


if __name__ == '__main__':
    asyncio.run(GA(rand_seed=None).simulate())
