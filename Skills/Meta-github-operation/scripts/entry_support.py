from __future__ import annotations


def push_contract_payload() -> dict[str, object]:
    return {
        "contract_name": "meta_github_operation_push_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "rules"],
        "optional_fields": ["remote_policy"],
        "entry": "push",
        "purpose": "Group push-related Git traceability tools and rules behind one explicit CLI-readable runtime entry.",
        "allowed_repos": ["Octopus_OS", "octopus-os-agent-console"],
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
        "remote_policy": {
            "Octopus_OS": {
                "origin": {
                    "role": "standard_primary_remote",
                    "automation_write_allowed": True,
                    "status": "enabled",
                }
            },
            "octopus-os-agent-console": {
                "origin": {
                    "role": "private_dev_remote",
                    "automation_write_allowed": True,
                    "status": "enabled",
                    "notes": [
                        "Use for automatic iteration pushes and same-turn Git traceability.",
                        "This remote is the default target for commit-and-push and push flows.",
                    ],
                },
                "public-release": {
                    "role": "future_public_release_remote",
                    "automation_write_allowed": False,
                    "manual_publish_allowed": False,
                    "status": "disabled",
                    "disabled_reason": "development has not reached a publishable closure and the release workflow is not designed yet",
                    "notes": [
                        "Reserved for future human-approved publishable snapshots only.",
                        "Do not use this remote for automatic iteration pushes.",
                    ],
                },
            },
        },
        "rules": [
            "Do not widen automation beyond the registered repos.",
            "Push-related runtime guidance must come from CLI JSON, not markdown.",
            "Use explicit scope selection for commits; do not silently widen scope.",
            "Use force-with-lease only when the caller explicitly requests it.",
            "For octopus-os-agent-console, automatic iteration pushes must go to origin only.",
            "For octopus-os-agent-console, public-release is currently disabled because development has not reached publishable closure and no release workflow is designed yet.",
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
        "allowed_repos": ["Octopus_OS", "octopus-os-agent-console"],
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


def baseline_contract_payload() -> dict[str, object]:
    return {
        "contract_name": "meta_github_operation_baseline_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "rules"],
        "optional_fields": ["release_publication_state"],
        "entry": "baseline",
        "purpose": "Create a named rollback anchor without overloading push semantics.",
        "allowed_repos": ["Octopus_OS", "octopus-os-agent-console"],
        "commands": [
            {
                "name": "baseline-create",
                "role": "create a local or remote rollback baseline as a tag-only anchor for clean repos or a commit-plus-tag anchor for dirty repos",
            },
        ],
        "release_publication_state": {
            "octopus-os-agent-console": {
                "public-release": {
                    "status": "disabled",
                    "disabled_reason": "development has not reached a publishable closure and the release workflow is not designed yet",
                }
            }
        },
        "rules": [
            "Baseline is a separate runtime entry from push.",
            "Clean repos should prefer tag-only baselines instead of empty traceability commits.",
            "Dirty repos may create a scoped baseline commit before tagging.",
            "Remote baseline publication must remain within the registered repos.",
            "For octopus-os-agent-console, do not publish baselines to public-release while the public release flow is disabled.",
        ],
    }
