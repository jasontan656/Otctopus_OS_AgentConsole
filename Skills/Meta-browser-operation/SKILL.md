---
name: "Meta-browser-operation"
description: "Family index for browser-operation methodology. Use only for browser tasks or explicit invocation of this skill. Route with exactly one mode parameter: `无头模式` (WSL MCP flow) or `有头模式` (Windows MCP flow)."
---

# Meta-browser-operation — Family Index

## Purpose
- Provide one browser-methodology entrypoint for this workspace.
- Keep two execution branches physically isolated:
  - `无头模式` branch for WSL MCP usage.
  - `有头模式` branch for Windows MCP usage.
- Headed branch canonical bridge is WSL dynamic gateway to Windows Edge debug port (`<WSL_GATEWAY_IP>:9333`) with fast-start-first policy and scripted recovery/reset fallback.
- Remove dispersed browser methodology from external sources and keep one maintainable source of truth here.
- Legacy `playwright` skill guidance is migrated into both branches, including CLI usage and headless/headed patterns.
- For house-listing browser operations, headed mode uses `HouseSale` as canonical asset root and fixed publish workflow source.

## Skill Layout Resolution (Hard)
- This is a family/router skill.
- Do not execute browser workflow directly from family root.
- Always route to one subskill reference first:
  - `references/subskills/meta-browser-operation-headless.md`
  - `references/subskills/meta-browser-operation-headed.md`

## Routing Parameters (Hard)
- Accept exactly one mode parameter:
  - `无头模式` -> route to headless subskill.
  - `有头模式` -> route to headed subskill.
- If both are present, stop with `MODE_CONFLICT`.
- If none is present:
  - when running in WSL context, default to `无头模式`;
  - otherwise ask user to provide one mode parameter explicitly.

## Decoupling Contract (Hard)
- `无头模式` and `有头模式` must remain independent branches.
- Do not share branch-specific scripts, commands, or state between the two branches.
- When a branch is selected, do not load the other branch unless the user explicitly switches mode.

## Subskill Reference Map
```yaml
subskill_reference_map:
  meta-browser-operation-headless: references/subskills/meta-browser-operation-headless.md
  meta-browser-operation-headed: references/subskills/meta-browser-operation-headed.md
```

## Trigger Scope
- Trigger only when:
  - the task is a browser task, or
  - user explicitly invokes `Meta-browser-operation`.
- For non-browser tasks, do not load this family.
