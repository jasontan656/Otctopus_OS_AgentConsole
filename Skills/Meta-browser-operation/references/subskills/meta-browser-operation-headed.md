---
name: meta-browser-operation-headed
description: Routing reference for `有头模式`. Use this branch for Windows-side MCP browser workflows.
---

# Meta-browser-operation — Headed Branch Router

## Branch Intent
- Execute browser tasks through Windows-side MCP runtime when desktop interaction is required.
- Use Windows Edge as the default headed browser runtime in this branch.
- Use `win_chrome_devtools` as the default headed server.
- Use WSL dynamic-gateway bridge mode as canonical path (`--browserUrl http://<WSL_GATEWAY_IP>:9333`).
- Use fast-start first (direct Edge debug start + preflight), then recovery/reset only as fallback.
- Follow handle-first lifecycle (`entry_page_id` + `opened_page_ids`) to prevent window leaks.
- For house-listing tasks, load fixed workflow and assets from `/home/jasontan656/AI_Projects/Human_Work_Zone/HouseSale`.
- Use scripted recovery/reset path for Windows bridge issues; do not hand-edit scattered config first.

## Route Target (Hard)
- `subskills/meta-browser-operation-headed/CONTRACT.md`

## Branch Boundary
- This branch is independent from the WSL headless workflow.
- Do not reuse headless-branch commands as a substitute for headed-branch contracts.
