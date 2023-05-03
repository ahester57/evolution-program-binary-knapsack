
## Penalty Methods

### Logarithmic Penalty

I chose this static penalty method because of its ease of use and proven performance.

$$Penalty(x) = log_2(1 + \rho \cdot (\sum_i^n{x_i \cdot W_i} - C))$$

#### Parameters for Dynamic Penalty

* Scalar of degree of violation, $\rho = 1.3$

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 56.96086516860768 :: [0 0 1 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0] => costing 39.99900703419182, 46)
Mean Best Fitness: 53.06670943662913
Standard Deviation of Best Fitness: 1.771948255995935
Mean Generation Best Was Acheived: 31.5
Standard Deviation of Generations: 13.037765657248688
```

----

### Absolute Penalty

Overage of any constraint leads to a zero fitness.

I chose this static penalty method because of its ease of use and to prove penalization works.

#### Results

I could not get results due to the following error:
```
  File ".\src\binary_knapsack\selection_mechanism\proportional.py", line 49, in _generate_pmf
    assert self.sum_of_fitnesses > 0
           ^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

The absolute penalty method was not able to acheive feasible results.

----

### Dynamic Penalty

As generations go by, the penalty for the same violation goes up.

$$Penalty(x) = (C * t)^{alpha} * \sum_j^m{f_j(x)^{beta}}$$

I chose this dynamic penalty method to test the claims that this method leads to premature convergence.

#### Parameters for Dynamic Penalty

* Scalar of generation number, $C = 0.5$
* Exponent of temporal harshening, $alpha = 2.0$
* Exponent of degree of violation, $beta = 2.0$

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 55.5352304177474 :: [0 1 0 1 1 0 1 1 0 1 1 0 0 0 0 0 0 0 0 0] => costing 39.49372651844115, 50)
Mean Best Fitness: 52.74168473724467
Standard Deviation of Best Fitness: 1.3731685279839918
Mean Generation Best Was Acheived: 29.933333333333334
Standard Deviation of Generations: 13.01520478346597
```

This did not perform as well as logarithmic, and also did not acheive feasible results sometimes.

----
