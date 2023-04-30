# ahester57

import numpy as np


def fn(alleles:np.ndarray[np.float64]):
    return np.sum(np.square(alleles))


if __name__ == '__main__':
    print(fn([1, 2]))
