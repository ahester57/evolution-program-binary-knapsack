# ahester57

import numpy as np
from binary_knapsack.chromosome import Chromosome

from crossover_method.method import CrossoverMethod


class SinglePoint(CrossoverMethod):
    """Facilitates single-point crossver between 2 parents.

    Attributes:
        random (np.random.Generator): The random number generator.
        p_c (float): Probability of crossover. In range [0, 1].
    """
    def __init__(self,
        random:np.random.Generator,
        p_c:float
    ) -> None:
        """
        Initialize the parameters for linear ranking selection with replacement.

        Args:
            random (np.random.Generator): The random number generator.
            p_c (float): Probability of crossover. In range [0, 1].
        """
        super().__init__(random, p_c)

    def crossover(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform single cut-point crossover on the population using self.p_c as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of single cut-point crossover.
        """
        # print('crossing')
        next_gen = []
        pop_size = len(population)
        randomness = self.random.uniform(0, 1, size=int(pop_size/2))
        for i in np.arange(0, pop_size, step=2):
            p1 : Chromosome = population[i]
            p2 : Chromosome = population[i+1]
            if randomness[int(i/2)] < self.p_c:
                # crossover, perform single-point crossover
                cut_point = self.random.integers(1, p1.num_items)
                p1_split = np.split(p1.bitstring, [cut_point])
                p2_split = np.split(p2.bitstring, [cut_point])
                # print('crossing')
                p1.bitstring = np.concatenate((p1_split[0], p2_split[1]))
                p2.bitstring = np.concatenate((p2_split[0], p1_split[1]))
            next_gen.append(p1)
            next_gen.append(p2)
        return next_gen

    @staticmethod
    def parameters() -> dict[str, tuple]:
        return {'p_c': ('Enter Probability of Crossover', 0.65)}
