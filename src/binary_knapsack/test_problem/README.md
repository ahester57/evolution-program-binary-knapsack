
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
