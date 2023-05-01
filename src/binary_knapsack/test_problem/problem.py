# ahester57

import numpy as np


class TestProblem(object):
    """Represents a generic test problem. Does not function as one. Only provides base.

    Attributes:
        random (np.random.Generator): The random number generator.
    """
    def __init__(self, random:np.random.Generator) -> None:
        """Initialize the problem parameters.

        Args:
            random (np.random.Generator): The random number generator.
        """
        assert type(random) is np.random.Generator
        self.random = random

    def try_with_bitstring(self, soln:np.ndarray[np.uint8]) -> tuple:
        """Evaluate a bit-string solution to the problem."""
        raise NotImplementedError

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError