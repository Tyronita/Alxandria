# Chapter 5 — Multi-armed bandits (draft skeleton)

**Citation keys**: `lai1985asymptotically`, `auer2002finite`, `agrawal2012analysis`, `russo2018tutorial`.

## Model

Arms $a \in \{1,\dots,K\}$; rewards bounded in $[0,1]$ i.i.d. given $a$. Policy $\pi$ chooses $A_t$ based on history.

### Regret

$$
\mathrm{Regret}_T = \sum_{t=1}^T \bigl(\mu^\star - \mu_{A_t}\bigr).
$$

### Lai–Robbins (inform)

Optimal policies must pull suboptimal arms at least logarithmically often under typical regularity—sets scaling expectations (`lai1985asymptotically`).

## UCB1 (sketch)

Index policy:

$$
A_t = \arg\max_a \hat{\mu}_a(t-1) + \sqrt{\frac{2\log t}{N_a(t-1)}}.
$$

Finite-time bound in `auer2002finite`.

## Thompson sampling

Maintain posterior $\pi_t$ over arm means; sample $\tilde{\mu}_a \sim \pi_t$, play $\arg\max_a \tilde{\mu}_a$ (`russo2018tutorial`).

## Bridge to evolution

Parent selection + stochastic mutation resembles **sequential resource allocation** among partially observed lineages—useful analogy, not literal equivalence—cite bandits formally (`lange2025shinka` uses bandits explicitly for LLM ensemble).

## Example box

Simulate $K=3$ Bernoulli arms with means $(0.5, 0.55, 0.8)$ for $T=500$; compare uniform exploration vs UCB table.
