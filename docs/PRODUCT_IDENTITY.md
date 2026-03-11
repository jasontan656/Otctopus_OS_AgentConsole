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

## Public Narrative

Recommended positioning:

> Octopus OS is a natural-language-driven multi-agent console.  
> It treats skills as capability units and composition as the operating model, allowing individuals to progressively build a personalized intelligent assistant system.

## Internal Narrative

The following facts still remain true internally:

- this repository is still the single editable source for the skill core
- skill changes still need to be pushed into `~/.codex/skills`
- public product surfaces must not be pushed into the codex installation directory

## Current Phase

- release stage: `alpha`
- distribution strategy: `local-first`
- remote strategy: `the current remote still acts mainly as backup and traceability origin`
