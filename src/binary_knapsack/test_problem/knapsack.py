# ahester57

import numpy as np

from binary_knapsack.test_problem.problem import TestProblem


class BinaryKnapsack(TestProblem):
    """A class for the 0/1 Knapsack Problem.

    Attributes:
        weights (np.ndarray[float]): The weights for each item. Aligned by index.
        profits (np.ndarray[float]): The profits for each item. Aligned by index.
        profit_correlation_factor (float): Constant used in generation of weakly correlated data sets.
        capacity (float): Capacity of the knapsack.
    """
    def __init__(self,
        random:np.random.Generator,
        num_items:int=20,
        max_item_weight:float=10.0,
        profit_correlation_factor:float=5.0,
        capacity:float=40.0
    ) -> None:
        """Initialize a problem test data set for the 0/1 Knapsack Problem.

        Args:
            random (np.random.Generator): The random number generator.
            num_items (int): The number of items to choose from.
            max_item_weight (float): Upper bound for weight.
            profit_correlation_factor (float): Constant used in generation of weakly correlated data sets.
            capacity (float): Capacity of the knapsack.
        """
        super().__init__()
        self.num_items = int(num_items)
        self.capacity = float(capacity)
        self.weights = random.uniform(1, max_item_weight, size=self.num_items)
        profit_variances = random.uniform(-profit_correlation_factor, profit_correlation_factor, size=self.num_items)
        # If profit ends up below 0, set to 0 and consider it actual garbage.
        self.profits = [np.max((0, self.weights[i] + profit_variances[i])) for i in range(self.num_items)]
        print('Profits\t\tWeights')
        print(np.dstack((self.profits, self.weights))[0])

    def try_with_bitstring(self, soln:np.ndarray[np.uint8]) -> tuple[float]:
        """Evaluate a bit-string solution to the problem.

        Args:
            soln (np.ndarray[np.uint8]): Represents a solution to the problem. \
                The i^th item is selected if and only if (iff) x_i == 1.

        Returns:
            tuple[float]: The (profit, weight) for the given solution to the problem.
        """
        assert len(soln) == self.num_items
        profit = 0
        weight = 0
        for i, x in enumerate(soln):
            if x == 1:
                profit += self.profits[i]
                weight += self.weights[i]
        return (profit, weight)

    @staticmethod
    def parameters() -> dict[str, tuple]:
        return {
            'num_items': ('Enter Number of Items', 20),
            'max_item_weight': ('Enter Maximum Weight of One Item', 10.0),
            'profit_correlation_factor': ('Enter Profit Correlation Factor', 5.0),
            'capacity': ('Enter Knapsack Capacity', 40.0)
        }


if __name__ == '__main__':
    problem = BinaryKnapsack(
        np.random.default_rng(np.random.randint(1, 123456789)),
        num_items=20,
        max_item_weight=10,
        profit_correlation_factor=5,
        capacity=40.0
    )
    print(problem.try_with_bitstring([0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0]))
