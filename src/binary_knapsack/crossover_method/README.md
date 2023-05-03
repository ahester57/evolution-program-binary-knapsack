
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
