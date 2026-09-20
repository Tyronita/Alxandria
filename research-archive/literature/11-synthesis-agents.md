# Chapter 11 — Synthesis: algorithm classes for self-evolving agents (draft skeleton)

This chapter expands the matrix in [synthesis_matrix.md](synthesis_matrix.md).

## Candidate classes

1. **Proof-gated self-modification** (`schmidhuber2007godel`).
2. **Empirical coding-agent evolution** (`zhang2025darwin`).
3. **Sample-efficient program evolution with LLM ensembles** (`lange2025shinka`).
4. **Meta-agent search over agent code** (`hu2025adas`).
5. **QD / novelty archives** (`mouret2015illuminating`, `lehman2011novelty`).
6. **Population-based hyperparameter / routing adaptation** (`jaderberg2017population`).

## Falsifiable predictions (examples)

- If evaluation noise dominates fitness differences, **bandit-style parent allocation** outperforms purely score-proportional selection (`auer2002finite`).
- If sandbox fidelity is low, empirical self-improvement **overfits** harness quirks—predict benchmark decay under distribution shift (`zeno2024continual` analog).
