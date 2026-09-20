# Alxandria — Roadmap

Originally built as a Perplexity Hackathon prototype (£1000, London #3).
Now evolving into a full autonomous research harness for ML science agents.

---

## What Alxandria is becoming

A research harness that wraps **aira-dojo** (the parallel scaffold framework from
[AIRS-Bench](https://github.com/facebookresearch/airs-bench)) and extends it with:

- A **task registry** that includes AIRS-Bench's 20 tasks plus custom tasks
  (protein variant effect prediction, kernel generation, open-ended evolution)
- A **Perplexity-powered ideation layer** (from the original Alxandria backend)
  that generates hypotheses and literature context before the agent starts
- A **scaffold library** with One-Shot, Greedy (tree search), and ReAct modes
- **Persistent experiment tracking** — every run logged, scored, compared to SOTA

The thesis in `research-archive/` provides the theoretical foundation:
open-endedness, LLM program evolution, Darwin-Gödel machine, and the synthesis
that motivates this architecture.

---

## Phase 1 — Integrate aira-dojo as the execution backbone

**Goal:** replace the current FastAPI backend with an aira-dojo harness that can
run any AIRS-Bench task end-to-end.

Steps:
- [ ] Clone and install [aira-dojo](https://github.com/facebookresearch/aira-dojo)
      as a git subtree under `harness/aira-dojo/`
- [ ] Map Alxandria's `/api/research/task-spec` endpoint → aira-dojo task spec format
      (`project_description.md` + `metadata.yaml`)
- [ ] Wire the Perplexity Sonar literature search into the task spec generation
      (pre-populate `project_description.md` with SOTA context before agent launch)
- [ ] Run the 20 AIRS-Bench tasks through aira-dojo's One-Shot scaffold as a
      baseline, record normalized scores
- [ ] Surface results in the existing React frontend (ShipPage → results dashboard)

---

## Phase 2 — Add custom tasks from our own research

Tasks to add to the registry on top of AIRS-Bench's 20:

| Task | Metric | SOTA source |
|---|---|---|
| `ProteinVariantEffectESM2` | Spearman ρ (217 assays) | Notin et al. NeurIPS 2023, ρ=0.414 |
| `ProteinVariantEffectESMC` | Spearman ρ (217 assays) | TBD (our Track C) |
| `LewyGym` | Spearman ρ (PD proteins) | LewyGym benchmark |
| `KernelGenPallas` | fast_p speedup | PallasBench |
| `KernelGenJax` | speedup over baseline | JaxBench |

Each task follows the aira-dojo spec: `project_description.md`, `metadata.yaml`,
`prepare.py`, `evaluate.py`.

---

## Phase 3 — Scaffold improvements

Based on findings from the thesis (`research-archive/thesis/sections/`):

- [ ] **Greedy + LLM mutation** — tree-search scaffold with LLM-guided crossover
      (from `metashinka/mutation.py` in the archived Evolve codebase)
- [ ] **Multi-island evolution** — parallel populations with migration
      (from `metashinka/multi_island_run.py`)
- [ ] **Open-ended mode** — no fixed task, agent proposes its own hypotheses,
      evaluated against literature claims (`research-archive/literature/claims_evidence.md`)

---

## Phase 4 — Leaderboard and publication

- [ ] Submit Alxandria agent runs to AIRS-Bench leaderboard
      (current top: Greedy gpt-oss-120b @ 0.402 avg normalised score)
- [ ] Add custom tasks to a public leaderboard
- [ ] Write up methods + results as a short paper, building on the thesis

---

## Research archive

`research-archive/thesis/` — ACM-format paper on open-ended program evolution
(from the Evolve repo, preserved here). 14 sections: preliminaries → genetic
algorithms → Darwinian mathematics → MABs → open-endedness → RL/CL → LLM
program evolution → Darwin-Gödel machine → synthesis agents → ethics.

`research-archive/literature/` — 16 literature review notes covering the same arc.

These form the theoretical backbone for Phase 3 scaffold work.
