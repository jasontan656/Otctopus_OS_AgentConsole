# Model Consumption Contract

## Purpose

This contract defines the stable way an agent or workflow should consume `Meta-code-graph-base`.
It is not a new feature surface. It is the fixed lookup order and CLI handling rule for the existing native TS commands.

## Stable Entry

All commands must go through the native CLI with an explicit runtime root:

```bash
META_CODE_GRAPH_RUNTIME_ROOT=/abs/runtime/root node /abs/skill/root/assets/gitnexus_core/dist/cli/index.js <subcommand> [args...]
```

## Read Order

1. Freshness gate
- Run `status` inside the target repo directory when you need to know whether the index exists or is stale.
- If the repo is not indexed and the codebase is substantial, run `analyze` before any semantic lookup.

2. Repo-level orientation
- Use `resource codegraph://repo/<name>/context` first when you need a broad repo picture.
- This is the default first read for architecture, module, process, and available-tool orientation.

3. Exact lookup
- Use `context` when you already know the symbol name or uid.
- Prefer this over `query` when the target is concrete.

4. Fuzzy lookup
- Use `query` when you only know a concept, phrase, or workflow description.
- Do not use it as the first step when an exact symbol target already exists.

5. Change risk
- Use `impact` only after you have a concrete symbol target.
- Use `detect-changes` after implementation to anchor the modified surface in current worktree reality.

## Repo Selection Rule

- `status` is cwd-scoped. Run it inside the target repo.
- `query/context/impact/detect-changes/rename/cypher` may be run outside the repo, but then they should carry `--repo <indexed_repo_name>`.

## Direct CLI IO Rule

- Parse `stdout` first.
- If `stdout` is empty, fallback to `stderr`.
- Some native graph commands emit structured payloads to `stderr`; this is part of the current stable consumption contract.

## Non-Goals

- This contract does not expose `map` or `wiki` as part of the governed public command surface.
- This contract does not define UI/viewer behavior; that remains in `Dev-VUE3-WebUI-Frontend`.
