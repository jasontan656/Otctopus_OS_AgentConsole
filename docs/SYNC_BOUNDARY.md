# Sync Boundary

## Core Principle

The Octopus OS repository now contains:

- the skill core
- the product facade
- product tooling

Only the skill core is allowed to flow into `~/.codex/skills`.

## Objects Allowed In The Codex Installation Directory

- top-level skill directories that contain `SKILL.md`
- the `.system/` system skill root

## Objects Forbidden From The Codex Installation Directory

- `README.md`
- `docs/`
- `product_tools/`
- `.git/`
- `.tooling_runtime/`
- any product-facing narrative, installation guide, branding text, or release helper assets

## Current Sync Strategy

`SkillsManager-Mirror-To-Codex` with `scope=all` now behaves as follows:

1. scan the repository root
2. discover only real syncable skill roots
3. run `rsync` per discovered skill root
4. never mirror the whole repository root directly into `~/.codex/skills`

## Why This Matters

- the product layer can evolve freely
- the codex installation directory stays execution-focused
- Git history can document product iteration without polluting downstream skill installs
