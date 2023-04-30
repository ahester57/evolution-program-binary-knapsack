# ahester57

import numpy as np

from typing import Callable


class Chromosome:
    """Depicts one individual in the population.

    Attributes:
        random (np.random.Generator): The random number generator.
        allele_precisions (ndarray of uint8): Size equal to number of real values to represent. \
                Each value is the # of bits used to represent the allele. Max sum = 256.
        domain_lower (float, optional): Gene value lower bound. Defaults to -7.0.
        domain_upper (float, optional): Gene value upper bound. Defaults to 4.0.
        bitstring (np.ndarray of uint8): The bitstring representation of the alleles.
        fitness_score (float): The fitness score
    """

    def __init__(self, random:np.random.Generator, allele_precisions:np.ndarray[np.uint8], domain_lower:float, domain_upper:float) -> None:
        """Depicts one individual in the population.

        Args:
            random (np.random.Generator): The random number generator.
            allele_precisions (ndarray of uint8): Size equal to number of real values to represent. \
                Each value is the # of bits used to represent the allele. Max sum = 256.
            domain_lower (float, optional): Gene value lower bound. Defaults to -7.0.
            domain_upper (float, optional): Gene value upper bound. Defaults to 4.0.
        """
        assert allele_precisions is not None and type(allele_precisions) is np.ndarray
        self.L = np.sum(allele_precisions)
        assert self.L <= 256
        self.allele_precisions = allele_precisions
        self.domain_lower = float(domain_lower)
        self.domain_upper = float(domain_upper)
        self.domain_diff = self.domain_upper - self.domain_lower
        self.fitness_score = None
        self.real_vals = None
        self.split_locations = np.cumsum(self.allele_precisions[:-1])
        self.bit_converters = {bit_size: 2**np.arange(bit_size)[::-1] for bit_size in self.allele_precisions}
        self.bitstring = random.integers(2, size=self.L, dtype=np.uint8)

    def evaluate(self, fitness_function:Callable) -> None:
        """Perform an evaluation of this chromosome with given fitness function.

        Args:
            fitness_function (Callable): Function of \vec{x}. Returns (float).

        Returns:
            float: The fitness score.
        """
        assert fitness_function is not None and callable(fitness_function)
        if self.is_evaluated:
            # no need to re-evaluate if bitstring has not changed
            return
        self.fitness_score = fitness_function(self.real_vals)

    @property
    def bitstring(self) -> np.ndarray[np.uint8]:
        return self._bitstring

    @bitstring.setter
    def bitstring(self, value:np.ndarray[np.uint8]) -> None:
        """bitstring update trigger clears fitness score."""
        assert value is not None and type(value) is np.ndarray and len(value) == self.L
        self.fitness_score = None
        self._bitstring = value
        self.real_vals = [
            self.domain_lower + (self.domain_diff * (bits.dot(self.bit_converters[bits.size]) / ((2**bits.size) - 1)))
            for bits in np.split(value, self.split_locations)
        ] # trim [:-1] from np.cumsum -- it always ends up empty due to bitstring's reliance on self.L

    @property
    def fitness_score(self) -> np.float64:
        return self._fitness_score

    @fitness_score.setter
    def fitness_score(self, value:np.float64) -> None:
        assert value is None or type(value) is np.float64
        self._fitness_score = value

    @property
    def is_evaluated(self) -> bool:
        return self.fitness_score is not None

    def __repr__(self) -> str:
        return f'{self.fitness_score} :: {self.bitstring}\n=> {self.real_vals}'
