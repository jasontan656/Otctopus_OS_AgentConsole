---
doc_id: skillsmanager_production_form.references_runtime_working_state
doc_type: topic_atom
topic: SkillsManager-Production-Form Working Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# SkillsManager-Production-Form Working Contract

## Purpose
- This file is the markdown audit surface for `WORKING_STATE.json`.
- The machine-readable contract remains the runtime rule source.

## Core Role
- Keep the console directory continuously available as a product-shaped skill-management surface.
- Preserve a local markdown design history for skills-as-console productization decisions.
- Provide a stable handoff layer between current console product-form work and later GitHub-facing release narratives.
- When console productization touches rootfile-managed external files, declare the boundary here but route the actual body maintenance to `$Meta-RootFile-Manager`.
- Keep the product narrative aligned around an AI-native, customizable personal-assistant methodology rather than a generic skill dump.

## Current Console Focus
- Brand: `Octopus OS`
- Engineering repository: `Otctopus_OS_AgentConsole`
- Console root: `Skills/`
- Positioning: console directory maintained as the product surface for the governed skill stack
- Current phase: continuous console productization around the Skills directory
- Product thesis: build a stronger personal assistant by continuously adding atomic skills, governance rules, workflows, and tool contracts
- Behavior goal: progressively move more agent behavior under governed skills, workflows, and tool contracts instead of leaving large behavior surfaces implicit
- Runtime strategy: rely on `GPT-5.4` with `high reasoning effort` plus `Codex CLI` native capabilities, keep token cost low, and move durable behavior into skills instead of prompt-heavy orchestration
- Evolution target: support daily development and broader personal work through multi-agent workflows, then continue toward richer multi-agent team collaboration
- Source-of-truth boundary: edit in the product repo mirror first, then sync to `~/.codex/skills`
- Deployment boundary: the Codex installation directory is a governed deployment surface, not the authoring surface
- Rootfile governance boundary: rootfile-managed files must not be directly edited from this skill; use `$Meta-RootFile-Manager` for their governed body updates
- Release split: one slower-moving release repo and one fast-moving dev repo can coexist as separate public surfaces
- Collaboration boundary: suggestions are welcome, code collaboration is currently closed, and disabled skills should be treated as incomplete and not recommended for normal use
- Usage boundary: current positioning is for learning, local reuse, and testing only, with no commercial-use allowance in the product narrative
- Maintenance identity: the project is maintained and developed by AI rather than human code contribution

## Logging Rule
- Read the current console intent before making new console productization decisions.
- Read the latest local iteration log before extending an existing design line.
- The active local iteration log now lives at `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md`.
- `references/runtime/ITERATION_LOG.md` is now only a legacy seed snapshot for first-run migration and must not receive new entries.
- Append a local log entry whenever a real console boundary, naming, or workflow decision is made.
- Do not use the local log for trivial command noise.

## Runtime And Output Roots
- Runtime observability root: `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form`
- Result root: `/home/jasontan656/AI_Projects/Codex_Skills_Result/SkillsManager-Production-Form`
- Current active runtime artifact: the iteration log markdown under the runtime root.
- Current default result policy: this skill does not emit file artifacts beyond the runtime log; future file artifacts must accept an explicit target path or default under the governed result root.

## Migration Rule
- If the governed runtime log does not exist yet, seed it from `references/runtime/ITERATION_LOG.md`.
- After seeding, all new log appends must stay in the runtime root.
- Keep the repo-side seed file readable for audit and bootstrap, but treat it as immutable history input rather than the active log sink.

## Future Switch
- This skill remains the continuity layer for console productization.
- When the console product form becomes stable enough, the main release-facing narrative can gradually move back to GitHub commits and public-facing logs.
