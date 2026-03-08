---
name: meta-browser-operation-headed
description: Methodology branch for Windows-side browser execution under `有头模式`, using Windows Edge via `win_chrome_devtools` as the default headed runtime.
---

# Meta-browser-operation — Headed Mode (Windows MCP)

## Goal
- Provide a dedicated branch for Windows desktop browser workflows.
- Standardize headed execution on Windows Edge.
- Keep Windows bridge configuration and verification contract in one place for long-term maintenance.
- Provide fixed publish workflow for house-listing tasks using HouseSale as the only asset root.

## Branch Status
- This branch runs on Windows-side MCP with Edge as default browser.
- Default bridge server for headed mode: `win_chrome_devtools`.
- Stable runtime contract (validated): MCP connects through WSL dynamic gateway to Windows Edge debug endpoint `http://<WSL_GATEWAY_IP>:9333`.
- Runtime policy: fast-start first, recovery only when fast-start fails.

## Canonical Runtime Setup (Required)
Keep existing WSL-local servers unchanged. Use a wrapper script to resolve dynamic WSL gateway, then keep this headed block in `~/.codex/config.toml`:

1. Create/maintain wrapper script `~/.codex/bin/win-chrome-devtools-mcp.sh`:

```bash
#!/usr/bin/env sh
set -eu
GW=$(ip route | awk '/default/ {print $3; exit}')
exec /mnt/c/Windows/System32/cmd.exe /c "C:\\Users\\HP\\.mcp-win\\node_modules\\.bin\\chrome-devtools-mcp.cmd" --browserUrl "http://$GW:9333" "$@"
```

2. Use this MCP config:

```toml
[mcp_servers.win_chrome_devtools]
type = "stdio"
command = "/home/jasontan656/.codex/bin/win-chrome-devtools-mcp.sh"
startup_timeout_ms = 180000
```

Before headed tasks, use fast-start first:

```bash
cmd.exe /c "powershell -NoProfile -Command \"Start-Process -FilePath 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe' -ArgumentList '--remote-debugging-port=9333','--user-data-dir=C:\\Users\\HP\\AppData\\Local\\EdgeMCPProfile','--new-window','about:blank'\""
```

If x86 path is missing, fallback to `C:\Program Files\Microsoft\Edge\Application\msedge.exe`.

## Preflight Verification (Required)
```bash
codex mcp get win_chrome_devtools
cmd.exe /c "C:\Users\HP\.mcp-win\node_modules\.bin\chrome-devtools-mcp.cmd --version"
cmd.exe /c "powershell -NoProfile -Command \"Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 9333 -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess\""
cmd.exe /c "powershell -NoProfile -Command \"Get-Process -Id <OwningProcessPID> | Select-Object Id,ProcessName,Path\""
GW=$(ip route | awk '/default/ {print $3; exit}')
curl "http://$GW:9333/json/version"
```
Expected:
- `win_chrome_devtools` is enabled.
- port `9333` is listening.
- owner process is `msedge.exe`.
- WSL curl reaches `/json/version` and response contains `Edg/`.

## Failure Escalation Ladder (Hard)
1. Level-1 (default): fast-start Edge debug + run preflight checks.
2. Level-2: restart Edge debug once and re-run preflight.
3. Level-3: run scripted recovery/reset from `references/windows-mcp-bridge.md`.
4. Only when Level-3 fails, return `WINDOWS_MCP_BRIDGE_UNAVAILABLE`.

## Window Lifecycle Contract (Hard)
- Do not open a new window by default for every new task.
- Always reuse existing page/window first.
- When creating a new page is necessary, capture lifecycle handles immediately.
- Required lifecycle fields for each run:
  - `mcp_server`: `win_chrome_devtools`
  - `entry_page_id` (selected page at start)
  - `opened_page_ids` (list, may be empty)
  - `close_required` (`true|false`, task-driven)
  - `closed_verified` (`true|false`)

## Core Workflow
1. Confirm `有头模式` route selected.
2. Complete preflight verification.
3. Use `win_chrome_devtools` for interaction loops.
4. Enumerate existing handles first:
   - `list_pages`
5. Capture `entry_page_id` from selected page.
6. Reuse existing handle when possible:
   - navigate existing page instead of opening a new one.
7. Only when a new handle is required:
   - create it (`new_page`),
   - append `page_id` into `opened_page_ids` immediately.
8. Perform interactions by latest element refs.
9. Re-snapshot after navigation or major DOM updates.
10. Capture screenshots/traces/network evidence for acceptance when requested.
11. Close handles only if task explicitly requires close:
   - close only `opened_page_ids`, never mass-close all pages.
12. Verify closure:
   - `list_pages` must no longer contain each `opened_page_id`.
13. If closure verification fails, run fallback cleanup defined in `references/windows-mcp-bridge.md`.

## Recovery And Reset (Hard)
- Recovery/reset is a fallback path, not default path.
- Use one-click recovery/reset in `references/windows-mcp-bridge.md` only when fast-start preflight fails or bridge is unstable:
  - Recovery: rebuild Edge debug + optional bridge rules + self-check.
  - Reset: clean previous 9333 bridge state first, then run recovery.
  - WSL fix: rewrite wrapper/config to dynamic gateway contract.
- Do not ad-hoc patch config manually before running the scripted recovery/reset path.

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
- `references/windows-mcp-bridge.md`
- `references/house-sale-headed-workflow.md`

## Guardrails
- Always snapshot before using refs.
- If bridge server is missing or disabled, return `WINDOWS_MCP_BRIDGE_UNAVAILABLE`.
- If lifecycle fields are missing, stop with `WINDOW_HANDLE_NOT_CAPTURED`.
- Never start a second task window before previous task handles are closed or explicitly handed over.
- If browser identity is ambiguous, perform process-level proof (`Get-NetTCPConnection` + `Get-Process`) before continuing.
- Keep this branch independent from `无头模式`; do not silently reroute.
