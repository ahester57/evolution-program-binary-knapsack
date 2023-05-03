# ahester57

from binary_knapsack.chromosome import Chromosome


class PenaltyMethod:
    """Represents a generic penalty method. Does not function as one. Only provides base.

    Attributes:
        constraints (list): The constraints.
    """
    def __init__(self, constraints: dict) -> None:
        """Initialize the parameters for penalization.
        
        Args:
            constraints (dict): The constraints.
        """
        assert type(constraints) is dict
        self.constraints = constraints

    def penalize(self, population:list[Chromosome], t:int=None) -> None:
        """Assess and penalize the population using a penalty method.

        Args:
            population (list of Chromosome): The population to assess.
            t (int): The current generation.
        """
        raise NotImplementedError

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError
