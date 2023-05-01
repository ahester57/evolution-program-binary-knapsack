# ahester57

import numpy as np


def fn(set_of_items:tuple[tuple[float]], soln:np.ndarray[np.uint8]) -> tuple[float]:
    assert np.shape(set_of_items[0])[0] == 2
    assert len(soln) == len(set_of_items)
    profit = 0
    weight = 0
    for i, x in enumerate(soln):
        if x == 1:
            profit += set_of_items[i][0]
            weight += set_of_items[i][1]
    return (profit, weight)

            # max_item_weight (float): Upper bound for weight.
            # profit_correlation_factor (float): Constant used in generation of weakly correlated data sets.
if __name__ == '__main__':
    print(fn([[1, 2],[3, 2],[4, 2],[2, 2]], [0,1,1,0]))
