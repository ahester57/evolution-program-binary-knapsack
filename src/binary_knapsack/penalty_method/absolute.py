# ahester57

import numpy as np

from binary_knapsack.chromosome import Chromosome
from binary_knapsack.penalty_method.method import PenaltyMethod


class AbsolutePenalty(PenaltyMethod):
    """Represents an absolute penalty. Overage of any constraint leads to zero fitness.

    Attributes:
        constraints (list): The constraints.
    """
    def __init__(self, constraints:dict) -> None:
        """Initialize the parameters for death penalty.
        
        Args:
            constraints (dict): The constraints. {'attribute_name': limit)
        """
        super().__init__(constraints)

    def penalize(self, population:list[Chromosome]) -> None:
        """Assess and penalize the population using a penalty method.

        Args:
            population (list of Chromosome): The population to assess.
        """
        for k, v in self.constraints.items():
            for c in population:
                if getattr(c, k) > v:
                    c.fitness_score = np.float64(0.0)

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        return {}