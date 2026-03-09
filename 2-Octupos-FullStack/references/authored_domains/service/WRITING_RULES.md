# Service Writing Rules

- Service family owns bounded-context, API, event, and dependency-boundary authored-doc updates.
- Do not collapse service writing rules into UI, gateway, or data rules.
- Service docs must update from their own common layer and keep drift markers explicit.
- Service container docs must explicitly split authored content into `overview/`, `features/`, `shared/`, and `common/`.
- `features/` may cover a semantic slice that spans multiple files; `shared/` carries inbound/outbound API, event, and cross-container dependency contracts.
