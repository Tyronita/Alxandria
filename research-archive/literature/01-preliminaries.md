# Chapter 1 — Preliminaries (draft skeleton)

**Citation keys**: probability foundations develop toward `sutton2018reinforcement` (appendices), optimization viewpoint `dejong2006evolutionary`.

## Learning objectives

- Interpret evolutionary search as repeated noisy evaluation of candidates drawn from a controlled stochastic policy (mutation/crossover/parent sampling).

## First principles

Let $(\Omega, \mathcal{F}, \mathbb{P})$ be a probability space. A **random fitness** $X_n$ for candidate $n$ may decompose into true performance plus measurement noise.

### Example box (finite horizon)

Consider minimizing unknown loss $\mu(a)$ for actions $a \in \{1,\dots,K\}$. Each trial observes $Y_t = \mu(A_t) + \epsilon_t$ with $\epsilon_t$ zero-mean bounded noise. Evolutionary algorithms that resample parents proportional to observed fitness inherit **selection noise** from both $\epsilon_t$ and finite population effects—connect forward to Chapter 5 (`auer2002finite`, `lai1985asymptotically`).

## Draft prose hooks

- Optimization as search: distinguish **representation**, **variation**, **selection**, **evaluation** (`back1993overview`).
- Markov viewpoint: under fixed operators, many EA variants induce a Markov chain over population states (`eiben2015introduction`).

## Figures

- TikZ: noisy evaluation funnel (candidate $\to$ sandbox $\to$ scalar score).

## Open questions

- When is treating evolution as Markov chain ergodic theory informative versus misleading for LLM mutation operators?
