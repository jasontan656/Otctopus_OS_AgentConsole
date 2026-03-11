# Octopus OS

Octopus OS is a natural-language-driven multi-agent console.

This repository is the product foundation for Octopus OS. It has two responsibilities at the same time:

- Public product surface: positioning, installation model, workspace mirror, and product-facing documentation.
- Internal skill source of truth: the skill core still evolves here first and can still be pushed into `~/.codex/skills`.

## Current Status

- Stage: Alpha
- Intended use: learning, testing, and trial runs
- Not recommended yet for critical production workflows

## How To Read This Repository

This is not just a generic skill mirror.

A better model is:

- Skill directories: the execution core of Octopus OS
- `skill-mirror-to-codex`: the internal bridge that pushes skill roots into `~/.codex/skills`
- `docs/` and `product_tools/`: product surfaces that must stay outside the codex installation directory
- Git history: an externalized product iteration log

## Hard Boundaries

- Product-facing files may evolve here, but they must not pollute `~/.codex/skills`
- Skill roots must remain pushable through `skill-mirror-to-codex`
- Install and cleanup must stay manifest-driven instead of using guess-based deletion

## Entry Documents

- `docs/PRODUCT_IDENTITY.md`
- `docs/SYNC_BOUNDARY.md`
- `docs/INSTALL_AND_CLEANUP_MODEL.md`
- `docs/PRODUCT_ITERATION_LOGGING.md`

## Directory Transition

The product engineering name is now `octopus-os-agent-console`.

For compatibility with existing runtime contracts and scripts, the workspace still keeps a legacy entry alias named `Codex_Skills_Mirror`. That alias exists only as a compatibility surface and no longer defines the product identity of this repository.
