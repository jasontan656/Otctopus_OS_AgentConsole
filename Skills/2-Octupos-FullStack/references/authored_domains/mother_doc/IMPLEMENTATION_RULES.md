# Mother_Doc Implementation Rules


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `policy_version`: `v1`
- `authz_result`: `allow_within_mother_doc_scope`
- `deny_code`: `MOTHER_DOC_SCOPE_VIOLATION`

- Implementation for this family targets the `Octopus_OS/Mother_Doc/` container root, not the docs tree.
- Read `common/code_abstractions/`, then drop code/runtime artifacts outside `docs/`.
- Keep docs, code, and graph assets separated as sibling scopes inside the Mother_Doc container.
