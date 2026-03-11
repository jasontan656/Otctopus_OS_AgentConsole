# Product Identity

## Brand

- Product brand: `Octopus OS`
- Public subtitle: `Natural-Language-Driven Multi-Agent Console`
- Engineering repository name: `octopus-os-agent-console`

## What This Repository Is

This repository is the control plane and skill foundation for Octopus OS.

It is not:

- a private backup-only skill mirror
- a documentation-only project
- a stable public release

It is:

- the product-facing shell around the skill system
- the skill-based foundation for natural-language-driven agent work
- the future entry point for installation, cleanup, workspace mirroring, and product iteration records
- the evolving control plane for a solo operator who wants AI collaborators to eventually cover development, deployment, operations, marketing work, and multi-agent orchestration
- currently scoped to Codex as the supported runtime
- currently scoped to Codex CLI in the author's Codex CLI + VS Code environment
- currently scoped to GPT-5.4 high reasoning effort as the only supported model profile
- currently not planning adapters for other host environments

## Public Narrative

Recommended positioning:

> Octopus OS is a natural-language-driven multi-agent console.  
> It treats skills as capability units and composition as the operating model, allowing a solo operator to progressively build a personalized, end-to-end assistant system from zero to one.

## Internal Narrative

The following facts still remain true internally:

- this repository is still the single editable source for the skill core
- skill changes still need to be pushed into `~/.codex/skills`
- public product surfaces must not be pushed into the codex installation directory
- the product workspace must still carry the repository root `AGENTS.md` and `Skills/AGENTS.md` as part of the operating ecosystem
- root-level `~/.codex/skills/AGENTS.md` is an accidental artifact and must be removed
- non-Codex model environments are not supported by the install surface at this stage

## Current Phase

- release stage: `alpha`
- distribution strategy: `local-first`
- remote strategy: `the current remote still acts mainly as backup and traceability origin`
- current development rhythm: `extremely high-frequency iteration`
- reading warning: `commit-by-commit reading is not currently a useful way to understand the product`
