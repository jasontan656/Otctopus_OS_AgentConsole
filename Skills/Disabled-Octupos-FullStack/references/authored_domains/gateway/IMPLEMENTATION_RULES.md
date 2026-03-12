# Gateway Implementation Rules


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `gateway`
- `policy_version`: `v1`
- `authz_result`: `allow_within_gateway_scope`
- `deny_code`: `GATEWAY_SCOPE_VIOLATION`

- Read gateway `common/code_abstractions/` and `common/dev_canon/` before code drop.
- Only canonized gateway stack and architecture decisions may be automated.
- Header policy, traffic policy, and routing mechanics stay `replace_me` until authored.
