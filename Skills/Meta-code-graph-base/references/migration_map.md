# Migration Map

## Upstream Origin

- upstream project: `GitNexus`
- upstream core path used as migration base: `Human_Work_Zone/GitNexus/gitnexus`
- current vendored core path: `assets/gitnexus_core`
- current license boundary:
  - repository root content remains under the repo root license
  - vendored `gitnexus_core` keeps its separate upstream license and notice requirements
- current attribution requirement:
  - any public release or repository description must explicitly state that `Meta-code-graph-base` contains migrated and modified core code from `GitNexus`

## Retained Core

- `src/core/graph/*`
- `src/core/ingestion/*`
- `src/core/tree-sitter/*`
- `src/core/kuzu/*`
- `src/core/search/*`
- `src/core/augmentation/*`
- `src/core/wiki/*` as optional upstream reference, but it is not part of the governed public command surface
- `src/storage/*`
- `src/mcp/local/local-backend.ts`
- `src/mcp/resources.ts`
- `src/mcp/staleness.ts`
- `src/mcp/tools.ts`

## Rewritten / Patched

- `src/storage/repo-manager.ts`
  - runtime storage root now comes only from explicit `META_CODE_GRAPH_RUNTIME_ROOT`
- `src/cli/index.ts`
  - removed setup / serve / mcp / eval-server
  - added direct `detect-changes` / `rename` / `resource`
- `src/cli/analyze.ts`
  - removed AGENTS/CLAUDE context generation
  - removed `.gitignore` mutation
- `src/mcp/resources.ts`
  - converted to local resource views
  - removed setup resource
  - URI scheme moved to `codegraph://`

## Removed External Shell

- `src/cli/setup.ts`
- `src/cli/serve.ts`
- `src/cli/ai-context.ts`
- `src/cli/eval-server.ts`
- `src/cli/mcp.ts`
- `src/mcp/server.ts`
- upstream hooks / skills / plugin / web / eval shell

## Current Gaps

- `detect_changes` 仍以 changed files -> symbols 为主，尚未升级为精确 changed lines 映射
- 上游 `src/core/wiki/*` 仍保留参考代码，但当前受治理公开命令面不再暴露 `wiki/map`
- 仍以 upstream TS engine 为主；当前稳定入口优先走原生 TS CLI
