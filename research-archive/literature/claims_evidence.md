# Claims vs evidence ledger

Use this table while drafting to keep survey claims aligned with Tier A/B sources (see [literature_protocol.md](literature_protocol.md)).

| Claim | Intended tier | Primary key(s) in `thesis/references.bib` | Notes |
|-------|----------------|-------------------------------------------|-------|
| Holland introduced the canonical GA framework | A | `holland1975adaptation`, `goldberg1989genetic` | Historical framing |
| UCB1 achieves $O(\sqrt{KT\log T})$ regret (finite-time bound form varies) | A | `auer2002finite` | Quote exact theorem from source |
| Thompson sampling has Bayesian regret analyses under priors | A | `russo2018tutorial`, `agrawal2012analysis` | Separate Bayesian vs frequentist regret |
| MAP-Elites maintains an archive of elites across niches | A | `mouret2015illuminating` | |
| Gödel machine requires provable improvement | A | `schmidhuber2007godel` | Contrast with empirical validation |
| Darwin Gödel Machine uses empirical benchmarks | B | `zhang2025darwin` | Preprint at time of writing |
| ShinkaEvolve uses bandit LLM selection + novelty rejection | B | `lange2025shinka` | Preprint |
| ADAS meta-agent builds agents in code | A | `hu2025adas` | ICLR 2025 |
| Fisher’s “fundamental theorem” is widely misread | A | `fisher1930genetical`, surveys | Add caution subsection |
| Continual learning catastrophic forgetting is structural for fixed-capacity models | A | `zeno2024continual`, `delange2021continual` | |
