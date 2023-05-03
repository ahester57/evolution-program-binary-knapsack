
## Test Data

The difficulty of the knapsack problem can be contributed to by the level of correlation of the Profits $P_i$ and Weights $W_i$.

This project uses a weakly correlated test data set to provide some challenge while still remaining solvable using penalty methods.

For each $i=1..n$

$$W_i = rand.float(1, v),$$

$$P_i = \max(0, W_i + rand.float(-r, r))$$

### Test Data Parameters

Defaults shown.

* Number of items to choose from, $n = 20$
* Upper bound for weight, $v = 10$
* Profit correlation factor, $r = 5$
* Capacity, $C = 40$

----

## Example Profits | Weights

```
Profits         Weights
[[ 1.41120996  4.66918325]
 [ 0.98976516  1.49829436]
 [ 9.7947617   8.0968139 ]
 [ 8.15973775  3.58574666]
 [ 8.38648779  5.05315528]
 [ 3.8183104   3.73521075]
 [ 7.0378312   5.73759572]
 [ 9.96465678  6.61430992]
 [ 7.46429557  7.99097912]
 [ 9.79907955  7.17617481]
 [11.19767219  9.82844977]
 [ 5.03030377  6.40734483]
 [ 3.47146217  8.32571668]
 [ 7.79765528  7.37780637]
 [ 0.          1.24781212]
 [ 5.58830843  9.13840496]
 [ 5.53806313  5.04914366]
 [ 0.          2.07032189]
 [ 7.50751635  8.51770158]
 [ 0.2206161   2.82023404]]
```

----

## Example Default Options

```
Options: {
  "Crossover_Method": "<class 'binary_knapsack.crossover_method.single_point.SinglePoint'>",
  "Penalty_Method": "<class 'binary_knapsack.penalty_method.logarithmic.LogarithmicPenalty'>",
  "Select_Mechanism": "<class 'binary_knapsack.selection_mechanism.proportional.Proportional'>",
  "crossover_parameters": {
    "p_c": 0.65
  },
  "maximize": true,
  "p_m": 0.05,
  "penalty_parameters": {
    "rho": 1.3
  },
  "pop_size": 30,
  "problem_instance": "Profits\t\tWeights\n[[ 1.41120996  4.66918325]\n [ 0.98976516  1.49829436]\n [ 9.7947617   8.0968139 ]\n [ 8.15973775  3.58574666]\n [ 8.38648779  5.05315528]\n [ 3.8183104   3.73521075]\n [ 7.0378312   5.73759572]\n [ 9.96465678  6.61430992]\n [ 7.46429557  7.99097912]\n [ 9.79907955  7.17617481]\n [11.19767219  9.82844977]\n [ 5.03030377  6.40734483]\n [ 3.47146217  8.32571668]\n [ 7.79765528  7.37780637]\n [ 0.          1.24781212]\n [ 5.58830843  9.13840496]\n [ 5.53806313  5.04914366]\n [ 0.          2.07032189]\n [ 7.50751635  8.51770158]\n [ 0.2206161   2.82023404]]",
  "problem_parameters": {
    "capacity": 40.0,
    "dims": 20,
    "max_item_weight": 10.0,
    "profit_correlation_factor": 5.0
  },
  "selection_parameters": {},
  "t_max": 50
}
```
