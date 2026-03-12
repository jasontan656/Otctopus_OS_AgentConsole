from __future__ import annotations

from pathlib import Path

from runtime_contract_support import (
    BaselineContractPayload,
    CommandSpec,
    PushContractPayload,
    ReleasePublicationState,
    RollbackContractPayload,
    RuntimeGovernancePayload,
)


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "octopus-os-agent-console"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Meta-github-operation script path")
    return repo_root.parent


PRODUCT_ROOT = _resolve_product_root()
SKILL_RUNTIME_ROOT = str((PRODUCT_ROOT / "Codex_Skill_Runtime" / "meta-github-operation").resolve())
CLAIMS_DIR = str((PRODUCT_ROOT / "Codex_Skill_Runtime" / "meta-github-operation" / "claims").resolve())
SKILL_RESULT_ROOT = str((PRODUCT_ROOT / "Codex_Skills_Result" / "meta-github-operation").resolve())
LEGACY_RUNTIME_FALLBACKS = [str((PRODUCT_ROOT / "Codex_Skill_Runtime").resolve())]


def runtime_governance_payload() -> RuntimeGovernancePayload:
    return {
        "skill_runtime_root": SKILL_RUNTIME_ROOT,
        "claims_dir": CLAIMS_DIR,
        "result_root": SKILL_RESULT_ROOT,
        "runtime_log_policy": (
            "This skill currently emits CLI JSON to stdout and does not persist its own rolling logs; "
            "runtime-owned claims files must stay under the governed skill runtime root."
        ),
        "result_policy": (
            "This skill does not emit file artifacts by default; future file outputs must accept an explicit target "
            "path or default under the governed result root."
        ),
        "legacy_runtime_fallbacks": LEGACY_RUNTIME_FALLBACKS,
        "migration_note": (
            "Legacy thread-owned claims files previously written directly under Codex_Skill_Runtime should be moved "
            "into the namespaced claims directory; active lookup falls back to the legacy root only for compatibility."
        ),
    }


def push_contract_payload() -> PushContractPayload:
    commands: list[CommandSpec] = [
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
        {
            "name": "repo-bootstrap",
            "role": "ensure private GitHub repo bootstrap, origin association, ignore hygiene, and first or follow-up push",
        },
    ]
    return {
        "contract_name": "meta_github_operation_push_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "runtime_governance", "rules"],
        "optional_fields": ["remote_policy"],
        "entry": "push",
        "purpose": "Group push-related Git traceability tools and rules behind one explicit CLI-readable runtime entry.",
        "allowed_repos": ["Octopus_OS", "octopus-os-agent-console"],
        "commands": commands,
        "remote_policy": {
            "Octopus_OS": {
                "origin": {
                    "role": "private_primary_remote",
                    "automation_write_allowed": True,
                    "status": "enabled",
                    "notes": [
                        "Repository is expected to remain private/closed-source.",
                        "Bootstrap flows should keep the remote repository name aligned with the local repository name.",
                    ],
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
            "Bootstrap flows may create or verify private GitHub repositories only for registered repos and should default to private visibility.",
            "Bootstrap flows should refresh local ignore hygiene for logs, temp files, virtual environments, caches, and .env-like files before the first or follow-up push.",
            "For octopus-os-agent-console, automatic iteration pushes must go to origin only.",
            "For octopus-os-agent-console, public-release is currently disabled because development has not reached publishable closure and no release workflow is designed yet.",
        ],
        "runtime_governance": runtime_governance_payload(),
    }


def rollback_contract_payload() -> RollbackContractPayload:
    commands: list[CommandSpec] = [
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
    ]
    return {
        "contract_name": "meta_github_operation_rollback_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "runtime_governance", "rules"],
        "optional_fields": [],
        "entry": "rollback",
        "purpose": "Group rollback-related Git restore tools and rules behind one explicit CLI-readable runtime entry.",
        "allowed_repos": ["Octopus_OS", "octopus-os-agent-console"],
        "commands": commands,
        "runtime_governance": runtime_governance_payload(),
        "rules": [
            "Rollback must make the restored scope match the selected backup ref.",
            "If a restored scope contains extra local files not present in the backup ref, delete them.",
            "Do not claim exact rollback semantics unless tests prove extra files are removed.",
            "Do not perform workspace-root Git automation.",
        ],
}


def baseline_contract_payload() -> BaselineContractPayload:
    commands: list[CommandSpec] = [
        {
            "name": "baseline-create",
            "role": "create a local or remote rollback baseline as a tag-only anchor for clean repos or a commit-plus-tag anchor for dirty repos",
        },
    ]
    release_publication_state: ReleasePublicationState = {
        "octopus-os-agent-console": {
            "public-release": {
                "status": "disabled",
                "disabled_reason": "development has not reached a publishable closure and the release workflow is not designed yet",
            }
        }
    }
    return {
        "contract_name": "meta_github_operation_baseline_contract",
        "contract_version": "v1",
        "validation_mode": "static_minimal",
        "required_fields": ["entry", "purpose", "allowed_repos", "commands", "runtime_governance", "rules"],
        "optional_fields": ["release_publication_state"],
        "entry": "baseline",
        "purpose": "Create a named rollback anchor without overloading push semantics.",
        "allowed_repos": ["Octopus_OS", "octopus-os-agent-console"],
        "commands": commands,
        "release_publication_state": release_publication_state,
        "runtime_governance": runtime_governance_payload(),
        "rules": [
            "Baseline is a separate runtime entry from push.",
            "Clean repos should prefer tag-only baselines instead of empty traceability commits.",
            "Dirty repos may create a scoped baseline commit before tagging.",
            "Remote baseline publication must remain within the registered repos.",
            "For octopus-os-agent-console, do not publish baselines to public-release while the public release flow is disabled.",
        ],
    }
