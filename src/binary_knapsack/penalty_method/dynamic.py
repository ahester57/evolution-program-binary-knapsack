# ahester57

import numpy as np

from binary_knapsack.chromosome import Chromosome
from binary_knapsack.penalty_method.method import PenaltyMethod


class DynamicPenalty(PenaltyMethod):
    """Represents a harshening dynamic penalty.

    As generations go by, the penalty for the same violation goes up.
    Penalty(x) = $(C * t)^{alpha} * \sum_j^m{f_j(x)^{beta}}$

    Attributes:
        constraints (list): The constraints.
        c (float): for (C * t)^alpha
        alpha (float): for (C * t)^alpha
        beta (float): for (degree of violation)^beta
    """
    def __init__(self,
        constraints:dict,
        c:float=0.5,
        alpha:float=2.0,
        beta:float=2.0
    ) -> None:
        """Initialize the parameters for dynamic penalty method.

        Args:
            constraints (dict): The constraints. {'attribute_name': limit)
            c (float): for (C * t)^alpha
            alpha (float): for (C * t)^alpha
            beta (float): for (degree of violation)^beta
        """
        super().__init__(constraints)
        assert type(c) is float
        assert type(alpha) is float
        assert type(beta) is float
        self.c = c
        self.alpha = alpha
        self.beta = beta

    def penalize(self, population:list[Chromosome], t:int) -> None:
        """Assess and penalize the population using absolute, static penalty.

        Penalty(x) = $(C * t)^{alpha} * \sum_j^m{f_j(x)^{beta}}$

        Args:
            population (list of Chromosome): The population to assess.
            t (int): The current generation
        """
        for k, v in self.constraints.items():
            for c in population:
                if getattr(c, k) > v:
                    c.fitness_score = np.float64(0.0)

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        return {
            'c': ('Enter \'c\' for (C * t)^alpha', 0.5),
            'alpha': ('Enter \'alpha\' for (C * t)^alpha', 2.0),
            'beta': ('Enter \'beta\' for (degree of violation)^beta', 2.0)
        }
