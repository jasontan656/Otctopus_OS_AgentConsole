---
name: WorkFlow-RealState-Posting-Web
description: 'Family index for real-estate posting web automation. Route with exactly one mode parameter: `无头模式` or `有头模式`.'
metadata:
  doc_structure:
    doc_id: workflow_realstate_posting_web.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the WorkFlow-RealState-Posting-Web skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# WorkFlow-RealState-Posting-Web

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/WorkFlow-RealState-Posting-Web/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## Purpose
- Provide one workflow entrypoint for房源发布类网页自动化。
- Keep two execution branches physically isolated:
  - `无头模式` branch for WSL browser execution
  - `有头模式` branch for Windows visual publish execution
- Keep domain focus on real-estate posting, not generic browser methodology.
- Reuse browser infrastructure from `Meta-Agent-Browser` instead of re-embedding generic browser runtime guidance here.
- Keep `HouseSale` as the canonical asset root for headed publish flows.

## Skill Layout Resolution (Hard)
- This is a family/router skill.
- Do not execute publish workflow directly from family root.
- Always route to one subskill reference first:
  - `references/subskills/realstate-posting-web-headless-route.md`
  - `references/subskills/realstate-posting-web-headed-route.md`

## Routing Parameters (Hard)
- Accept exactly one mode parameter:
  - `无头模式` -> route to headless subskill
  - `有头模式` -> route to headed subskill
- If both are present, stop with `MODE_CONFLICT`.
- If none is present:
  - when running in WSL context, default to `无头模式`
  - otherwise ask user to provide one mode parameter explicitly

## Decoupling Contract (Hard)
- `无头模式` and `有头模式` must remain independent branches.
- Do not share branch-specific scripts, commands, or state between the two branches.
- When a branch is selected, do not load the other branch unless the user explicitly switches mode.

## Browser Infrastructure Dependency
- Generic browser runtime selection now belongs to `Meta-Agent-Browser`.
- Before entering this workflow family, browser routing should follow:
  - `Meta-Agent-Browser/references/browser-total-entry.md`
- For Windows headed bridge setup, load:
  - `Meta-Agent-Browser/references/windows-headed-bridge.md`

## Subskill Reference Map
```yaml
subskill_reference_map:
  workflow-realstate-posting-web-headless: references/subskills/realstate-posting-web-headless-route.md
  workflow-realstate-posting-web-headed: references/subskills/realstate-posting-web-headed-route.md
```

## Trigger Scope
- Trigger only when:
  - the task is a real-estate posting web automation task, or
  - user explicitly invokes `WorkFlow-RealState-Posting-Web`
- For generic browser tasks without posting workflow intent, do not load this family directly; route from `Meta-Agent-Browser` first.
