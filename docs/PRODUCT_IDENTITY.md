# Product Identity

## Brand

- Product brand: `Octopus OS`
- Public subtitle: `Natural-Language-Driven Multi-Agent Console`
- Engineering repository name: `Otctopus_OS_AgentConsole`

## What This Repository Is

This repository is the control plane and skill foundation for Octopus OS.

It is not:

- a private backup-only skill mirror
- a documentation-only project
- a stable public release

It is:

- the product-facing shell around the skill system
- the skill-based foundation for natural-language-driven agent work
- the governed growth surface for progressively turning an agent into a stronger personalized assistant
- the future entry point for installation, cleanup, workspace mirroring, and product iteration records
- the evolving control plane for a solo operator who wants AI collaborators to eventually cover development, deployment, operations, marketing work, and multi-agent orchestration
- currently scoped to Codex as the supported runtime
- currently scoped to Codex CLI in the author's Codex CLI + VS Code environment
- currently scoped to GPT-5.4 high reasoning effort as the only supported model profile
- currently requiring a dedicated GitHub skill repository binding as part of installation
- currently not planning adapters for other host environments

## Public Narrative

Recommended positioning:

> Octopus OS is a natural-language-driven multi-agent console.  
> It treats skills as atomic capability units and governed composition as the operating model, allowing a solo operator to progressively build a personalized, end-to-end assistant system from zero to one.  
> The deeper direction is to keep giving the agent the governed skills, workflows, and tool contracts it still lacks, so more of its behavior becomes explicit, controllable, and reusable over time.

Public-facing facts that should stay aligned with that positioning:

- the project is published through a slower-moving release repository and a faster-moving dev repository
- the current public posture is for learning, local reuse, and testing rather than commercial deployment
- disabled skills should be treated as incomplete historical surfaces, not recommended default building blocks
- suggestions are welcome, but direct code collaboration is currently closed
- the current implementation and maintenance loop is AI-produced and AI-maintained

## Internal Narrative

The following facts still remain true internally:

- this repository is still the single editable source for the skill core
- skill changes still need to be pushed into `~/.codex/skills`
- the canonical install flow now provisions a dedicated Codex install root with an internal `console/`, `Codex_Skill_Runtime/`, `Codex_Skills_Result/`, and `Octopus_OS/` layout instead of attaching to an arbitrary pre-existing codex home
- public product surfaces must not be pushed into the codex installation directory
- the product workspace must still carry the repository root `AGENTS.md` and `Skills/AGENTS.md` as part of the operating ecosystem
- root-level `~/.codex/skills/AGENTS.md` is an accidental artifact and must be removed
- a GitHub skill repository binding is now part of the product operating prerequisites
- non-Codex model environments are not supported by the install surface at this stage

## Current Phase

- release stage: `alpha`
- distribution strategy: `local-first`
- public release shape: `slower release repo + faster dev repo`
- remote strategy: `the current remote still acts mainly as backup and traceability origin`
- current development rhythm: `extremely high-frequency iteration`
- reading warning: `commit-by-commit reading is not currently a useful way to understand the product`
