# An Evolution Program

## Objective

Solve the following optimization of the 0/1 Knapsack Problem

With bounds $$-7.0 \leq x_i \leq 4.0, i = 1, 2, 3$$

## Decoder

TODO: describe decoder

----

## Details of Genetic Algorithm

### GA Properties

* Chromosomes (input vector $\vec{s}$) made up of bit-string values, e.g. $1000101000110110111100110$
* Proportional selection, i.e. probability of advancement equal to fitness values over sum of all fitness values.
* Single-point crossover, i.e. from two parents, choose a cut-point and swap sides of each parent to create two children.
* Gene-wise mutation, i.e. each gbitene ($s_i$) has equal but indenpendent chance ($p_m$) to mutate a small amount.

### Parameters

* Dimensions, $d = 3$
* Population Size, $N = 30$
* Crossover probability, $p_c = 0.65$
* Mutation probability, $p_m = 0.05$

### Termination Condition

* Terminate simulation after $t_{max}$ generations, $t_{max} = 50$

----
