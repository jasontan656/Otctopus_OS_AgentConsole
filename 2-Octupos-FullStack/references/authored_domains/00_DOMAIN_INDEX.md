# Authored Domain Index


## Permission Boundary Contract
- `actor_id`: `codex_agent`
- `role`: `domain_policy_operator`
- `policy_version`: `v1`
- `authz_result`: `allow_within_00_DOMAIN_INDEX.md_scope`
- `deny_code`: `00_DOMAIN_INDEX.MD_SCOPE_VIOLATION`

适用技能：`2-Octupos-FullStack`

## Purpose

- This index groups authored product-domain rule families.
- Each family owns its own writing rules, implementation rules, and development canon automation scope.
- Each container under `Mother_Doc/docs` mirrors those families through `common/writing_guides/`, `common/code_abstractions/`, and `common/dev_canon/`.
- Do not collapse all authored domains into a single `mother_doc` rule set.

## Families

- `mother_doc`
- `ui`
- `gateway`
- `service`
- `data_infra`

## Loading Rule

- implementation must first load the matching domain family rules.
- Then load the target container's `common/code_abstractions/`, `common/writing_guides/`, and `common/dev_canon/` documents under `Octopus_OS/Mother_Doc/docs/<Container_Name>/`.
