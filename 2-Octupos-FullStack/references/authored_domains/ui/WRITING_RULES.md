# UI Writing Rules

- UI family owns its own authored-doc update rules; do not reuse service or gateway writing rules.
- Screen, component, route, and state documents must be updated from the UI family's own common layer.
- UI docs should stay human-readable first, with machine-detectable status blocks preserved.
- UI container docs must explicitly split authored content into `overview/`, `features/`, `shared/`, and `common/`.
- `overview/` carries product-facing screen and capability summaries; `features/` carries UI feature scopes and unresolved UI asks; `shared/` carries API/event/shared dependency notes consumed by the UI.
