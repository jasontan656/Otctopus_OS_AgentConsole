# Octopus OS

Octopus OS is a natural-language-driven multi-agent console.

It is being shaped for a solo operator building a complete AI collaboration stack from the ground up: development, deployment, operations, market work, workflow orchestration, multi-agent collaboration, and natural-language-driven execution.

This repository is the product foundation for Octopus OS. It has two responsibilities at the same time:

- Public product surface: positioning, installation model, workspace mirror, and product-facing documentation.
- Internal skill source of truth: the skill core still evolves here first and can still be pushed into `~/.codex/skills`.

## Current Status

- Stage: Alpha
- Intended use: learning, testing, and trial runs
- Not recommended yet for critical production workflows
- The repository currently changes at a very high pace, often every 10 to 15 minutes
- Commit-by-commit reading is not a meaningful way to learn the system yet; use the higher-level product documents instead

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
- The long-term target is a self-contained stack of skills and workflows owned by the product itself, reducing dependence on third-party skill installs and keeping AI behavior explicit, safe, and controllable

## Entry Documents

- `docs/PRODUCT_IDENTITY.md`
- `docs/OPERATOR_AND_SECURITY_MODEL.md`
- `docs/SYNC_BOUNDARY.md`
- `docs/INSTALL_AND_CLEANUP_MODEL.md`
- `docs/PRODUCT_ITERATION_LOGGING.md`

## Directory Transition

The product engineering name is now `octopus-os-agent-console`.
Internally, this repository still acts as the governed source that maps syncable skill roots into `~/.codex/skills`.
