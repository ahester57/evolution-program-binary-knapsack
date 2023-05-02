# ahester57

import numpy as np

from binary_knapsack.chromosome import Chromosome
from crossover_method.method import CrossoverMethod


class PUniform(CrossoverMethod):
    """Facilitates p-uniform crossver between 2 parents.

    Attributes:
        random (np.random.Generator): The random number generator.
        p_c (float): Probability of crossover. In range [0, 1].
        p (float): Probability of parent 1 donating its allele (independent for each locus).
    """
    def __init__(self,
        random:np.random.Generator,
        p_c:float,
        p:float=0.5
    ) -> None:
        """
        Initialize the parameters for linear ranking selection with replacement.

        Args:
            random (np.random.Generator): The random number generator.
            p_c (float): Probability of crossover. In range [0, 1].
            p (float): Probability of parent 1 donating its allele (independent for each locus).
        """
        super().__init__(random, p_c)
        self.p = p

    def crossover(self, population:list[Chromosome]) -> list[Chromosome]:
        """Perform single cut-point crossover on the population using self.p_c as probability of occurrence.

        Args:
            population (list of Chromosome): The population to act upon.

        Returns:
            list of Chromosome: A new population after a round of single cut-point crossover.
        """
        # print('crossing')
        next_gen = []
        pop_size = len(population)
        randomness = self.random.uniform(0, 1, size=int(pop_size/2))
        for i in np.arange(0, pop_size, step=2):
            p1 : Chromosome = population[i]
            p2 : Chromosome = population[i+1]
            if randomness[int(i/2)] < self.p_c:
                # crossover, perform p-uniform crossover
                ranked_parents = [p1]
                if p2.fitness_score > p1.fitness_score:
                    ranked_parents.insert(0, p2)
                else:
                    ranked_parents.append(p2)
                bit_randomness = self.random.uniform(0, 1, size=int(p1.num_items))
                p1_new_bitstring = np.zeros(p1.num_items, dtype=np.uint8)
                p2_new_bitstring = np.zeros(p1.num_items, dtype=np.uint8)
                for j in np.arange(0, p1.num_items):
                    if bit_randomness[j] < self.p:
                        p1_new_bitstring[j] = ranked_parents[0].bitstring[j]
                        p2_new_bitstring[j] = ranked_parents[1].bitstring[j]
                    else:
                        p1_new_bitstring[j] = ranked_parents[1].bitstring[j]
                        p2_new_bitstring[j] = ranked_parents[0].bitstring[j]
                # print('crossing')
                p1.bitstring = p1_new_bitstring
                p2.bitstring = p2_new_bitstring
            next_gen.append(p1)
            next_gen.append(p2)
        return next_gen

    @staticmethod
    def parameters() -> dict[str, tuple]:
        return {
            'p_c': ('Enter Probability of Crossover', 0.65),
            'p': ('Enter \'p\' for p-uniform Crossover', 0.5)
        }
