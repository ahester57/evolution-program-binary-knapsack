
## Selection Mechanisms

### Proportional Selection

An individual's probability of advancement equal to fitness score over sum of all fitness scores.

$$P(x_i) = f(x_i) / \sum_j^N{f(x_j)}$$

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 56.96086516860768 :: [0 0 1 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0] => costing 39.99900703419182, 32)
Mean Best Fitness: 53.09012691182008
Standard Deviation of Best Fitness: 1.4157700470325698
Mean Generation Best Was Acheived: 30.3
Standard Deviation of Generations: 12.607273033187365
```

----

### Truncation Selection

The top $\tau\%$ are selected for advancement. The next generation
is sampled uniformly random with replacement from the top $\tau\%$.

#### Parameters for Truncation Selection

* Top tau, $\tau = 0.4$

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 56.96086516860768 :: [0 0 1 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0] => costing 39.99900703419182, 39)
Mean Best Fitness: 51.930860569359396
Standard Deviation of Best Fitness: 5.591743945371317
Mean Generation Best Was Acheived: 26.866666666666667
Standard Deviation of Generations: 16.390512160664443
```

----

### Deterministic Tournament Selection

Pick two individuals from the current population uniformly randomly with replacement.  
Advance the chromosome $\vec{x}$ with the better fitness score.  
Repeat $N$ times.

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 55.5352304177474 :: [0 1 0 1 1 0 1 1 0 1 1 0 0 0 0 0 0 0 0 0] => costing 39.49372651844115, 19)
Mean Best Fitness: 49.19210281339055
Standard Deviation of Best Fitness: 8.154572784009153
Mean Generation Best Was Acheived: 24.666666666666668
Standard Deviation of Generations: 17.793881595150122
```

----

### Stochastic Tournament Selection

Same as deterministic tournament selection, except the worse chromosome $\vec{x}$ advances
with a typically small random chance.

#### Parameters for Stochastic Tournament Selection

* Probability of the higher performer winning, $prob = 0.9$

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 56.96086516860768 :: [0 0 1 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0] => costing 39.99900703419182, 32)
Mean Best Fitness: 46.870285204235365
Standard Deviation of Best Fitness: 5.924614709499177
Mean Generation Best Was Acheived: 13.533333333333333
Standard Deviation of Generations: 16.036901889773546
```

----

### Linear Ranking Selection

Each chromosome $\vec{x}$ is ranked from best to worst based on fitness score.  
An individual's probability of advancement is proportional to its rank.

#### Parameters for Linear Ranking Selection

* Expected # of copies of best $\vec{x}$, $max = 1.2$

#### Results

```
Stats over 30 runs:
Best Overall: (Score: 54.89214401149931 :: [0 1 1 1 1 0 0 1 0 1 0 0 0 1 0 0 0 0 0 0] => costing 39.40230129792615, 4)
Mean Best Fitness: 47.97313785058804
Standard Deviation of Best Fitness: 2.9990674396662595
Mean Generation Best Was Acheived: 22.133333333333333
Standard Deviation of Generations: 15.622064168633058
```

----
