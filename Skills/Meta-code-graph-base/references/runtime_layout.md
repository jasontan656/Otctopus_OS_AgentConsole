# Runtime Layout

Root:
- caller-provided runtime root via `--runtime-root <abs/runtime/root>` or `META_CODE_GRAPH_RUNTIME_ROOT`

Subdirectories:
- `<runtime-root>/registry`: indexed repo registry
- `<runtime-root>/indexes`: per-repo graph index storage, including kuzu + meta
- `<runtime-root>/reports`: impact / detect-changes / audit style reports
- `<runtime-root>/maps`: per-repo resource snapshots and graph-derived maps
- `<runtime-root>/wiki`: per-repo wiki and graph-derived documentation
- `<runtime-root>/snapshots`: future snapshots / compare artifacts

UI handoff:
- This runtime layout is the source area for code-graph-facing viewer data.
- Final UI presentation is owned by `Dev-VUE3-WebUI-Frontend`, not by this skill.
- Viewer-side adapters should discover repo availability from `registry/` and consume repo-specific resources from `maps/`, `wiki/`, or `resource codegraph://...` handles.
