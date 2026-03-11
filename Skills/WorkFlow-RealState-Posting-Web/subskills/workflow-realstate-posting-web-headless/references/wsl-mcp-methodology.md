# WSL MCP Browser Methodology (Headless Branch)

## Scope
- This file defines browser-task methodology for WSL `无头模式` only.
- It is the canonical place for WSL-side browser MCP execution guidance.

## Tool Selection Matrix
- Page-level diagnostics, network timeline, performance insight:
  - prefer `chrome-devtools` MCP.
- Long sequential interaction, robust form automation, scripted loops:
  - prefer `playwright` MCP.

## Standard Execution Loop
1. Open/navigate target page.
2. Capture textual snapshot.
3. Perform one atomic interaction.
4. Wait for expected text/state.
5. Capture snapshot again.
6. Repeat until acceptance criteria are satisfied.

## Evidence Contract
- Keep machine-readable evidence and visual evidence per run:
  - snapshots (`*.md` or tool-returned snapshot content),
  - screenshots (`*.png`),
  - optional network/performance exports where needed.
- Record failures with step number and observable mismatch; never silently skip.

## Reliability Rules
- Do not chain multiple interactions without intermediate state checks.
- Prefer stable, human-readable element anchors from snapshots.
- When selectors become unstable, re-snapshot and re-anchor; avoid hardcoded fragile paths.

## Exit Criteria
- Required user flow has deterministic reproduction steps.
- Final evidence set proves expected UI state.
