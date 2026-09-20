# AutoImprove ↔ ShinkaEvolve/DGM concepts

AutoImprove ([README.md](../README.md))forks Shinka-style evolution and adds RunPod, OpenRouter, Docker sandboxes, and a web portal. This note maps **claims** in `lange2025shinka` / `zhang2025darwin` to **modules** in this repository.

## Mutation operator (`autoimprove/core/evolution.py`)

- **`MutationOperator`** calls `LLMClient.generate` with a **mutation prompt** built from score + feedback (`MutationOperator.mutate`, `_build_mutation_prompt`). This corresponds to **LLM-as-mutation** in ShinkaEvolve, though Shinka documents additional machinery (novelty rejection, multi-LLM bandits).

## Evaluation (`autoimprove/core/evaluator.py`, `Orchestrator`)

- **`Evaluator`**: repeated runs, aggregation of scores, optional external eval scripts—maps to **fitness evaluation** / noisy measurement in evolutionary loops.
- **`Orchestrator._evaluate_candidate`**: writes candidate program to temp file; chooses **Docker** (`DockerSandbox.run_eval`) or **RunPod** path—implements **sandboxed execution** analogous to DGM safety emphasis (`zhang2025darwin`).

## Evolution engine (`EvolutionEngine`)

- **`_select_parents`**: sorts by `combined_score`, retains top half—**exploitation-heavy** parent selection.
- **`step`**: mutates each selected parent—generation loop core.
- **`crossover`**: optional LLM-based recombination—maps to **recombination** operators in program evolution literature.

## Configuration knobs (`EvolutionConfig`)

| Field | Role | Shinka/DGM analogy |
|-------|------|---------------------|
| `archive_enabled` | toggle archive behavior | DGM / Shinka archives |
| `novelty_detection` | enable novelty checks | Shinka novelty rejection |
| `num_islands` | island parallelism | exploration partitions |
| `llm_models` | ensemble endpoints | Shinka bandit LLM selection target |
| `max_api_cost` | budget | empirical gate like DGM compute limits |

## Gap analysis (honest)

Present AutoImprove code paths simplify several documented Shinka mechanisms—**bandit-based ensemble selection** and **code novelty rejection sampling** should be treated as **design targets** when extending this fork toward `lange2025shinka` parity.

## Darwin Gödel Machine alignment

DGM requires **self-edit of agent codebase** plus **benchmark validation**. AutoImprove modes (`repo_improve`, `kaggle`, `lean4`) instantiate **task-directed** evolution; achieving DGM-like **self-referential improvement** would require wiring evaluation to measure **the agent’s own editing capability** on held-out tasks—conceptually parallel to `zhang2025darwin`, not guaranteed by defaults.
