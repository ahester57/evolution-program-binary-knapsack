
## Crossover Methods

### Single-Point Crossover

From two parents, randomly choose a cut-point and swap sides of each parent to create two children.

#### Parameters for Single-Point Crossover

* Crossover probability, $p_c = 0.65$

#### Results

```yaml
Stats over 30 runs:
Best Overall: (Score: 55.5352304177474 :: [0 1 0 1 1 0 1 1 0 1 1 0 0 0 0 0 0 0 0 0] => costing 39.49372651844115, 31)
Mean Best Fitness: 52.81255744849033
Standard Deviation of Best Fitness: 1.328633982424607
Mean Generation Best Was Acheived: 30.333333333333332
Standard Deviation of Generations: 14.25794125702897
```

----

### P-Uniform Crossover

From two parents and for each locus, randomly choose which parent to use at that locus. Choose the better parent with probability $p$. This process produces two children per set of parents.

#### Parameters for P-Uniform Crossover

* Crossover probability, $p_c = 0.65$
* Probability that the higher-performing parent donates their allele, $p = 0.5$

#### Results

```yaml
Stats over 30 runs:
Best Overall: (Score: 56.96086516860768 :: [0 0 1 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0] => costing 39.99900703419182, 14)
Mean Best Fitness: 53.27474215638246
Standard Deviation of Best Fitness: 1.5440293311694724
Mean Generation Best Was Acheived: 30.466666666666665
Standard Deviation of Generations: 11.315868896770096
```

----

### Majority Voting Crossover

From multiple parents and for each locus, deterministicly choose the most common allele for that locus.

#### Parameters for Majority Voting Crossover

* Crossover probability, $p_c = 0.65$
* The number of parents to produce one child, $parents = 4$

#### Results

```yaml
Stats over 30 runs:
Best Overall: (Score: 55.30528934249181 :: [0 0 0 1 1 0 0 1 0 1 1 0 0 1 0 0 0 0 0 0] => costing 39.63564280822889, 7)
Mean Best Fitness: 50.370564380480324
Standard Deviation of Best Fitness: 2.406028580696979
Mean Generation Best Was Acheived: 31.833333333333332
Standard Deviation of Generations: 14.758236871508586
```

----
