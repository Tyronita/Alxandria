# Algorithm class recommendation matrix

Legend: **Eval** = cost per candidate evaluation; **Obs** = observability of true fitness; **Safe** = strength of sandbox; **Mod** = modularity of genome (program vs weights).

| Regime | Structure | Budget | Preferred class | Key assumptions | If violated |
|--------|-----------|--------|-----------------|-----------------|-------------|
| Differentiable simulator, smooth rewards | Low epistasis | Medium–high | PBT / RL (`jaderberg2017population`, `sutton2018reinforcement`) | Gradients informative | Evolved instability, exploitability |
| Black-box scores, parallelizable | Unknown landscape | High | ES / CMA-ES (`hansen2001completely`) | Stationary noise | Non-stationary benchmarks mislead |
| Discrete programs, test suites | Modularity in code | Medium | LLM mutation + archive (`lange2025shinka`) | Tests approximate goals | Goodharting tests |
| Self-referential agent code | Downstream = self-edit task | High | DGM-style empirical validation (`zhang2025darwin`) | Benchmark tracks self-improvement | Overfitting harness |
| Need stepping stones / diversity | Deceptive objective | Medium–high | QD / novelty (`mouret2015illuminating`, `lehman2011novelty`) | Descriptor captures diversity | Descriptor omitting critical axes |
| Streaming tasks, plasticity required | Distribution shift | Medium | Continual methods + replay/reg (`zeno2024continual`) | Task relatedness estimable | Negative transfer dominates |

## Falsifiable predictions

1. **Bandit allocation**: When candidate evaluations are noisy Bernoulli passes, policies approximating UCB/Thompson on parent lineages reduce variance of best-found fitness versus purely elite truncation after finite horizons (`auer2002finite`, `lange2025shinka`).
2. **Archive vs chain**: Maintaining archives beats greedy “latest-only” self-modification when destructive edits occur with non-zero probability (`zhang2025darwin` baseline narrative).
3. **QD descriptors**: MAP-Elites improves robustness on deceptive tasks **only if** behavior descriptors correlate with escape paths (`mouret2015illuminating`).
