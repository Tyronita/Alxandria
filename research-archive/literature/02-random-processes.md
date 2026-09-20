# Chapter 2 — Random processes before biology (draft skeleton)

**Citation keys**: `ewens2004mathematical`, `durrett2008probability`, Wright–Fisher and Moran processes.

## First principles

### Wright–Fisher (neutral drift sketch)

Fix diploid population size $N$. Let allele frequency $X_t \in \{0,1/N,\dots,1\}$ under neutrality follow binomial sampling:

$$
X_{t+1} \sim \frac{1}{2N}\mathrm{Binomial}(2N, X_t).
$$

This is a finite-state Markov chain with absorbing states at $0$ and $1$. Mean stays fixed; variance builds until fixation—**genetic drift**.

### Moran process (continuous-time alternative)

Moran models swap identity events one-by-one; coalescent limits link to Kingman coalescent (`ewens2004mathematical`).

## Example box

Compute fixation probability starting from one mutant copy under selective advantage—sketch diffusion approximation scales.

## Narrative bridge

These processes formalize **why finite populations need exploration**: drift can erase informative variation unless selection pressure or population structure intervenes—preview Island Models / QD archives (`mouret2015illuminating`).

## Figures

- TikZ: Wright–Fisher transition diagram for small $N$.
