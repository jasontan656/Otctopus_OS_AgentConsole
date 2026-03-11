# Service Implementation Rules


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `service`
- `policy_version`: `v1`
- `authz_result`: `allow_within_service_scope`
- `deny_code`: `SERVICE_SCOPE_VIOLATION`

- Read service `common/code_abstractions/` and `common/dev_canon/`.
- Only canonized runtime, transport, storage, and architecture decisions may be automated.
- Uncanonized service design detail must remain `replace_me`.
