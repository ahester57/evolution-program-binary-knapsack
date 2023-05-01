# ahester57

import numpy as np

from typing import Callable


class Chromosome:
    """Depicts one solution in the population. Adapted for the 0/1 Knapsack problem.

    Attributes:
        random (np.random.Generator): The random number generator.
        num_items (int): The number of items to choose from.
        bitstring (np.ndarray of uint8): The bitstring representation of the alleles.
        fitness_score (float): The fitness score
    """

    def __init__(self, random:np.random.Generator, num_items:int) -> None:
        """Depicts one individual in the population.

        Args:
            random (np.random.Generator): The random number generator.
            num_items (int): The number of items to choose from.
        """
        assert num_items > 0 and num_items <= 256
        self.num_items = num_items
        self.fitness_score = None
        self.fitness_cost = None
        self.bitstring = random.integers(2, size=self.num_items, dtype=np.uint8)

    def evaluate(self, set_of_items:tuple[tuple[float]], fitness_function:Callable) -> None:
        """Perform an evaluation of this chromosome with given fitness function.

        Args:
            set_of_items (tuple[tuple[float]])
            fitness_function (Callable): Function of \vec{x}. Returns (float).

        Returns:
            float: The fitness score.
        """
        assert set_of_items is not None and len(set_of_items[0]) == 2
        assert fitness_function is not None and callable(fitness_function)
        if self.is_evaluated:
            # no need to re-evaluate if bitstring has not changed
            return
        self.fitness_score = fitness_function(set_of_items, self.bitstring)

    @property
    def bitstring(self) -> np.ndarray[np.uint8]:
        return self._bitstring

    @bitstring.setter
    def bitstring(self, value:np.ndarray[np.uint8]) -> None:
        """bitstring update trigger clears fitness score."""
        assert value is not None and type(value) is np.ndarray and len(value) == self.num_items
        self.fitness_score = None
        self._bitstring = value

    @property
    def fitness_score(self) -> np.float64:
        return self._fitness_score

    @fitness_score.setter
    def fitness_score(self, value:tuple[float]) -> None:
        assert value is None or type(value) is tuple
        if value is None:
            self._fitness_score = value
            self.fitness_cost = value
        else:
            self._fitness_score = value[0]
            self.fitness_cost = value[1]

    @property
    def is_evaluated(self) -> bool:
        return self.fitness_score is not None

    def __repr__(self) -> str:
        return f'Score: {self.fitness_score} :: {self.bitstring}\n => costing {self.fitness_cost}'
