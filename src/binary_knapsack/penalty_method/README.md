
## Penalty Methods

### Absolute Penalty

Overage of any constraint leads to a zero fitness.

I chose this static penalty method because of its ease of use and to prove penalization works.

----

### Dynamic Penalty

As generations go by, the penalty for the same violation goes up.

$$Penalty(x) = (C * t)^{alpha} * \sum_j^m{f_j(x)^{beta}}$$

I chose this dynamic penalty method to test the claims that this method leads to premature convergence.

#### Parameters for Dynamic Penalty

* Scalar of generation number, $C = 0.5$
* Exponent of temporal harshening, $alpha = 2.0$
* Exponent of degree of violation, $beta = 2.0$

----
