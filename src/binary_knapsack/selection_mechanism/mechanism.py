# ahester57

import numpy as np


class SelectionMechanism:
    def __init__(self, random:np.random.Generator, population_fitnesses:tuple[float], sum_of_fitnesses:float=None, maximize:bool=True, **kwargs) -> None:
        """
        Initialize the parameters for proportional selection with replacement.

        Args:
            random (np.random.Generator): The random number generator.
            population_fitnesses (tuple of float): The population fitness scores, in order.
            sum_of_fitnesses (float, optional): The sum of the populations' fitness scores.
            maximize (bool, optional): (False)[minimize]; (True)[maximize]. Default True.
        """
        assert population_fitnesses is not None
        self.random = random
        self.population_fitnesses = population_fitnesses
        self.sum_of_fitnesses = sum_of_fitnesses
        self.maximize = maximize
        if self.sum_of_fitnesses is None:
            self.sum_of_fitnesses = np.sum(population_fitnesses)
        self.pop_size = len(self.population_fitnesses)

    def next_population(self) -> tuple[int]:
        raise NotImplementedError

    @staticmethod
    def parameters(self) -> dict[str, tuple]:
        """{'param_name': tuple('description', default_value)}"""
        raise NotImplementedError
