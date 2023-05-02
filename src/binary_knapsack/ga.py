# ahester57

import asyncio
import copy
import numpy as np
import sys
import time

from collections import deque

from binary_knapsack.chromosome import Chromosome
from binary_knapsack.population import Population
from binary_knapsack.selection_mechanism.mechanism import SelectionMechanism
from binary_knapsack.selection_mechanism.proportional import Proportional
from binary_knapsack.test_problem.knapsack import BinaryKnapsack
from binary_knapsack.test_problem.problem import TestProblem
from binary_knapsack.crossover_method.method import CrossoverMethod
from binary_knapsack.crossover_method.single_point import SinglePoint


class GA:
    """A class for a genetic algorithm (GA).

    Attributes:
        dims (int): Dimensions of chromosome vector. Represents the number of items to choose from.
        pop_size (int): Population size. Defaults to 30.
        p_m (float): Probability of mutation. In range [0, 1].
        t_max (int): Maximum iterations/generations.
        random (np.random.Generator): The random number generator.
        population (Population): Collection of current generation's individual chromosomes.
        problem_instance (TestProblem): The configured instance of the "objective function."
        maximize (bool): (False)[minimize]; (True)[maximize].
        Select_Mechanism (SelectionMechanism): The selected selection mechanism.
        selection_parameters (dict): The selected selection mechanism parameters.
        crossover_instance (CrossoverMethod): The configured instance of the chosen method.
    """
    def __init__(
        self,
        pop_size:int=300,
        p_m:float=0.05,
        t_max:int=50,
        rand_seed:int=None,
        problem_instance:TestProblem=None,
        maximize:bool=True,
        Select_Mechanism:SelectionMechanism=Proportional,
        selection_parameters:dict={},
        Crossover_Method:CrossoverMethod=SinglePoint,
        crossover_parameters:dict={'p_c': 0.65}
    ) -> None:
        """Initialize the parameters for a genetic algorithm.

        Args:
            pop_size (int, optional): Population size. Defaults to 30.
            p_m (float, optional): Probability of mutation. In range [0, 1]. Defaults to 0.05.
            t_max (int, optional): Maximum iterations/generations. Defaults to 50.
            rand_seed(int, optional): Seed for random number generator.
            problem_instance (TestProblem): The configured instance of the "objective function."
            maximize (bool, optional): (False)[minimize]; (True)[maximize]. Default True.
            Select_Mechanism (SelectionMechanism): The selected selection mechanism. Default Proportional.
            selection_parameters (dict, optional): The selected selection mechanism parameters.
            Crossover_Method (CrossoverMethod): The selected crossover method. Default SinglePoint.
            crossover_parameters (dict, optional): The selected crossover method parameters.
        """
        assert pop_size > 0 and pop_size % 2 == 0
        assert p_m >= 0 and p_m <= 1
        assert t_max > 0
        assert maximize in (False, True)
        assert problem_instance is not None and problem_instance.dims is not None
        self.problem_instance = problem_instance
        assert self.problem_instance.dims > 0
        self._bitstring_length = None
        self.pop_size = int(pop_size)
        self.p_m = float(p_m)
        self.t_max = int(t_max)
        self.t = 0
        self.test_data_set = None
        self.population = None
        self.best_of_run = None
        self.maximize = maximize
        self.Select_Mechanism = Select_Mechanism
        self.selection_parameters = selection_parameters
        self.random = None
        self.seed_random(rand_seed)
        self.crossover_instance : CrossoverMethod = Crossover_Method(
            self.random,
            **crossover_parameters
        )

    async def simulate(self) -> Chromosome:
        """Simulate the genetic algorithm with configured parameters."""
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

    def evaluate_population(self) -> None:
        """Evaluate an entire iteration/generation's population.
        
        Track fitness scores using a tuple containing (index, fitness_score).
        """
        try:
            self.population.evaluate(self.problem_instance)
        except NotImplementedError:
            print('Provided TestProblem not supported.')
            sys.exit(1)
        if self.maximize:
            if self.best_of_run is None or self.population.high_score.fitness_score > self.best_of_run.fitness_score:
                self.best_of_run = copy.deepcopy(self.population.high_score)
        else:
            if self.best_of_run is None or self.population.low_score.fitness_score < self.best_of_run.fitness_score:
                self.best_of_run = copy.deepcopy(self.population.low_score)

    def create_next_population(self) -> Population:
        """Perform selection, crossover, and mutation on the population.

        Returns:
            Population: The proposed next generation of the population.
        """
        return Population(self.bitwise_gene_mutation(
                            self.crossover_method(
                                self.selection_mechanism())))

    def selection_mechanism(self) -> list[Chromosome]:
        """Perform selection on the population.

        Returns:
            list of Chromosome: A new population after a round of selection.
        """
        assert self.population.is_evaluated
        # print('selecting')
        try:
            mechanism : SelectionMechanism = self.Select_Mechanism(
                self.random,
                tuple(c.fitness_score for c in self.population.members),
                self.population.sum_of_fitnesses,
                self.maximize,
                **self.selection_parameters
            )
        except NotImplementedError:
            print('Provided SelectionMechanism not supported.')
            sys.exit(1)
        return [copy.deepcopy(self.population.members[i]) for i in mechanism.next_population()]

    def crossover_method(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform on the population using self.p_c as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of crossover.
        """
        try:
            return self.crossover_instance.crossover(population)
        except NotImplementedError:
            print('Provided CrossoverMethod not supported.')
            sys.exit(1)

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

    def initialize_population(self) -> None:
        """Initialize a population for the GA within configured parameters.
        
        This can only happen when there is no current population.
        """
        if self.population is not None:
            raise RuntimeError('Population already initialized')
        self.population = Population(
            tuple(
                Chromosome(self.random, self.problem_instance.dims)
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
        self._bitstring_length = self.problem_instance.dims
        return self._bitstring_length


if __name__ == '__main__':
    asyncio.run(GA(
        rand_seed=None,
        problem_instance=BinaryKnapsack()
    ).simulate())
