# Chapter 3 — Selection mathematics (draft skeleton)

**Citation keys**: `price1970selection`, `frank1995george`, `fisher1930genetical`.

## Price equation (structure)

Let traits have frequencies $p_i$ and fitness $w_i$. For arbitrary measurable trait $z$:

$$
\Delta \bar{z} = \mathrm{Cov}(w_i, z_i)/\bar{w} + \mathbb{E}[w_i \Delta z_i]/\bar{w}.
$$

Interpretation discipline: first term is **selection**; second term captures **transmission bias / mutation** (`price1970selection`).

## Fisher’s fundamental theorem (careful)

Modern readings emphasize scope conditions and common textbook misstatements (`frank1995george`). Thesis section must separate:

- **Theorem-class** population-genetics statements under explicit models.
- **Heuristic** analogies to optimization landscapes.

## Fitness landscapes

Encode genotypes $g \in \mathcal{G}$ with fitness $f(g)$. Local optima and epistasis motivate **crossover** and **QD** (`lehman2011novelty`, `mouret2015illuminating`).

## Example box

Construct a tiny $n=4$ hypercube landscape with **deceptive** global structure; show why greedy hill-climbing fails while archive methods may escape (`ecoffet2019go`).
