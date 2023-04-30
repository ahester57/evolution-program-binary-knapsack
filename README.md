# An Evolution Program

## Objective

Solve the following optimization of the 0/1 Knapsack Problem.

### Given

* Weights, $W_i$
* Profits, $P_i$
* Capacity, $C$,

### Find a binary vector

$$\vec{x} = \langle x_1, x_2, \ldots, x_n \rangle, x_i \in \lbrace 0, 1 \rbrace,$$

### which maximizes

$$P(x) = \sum_i^n{(x_i \times P_i)},$$

### subject to

$$\sum_i^n{(x_i \times W_i)} \leq C.$$

----

## Test Data

The difficulty of the knapsack problem can be contributed to by the level of correlation of the Profits $P_i$ and Weights $W_i$.

This project uses a weakly correlated test data set to provide some challenge while still remaining solvable using penalty methods.

For each $i=1..n$

$$W_i = rand.float(1, v),$$

$$P_i = W_i + rand.float(-r, r)$$

If $P_i \leq 0$ 

### Test Data Parameters

Defaults shown.

* Number of items to choose from, $n = 20$
* Upper bound for weight, $v = 10$
* Profit correlation variance, $r = 5$
* Capacity, $C = 20$

----

## Details of Evolution Program

### Representation

* Chromosomes (input vector $\vec{s}$) made up of bit-string values, e.g. $\langle10010101101101100110\rangle$.
* The $i^{th}$ item is selected if and only if $x_i = 1$.

### Selection Mechanisms

* Proportional selection, i.e. probability of advancement equal to fitness values over sum of all fitness values.

### Crossover Methods

* Single-point crossover, i.e. from two parents, choose a cut-point and swap sides of each parent to create two children.

### Mutation Methods

* Gene-wise mutation, i.e. each gbitene ($s_i$) has equal but indenpendent chance ($p_m$) to mutate a small amount.

### Termination Conditions

Simulate until one of the following has been met:

* Simulation reaches $t_{max}$ generations.
* Population fully converges.

### Evolution Program Parameters

Defaults shown.

* Population Size, $N = 300$
* Crossover probability, $p_c = 0.65$
* Mutation probability, $p_m = 0.05$
* Maximum generations, $t_{max} = 50$

----

## Local Installation

From the project root, run `pip install -e src/`.
