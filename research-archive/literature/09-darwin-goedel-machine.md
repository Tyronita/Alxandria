# Chapter 9 — Darwin Gödel Machine (draft skeleton)

**Citation keys**: `schmidhuber2007godel`, `zhang2025darwin`, `hu2025adas`, benchmarks `jimenez2024swebench`.

## Gödel machine vs Darwin Gödel Machine

| Aspect | Gödel machine (`schmidhuber2007godel`) | DGM (`zhang2025darwin`) |
|--------|----------------------------------------|-------------------------|
| Gate for self-change | formal proof of improvement | empirical benchmark gains |
| Search | directed by theorem-proving machinery | evolutionary archive + coding agents |

## Open-ended archive

Non-zero parent sampling probability; stepping stones along lineage trees (`zhang2025darwin`).

## Safety narrative

Sandboxing, traceability—mirror engineering constraints in AutoImprove Docker/RunPod isolation.

## Example box

Walk through one iteration: select parent $\to$ propose feature $\to$ patch codebase $\to$ evaluate on SWE-bench subset $\to$ archive update—hypothetical numbers consistent with paper ranges, clearly labeled as illustrative.
