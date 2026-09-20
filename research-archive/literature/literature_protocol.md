# Literature survey protocol

This document defines how sources were selected for the thesis *Open-endedness — the beginning of unwritten worlds*, aligned with a **deep-narrow** scope (~50–70 references).

## Inclusion tiers

| Tier | Definition | Use in thesis |
|------|------------|----------------|
| **A** | Peer-reviewed books, journal articles, or major conference proceedings (ACM, IEEE, NeurIPS, ICML, ICLR, GECCO, etc.) | Primary claims, definitions, and historical narrative |
| **B** | Highly influential technical reports or **preprints** (arXiv, institutional reports) | Recent systems work where peer review is pending or supplementary; **explicitly labeled** in prose as preprint |

**Exclusion**: blog posts, forum threads, and non-archival slides unless they duplicate a primary citation already included.

## Seed clusters (anchors)

Each cluster starts from **canonical** works; expansion follows the snowball rule below.

1. **Evolutionary computation foundations**: genetic algorithms, evolution strategies, genetic programming; scalability and representation.
2. **Population genetics / selection mathematics** (as modeling vocabulary): Price equation, Fisher’s fundamental theorem (with careful interpretation), Wright–Fisher and Moran processes.
3. **Exploration–exploitation**: multi-armed bandits (lower bounds, UCB, Thompson sampling).
4. **Quality diversity and open-endedness**: novelty search, MAP-Elites, POET-style stepping stones, surveys on open-ended AI.
5. **Meta-optimization and RL intersection**: population-based training; evolutionary RL touchpoints.
6. **Continual learning**: catastrophic forgetting, replay, regularization; survey papers.
7. **Self-modifying AI**: Gödel machine (theoretical); empirical LLM agents that edit their own harness/code (Darwin Gödel Machine, related concurrent work).
8. **LLM-driven program evolution**: ShinkaEvolve; FunSearch/AlphaEvolve-class program search (high-level comparison only).

## Snowballing and stopping rules

For each cluster:

1. Add **direct citations** from anchor papers that define mechanisms we reuse (e.g., MAP-Elites grid, UCB index).
2. Add **surveys** where they subsume many primary papers (preferred over citing 20 overlapping empirical papers).
3. **Stop** adding to a cluster when:
   - a survey already covers the subtopic; or
   - marginal novelty **per added paper** drops (three consecutive additions fail to introduce a new mechanism or historical episode); or
   - cluster reaches **~12–18** sources.

**Global cap**: **50–70** total references.

## Claims vs evidence hygiene

- **Theorem-class statements** (regret bounds, impossibility results, Price equation structure): cite the original proof or a standard textbook treatment.
- **Heuristic analogies** (e.g., “evolution as bandit”): framed explicitly as analogy; cite formal bandit literature separately from biological metaphor.
- **Systems results** (e.g., benchmark percentages): cite the **primary** system paper and, where applicable, the **benchmark** paper.

## Version notes

Preprints are cited with arXiv identifiers in `thesis/references.bib` using the `eprint`/`archivePrefix` fields where appropriate. When a peer-reviewed version supersedes a preprint, the bibliography should be updated to the archival venue.
