# Mother_Doc Dev Canon Automation Scope


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `scope`: `mother_doc`
- `action`: `dev_canon_scope_selection`
- `policy_version`: `v1`
- `authz_result`: `allow_within_mother_doc_scope`
- `deny_code`: `MOTHER_DOC_SCOPE_VIOLATION`

- Only canonized development rules under `common/dev_canon/` may be auto-consumed.
- Preferred automation topics:
  - stack selection
  - architecture selection
  - graph asset placement
- Non-canonized areas must stay `replace_me`.
