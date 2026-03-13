---
name: workflow-realstate-posting-web-headed
description: Routing reference for `有头模式`. Use this branch for Windows-side visual publish workflows.
doc_id: workflow_realstate_posting_web.references_subskills_realstate_posting_web_headed_route
doc_type: routing_doc
topic: WorkFlow-RealState-Posting-Web — Headed Branch Router
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# WorkFlow-RealState-Posting-Web — Headed Branch Router

## Branch Intent
- Execute房源发布网页任务 through Windows-side visible browser runtime when desktop interaction is required.
- Use `HouseSale` as the canonical asset and evidence root.
- Reuse Windows headed bridge methodology from `Meta-Agent-Browser`.
- Keep the branch focused on publish workflow orchestration, evidence, and asset discipline.

## Route Target (Hard)
- `subskills/workflow-realstate-posting-web-headed/CONTRACT.md`

## Browser Runtime Dependency
- Load browser bridge setup from:
  - `$CODEX_HOME/skills/Meta-Agent-Browser/references/windows-headed-bridge.md`

## Branch Boundary
- This branch is independent from the WSL headless workflow.
- Do not reuse headless-branch commands as a substitute for headed-branch contracts.
