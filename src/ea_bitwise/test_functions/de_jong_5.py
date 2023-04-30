# ahester57

import numpy as np


def fn(alleles:np.ndarray[np.float64]):
    A = np.zeros([2, 25])
    a = [-32, -16, 0, 16, 32]
    A[0] = np.tile(a, (1, 5))
    A[1] = np.repeat(a, 5)
    sum = 0
    for i in np.arange(25):
        a0i = A[0, i]
        a1i = A[1, i]
        t2 = (alleles[0] - a0i) ** 6
        t3 = (alleles[1] - a1i) ** 6
        new = np.divide(1, (i + t2 + t3))
        sum = sum + new
    return np.divide(1, (0.002 + sum))


if __name__ == '__main__':
    print(fn([1, 2]))
