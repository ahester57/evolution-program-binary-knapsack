# ahester57

import numpy as np

from binary_knapsack.chromosome import Chromosome
from binary_knapsack.penalty_method.method import PenaltyMethod


class LogarithmicPenalty(PenaltyMethod):
    """Represents a simple logarithmic penalty.

    Penalty(x) = log_2(1 + \rho * (fitness_cost - constraint_limit)

    Attributes:
        constraints (list): The constraints.
    """
    def __init__(self, constraints:dict, rho:float) -> None:
        """Initialize the parameters for absolute penalty.
        
        Args:
            constraints (dict): The constraints. {'attribute_name': limit)
            rho (float): Factor in penalty function.
        """
        super().__init__(constraints)
        self.rho = rho

    def penalize(self, population:list[Chromosome], t:int=None) -> None:
        """Assess and penalize the population using absolute, static penalty.

        Penalty(x) = log_2(1 + \rho * (fitness_cost - constraint_limit)

        Args:
            population (list of Chromosome): The population to assess.
            t (int): The current generation. Ignored for static penalty methods.
        """
        for k, v in self.constraints.items():
            for c in population:
                attr_val = getattr(c, k)
                if attr_val > v:
                    c.fitness_score = np.log2(1 + self.rho * (attr_val - v))

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        return {'rho': ('Enter Rho for Logarithmic Penalty', 1.3)}
