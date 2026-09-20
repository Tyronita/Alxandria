# Chapter 8 — LLMs as mutation operators (draft skeleton)

**Citation keys**: `lange2025shinka`, `romera2024mathematical`, `hu2025adas`.

## ShinkaEvolve mechanisms (cite precisely)

1. **Parent sampling** balancing exploration/exploitation among archived programs.
2. **Code novelty rejection sampling** to avoid redundant mutations.
3. **Bandit-based LLM ensemble selection** (`lange2025shinka`).

## Related discovery systems

FunSearch / learned program patterns (`romera2024mathematical`). Compare scopes honestly—domains differ.

## Bridge to AutoImprove

See [autoimprove_mapping.md](autoimprove_mapping.md).

## Example box

Describe a minimal archive $\mathcal{A}_t$, novelty predicate $\mathrm{Nov}(p; \mathcal{A}_t)$, and bandit arms as LLM endpoints—pseudoalgorithm aligned with thesis TikZ figure.
