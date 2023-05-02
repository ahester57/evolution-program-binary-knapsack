# ahester57

from binary_knapsack.chromosome import Chromosome


class PenaltyMethod:
    """Represents a generic penalty method. Does not function as one. Only provides base.

    Attributes:
        constraints (list): The constraints.
    """
    def __init__(self, constraints) -> None:
        """Initialize the parameters for penalization.
        
        Args:
            constraints (list): The constraints.
        """
        self.constraints = constraints

    def penalize(self, population:list[Chromosome]) -> list[Chromosome]:
        """Assess and penalize the population using a penalty method.

        Args:
            population (list of Chromosome): The population to assess.

        Returns:
            list of Chromosome: A new population after a round of penalization.
        """
        raise NotImplementedError

    @staticmethod
    def parameters(self) -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError
