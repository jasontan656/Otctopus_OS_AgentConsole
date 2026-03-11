# Service Writing Rules


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `service`
- `action`: `authored_doc_write`
- `policy_version`: `v1`
- `authz_result`: `allow_within_service_scope`
- `deny_code`: `SERVICE_SCOPE_VIOLATION`

- Service family owns bounded-context, API, event, and dependency-boundary authored-doc updates.
- Do not collapse service writing rules into UI, gateway, or data rules.
- Service docs must update from their own common layer and keep drift markers explicit.
- Service container docs must explicitly split authored content into `overview/`, `features/`, `shared/`, and `common/`.
- `features/` may cover a semantic slice that spans multiple files; `shared/` carries inbound/outbound API, event, and cross-container dependency contracts.
