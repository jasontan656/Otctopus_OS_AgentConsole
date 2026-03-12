# Gateway Dev Canon Automation Scope


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `action`: `dev_canon_scope_selection`
- `policy_version`: `v1`
- `authz_result`: `allow_within_gateway_scope`
- `deny_code`: `GATEWAY_SCOPE_VIOLATION`

- Automation scope is limited to canonized gateway stack and routing architecture.
- Upstream semantics and auth semantics must remain authored-first unless explicitly canonized.
- Non-canonized gateway detail must not be auto-filled.
