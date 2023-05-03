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

$$P(x) = \sum_i^n{(x_i \cdot P_i)},$$

### subject to

$$\sum_i^n{(x_i \cdot W_i)} \leq C.$$

----

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

## Representation

* Chromosomes (input vector $\vec{x}$) made up of bit-string values, e.g. $\langle10010101101101100110\rangle$.
* The $i^{th}$ item is selected if and only if $x_i = 1$.

----

## Evolution Program Parameters

Defaults shown.

* Population size, $N = 300$
* Mutation probability, $p_m = 0.05$
* Maximum generations, $t_{max} = 50$

----

## Penalty Methods

### Logarithmic Penalty

I chose this static penalty method because of its ease of use and proven performance.

$$Penalty(x) = log_2(1 + \rho \cdot (\sum_i^n{x_i \cdot W_i} - C))$$

#### Parameters for Dynamic Penalty

* Scalar of degree of violation, $\rho = 1.3$

----

### Absolute Penalty

Overage of any constraint leads to a zero fitness.

I chose this static penalty method because of its ease of use and to prove penalization works.

----

### Dynamic Penalty

As generations go by, the penalty for the same violation goes up.

$$Penalty(x) = (c \cdot t)^{alpha} \cdot \sum_j^m{f_j(x)^{beta}}$$
, where $m$ is the number of constraints.

I chose this dynamic penalty method to test the claims that this method leads to premature convergence.

#### Parameters for Dynamic Penalty

* Scalar of generation number, $c = 0.5$
* Exponent of temporal harshening, $alpha = 2.0$
* Exponent of degree of violation, $beta = 2.0$

----

## Selection Mechanisms

### Proportional Selection

An individual's probability of advancement equal to fitness score over sum of all fitness scores.

$$P(x_i) = f(x_i) / \sum_j^N{f(x_j)}$$

----

### Truncation Selection

The top $\tau\%$ are selected for advancement. The next generation
is sampled uniformly random with replacement from the top $\tau\%$.

#### Parameters for Truncation Selection

* Top tau, $\tau = 0.4$

----

### Deterministic Tournament Selection

Pick two individuals from the current population uniformly randomly with replacement.  
Advance the chromosome $\vec{x}$ with the better fitness score.  
Repeat $N$ times.

----

### Stochastic Tournament Selection

Same as deterministic tournament selection, except the worse chromosome $\vec{x}$ advances
with a typically small random chance.

#### Parameters for Stochastic Tournament Selection

* Probability of an upset, $prob = 0.9$

----

### Linear Ranking Selection

Each chromosome $\vec{x}$ is ranked from best to worst based on fitness score.  
An individual's probability of advancement is proportional to its rank.

#### Parameters for Linear Ranking Selection

* Expected # of copies of best $\vec{x}$, $max = 1.2$

----

## Crossover Methods

### Single-Point Crossover

From two parents, randomly choose a cut-point and swap sides of each parent to create two children.

#### Parameters for Single-Point Crossover

* Crossover probability, $p_c = 0.65$

----

### P-Uniform Crossover

From two parents and for each locus, randomly choose which parent to use at that locus. Choose the better parent with probability $p$. This process produces two children per set of parents.

#### Parameters for P-Uniform Crossover

* Crossover probability, $p_c = 0.65$
* Probability that the higher-performing parent donates their allele, $p = 0.5$

----

### Majority Voting Crossover

From multiple parents and for each locus, deterministicly choose the most common allele for that locus.

#### Parameters for Majority Voting Crossover

* Crossover probability, $p_c = 0.65$
* The number of parents to produce one child, $num\_parents = 4$

----

## Mutation Methods

### Gene-wise Mutation

Each bit ($x_i$) of chromosome $\vec{x}$  has equal but independent chance ($p_m$) to mutate a small amount.

----

## Termination Conditions

Simulate until one of the following has been met:

* Simulation reaches $t_{max}$ generations.
* Population fully converges.

----

## Local Installation

From the project root, run `pip install -e src/`.
