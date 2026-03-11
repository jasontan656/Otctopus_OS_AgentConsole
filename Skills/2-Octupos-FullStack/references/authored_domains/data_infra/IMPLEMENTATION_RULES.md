# Data Infra Implementation Rules


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `data_infra`
- `policy_version`: `v1`
- `authz_result`: `allow_within_data_infra_scope`
- `deny_code`: `DATA_INFRA_SCOPE_VIOLATION`

- Read data/infra `common/code_abstractions/` and `common/dev_canon/`.
- Only canonized engine, persistence, and deployment decisions may be automated.
- Recovery, monitoring, and retention details stay `replace_me` until authored.
