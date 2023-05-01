# ahester57

import numpy as np


class TestProblem(object):
    def __init__(self) -> None:
        pass

    def try_with_bitstring(self, soln:np.ndarray[np.uint8]) -> tuple:
        """Evaluate a bit-string solution to the problem."""
        raise NotImplementedError

    @staticmethod
    def parameters() -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError