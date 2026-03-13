---
doc_id: workflow_realstate_posting_web.subskills_workflow_realstate_posting_web_headed_contract
doc_type: topic_atom
topic: Contract Header
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

---

## Contract Header
- `contract_name`: `workflow_realstate_posting_web_subskills_workflow_realstate_posting_web_headed_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

name: workflow-realstate-posting-web-headed
description: Headed branch for real-estate posting web execution under `有头模式`, using Windows visible browser runtime and HouseSale as the only asset root.
---

# WorkFlow-RealState-Posting-Web — Headed Mode

## Goal
- Provide a dedicated headed branch for房源发布网页自动化。
- Keep Windows visible browser execution as a browser dependency, not as this skill family's generic concern.
- Standardize publish workflow on `HouseSale` assets and evidence.

## Browser Runtime Dependency
- Before running this branch, complete headed bridge setup from:
  - `$CODEX_HOME/skills/Meta-Agent-Browser/references/windows-headed-bridge.md`
- If the Windows bridge is unavailable, return `WINDOWS_MCP_BRIDGE_UNAVAILABLE`.

## Branch Status
- This branch runs on Windows-side MCP with Edge-visible verification when required.
- Default bridge server for headed mode: `win_chrome_devtools`.
- Runtime policy: fast-start first, recovery only when fast-start fails.

## Window Lifecycle Contract (Hard)
- Do not open a new window by default for every new task.
- Always reuse existing page/window first.
- When creating a new page is necessary, capture lifecycle handles immediately.
- Required lifecycle fields for each run:
  - `mcp_server`: `win_chrome_devtools`
  - `entry_page_id`
  - `opened_page_ids`
  - `close_required`
  - `closed_verified`

## Core Workflow
1. Confirm `有头模式` route selected.
2. Validate Windows bridge readiness via `Meta-Agent-Browser` bridge doc.
3. Enumerate existing handles first:
   - `list_pages`
4. Capture `entry_page_id` from selected page.
5. Reuse existing handle when possible.
6. Only when a new handle is required:
   - create it (`new_page`)
   - append `page_id` into `opened_page_ids`
7. Perform publish interactions by latest element refs.
8. Re-snapshot after navigation or major DOM updates.
9. Capture screenshots/traces/network evidence for acceptance when requested.
10. Close handles only if task explicitly requires close.
11. Verify closure:
   - `list_pages` must no longer contain each `opened_page_id`

## HouseSale Asset Root (Hard)
- For house-listing tasks in headed mode, use this root only:
  - `/home/jasontan656/AI_Projects/Human_Work_Zone/HouseSale`
- Listing payload source:
  - `listings/active/<property_id>.yaml`
- Media source:
  - `assets/properties/<property_id>/images/`
- Do not pull listing payload from chat text when the same fields already exist in HouseSale assets.

## Fixed Publish Workflow (Headed / HouseSale)
1. Resolve property payload from `HouseSale/listings/active`.
2. Resolve image assets from `HouseSale/assets/properties/<property_id>/images`.
3. Execute OnePropertee publish workflow (currently stable for live activation).
4. Execute Facebook Marketplace workflow when task requires Facebook同步发布。
5. Persist run evidence to `HouseSale/execution_logs`.
6. Update platform workflow YAML evidence blocks for active platforms only.

## Required Reference
- `references/house-sale-headed-workflow.md`
- `$CODEX_HOME/skills/Meta-Agent-Browser/references/windows-headed-bridge.md`

## Guardrails
- Always snapshot before using refs.
- If lifecycle fields are missing, stop with `WINDOW_HANDLE_NOT_CAPTURED`.
- Never start a second task window before previous task handles are closed or explicitly handed over.
- If browser identity is ambiguous, perform process-level proof before continuing.
- Keep this branch independent from `无头模式`; do not silently reroute.
