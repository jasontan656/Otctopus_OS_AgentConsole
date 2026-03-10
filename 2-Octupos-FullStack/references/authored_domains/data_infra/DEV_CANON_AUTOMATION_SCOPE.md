# Data Infra Dev Canon Automation Scope


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `action`: `dev_canon_scope_selection`
- `policy_version`: `v1`
- `authz_result`: `allow_within_data_infra_scope`
- `deny_code`: `DATA_INFRA_SCOPE_VIOLATION`

- Automation scope is limited to canonized data engine, persistence, and architecture choices.
- Operational semantics must remain manual unless they are explicitly canonized.
- Non-canonized data/infra detail must not be auto-filled.
