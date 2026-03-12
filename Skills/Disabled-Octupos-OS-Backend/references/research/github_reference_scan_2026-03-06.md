# GitHub Reference Scan for Octopus Backend Skill

## Goal

Use external reference projects to redesign OctopusOS backend skill from "artifact-complete" to "production-proof".

## Local Clone Root

`/home/jasontan656/AI_Projects/Human_Work_Zone/octopus_skill_reference_scan`

## Repositories

### 1. OpenSpec

- GitHub: `https://github.com/Fission-AI/OpenSpec`
- Local: `/home/jasontan656/AI_Projects/Human_Work_Zone/octopus_skill_reference_scan/OpenSpec`
- Borrow:
  - Schema-driven artifact graph instead of hard-coded package counts.
  - `proposal -> specs -> design -> tasks -> implement` modeled as dependency graph.
  - Separate `verify` step that checks completeness, correctness, and coherence against artifacts.
- Octopus mapping:
  - Replace "chapter coverage" with machine-readable clause graph.
  - Keep four explicit stages, but drive them from a stage schema with required inputs, outputs, and witnesses.
  - Preserve flexibility, but never allow stage completion without required downstream evidence bindings.

### 2. Spec Kit

- GitHub: `https://github.com/github/spec-kit`
- Local: `/home/jasontan656/AI_Projects/Human_Work_Zone/octopus_skill_reference_scan/spec-kit`
- Borrow:
  - Spec-first worldview: requirements are primary, code is expression.
  - `specify -> plan -> tasks -> implement` with optional `clarify`, `analyze`, `checklist`.
  - Task derivation from contracts, models, scenarios, and research artifacts.
- Octopus mapping:
  - Add a mandatory `clarify` sub-loop before the AI writes the construction plan when mother doc has unresolved operational blanks.
  - Generate packages from normalized requirement atoms, not section buckets.
  - Add post-plan checklist generation for ambiguity, contradiction, and missing acceptance coverage.

### 3. Specs CLI

- GitHub: `https://github.com/specs-cli/specs-cli`
- Local: `/home/jasontan656/AI_Projects/Human_Work_Zone/octopus_skill_reference_scan/specs-cli`
- Borrow:
  - DSPI chain: discovery, specification, staged construction planning, implementation.
  - Planning mode detection based on repository maturity.
  - Explicit rule that every task maps back to spec and success criteria.
- Octopus mapping:
  - Your requested four stages are correct, but stage 1 should be `mother_doc/discovery`, not just static writing.
  - Add "baseline mode" detection:
    - `empty_baseline`
    - `real_codebase`
    - `current_artifact_reuse_review`
  - Different modes should allow different tool sets and restore strategies.

### 4. Spec Kitty

- GitHub: `https://github.com/Priivacy-ai/spec-kitty`
- Local: `/home/jasontan656/AI_Projects/Human_Work_Zone/octopus_skill_reference_scan/spec-kitty`
- Borrow:
  - Mandatory interview gates with blocking states like `WAITING_FOR_DISCOVERY_INPUT`.
  - Research-first Phase 0 before task generation.
  - Work-package lanes and acceptance command with metadata + activity log.
  - ADR separation: architecture decisions are distinct from implementation details.
- Octopus mapping:
  - Introduce a blocking `NEEDS_INPUT` / `NEEDS_REAL_ENV` state instead of letting model invent missing infra.
  - Add explicit `research/evidence phase 0` when mother doc depends on external systems, protocols, or vendor constraints.
  - Keep stage 4 as `verification + evidence writeback`, but give it lane/state semantics and immutable acceptance metadata.
  - Split architecture contracts from per-run implementation docs so future replacement is precise.

### 5. GTPlanner

- GitHub: `https://github.com/OpenSQZ/GTPlanner`
- Local: `/home/jasontan656/AI_Projects/Human_Work_Zone/octopus_skill_reference_scan/GTPlanner`
- Borrow:
  - Determinism and composability as first-class design goals.
  - Reusable prefabs/modules instead of one giant prompt blob.
  - Flow engine structure for subflows such as construction planning, tool recommendation, and design.
- Octopus mapping:
  - Refactor Octopus skill into composable stage modules instead of one monolithic workflow contract.
  - Introduce reusable prefabs:
    - requirement atomizer
    - package derivation
    - infra witness verifier
    - behavior replay verifier
    - delivery report composer
  - Make "best backend terminal model" a stage config, not hidden prompt text.

## Direct Diagnosis of Octopus Skill

- Current core failure is not missing gates alone.
- The deeper problem is that Octopus still treats completion as "documents + gates + tests exist".
- It does not model:
  - requirement atoms as durable objects
  - task packages as traceable descendants of those atoms
  - real-world witnesses as exclusive completion proof
  - blocked states when environment truth is unavailable
  - architectural decisions as separate stable records

## Recommended Target Architecture

### Stage 1. Mother Doc / Discovery

- Input: raw mother doc plus repo/runtime baseline scan.
- Output:
  - normalized requirement atoms
  - ambiguity list
  - missing-env list
  - architecture decision candidates
- Hard rule:
  - no package generation until every atom has type, priority, dependency, acceptance form, and real witness type.

### Stage 2. Construction Plan

- Input: approved requirement atoms plus research artifacts.
- Output:
  - package graph
  - per-package acceptance checklist
  - per-package required witnesses
  - execution order and parallel groups
- Hard rule:
  - package count is emergent from graph size; never fixed by min/max numbers.

### Stage 3. Implementation

- Input: package graph, baseline mode, architecture constraints.
- Output:
  - real code
  - config
  - migrations
  - runtime scripts
  - requirement-linked tests
- Hard rule:
  - no stub service, in-memory authority source, or self-authored fake witness may satisfy completion.

### Stage 4. Verification / Evidence Writeback

- Input: running system plus external dependencies.
- Output:
  - external witness bundle
  - behavior replay traces
  - acceptance matrix by requirement atom
  - delivery report
- Hard rule:
  - stage complete only when every requirement atom has `implemented + tested + externally witnessed`.

## Concrete Changes Octopus Should Absorb

1. Replace section-level `source_requirement` with clause-level `requirement_atom_id`.
2. Add `witness_type` enum per atom:
   - `db_row`
   - `mq_message`
   - `redis_key`
   - `telegram_message`
   - `http_webhook`
   - `filesystem_artifact`
   - `human_interaction_trace`
3. Add `blocked_reason` states instead of fabricated pass reports.
4. Add `baseline_mode` router before restore or implementation.
5. Add phase-specific tool allowlists.
6. Add ADR-like architecture records for decisions that outlive one run.
7. Make tests assert requirement behavior, not package labels or `feature_id`.
8. Make final completion depend on requirement-atom acceptance matrix, not package summary.

## Why This Matters

The outside projects are not valuable because they are "better prompts". They are valuable because they turn fuzzy intent into durable artifacts with state transitions, dependency edges, and traceability. Octopus will keep drifting into pseudo-completion until its runtime model is changed at that level.
