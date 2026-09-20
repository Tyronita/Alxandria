# Chapter 7 — RL, evolution, continual learning (draft skeleton)

**Citation keys**: `sutton2018reinforcement`, `jaderberg2017population`, `silver2017mastering`, `such2017deep`, `kirkpatrick2017overcoming`, `delange2021continual`, `zeno2024continual`.

## Axes

| Mechanism | Strength | Typical failure |
|-----------|----------|-----------------|
| Gradient RL | high SNR in differentiable simulators | sample inefficiency / exploitability |
| Evolution | parallelism, non-differentiable objectives | credit assignment noise |
| Continual learning | plasticity vs stability tradeoff | forgetting (`kirkpatrick2017overcoming`) |

## PBT

Treat hyperparameters as evolving population members (`jaderberg2017population`).

## Neuroevolution contrast

Deep GA competes on RL benchmarks under certain conditions (`such2017deep`).

## Example box

Split MNIST-style toy—show EWC penalty derivation sketch (`kirkpatrick2017overcoming`).
