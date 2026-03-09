from __future__ import annotations


def push_contract_payload() -> dict[str, object]:
    return {
        "contract_name": "meta_github_operation_push_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "rules"],
        "optional_fields": [],
        "entry": "push",
        "purpose": "Group push-related Git traceability tools and rules behind one explicit CLI-readable runtime entry.",
        "allowed_repos": ["Octopus_OS", "Codex_Skills_Mirror"],
        "commands": [
            {
                "name": "status",
                "role": "inspect branch, dirty state, and ahead/behind before push decisions",
            },
            {
                "name": "remote-info",
                "role": "inspect configured remotes before push decisions",
            },
            {
                "name": "fetch",
                "role": "refresh remote refs before push decisions",
            },
            {
                "name": "pull-rebase",
                "role": "rebase local branch on the remote branch before push when needed",
            },
            {
                "name": "commit",
                "role": "create a scoped local traceability commit without pushing",
            },
            {
                "name": "commit-and-push",
                "role": "stage the resolved scope, create the commit, and push it",
            },
            {
                "name": "push",
                "role": "push the current branch state without creating a new commit",
            },
        ],
        "rules": [
            "Do not widen automation beyond the registered repos.",
            "Push-related runtime guidance must come from CLI JSON, not markdown.",
            "Use explicit scope selection for commits; do not silently widen scope.",
            "Use force-with-lease only when the caller explicitly requests it.",
        ],
    }


def rollback_contract_payload() -> dict[str, object]:
    return {
        "contract_name": "meta_github_operation_rollback_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "rules"],
        "optional_fields": [],
        "entry": "rollback",
        "purpose": "Group rollback-related Git restore tools and rules behind one explicit CLI-readable runtime entry.",
        "allowed_repos": ["Octopus_OS", "Codex_Skills_Mirror"],
        "commands": [
            {
                "name": "status",
                "role": "inspect current repo drift before rollback",
            },
            {
                "name": "remote-info",
                "role": "inspect remotes before choosing a backup ref",
            },
            {
                "name": "fetch",
                "role": "refresh remote refs before rollback decisions",
            },
            {
                "name": "rollback-paths",
                "role": "strongly sync one or more explicit paths to a backup ref",
            },
            {
                "name": "rollback-sync",
                "role": "strongly sync explicit paths or the entire repo to a backup ref, deleting extra local files",
            },
        ],
        "rules": [
            "Rollback must make the restored scope match the selected backup ref.",
            "If a restored scope contains extra local files not present in the backup ref, delete them.",
            "Do not claim exact rollback semantics unless tests prove extra files are removed.",
            "Do not perform workspace-root Git automation.",
        ],
    }
