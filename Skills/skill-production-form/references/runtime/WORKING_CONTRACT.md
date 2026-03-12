# Skill-Production-Form Working Contract

## Purpose
- This file is the markdown audit surface for `WORKING_CONTRACT.json`.
- The machine-readable contract remains the runtime rule source.

## Core Role
- Keep the console directory continuously available as a product-shaped skill-management surface.
- Preserve a local markdown design history for skills-as-console productization decisions.
- Provide a stable handoff layer between current console product-form work and later GitHub-facing release narratives.

## Current Console Focus
- Brand: `Octopus OS`
- Engineering repository: `octopus-os-agent-console`
- Console root: `Skills/`
- Positioning: console directory maintained as the product surface for the governed skill stack
- Current phase: continuous console productization around the Skills directory
- Source-of-truth boundary: edit in the product repo mirror first, then sync to `~/.codex/skills`
- Deployment boundary: the Codex installation directory is a governed deployment surface, not the authoring surface

## Logging Rule
- Read the current console intent before making new console productization decisions.
- Read the latest local iteration log before extending an existing design line.
- The active local iteration log now lives at `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form/ITERATION_LOG.md`.
- `references/runtime/ITERATION_LOG.md` is now only a legacy seed snapshot for first-run migration and must not receive new entries.
- Append a local log entry whenever a real console boundary, naming, or workflow decision is made.
- Do not use the local log for trivial command noise.

## Runtime And Output Roots
- Runtime observability root: `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form`
- Result root: `/home/jasontan656/AI_Projects/Codex_Skills_Result/skill-production-form`
- Current active runtime artifact: the iteration log markdown under the runtime root.
- Current default result policy: this skill does not emit file artifacts beyond the runtime log; future file artifacts must accept an explicit target path or default under the governed result root.

## Migration Rule
- If the governed runtime log does not exist yet, seed it from `references/runtime/ITERATION_LOG.md`.
- After seeding, all new log appends must stay in the runtime root.
- Keep the repo-side seed file readable for audit and bootstrap, but treat it as immutable history input rather than the active log sink.

## Future Switch
- This skill remains the continuity layer for console productization.
- When the console product form becomes stable enough, the main release-facing narrative can gradually move back to GitHub commits and public-facing logs.
