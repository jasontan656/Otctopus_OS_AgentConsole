# UI Implementation Rules


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `ui`
- `policy_version`: `v1`
- `authz_result`: `allow_within_ui_scope`
- `deny_code`: `UI_SCOPE_VIOLATION`

- Implementation must read the UI family's `common/code_abstractions/` and `common/dev_canon/`.
- Only canonized stack and architecture choices may be auto-applied.
- Remaining UI implementation detail stays `replace_me` until authored in the target container docs.
