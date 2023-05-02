# ahester57

import numpy as np

from binary_knapsack.chromosome import Chromosome


class CrossoverMethod:
    """Represents a generic crossover method. Does not function as one. Only provides base.

    Attributes:
        random (np.random.Generator): The random number generator.
        p_c (float): Probability of crossover. In range [0, 1].
    """
    def __init__(self,
        random:np.random.Generator,
        p_c:float=0.65
    ) -> None:
        """Initialize the parameters for crossover.

        Args:
            random (np.random.Generator): The random number generator.
            p_c (float, optional): Probability of crossover. In range [0, 1]. Defaults to 0.65.
        """
        assert type(random) is np.random.Generator
        assert p_c >= 0 and p_c <= 1
        self.random = random
        self.p_c = p_c

    def crossover(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform on the population using self.p_c as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of crossover.
        """
        raise NotImplementedError

    @staticmethod
    def parameters(self) -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError
