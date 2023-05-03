# ahester57

import numpy as np

from binary_knapsack.chromosome import Chromosome
from binary_knapsack.crossover_method.method import CrossoverMethod


class MajorityVoting(CrossoverMethod):
    """Facilitates multi-parent majority-voting crossover between 2 parents.

    Attributes:
        random (np.random.Generator): The random number generator.
        p_c (float): Probability of crossover. In range [0, 1].
        num_parents (int): Number of parents contributing to each child.
    """
    def __init__(self,
        random:np.random.Generator,
        p_c:float,
        num_parents:int=4
    ) -> None:
        """Initialize the parameters for multi-parent majority-voting crossover.

        Args:
            random (np.random.Generator): The random number generator.
            p_c (float): Probability of crossover. In range [0, 1].
            num_parents (int): Number of parents contributing to each child.
        """
        super().__init__(random, p_c)
        assert num_parents > 0
        self.num_parents = num_parents

    def crossover(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform multi-parent majority-voting crossover on the population using self.p_c as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of single cut-point crossover.
        """
        # print('crossing')
        next_gen = []
        pop_size = len(population)
        randomness = self.random.uniform(0, 1, size=pop_size)
        for i in range(pop_size):
            parent_indices = self.random.integers(0, pop_size, size=self.num_parents)
            parent_bitstrings = [population[pi].bitstring for pi in parent_indices]
            if randomness[i] < self.p_c:
                # crossover, perform majority voting crossover
                child = Chromosome(None, len(parent_bitstrings[0]))
                child_bitstring = child.bitstring
                for j in range(child.num_items):
                    if np.sum(
                            [pb[j] for pb in parent_bitstrings]
                        ) > (float)(self.num_parents / 2):
                        child_bitstring[j] = 1
                child.bitstring = child_bitstring
                next_gen.append(child)
            else:
                next_gen.append(population[i])
        return next_gen

    @staticmethod
    def parameters() -> dict[str, tuple]:
        return {
            'p_c': ('Enter Probability of Crossover', 0.65),
            'num_parents': ('Enter Number of Parents per Child', 4)
        }
