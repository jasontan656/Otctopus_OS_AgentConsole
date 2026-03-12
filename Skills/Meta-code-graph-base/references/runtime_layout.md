# Runtime Layout

Root:
- `/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend/code_graph_runtime`

Subdirectories:
- `registry/`: indexed repo registry
- `indexes/`: per-repo graph index storage, including kuzu + meta
- `reports/`: impact / detect-changes / audit style reports
- `maps/`: per-repo resource snapshots and graph-derived maps
- `wiki/`: per-repo wiki and graph-derived documentation
- `snapshots/`: future snapshots / compare artifacts

UI handoff:
- This runtime layout is the source area for code-graph-facing viewer data.
- Final UI presentation is owned by `Dev-VUE3-WebUI-Frontend`, not by this skill.
- Viewer-side adapters should discover repo availability from `registry/` and consume repo-specific resources from `maps/`, `wiki/`, or `resource codegraph://...` handles.
