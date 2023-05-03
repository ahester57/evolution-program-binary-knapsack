
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
