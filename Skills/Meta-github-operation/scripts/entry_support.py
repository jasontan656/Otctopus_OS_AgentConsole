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


def _resolve_ai_projects_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve AI_Projects root from Meta-github-operation script path")
    return repo_root.parent


AI_PROJECTS_ROOT = _resolve_ai_projects_root()
SKILL_RUNTIME_ROOT = str((AI_PROJECTS_ROOT / "Codex_Skill_Runtime" / "meta-github-operation").resolve())
CLAIMS_DIR = str((AI_PROJECTS_ROOT / "Codex_Skill_Runtime" / "meta-github-operation" / "claims").resolve())
SKILL_RESULT_ROOT = str((AI_PROJECTS_ROOT / "Codex_Skills_Result" / "meta-github-operation").resolve())
PUSH_LOCK_DIR = str((AI_PROJECTS_ROOT / "Codex_Skill_Runtime" / "meta-github-operation" / "push_locks").resolve())


def runtime_governance_payload() -> RuntimeGovernancePayload:
    return {
        "skill_runtime_root": SKILL_RUNTIME_ROOT,
        "claims_dir": CLAIMS_DIR,
        "result_root": SKILL_RESULT_ROOT,
        "push_lock_dir": PUSH_LOCK_DIR,
        "runtime_log_policy": (
            "This skill currently emits CLI JSON to stdout and does not persist its own rolling logs; "
            "runtime-owned claims files must stay under the governed skill runtime root."
        ),
        "result_policy": (
            "This skill does not emit file artifacts by default; future file outputs must accept an explicit target "
            "path or default under the governed result root."
        ),
        "legacy_runtime_fallbacks": [],
        "migration_note": "Thread-owned claims files must live only under the namespaced claims directory.",
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
        "allowed_repos": ["Octopus_OS", "Otctopus_OS_AgentConsole"],
        "commands": commands,
        "remote_policy": {
            "Octopus_OS": {
                "origin": {
                    "role": "private_ai_daily_remote",
                    "automation_write_allowed": True,
                    "status": "enabled",
                    "notes": [
                        "Repository is expected to remain private/closed-source.",
                        "Origin should point to the Octopus_OS_AI repository for AI daily pushes.",
                    ],
                },
                "human-sync": {
                    "role": "private_human_explicit_remote",
                    "automation_write_allowed": False,
                    "manual_publish_allowed": True,
                    "status": "enabled",
                    "notes": [
                        "Repository is expected to remain private/closed-source.",
                        "human-sync should point to the Octopus_OS_humen repository.",
                        "Use this remote only when the human explicitly asks for a push.",
                    ],
                }
                },
                "Otctopus_OS_AgentConsole": {
                    "origin": {
                    "role": "private_ai_daily_remote",
                    "automation_write_allowed": True,
                    "status": "enabled",
                    "notes": [
                        "Use for AI daily iteration pushes and same-turn Git traceability.",
                        "This remote should point to the Otctopus_OS_AgentConsole_AI_dev repository.",
                    ],
                },
                "public-release": {
                    "role": "human_explicit_public_release_remote",
                    "automation_write_allowed": False,
                    "manual_publish_allowed": True,
                    "status": "enabled",
                    "notes": [
                        "This remote is the open-source publication repository for Otctopus_OS_AgentConsole.",
                        "Only use it when the human explicitly asks for a push.",
                    ],
                },
            },
        },
        "rules": [
            "Do not widen automation beyond the registered repos.",
            "Push-related runtime guidance must come from CLI JSON, not markdown.",
            "Use explicit scope selection for commits; do not silently widen scope.",
            "Traceability commit messages must use development-log style details and explicitly state the problem solved or risk reduced.",
            "Use force-with-lease only when the caller explicitly requests it.",
            "Remote write flows must run serially per repo; do not parallelize push, commit-and-push, repo-bootstrap publish, or remote baseline publication.",
            "Bootstrap flows may create or verify private GitHub repositories only for registered repos and should default to private visibility.",
            "Bootstrap flows should refresh local ignore hygiene for logs, temp files, virtual environments, caches, and .env-like files before the first or follow-up push.",
            "Manual-only remotes require an explicit human request flag before write operations are allowed.",
            "For Otctopus_OS_AgentConsole, automatic iteration pushes must go to origin only.",
            "For Octopus_OS, human-sync is reserved for human-explicit pushes only.",
            "For Otctopus_OS_AgentConsole, public-release is allowed only when the human explicitly requests the push.",
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
        "allowed_repos": ["Octopus_OS", "Otctopus_OS_AgentConsole"],
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
        "Otctopus_OS_AgentConsole": {
            "public-release": {
                "status": "human_explicit_only",
                "disabled_reason": "automatic publish is disabled; human explicit request is required",
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
        "allowed_repos": ["Octopus_OS", "Otctopus_OS_AgentConsole"],
        "commands": commands,
        "release_publication_state": release_publication_state,
        "runtime_governance": runtime_governance_payload(),
        "rules": [
            "Baseline is a separate runtime entry from push.",
            "Clean repos should prefer tag-only baselines instead of empty traceability commits.",
            "Dirty repos may create a scoped baseline commit before tagging.",
            "Remote baseline publication must remain within the registered repos.",
            "Manual-only remotes require an explicit human request flag before baseline publication is allowed.",
        ],
    }
