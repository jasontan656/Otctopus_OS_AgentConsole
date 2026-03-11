# Service Dev Canon Automation Scope


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `service`
- `action`: `dev_canon_scope_selection`
- `policy_version`: `v1`
- `authz_result`: `allow_within_service_scope`
- `deny_code`: `SERVICE_SCOPE_VIOLATION`

- Automation may consume canonized service stack and architecture choices.
- API patterns, event semantics, and job behavior stay manual until they enter `dev_canon`.
- Non-canonized service detail must not be auto-filled.
