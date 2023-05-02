# ahester57

import numpy as np


class TestProblem(object):
    """Represents a generic test problem. Does not function as one. Only provides base.

    Attributes:
        dims (int): The number of items to choose from.
    """
    def __init__(self, dims:int=20) -> None:
        """Initialize the problem parameters.

        Args:
            dims (int): The number of items to choose from.
        """
        self.dims = int(dims)
        assert self.dims > 0

    def try_with_bitstring(self, soln:np.ndarray[np.uint8]) -> tuple:
        """Evaluate a bit-string solution to the problem."""
        raise NotImplementedError

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError