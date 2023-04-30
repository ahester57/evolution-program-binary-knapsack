# ahester57

import numpy as np

from binary_knapsack.selection_mechanism.mechanism import SelectionMechanism


class LinearRanking(SelectionMechanism):
    """Facilitates linear ranking selection with replacement.

    Attributes:
        random (np.random.Generator): The random number generator.
        population_fitnesses (tuple of float): The population fitness scores, in order.
        sum_of_fitnesses (float): The sum of the populations' fitness scores.
        maximize (bool): (False)[minimize]; (True)[maximize]. Default True.
        pop_size (int): The size of the population.
        max (float): The expected number of copies of the most fit individual in the next generation.
        min (float): The expected number of copies of the least fit individual in the next generation.
    """
    def __init__(self, random:np.random.Generator, population_fitnesses:tuple[float], sum_of_fitnesses:float=None, maximize:bool=True, **kwargs) -> None:
        """
        Initialize the parameters for linear ranking selection with replacement.

        Args:
            random (np.random.Generator): The random number generator.
            population_fitnesses (tuple of float): The population fitness scores, in order.
            sum_of_fitnesses (float): The sum of the populations' fitness scores.
            maximize (bool): (False)[minimize]; (True)[maximize]. Default True.
            max (float): The expected number of copies of the most fit individual in the next generation.
        """
        super().__init__(random, population_fitnesses, sum_of_fitnesses, maximize, **kwargs)
        if 'max' in kwargs.keys():
            self.max = float(kwargs['max'])
        else:
            self.max = self.parameters()['max'][1]
        assert self.max >= 1 and self.max <= 2
        self.min = 2 - self.max
        self._max_min = self.max - self.min

    def next_population(self) -> tuple[int]:
        """Perform linear ranking selection on the population.

        Returns:
            tuple of int: An index-defined population after a round of linear ranking selection.
        """
        rank_list = self._generate_linear_ranks()
        return tuple(rank_list[i] for i in self._sample_from_pmf(self._generate_pmf()))

    def _generate_linear_ranks(self) -> tuple[int]:
        """Generate a ranked list of members in order of fitness score.

        Returns:
            tuple of int: A population-sized list containing original index in order of rank.
        """
        # TODO: numpy-ify this
        assert self.sum_of_fitnesses > 0
        sorted_keep_indices = [(i, f) for i, f in enumerate(self.population_fitnesses)]
        sorted_keep_indices.sort(key=lambda x:x[1], reverse=not self.maximize)
        return tuple(f[0] for f in sorted_keep_indices)

    def _generate_pmf(self) -> tuple[float]:
        """Generate a probability mass function for the current population.

        Returns:
            list of tuple: A population-sized list containing pmf for this population.
        """
        # TODO: numpy-ify this
        return tuple(
            er / self.pop_size
            for er in tuple(
                self.min + (float(rank) / (self.pop_size - 1) * self._max_min)
                for rank in np.arange(self.pop_size)
            )
        )

    def _sample_from_pmf(self, pmf:tuple[float]) -> np.ndarray[np.signedinteger]:
        """Generate a new index-defined population by stochastic choice based on the given ranks.

        Args:
            pmf (tuple of float): Probability Mass Function of population's fitness scores.

        Returns:
            tuple of int: A population-sized list containing indices of chosen individuals.
        """
        return self.random.choice(self.pop_size, size=self.pop_size, replace=True, p=pmf)

    @staticmethod
    def parameters() -> dict[str, tuple]:
        return {'max': ('Enter Max (from 1 to 2)', 1.2)}
