---
name: "WorkFlow-RealState-Posting-Web"
description: "Family index for real-estate posting web automation. Route with exactly one mode parameter: `无头模式` or `有头模式`."
---

# WorkFlow-RealState-Posting-Web

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
  - `references/subskills/workflow-realstate-posting-web-headless.md`
  - `references/subskills/workflow-realstate-posting-web-headed.md`

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
  workflow-realstate-posting-web-headless: references/subskills/workflow-realstate-posting-web-headless.md
  workflow-realstate-posting-web-headed: references/subskills/workflow-realstate-posting-web-headed.md
```

## Trigger Scope
- Trigger only when:
  - the task is a real-estate posting web automation task, or
  - user explicitly invokes `WorkFlow-RealState-Posting-Web`
- For generic browser tasks without posting workflow intent, do not load this family directly; route from `Meta-Agent-Browser` first.
