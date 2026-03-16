# Runtime Layout

Root:
- caller-provided runtime root via `META_CODE_GRAPH_RUNTIME_ROOT`
- native `status` resolution remains cwd-scoped, so status checks should run inside the target repo directory

Subdirectories:
- `<runtime-root>/registry`: indexed repo registry
- `<runtime-root>/indexes`: per-repo graph index storage, including kuzu + meta
- `<runtime-root>/reports`: impact / detect-changes / audit style reports
- `<runtime-root>/snapshots`: future snapshots / compare artifacts

UI handoff:
- This runtime layout is the source area for code-graph-facing viewer data.
- Final UI presentation is owned by `Dev-VUE3-WebUI-Frontend`, not by this skill.
- Viewer-side adapters should discover repo availability from `registry/` and consume repo-specific resources from `resource codegraph://...` handles.

Consumption rule:
- The fixed agent lookup order and direct CLI IO fallback rule are defined in `references/model_consumption_contract.md`.
