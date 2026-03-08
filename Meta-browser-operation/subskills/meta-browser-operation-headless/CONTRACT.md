---
name: meta-browser-operation-headless
description: Methodology for browser tasks in WSL under `无头模式`, including full Playwright CLI guidance (headless/headed), browser workflow patterns, and MCP-first execution guardrails.
---

# Meta-browser-operation — Headless Mode (WSL MCP)

## Goal
- Run browser tasks reliably in WSL.
- Keep Playwright professional guidance and CLI usage in this branch after migration from legacy `playwright` skill.

## Preconditions
- Runtime is WSL.
- MCP tools for `chrome-devtools` and/or `playwright` are installed and callable.
- `npx` is available for the branch-local Playwright CLI wrapper.

## Prerequisite Check (Required)
Before proposing wrapper commands:

```bash
command -v npx >/dev/null 2>&1
```

If missing, require Node.js/npm installation first.

## Branch-Local Wrapper Path
```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/Meta-browser-operation/subskills/meta-browser-operation-headless/scripts/playwright_cli.sh"
```

## Playwright Quick Start
Headed run:
```bash
"$PWCLI" open https://playwright.dev --headed
"$PWCLI" snapshot
"$PWCLI" click e15
"$PWCLI" type "Playwright"
"$PWCLI" press Enter
"$PWCLI" screenshot
```

Headless run:
```bash
"$PWCLI" open https://example.com
"$PWCLI" snapshot
"$PWCLI" click e3
"$PWCLI" snapshot
```

## Core Workflow (MCP + CLI)
1. Select primary tool:
   - `chrome-devtools` for inspection/network/performance debugging.
   - Playwright CLI wrapper for repeatable interaction loops.
2. Snapshot before first interaction:
   - `chrome-devtools`: `take_snapshot`
   - Playwright CLI: `snapshot`
3. Execute interaction loop:
   - navigate -> snapshot -> click/fill/type -> wait -> snapshot
4. Collect evidence:
   - screenshots for visual proof;
   - snapshots for structural proof.
5. Store artifacts:
   - `<WorkspaceRoot>/ChangeLog/BrowserTests/consumers/<consumer_id>/runs/<run_id>/`

## Snapshot Refresh Rules
Refresh snapshot after:
- navigation;
- modal/menu open-close;
- significant DOM updates;
- tab switch.

If element refs become stale, snapshot again before retry.

## Required References
- `references/wsl-mcp-methodology.md`
- `references/playwright-cli.md`
- `references/playwright-workflows.md`

## Guardrails
- Always snapshot before using element refs (`e12` style).
- Prefer explicit CLI commands; avoid `eval`/`run-code` unless necessary.
- Use `--headed` when visual verification helps.
- Keep this branch independent from `有头模式`; do not import Windows branch runtime assumptions.
