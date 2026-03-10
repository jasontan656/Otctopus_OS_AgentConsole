# UI Dev Canon Automation Scope


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `ui`
- `action`: `dev_canon_scope_selection`
- `policy_version`: `v1`
- `authz_result`: `allow_within_ui_scope`
- `deny_code`: `UI_SCOPE_VIOLATION`

- Automation may consume canonized UI stack and architecture constraints.
- Component patterns, route conventions, and event boundaries may be automated only after they enter `dev_canon`.
- Non-canonized UI detail must not be auto-filled.
