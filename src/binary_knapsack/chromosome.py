# ahester57

import numpy as np

from binary_knapsack.test_problem.problem import TestProblem


class Chromosome:
    """Depicts one solution in the population. Adapted for the 0/1 Knapsack problem.

    Attributes:
        num_items (int): The number of items to choose from.
        bitstring (np.ndarray of uint8): The bitstring representation of the alleles.
        fitness_score (float): The fitness score.
        fitness_cost (float): The fitness cost.
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
        if random is not None:
            self.bitstring = random.integers(2, size=self.num_items, dtype=np.uint8)
        else:
            self.bitstring = np.zeros(self.num_items, dtype=np.uint8)

    def evaluate(self, problem_instance:TestProblem) -> float:
        """Perform an evaluation of this chromosome with given fitness function.

        Args:
            problem_instance (TestProblem): Function of \vec{x}. Returns (tuple[float]).

        Returns:
            float: The fitness score.
        """
        assert problem_instance is not None and callable(problem_instance.try_with_bitstring)
        if self.is_evaluated:
            # no need to re-evaluate if bitstring has not changed
            return
        self.fitness_score, self.fitness_cost = problem_instance.try_with_bitstring(self.bitstring)
        return self.fitness_score

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
    def fitness_score(self, value:np.float64) -> None:
        assert value is None or type(value) is np.float64
        self._fitness_score = value

    @property
    def fitness_cost(self) -> np.float64:
        return self._fitness_cost

    @fitness_cost.setter
    def fitness_cost(self, value:np.float64) -> None:
        assert value is None or type(value) is np.float64
        self._fitness_cost = value

    @property
    def is_evaluated(self) -> bool:
        return self.fitness_score is not None

    def __repr__(self) -> str:
        return f'Score: {self.fitness_score} :: {self.bitstring}\n => costing {self.fitness_cost}'
