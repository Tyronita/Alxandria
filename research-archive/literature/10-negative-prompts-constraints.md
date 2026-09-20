# Chapter 10 — Negative prompts as constraints (draft skeleton)

**Citation keys**: `ho2022classifier`, `raffel2020exploring` (T5 framing), plus optimization texts via `deb2002fast` for constrained MOO analogy.

## Precise terminology

- **Diffusion / classifier-free guidance**: negative prompts steer conditional expectations (`ho2022classifier`).
- **LLM steering**: negation in natural language is **not** a linear operator in latent space—methods range from logit bias to constrained decoding.

## Evolutionary analogues

- Penalty objectives $f(x) + \lambda g(x)$.
- Constrained MAP-Elites: feasibility per niche (`deb2002fast` for Pareto framing).

## Example box

CFG-style guidance equation sketch:

$$
\epsilon_\theta(z_t, c) \leftarrow (1+w)\epsilon_\theta(z_t, c) - w \epsilon_\theta(z_t, \emptyset)
$$

with caveats about scheduler and training assumptions (`ho2022classifier`).

## Thesis caution

“Truly negative prompts” must be defined operationally—otherwise readers confuse diffusion jargon with RL/Evo penalties.
