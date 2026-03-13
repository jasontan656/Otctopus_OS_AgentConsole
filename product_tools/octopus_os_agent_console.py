#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import stat
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any


RSYNC_EXCLUDES = (
    ".git/",
    "__pycache__/",
    "*.pyc",
    ".tooling_runtime/",
    ".product_runtime/",
)
SYSTEM_SKILL_NAMESPACE = ".system"
SYSTEM_SKILL_MARKER = ".codex-system-skills.marker"
SKILLS_DIR_NAME = "Skills"
WORKSPACE_MARKER = ".octopus_os_workspace_install.json"
PRODUCT_RUNTIME_DIR = ".product_runtime"
GITHUB_BINDING_FILE = "github_skill_repo_binding.json"
DEFAULT_CONSOLE_DIR_NAME = "console"
DEFAULT_SKILL_RUNTIME_DIR_NAME = "Codex_Skill_Runtime"
DEFAULT_SKILL_RESULT_DIR_NAME = "Codex_Skills_Result"
DEFAULT_OCTOPUS_OS_DIR_NAME = "Octopus_OS"
CODEX_HOME_DIR_NAME = ".codex"
CODEX_CLI_PACKAGE = "@openai/codex@latest"
CODEX_CLI_INSTALL_MODE_ENV = "OCTOPUS_OS_CODEX_INSTALL_MODE"
EXTERNAL_DEPENDENCY_INSTALL_MODE_ENV = "OCTOPUS_OS_EXTERNAL_DEPENDENCY_MODE"
DEFAULT_CODEX_CLI_MODE = "auto"
DEFAULT_EXTERNAL_DEPENDENCY_MODE = "auto"
DEFAULT_GITHUB_API_ENV_VAR = "GITHUB_TOKEN"
PRODUCT_NAME = "Octopus OS - Natural-Language-Driven Multi-Agent Console"
SUPPORTED_RUNTIME_TARGET = "codex-gpt-5.4-high"
SUPPORTED_RUNTIME_LABEL = "Codex + GPT-5.4 high reasoning effort"
SUPPORTED_HOST_ENV_LABEL = "Codex CLI + VS Code"
FORBIDDEN_CODEX_ROOT_FILES = ("AGENTS.md",)
ALLOWED_CLEAN_CODEX_ROOT_ENTRIES = {SYSTEM_SKILL_NAMESPACE}
EXTERNAL_RUNTIME_DEPENDENCY_MANIFEST_RELATIVE_PATH = Path(
    "references/runtime_contracts/EXTERNAL_RUNTIME_DEPENDENCIES.json"
)
EXTERNAL_RUNTIME_DEPENDENCY_ROOT_DIR_NAME = "external_runtime_dependencies"


def _shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in parts)


def _resolve_repo_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def _validate_legacy_codex_root(raw: str) -> Path:
    codex_root = Path(raw).expanduser().resolve()
    if codex_root.name != "skills" or codex_root.parent.name != CODEX_HOME_DIR_NAME:
        raise ValueError(
            "legacy codex root must match .../.codex/skills when used as a compatibility input; "
            f"got: {codex_root}"
        )
    return codex_root


def _resolve_install_root(raw: str | None, legacy_codex_root: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    if legacy_codex_root:
        return _validate_legacy_codex_root(legacy_codex_root).parent.parent.resolve()
    return (Path.home() / "Octopus_Runtime" / "codex-home").resolve()


def _derive_codex_home(install_root: Path) -> Path:
    return install_root / CODEX_HOME_DIR_NAME


def _derive_codex_root(install_root: Path) -> Path:
    return _derive_codex_home(install_root) / "skills"


def _derive_codex_cli_bin(install_root: Path) -> Path:
    return install_root / "bin" / "codex"


def _derive_console_root(install_root: Path) -> Path:
    return install_root / DEFAULT_CONSOLE_DIR_NAME


def _derive_skill_runtime_root(install_root: Path) -> Path:
    return install_root / DEFAULT_SKILL_RUNTIME_DIR_NAME


def _derive_skill_result_root(install_root: Path) -> Path:
    return install_root / DEFAULT_SKILL_RESULT_DIR_NAME


def _derive_octopus_os_root(install_root: Path) -> Path:
    return install_root / DEFAULT_OCTOPUS_OS_DIR_NAME


def _derive_external_runtime_dependency_root(install_root: Path) -> Path:
    return install_root / PRODUCT_RUNTIME_DIR / EXTERNAL_RUNTIME_DEPENDENCY_ROOT_DIR_NAME


def _resolve_workspace_root(raw: str | None, install_root: Path) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return _derive_console_root(install_root).resolve()


def _resolve_state_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".Otctopus_OS_AgentConsole" / "install_sessions").resolve()


def _require_supported_runtime_target(runtime_target: str | None) -> str:
    normalized = str(runtime_target or "").strip()
    if normalized != SUPPORTED_RUNTIME_TARGET:
        raise ValueError(
            "installation is limited to Codex with GPT-5.4 high reasoning effort; "
            f"rerun with --runtime-target {SUPPORTED_RUNTIME_TARGET}"
        )
    return normalized


def _normalize_required_text(raw: str | None, field_name: str) -> str:
    value = str(raw or "").strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    return value


def _normalize_optional_text(raw: str | None) -> str | None:
    value = str(raw or "").strip()
    return value or None


def _replace_placeholders(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        rendered = value
        for placeholder, replacement in replacements.items():
            rendered = rendered.replace(placeholder, replacement)
        return rendered
    if isinstance(value, list):
        return [_replace_placeholders(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: _replace_placeholders(item, replacements) for key, item in value.items()}
    return value


def _path_with_prepend(existing_path: str | None, prepend_items: list[str]) -> str:
    filtered_items = [item for item in prepend_items if item]
    if existing_path:
        filtered_items.append(existing_path)
    return os.pathsep.join(filtered_items)


def _build_codex_cli_install_command(install_root: Path) -> str:
    return _shell_join(["npm", "install", "-g", CODEX_CLI_PACKAGE, "--prefix", str(install_root)])


def _derive_managed_npm_root(install_root: Path) -> Path:
    return install_root / PRODUCT_RUNTIME_DIR / "npm"


def _prepare_managed_npm_environment(
    install_root: Path,
    *,
    home_root: Path | None = None,
    namespace: str = "npm",
) -> dict[str, str]:
    npm_root = install_root / PRODUCT_RUNTIME_DIR / namespace
    cache_root = npm_root / "cache"
    logs_root = npm_root / "logs"
    userconfig_path = npm_root / "npmrc"

    cache_root.mkdir(parents=True, exist_ok=True)
    logs_root.mkdir(parents=True, exist_ok=True)
    userconfig_path.parent.mkdir(parents=True, exist_ok=True)
    if not userconfig_path.exists():
        userconfig_path.write_text("", encoding="utf-8")

    return {
        **os.environ,
        "HOME": str(home_root or install_root),
        "NPM_CONFIG_CACHE": str(cache_root),
        "npm_config_cache": str(cache_root),
        "NPM_CONFIG_LOGS_DIR": str(logs_root),
        "npm_config_logs_dir": str(logs_root),
        "NPM_CONFIG_USERCONFIG": str(userconfig_path),
        "npm_config_userconfig": str(userconfig_path),
        "NPM_CONFIG_FUND": "false",
        "npm_config_fund": "false",
        "NPM_CONFIG_AUDIT": "false",
        "npm_config_audit": "false",
        "NPM_CONFIG_UPDATE_NOTIFIER": "false",
        "npm_config_update_notifier": "false",
    }


def _apply_environment_overrides(
    base_env: dict[str, str],
    overrides: dict[str, Any] | None,
) -> dict[str, str]:
    env = dict(base_env)
    if not overrides:
        return env

    path_prepend_raw = overrides.get("PATH_prepend", [])
    if path_prepend_raw:
        path_prepend = [str(item) for item in path_prepend_raw]
        env["PATH"] = _path_with_prepend(env.get("PATH"), path_prepend)

    for key, value in overrides.items():
        if key == "PATH_prepend":
            continue
        env[str(key)] = str(value)
    return env


def _run_command(command: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, check=False, capture_output=True, text=True, env=env)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or f"command failed: {command}")
    return completed


def _normalize_codex_cli_mode(raw: str | None) -> str:
    normalized = str(raw or DEFAULT_CODEX_CLI_MODE).strip().lower()
    if normalized not in {"auto", "attach", "install"}:
        raise ValueError("--codex-cli-mode must be auto, attach, or install")
    return normalized


def _resolve_existing_codex_cli(raw: str | None) -> tuple[Path | None, str | None]:
    if raw:
        candidate = Path(raw).expanduser().resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"codex cli binary does not exist: {candidate}")
        if not os.access(candidate, os.X_OK):
            raise PermissionError(f"codex cli binary is not executable: {candidate}")
        return candidate, "explicit"

    detected = shutil.which("codex")
    if not detected:
        return None, None
    candidate = Path(detected).expanduser().resolve()
    if not candidate.exists():
        return None, None
    return candidate, "path"


def _inspect_codex_cli_version(codex_cli_bin: Path, *, codex_home: Path | None = None) -> str:
    env = dict(os.environ)
    if codex_home is not None:
        env["HOME"] = str(codex_home)
    completed = subprocess.run(
        [str(codex_cli_bin), "--version"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    return completed.stdout.strip() or completed.stderr.strip() or "unknown"


def _build_codex_launch_command(codex_cli_bin: Path, codex_home: Path, workspace_root: Path) -> str:
    command = _shell_join(
        [
            str(codex_cli_bin),
            "-C",
            str(workspace_root),
            "-m",
            "gpt-5.4",
            "-c",
            'model_reasoning_effort="high"',
        ]
    )
    return f"HOME={shlex.quote(str(codex_home))} {command}"


def _build_github_binding(args: argparse.Namespace, *, require_complete: bool) -> dict[str, object]:
    repo = _normalize_optional_text(getattr(args, "github_skill_repo", None))
    auth_mode = _normalize_optional_text(getattr(args, "github_auth_mode", None))
    if require_complete:
        repo = _normalize_required_text(repo, "--github-skill-repo")
        auth_mode = _normalize_required_text(auth_mode, "--github-auth-mode")
        if auth_mode not in {"ssh", "api"}:
            raise ValueError("--github-auth-mode must be ssh or api")
        if not getattr(args, "acknowledge_github_control_risk", False):
            raise ValueError(
                "install requires --acknowledge-github-control-risk because Octopus OS will drive GitHub workflows on this machine"
            )
    elif auth_mode and auth_mode not in {"ssh", "api"}:
        raise ValueError("--github-auth-mode must be ssh or api")

    if not repo or not auth_mode:
        return {
            "configured": False,
            "repo": repo,
            "auth_mode": auth_mode,
            "warning": (
                "Octopus OS requires a dedicated GitHub repository binding for skill evolution and Git automation."
            ),
        }

    github_api_env_var = None
    github_ssh_key_path = None
    if auth_mode == "api":
        github_api_env_var = _normalize_optional_text(getattr(args, "github_api_env_var", None)) or DEFAULT_GITHUB_API_ENV_VAR
    else:
        github_ssh_key_path = _normalize_optional_text(getattr(args, "github_ssh_key_path", None))

    return {
        "configured": True,
        "repo": repo,
        "auth_mode": auth_mode,
        "github_api_env_var": github_api_env_var,
        "github_ssh_key_path": github_ssh_key_path,
        "risk_acknowledged": bool(getattr(args, "acknowledge_github_control_risk", False)),
        "warning": (
            "Use a fresh GitHub account for Octopus OS, or fully back up and clear any existing account state before binding. "
            "This machine workflow is intentionally GitHub-controlling."
        ),
    }


def _cleanup_forbidden_codex_root_files(codex_root: Path) -> list[str]:
    removed: list[str] = []
    for name in FORBIDDEN_CODEX_ROOT_FILES:
        target = codex_root / name
        if not target.exists():
            continue
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        removed.append(str(target))
    return removed


def _summarize_codex_root_cleanliness(codex_root: Path) -> dict[str, object]:
    if not codex_root.exists():
        return {
            "state": "missing",
            "is_clean": True,
            "root_entries": [],
            "unexpected_root_entries": [],
        }

    root_entries = sorted(child.name for child in codex_root.iterdir())
    unexpected_root_entries = [
        entry for entry in root_entries if entry not in ALLOWED_CLEAN_CODEX_ROOT_ENTRIES
    ]
    return {
        "state": "existing",
        "is_clean": not unexpected_root_entries,
        "root_entries": root_entries,
        "unexpected_root_entries": unexpected_root_entries,
    }


def _assert_clean_codex_root(codex_root: Path) -> tuple[dict[str, object], list[str]]:
    removed_forbidden = _cleanup_forbidden_codex_root_files(codex_root)
    summary = _summarize_codex_root_cleanliness(codex_root)
    unexpected = summary["unexpected_root_entries"]
    if unexpected:
        raise ValueError(
            "codex skills root is not clean; only Codex initial .system entries may exist before Octopus OS install. "
            f"Unexpected entries: {unexpected}"
        )
    return summary, removed_forbidden


def _install_codex_cli_latest(install_root: Path) -> dict[str, object]:
    install_root.mkdir(parents=True, exist_ok=True)
    mode = os.environ.get(CODEX_CLI_INSTALL_MODE_ENV, "npm").strip().lower()
    codex_bin = _derive_codex_cli_bin(install_root)
    npm_env = _prepare_managed_npm_environment(install_root)

    if mode == "stub":
        codex_bin.parent.mkdir(parents=True, exist_ok=True)
        codex_bin.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        codex_bin.chmod(codex_bin.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        system_root = _derive_codex_root(install_root) / SYSTEM_SKILL_NAMESPACE
        system_root.mkdir(parents=True, exist_ok=True)
        marker = system_root / SYSTEM_SKILL_MARKER
        if not marker.exists():
            marker.write_text("marker\n", encoding="utf-8")
        return {
            "mode": "stub",
            "command": [CODEX_CLI_INSTALL_MODE_ENV, "stub"],
            "codex_cli_bin": str(codex_bin),
            "codex_cli_install_command": _build_codex_cli_install_command(install_root),
            "version": "stub",
        }

    npm_bin = shutil.which("npm")
    if not npm_bin:
        raise FileNotFoundError("npm is required to install the latest Codex CLI")

    command = [npm_bin, "install", "-g", CODEX_CLI_PACKAGE, "--prefix", str(install_root)]
    completed = subprocess.run(command, check=False, capture_output=True, text=True, env=npm_env)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "failed to install Codex CLI")
    if not codex_bin.exists():
        raise FileNotFoundError(f"Codex CLI install completed but binary is missing: {codex_bin}")

    version = _inspect_codex_cli_version(codex_bin, codex_home=install_root)
    return {
        "mode": "npm",
        "command": command,
        "codex_cli_bin": str(codex_bin),
        "codex_cli_install_command": _build_codex_cli_install_command(install_root),
        "version": version,
    }


def _resolve_codex_cli_strategy(
    install_root: Path,
    *,
    requested_mode: str,
    provided_bin: str | None,
    execute_install: bool,
) -> dict[str, object]:
    existing_bin, existing_source = _resolve_existing_codex_cli(provided_bin)

    if requested_mode == "attach":
        if existing_bin is None:
            raise FileNotFoundError(
                "attach mode requires an existing codex binary; provide --codex-cli-bin or ensure codex is on PATH"
            )
        return {
            "mode": "attach",
            "requested_mode": requested_mode,
            "resolved_from": existing_source,
            "command": None,
            "codex_cli_bin": str(existing_bin),
            "codex_cli_install_command": None,
            "version": _inspect_codex_cli_version(existing_bin),
        }

    if requested_mode == "auto" and existing_bin is not None:
        return {
            "mode": "attach",
            "requested_mode": requested_mode,
            "resolved_from": existing_source,
            "command": None,
            "codex_cli_bin": str(existing_bin),
            "codex_cli_install_command": None,
            "version": _inspect_codex_cli_version(existing_bin),
        }

    if not execute_install:
        codex_bin = _derive_codex_cli_bin(install_root)
        return {
            "mode": "install",
            "requested_mode": requested_mode,
            "resolved_from": "target-install",
            "command": None,
            "codex_cli_bin": str(codex_bin),
            "codex_cli_install_command": _build_codex_cli_install_command(install_root),
            "version": None,
        }

    codex_install = _install_codex_cli_latest(install_root)
    return {
        **codex_install,
        "mode": "install",
        "requested_mode": requested_mode,
        "resolved_from": "target-install",
    }


def _resolve_skills_root(repo_root: Path) -> Path:
    skills_root = repo_root / SKILLS_DIR_NAME
    if skills_root.is_dir():
        return skills_root.resolve()
    return repo_root.resolve()


def _discover_skill_roots(repo_root: Path) -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    skills_root = _resolve_skills_root(repo_root)
    for child in sorted(skills_root.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if child.name == ".git":
            continue
        if child.name == SYSTEM_SKILL_NAMESPACE:
            if (child / SYSTEM_SKILL_MARKER).exists():
                skills.append(
                    {
                        "name": child.name,
                        "source": str(child.resolve()),
                        "destination_name": child.name,
                    }
                )
            continue
        if child.name.startswith("."):
            continue
        if (child / "SKILL.md").is_file():
            skills.append(
                {
                    "name": child.name,
                    "source": str(child.resolve()),
                    "destination_name": child.name,
                }
            )
    if not skills:
        raise FileNotFoundError(f"no syncable skill roots found under skills root: {skills_root}")
    return skills


def _load_external_runtime_dependencies_for_skill(
    skill: dict[str, object],
    *,
    install_root: Path,
    codex_home: Path,
) -> list[dict[str, object]]:
    skill_source_root = Path(str(skill["source"]))
    manifest_path = skill_source_root / EXTERNAL_RUNTIME_DEPENDENCY_MANIFEST_RELATIVE_PATH
    if not manifest_path.exists():
        return []

    replacements = {
        "__SKILL_NAME__": str(skill["name"]),
        "__SKILL_ROOT__": str(skill_source_root),
        "__PRODUCT_ROOT__": str(codex_home),
        "__WORKSPACE_ROOT__": str(install_root),
        "__RUNTIME_DIR__": str(_derive_skill_runtime_root(install_root) / str(skill["name"])),
        "__RESULT_DIR__": str(_derive_skill_result_root(install_root) / str(skill["name"])),
    }
    payload = _replace_placeholders(
        json.loads(manifest_path.read_text(encoding="utf-8")),
        replacements,
    )
    dependencies = payload.get("dependencies", [])
    if not isinstance(dependencies, list):
        raise ValueError(f"external dependency manifest must contain a dependency list: {manifest_path}")

    normalized: list[dict[str, object]] = []
    for dependency in dependencies:
        dependency_id = str(dependency["dependency_id"])
        normalized.append(
            {
                "dependency_id": dependency_id,
                "display_name": str(dependency.get("display_name") or dependency_id),
                "install_type": str(dependency["install_type"]),
                "install_root": str(dependency["install_root"]),
                "binary_name": str(dependency["binary_name"]),
                "binary_path": str(dependency["binary_path"]),
                "runtime_env": dict(dependency.get("runtime_env") or {}),
                "install_commands": list(dependency.get("install_commands") or []),
                "validate_commands": list(dependency.get("validate_commands") or []),
                "required_artifacts": list(dependency.get("required_artifacts") or []),
                "host_requirements": list(dependency.get("host_requirements") or []),
                "install_help": _normalize_optional_text(dependency.get("install_help")),
                "manifest_path": str(manifest_path),
                "required_by_skills": [str(skill["name"])],
            }
        )
    return normalized


def _merge_external_runtime_dependencies(
    dependencies: list[dict[str, object]],
) -> list[dict[str, object]]:
    merged: dict[str, dict[str, object]] = {}
    for dependency in dependencies:
        dependency_id = str(dependency["dependency_id"])
        existing = merged.get(dependency_id)
        if existing is None:
            merged[dependency_id] = dependency
            continue

        comparable_fields = (
            "display_name",
            "install_type",
            "install_root",
            "binary_name",
            "binary_path",
            "runtime_env",
            "install_commands",
            "validate_commands",
            "required_artifacts",
            "host_requirements",
            "install_help",
        )
        if any(existing[field] != dependency[field] for field in comparable_fields):
            raise ValueError(
                "conflicting external runtime dependency declarations detected for "
                f"{dependency_id}: {existing['manifest_path']} vs {dependency['manifest_path']}"
            )

        for skill_name in dependency["required_by_skills"]:
            if skill_name not in existing["required_by_skills"]:
                existing["required_by_skills"].append(skill_name)

    return [merged[key] for key in sorted(merged)]


def _discover_external_runtime_dependencies(
    skills: list[dict[str, object]],
    *,
    install_root: Path,
    codex_home: Path,
) -> list[dict[str, object]]:
    discovered: list[dict[str, object]] = []
    for skill in skills:
        discovered.extend(
            _load_external_runtime_dependencies_for_skill(
                skill,
                install_root=install_root,
                codex_home=codex_home,
            )
        )
    return _merge_external_runtime_dependencies(discovered)


def _rsync(src: Path, dst: Path) -> list[str]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["rsync", "-a", "--delete"]
    for pattern in RSYNC_EXCLUDES:
        cmd.extend(["--exclude", pattern])
    cmd.extend([f"{src}/", f"{dst}/"])
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "rsync failed")
    return cmd


def _copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)


def _ensure_directory(path: Path) -> bool:
    existed = path.exists()
    path.mkdir(parents=True, exist_ok=True)
    return existed


def _snapshot_relative_tree(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}

    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            snapshot[relative] = "symlink"
        elif path.is_dir():
            snapshot[relative] = "dir"
        else:
            snapshot[relative] = "file"
    return snapshot


def _collect_created_entries(
    before_snapshot: dict[str, str],
    after_snapshot: dict[str, str],
) -> list[dict[str, str]]:
    created_entries: list[dict[str, str]] = []
    for relative_path, kind in after_snapshot.items():
        if relative_path in before_snapshot:
            continue
        created_entries.append({"path": relative_path, "kind": kind})
    return created_entries


def _normalize_external_dependency_mode() -> str:
    normalized = os.environ.get(
        EXTERNAL_DEPENDENCY_INSTALL_MODE_ENV,
        DEFAULT_EXTERNAL_DEPENDENCY_MODE,
    ).strip().lower()
    if normalized not in {"auto", "stub"}:
        raise ValueError(
            f"{EXTERNAL_DEPENDENCY_INSTALL_MODE_ENV} must be auto or stub; got: {normalized}"
        )
    return normalized


def _validate_required_artifacts(
    dependency: dict[str, object],
    *,
    artifacts: list[dict[str, object]],
) -> None:
    for artifact in artifacts:
        path = Path(str(artifact["path"]))
        kind = str(artifact.get("kind") or "path")
        if kind == "file":
            if not path.is_file():
                raise FileNotFoundError(
                    f"required external dependency file is missing for {dependency['dependency_id']}: {path}"
                )
            continue
        if kind == "dir":
            if not path.is_dir():
                raise FileNotFoundError(
                    f"required external dependency directory is missing for {dependency['dependency_id']}: {path}"
                )
            continue
        if kind == "nonempty_dir":
            if not path.is_dir() or not any(path.iterdir()):
                raise FileNotFoundError(
                    f"required external dependency directory is empty for {dependency['dependency_id']}: {path}"
                )
            continue
        raise ValueError(f"unsupported required artifact kind: {kind}")


def _install_external_dependency_stub(
    dependency: dict[str, object],
    *,
    install_root: Path,
) -> None:
    dependency_root = Path(str(dependency["install_root"]))
    dependency_root.mkdir(parents=True, exist_ok=True)

    binary_path = Path(str(dependency["binary_path"]))
    binary_path.parent.mkdir(parents=True, exist_ok=True)
    binary_name = str(dependency["binary_name"])
    default_browser_root = dependency_root / "ms-playwright"
    stub_script = (
        "#!/bin/sh\n"
        "if [ \"$1\" = \"--version\" ]; then\n"
        f"  echo '{binary_name} stub 1.0.0'\n"
        "  exit 0\n"
        "fi\n"
        "if [ \"$1\" = \"install\" ]; then\n"
        f"  target_dir=\"${{PLAYWRIGHT_BROWSERS_PATH:-{default_browser_root}}}\"\n"
        "  mkdir -p \"$target_dir/chrome-headless-shell-linux64\"\n"
        "  touch \"$target_dir/chrome-headless-shell-linux64/chrome-headless-shell\"\n"
        "  exit 0\n"
        "fi\n"
        "exit 0\n"
    )
    binary_path.write_text(stub_script, encoding="utf-8")
    binary_path.chmod(binary_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    for artifact in dependency["required_artifacts"]:
        path = Path(str(artifact["path"]))
        kind = str(artifact.get("kind") or "path")
        if kind in {"dir", "nonempty_dir"}:
            path.mkdir(parents=True, exist_ok=True)
            if kind == "nonempty_dir":
                placeholder = path / ".octopus-os-placeholder"
                placeholder.write_text("placeholder\n", encoding="utf-8")
        elif kind == "file":
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("placeholder\n", encoding="utf-8")

    stub_env = _apply_environment_overrides(
        dict(os.environ),
        dict(dependency.get("runtime_env") or {}),
    )
    for command_entry in dependency["install_commands"]:
        env = _apply_environment_overrides(stub_env, dict(command_entry.get("env") or {}))
        _run_command([str(item) for item in command_entry["argv"]], env=env)

    _validate_required_artifacts(
        dependency,
        artifacts=list(dependency.get("required_artifacts") or []),
    )


def _install_external_runtime_dependencies(
    dependencies: list[dict[str, object]],
    *,
    install_root: Path,
    codex_home: Path,
    backup_root: Path,
) -> list[dict[str, object]]:
    if not dependencies:
        return []

    install_mode = _normalize_external_dependency_mode()
    npm_env = _prepare_managed_npm_environment(
        install_root,
        home_root=codex_home,
        namespace="npm_external_runtime_dependencies",
    )
    installed_dependencies: list[dict[str, object]] = []

    for dependency in dependencies:
        dependency_root = Path(str(dependency["install_root"]))
        backup_path = None
        if dependency_root.exists():
            backup_path = backup_root / str(dependency["dependency_id"])
            _copy_tree(dependency_root, backup_path)
            shutil.rmtree(dependency_root)

        if install_mode == "stub":
            _install_external_dependency_stub(dependency, install_root=install_root)
        else:
            base_env = _apply_environment_overrides(
                npm_env,
                dict(dependency.get("runtime_env") or {}),
            )
            for command_entry in dependency["install_commands"]:
                env = _apply_environment_overrides(base_env, dict(command_entry.get("env") or {}))
                _run_command([str(item) for item in command_entry["argv"]], env=env)

            for command_entry in dependency["validate_commands"]:
                env = _apply_environment_overrides(base_env, dict(command_entry.get("env") or {}))
                _run_command([str(item) for item in command_entry["argv"]], env=env)

            _validate_required_artifacts(
                dependency,
                artifacts=list(dependency.get("required_artifacts") or []),
            )

        installed_dependencies.append(
            {
                "dependency_id": dependency["dependency_id"],
                "display_name": dependency["display_name"],
                "install_type": dependency["install_type"],
                "install_root": str(dependency_root),
                "binary_path": str(dependency["binary_path"]),
                "manifest_path": dependency["manifest_path"],
                "required_by_skills": list(dependency["required_by_skills"]),
                "runtime_env": dict(dependency.get("runtime_env") or {}),
                "required_artifacts": list(dependency.get("required_artifacts") or []),
                "host_requirements": list(dependency.get("host_requirements") or []),
                "backup_path": str(backup_path) if backup_path else None,
            }
        )

    return installed_dependencies


def _initialize_product_directories(install_root: Path) -> list[dict[str, object]]:
    directories = [
        ("console_root", _derive_console_root(install_root)),
        ("skill_runtime_root", _derive_skill_runtime_root(install_root)),
        ("skill_result_root", _derive_skill_result_root(install_root)),
        ("octopus_os_root", _derive_octopus_os_root(install_root)),
    ]
    initialized: list[dict[str, object]] = []
    for name, path in directories:
        initialized.append(
            {
                "name": name,
                "path": str(path),
                "existed_before_install": _ensure_directory(path),
            }
        )
    return initialized


def _build_recommended_install_command(
    install_root: Path,
    github_binding: dict[str, object],
) -> str:
    repo = str(github_binding.get("repo") or "git@github.com:YOUR_ACCOUNT/octopus-os-skills.git")
    auth_mode = str(github_binding.get("auth_mode") or "ssh")
    parts = [
        "python3",
        "product_tools/octopus_os_agent_console.py",
        "install",
        "--runtime-target",
        SUPPORTED_RUNTIME_TARGET,
        "--install-root",
        str(install_root),
        "--github-skill-repo",
        repo,
        "--github-auth-mode",
        auth_mode,
        "--acknowledge-github-control-risk",
    ]
    if auth_mode == "api":
        parts.extend(
            [
                "--github-api-env-var",
                str(github_binding.get("github_api_env_var") or DEFAULT_GITHUB_API_ENV_VAR),
            ]
        )
    elif github_binding.get("github_ssh_key_path"):
        parts.extend(["--github-ssh-key-path", str(github_binding["github_ssh_key_path"])])
    return _shell_join(parts)


def _build_plan(
    repo_root: Path,
    install_root: Path,
    workspace_root: Path,
    github_binding: dict[str, object],
    codex_cli_strategy: dict[str, object],
) -> dict[str, object]:
    codex_root = _derive_codex_root(install_root)
    codex_home = _derive_codex_home(install_root)
    codex_cli_bin = Path(str(codex_cli_strategy["codex_cli_bin"]))
    cleanliness = _summarize_codex_root_cleanliness(codex_root)
    skills: list[dict[str, object]] = []
    overwrite_skills: list[str] = []
    for skill in _discover_skill_roots(repo_root):
        destination = codex_root / skill["destination_name"]
        exists = destination.exists()
        if exists:
            overwrite_skills.append(skill["name"])
        skills.append(
            {
                **skill,
                "destination": str(destination),
                "destination_exists": exists,
            }
        )
    external_runtime_dependencies = _discover_external_runtime_dependencies(
        skills,
        install_root=install_root,
        codex_home=codex_home,
    )
    install_command = _build_recommended_install_command(install_root, github_binding)
    return {
        "repo_root": str(repo_root),
        "skills_root": str(_resolve_skills_root(repo_root)),
        "install_root": str(install_root),
        "codex_home": str(codex_home),
        "codex_root": str(codex_root),
        "codex_cli_bin": str(codex_cli_bin),
        "codex_cli_mode": str(codex_cli_strategy["mode"]),
        "codex_cli_requested_mode": str(codex_cli_strategy["requested_mode"]),
        "codex_cli_resolved_from": codex_cli_strategy.get("resolved_from"),
        "console_root": str(_derive_console_root(install_root)),
        "workspace_root": str(workspace_root),
        "skill_runtime_root": str(_derive_skill_runtime_root(install_root)),
        "skill_result_root": str(_derive_skill_result_root(install_root)),
        "octopus_os_root": str(_derive_octopus_os_root(install_root)),
        "supported_host_env": SUPPORTED_HOST_ENV_LABEL,
        "supported_runtime_target": SUPPORTED_RUNTIME_TARGET,
        "supported_runtime_label": SUPPORTED_RUNTIME_LABEL,
        "codex_cli_install_command": codex_cli_strategy["codex_cli_install_command"],
        "codex_cli_version": codex_cli_strategy.get("version"),
        "codex_launch_command": _build_codex_launch_command(codex_cli_bin, codex_home, workspace_root),
        "recommended_install_command": install_command,
        "recommended_install_and_launch_command": f"{install_command} && {_build_codex_launch_command(codex_cli_bin, codex_home, workspace_root)}",
        "codex_root_cleanliness": cleanliness,
        "skills": skills,
        "overwrite_skills": overwrite_skills,
        "external_runtime_dependencies": external_runtime_dependencies,
        "workspace_exists": workspace_root.exists(),
        "github_binding": github_binding,
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_manifest(state_root: Path, session_id: str | None) -> tuple[Path, dict[str, object]]:
    if session_id:
        manifest_path = state_root / session_id / "install_manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest does not exist: {manifest_path}")
        return manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest_paths = sorted(state_root.glob("*/install_manifest.json"))
    if not manifest_paths:
        raise FileNotFoundError(f"no install manifest found under state root: {state_root}")
    manifest_path = manifest_paths[-1]
    return manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))


def _label(lang: str, en: str, zh: str) -> str:
    if lang == "zh":
        return zh
    if lang == "bilingual":
        return f"{en} / {zh}"
    return en


def _clear_screen() -> None:
    print("\033[2J\033[H", end="")


def _print_header(lang: str, title_en: str, title_zh: str) -> None:
    _clear_screen()
    title = _label(lang, title_en, title_zh)
    line = "=" * len(title)
    print(line)
    print(title)
    print(line)
    print()


def _prompt_text(lang: str, prompt_en: str, prompt_zh: str, default: str) -> str:
    prompt = _label(lang, prompt_en, prompt_zh)
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer or default


def _prompt_confirm(lang: str, prompt_en: str, prompt_zh: str, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    prompt = _label(lang, prompt_en, prompt_zh)
    answer = input(f"{prompt} [{suffix}]: ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes", "1", "true", "ok", "zh", "en"}


def _prompt_choice(
    lang: str,
    prompt_en: str,
    prompt_zh: str,
    options: dict[str, str],
    default: str,
) -> str:
    prompt = _label(lang, prompt_en, prompt_zh)
    answer = input(f"{prompt} [{default}]: ").strip().lower()
    selected = answer or default
    if selected not in options:
        raise ValueError(f"unsupported choice: {selected}")
    return selected


def _select_wizard_language(args: argparse.Namespace) -> str:
    if args.wizard_language and args.wizard_language != "auto":
        return args.wizard_language
    if args.yes:
        return "bilingual"

    _clear_screen()
    print("==============================")
    print("Octopus OS Wizard Language")
    print("章鱼 OS 向导语言")
    print("==============================")
    print()
    print("1. English")
    print("2. 中文")
    print("3. Bilingual / 双语")
    print()
    answer = input("Select language / 选择语言 [3]: ").strip() or "3"
    mapping = {"1": "en", "2": "zh", "3": "bilingual"}
    return mapping.get(answer, "bilingual")


def _print_plan_summary(lang: str, plan: dict[str, object]) -> None:
    skills = plan["skills"]
    external_runtime_dependencies = plan["external_runtime_dependencies"]
    workspace_exists = plan["workspace_exists"]
    cleanliness = plan["codex_root_cleanliness"]
    github_binding = plan["github_binding"]
    print(_label(lang, "Product:", "产品："), PRODUCT_NAME)
    print(_label(lang, "Supported host:", "受支持宿主："), SUPPORTED_HOST_ENV_LABEL)
    print(_label(lang, "Supported runtime:", "受支持运行时："), SUPPORTED_RUNTIME_LABEL)
    print(_label(lang, "Install root:", "安装根目录："), plan["install_root"])
    print(_label(lang, "Codex home:", "Codex Home："), plan["codex_home"])
    print(_label(lang, "Codex skills root:", "Codex 技能根目录："), plan["codex_root"])
    print(_label(lang, "Console root:", "Console 根目录："), plan["console_root"])
    print(_label(lang, "Workspace root:", "工作区根目录："), plan["workspace_root"])
    print(_label(lang, "Skill runtime root:", "技能运行时根目录："), plan["skill_runtime_root"])
    print(_label(lang, "Skill result root:", "技能结果根目录："), plan["skill_result_root"])
    print(_label(lang, "Octopus OS root:", "章鱼 OS 根目录："), plan["octopus_os_root"])
    print(_label(lang, "Codex CLI mode:", "Codex CLI 模式："), plan["codex_cli_mode"])
    print(_label(lang, "Codex CLI resolved from:", "Codex CLI 来源："), plan["codex_cli_resolved_from"])
    print(_label(lang, "Codex CLI install command:", "Codex CLI 安装命令："), plan["codex_cli_install_command"])
    print(_label(lang, "Launch command:", "启动命令："), plan["codex_launch_command"])
    print(_label(lang, "Codex root clean state:", "Codex 根目录洁净状态："), cleanliness["state"])
    print(_label(lang, "Unexpected codex root entries:", "Codex 根目录异常项："), cleanliness["unexpected_root_entries"])
    print(_label(lang, "GitHub skill repo:", "GitHub 技能仓库："), github_binding.get("repo"))
    print(_label(lang, "GitHub auth mode:", "GitHub 认证模式："), github_binding.get("auth_mode"))
    print(_label(lang, "Syncable skills:", "可同步技能："), len(skills))
    for skill in skills:
        print(f"  - {skill['name']} -> {skill['destination']}")
    print(_label(lang, "External runtime dependencies:", "外部运行时依赖："), len(external_runtime_dependencies))
    for dependency in external_runtime_dependencies:
        required_by = ", ".join(dependency["required_by_skills"])
        print(f"  - {dependency['dependency_id']} -> {dependency['install_root']} [{required_by}]")
    print()
    if workspace_exists:
        print(_label(lang, "The workspace root already exists.", "工作区根目录已存在。"))
        print()

    print(_label(lang, "Current warning:", "当前警告："))
    print(f"  - {_label(lang, 'This build is for local trial only.', '当前构建仅供本地试用。')}")
    print(f"  - {_label(lang, 'The repository may change again within 10 to 15 minutes.', '仓库可能在 10 到 15 分钟内再次变化。')}")
    print(f"  - {_label(lang, 'Installable does not mean stable.', '可安装不代表稳定。')}")
    print(
        f"  - {_label(lang, 'Only Codex with GPT-5.4 high reasoning effort is supported.', '仅支持 Codex + GPT-5.4 high reasoning effort。')}"
    )
    print(
        f'  - {_label(lang, "Only Codex CLI in the author\'s Codex CLI + VS Code environment is currently supported.", "当前仅支持作者使用中的 Codex CLI + VS Code 环境。")}'
    )
    print(
        f"  - {_label(lang, 'Use a fresh GitHub account, or back up and clear the existing one before binding it to Octopus OS.', '请使用新的 GitHub 账户，或先完整备份并清空旧账户资产后再绑定到 Octopus OS。')}"
    )
    print()


def _write_github_binding(workspace_root: Path, github_binding: dict[str, object]) -> Path:
    binding_path = workspace_root / PRODUCT_RUNTIME_DIR / GITHUB_BINDING_FILE
    _write_json(binding_path, github_binding)
    return binding_path


def plan_command(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    install_root = _resolve_install_root(args.install_root, args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root, install_root)
    github_binding = _build_github_binding(args, require_complete=False)
    codex_cli_strategy = _resolve_codex_cli_strategy(
        install_root,
        requested_mode=_normalize_codex_cli_mode(getattr(args, "codex_cli_mode", None)),
        provided_bin=getattr(args, "codex_cli_bin", None),
        execute_install=False,
    )
    payload = {
        "status": "ok",
        "action": "plan",
        "product_name": PRODUCT_NAME,
        "plan": _build_plan(repo_root, install_root, workspace_root, github_binding, codex_cli_strategy),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def install_command(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    install_root = _resolve_install_root(args.install_root, args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root, install_root)
    state_root = _resolve_state_root(args.state_root)
    runtime_target = _require_supported_runtime_target(getattr(args, "runtime_target", None))
    github_binding = _build_github_binding(args, require_complete=True)
    install_root_existed_before_install = install_root.exists()
    codex_home = _derive_codex_home(install_root)
    codex_home_existed_before_install = codex_home.exists()
    codex_root = _derive_codex_root(install_root)
    codex_root_existed_before_install = codex_root.exists()
    install_root_snapshot_before_codex = _snapshot_relative_tree(install_root)
    codex_install = _resolve_codex_cli_strategy(
        install_root,
        requested_mode=_normalize_codex_cli_mode(getattr(args, "codex_cli_mode", None)),
        provided_bin=getattr(args, "codex_cli_bin", None),
        execute_install=True,
    )
    install_root_snapshot_after_codex = _snapshot_relative_tree(install_root)
    codex_install["created_entries"] = (
        _collect_created_entries(install_root_snapshot_before_codex, install_root_snapshot_after_codex)
        if codex_install["mode"] == "install"
        else []
    )
    clean_summary, removed_forbidden_codex_root_files = _assert_clean_codex_root(codex_root)
    plan = _build_plan(repo_root, install_root, workspace_root, github_binding, codex_install)

    if workspace_root.exists() and any(workspace_root.iterdir()) and not args.allow_replace_workspace:
        raise ValueError(
            "workspace root already exists and is not empty; rerun with --allow-replace-workspace"
        )

    session_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    session_root = state_root / session_id
    backup_root = session_root / "backups"
    external_dependency_backup_root = session_root / "external_dependency_backups"
    product_directories = _initialize_product_directories(install_root)
    installed_external_runtime_dependencies = _install_external_runtime_dependencies(
        list(plan["external_runtime_dependencies"]),
        install_root=install_root,
        codex_home=codex_home,
        backup_root=external_dependency_backup_root,
    )

    installed_entries: list[dict[str, object]] = []
    for skill in plan["skills"]:
        source = Path(str(skill["source"]))
        destination = Path(str(skill["destination"]))
        backup_path = None
        if destination.exists():
            backup_path = backup_root / str(skill["name"])
            _copy_tree(destination, backup_path)
        command = _rsync(source, destination)
        installed_entries.append(
            {
                "name": skill["name"],
                "source": str(source),
                "destination": str(destination),
                "had_existing_destination": bool(skill["destination_exists"]),
                "backup_path": str(backup_path) if backup_path else None,
                "command": command,
            }
        )

    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    _rsync(repo_root, workspace_root)

    github_binding_path = _write_github_binding(workspace_root, github_binding)
    workspace_marker = workspace_root / WORKSPACE_MARKER
    _write_json(
        workspace_marker,
        {
            "session_id": session_id,
            "repo_root": str(repo_root),
            "install_root": str(install_root),
            "workspace_root": str(workspace_root),
        },
    )

    manifest = {
        "session_id": session_id,
        "product_name": PRODUCT_NAME,
        "supported_runtime_target": runtime_target,
        "repo_root": str(repo_root),
        "install_root": str(install_root),
        "install_root_existed_before_install": install_root_existed_before_install,
        "codex_home": str(codex_home),
        "codex_home_existed_before_install": codex_home_existed_before_install,
        "codex_root": str(codex_root),
        "codex_root_existed_before_install": codex_root_existed_before_install,
        "codex_cli_bin": codex_install["codex_cli_bin"],
        "codex_cli_install": codex_install,
        "workspace_root": str(workspace_root),
        "product_directories": product_directories,
        "installed_entries": installed_entries,
        "workspace_marker": str(workspace_marker),
        "github_binding_path": str(github_binding_path),
        "github_binding": github_binding,
        "codex_root_cleanliness": clean_summary,
        "removed_forbidden_codex_root_files": removed_forbidden_codex_root_files,
        "external_runtime_dependencies": installed_external_runtime_dependencies,
    }
    manifest_path = session_root / "install_manifest.json"
    _write_json(manifest_path, manifest)

    payload = {
        "status": "ok",
        "action": "install",
        "manifest_path": str(manifest_path),
        "session_id": session_id,
        "install_root": str(install_root),
        "codex_root": str(codex_root),
        "console_root": str(_derive_console_root(install_root)),
        "workspace_root": str(workspace_root),
        "skill_runtime_root": str(_derive_skill_runtime_root(install_root)),
        "skill_result_root": str(_derive_skill_result_root(install_root)),
        "octopus_os_root": str(_derive_octopus_os_root(install_root)),
        "supported_host_env": SUPPORTED_HOST_ENV_LABEL,
        "supported_runtime_target": runtime_target,
        "codex_cli_mode": codex_install["mode"],
        "codex_cli_requested_mode": codex_install["requested_mode"],
        "codex_cli_resolved_from": codex_install.get("resolved_from"),
        "codex_cli_bin": codex_install["codex_cli_bin"],
        "codex_cli_version": codex_install["version"],
        "codex_cli_install_command": codex_install["codex_cli_install_command"],
        "codex_launch_command": _build_codex_launch_command(
            Path(str(codex_install["codex_cli_bin"])),
            _derive_codex_home(install_root),
            workspace_root,
        ),
        "recommended_install_and_launch_command": plan["recommended_install_and_launch_command"],
        "removed_forbidden_codex_root_files": removed_forbidden_codex_root_files,
        "codex_root_cleanliness": clean_summary,
        "github_binding_path": str(github_binding_path),
        "github_binding": github_binding,
        "external_runtime_dependencies": installed_external_runtime_dependencies,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def uninstall_command(args: argparse.Namespace) -> int:
    state_root = _resolve_state_root(args.state_root)
    manifest_path, manifest = _load_manifest(state_root, args.session_id)
    install_root = Path(str(manifest["install_root"]))
    codex_home = Path(str(manifest["codex_home"]))
    codex_root = Path(str(manifest["codex_root"]))
    workspace_root = Path(str(manifest["workspace_root"]))

    restored_backups: list[str] = []
    removed_entries: list[str] = []
    restored_external_runtime_dependency_backups: list[str] = []
    removed_external_runtime_dependencies: list[str] = []

    for entry in reversed(list(manifest["installed_entries"])):
        destination = Path(str(entry["destination"]))
        backup_path_raw = entry.get("backup_path")
        if destination.exists():
            shutil.rmtree(destination)
            removed_entries.append(str(destination))
        if backup_path_raw:
            backup_path = Path(str(backup_path_raw))
            if backup_path.exists():
                _copy_tree(backup_path, destination)
                restored_backups.append(str(destination))

    for entry in reversed(list(manifest.get("external_runtime_dependencies", []))):
        dependency_root = Path(str(entry["install_root"]))
        backup_path_raw = entry.get("backup_path")
        if dependency_root.exists():
            shutil.rmtree(dependency_root)
            removed_external_runtime_dependencies.append(str(dependency_root))
        if backup_path_raw:
            backup_path = Path(str(backup_path_raw))
            if backup_path.exists():
                _copy_tree(backup_path, dependency_root)
                restored_external_runtime_dependency_backups.append(str(dependency_root))

    workspace_removed = False
    marker_path = workspace_root / WORKSPACE_MARKER
    if workspace_root.exists() and marker_path.exists():
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        if marker.get("session_id") == manifest.get("session_id"):
            shutil.rmtree(workspace_root)
            workspace_removed = True

    removed_product_directories: list[str] = []
    kept_nonempty_product_directories: list[str] = []
    for entry in reversed(list(manifest.get("product_directories", []))):
        if entry.get("existed_before_install"):
            continue
        path = Path(str(entry["path"]))
        if not path.exists():
            continue
        try:
            path.rmdir()
            removed_product_directories.append(str(path))
        except OSError:
            kept_nonempty_product_directories.append(str(path))

    codex_cli_install = manifest.get("codex_cli_install", {})
    removed_codex_cli_entries: list[str] = []
    kept_nonempty_codex_cli_entries: list[str] = []
    for entry in reversed(list(codex_cli_install.get("created_entries", []))):
        target = install_root / str(entry["path"])
        kind = str(entry.get("kind") or "")
        if not target.exists():
            continue
        if kind in {"file", "symlink"}:
            target.unlink()
            removed_codex_cli_entries.append(str(target))
            continue
        if kind == "dir":
            try:
                target.rmdir()
                removed_codex_cli_entries.append(str(target))
            except OSError:
                kept_nonempty_codex_cli_entries.append(str(target))

    removed_runtime_roots: list[str] = []
    kept_nonempty_runtime_roots: list[str] = []
    root_cleanup_candidates = [
        (codex_root, bool(manifest.get("codex_root_existed_before_install"))),
        (codex_home, bool(manifest.get("codex_home_existed_before_install"))),
        (install_root, bool(manifest.get("install_root_existed_before_install"))),
    ]
    for path, existed_before_install in root_cleanup_candidates:
        if existed_before_install or not path.exists():
            continue
        try:
            path.rmdir()
            removed_runtime_roots.append(str(path))
        except OSError:
            kept_nonempty_runtime_roots.append(str(path))

    payload = {
        "status": "ok",
        "action": "uninstall",
        "manifest_path": str(manifest_path),
        "session_id": manifest["session_id"],
        "removed_entries": removed_entries,
        "restored_backups": restored_backups,
        "removed_external_runtime_dependencies": removed_external_runtime_dependencies,
        "restored_external_runtime_dependency_backups": restored_external_runtime_dependency_backups,
        "workspace_removed": workspace_removed,
        "removed_product_directories": removed_product_directories,
        "kept_nonempty_product_directories": kept_nonempty_product_directories,
        "removed_codex_cli_entries": removed_codex_cli_entries,
        "kept_nonempty_codex_cli_entries": kept_nonempty_codex_cli_entries,
        "removed_runtime_roots": removed_runtime_roots,
        "kept_nonempty_runtime_roots": kept_nonempty_runtime_roots,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def wizard_command(args: argparse.Namespace) -> int:
    lang = _select_wizard_language(args)
    repo_root = _resolve_repo_root(args.repo_root)
    install_root = _resolve_install_root(args.install_root, args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root, install_root)
    state_root = _resolve_state_root(args.state_root)

    if not args.yes:
        _print_header(lang, "Octopus OS Installation Wizard", "章鱼 OS 安装向导")
        install_root = Path(
            _prompt_text(
                lang,
                "Dedicated Codex install root",
                "专用 Codex 安装根目录",
                str(install_root),
            )
        ).expanduser().resolve()
        workspace_root = _resolve_workspace_root(args.workspace_root, install_root)
        args.github_skill_repo = _prompt_text(
            lang,
            "GitHub skill repository for Octopus OS",
            "Octopus OS 使用的 GitHub 技能仓库",
            str(getattr(args, "github_skill_repo", "") or "git@github.com:YOUR_ACCOUNT/octopus-os-skills.git"),
        )
        args.github_auth_mode = _prompt_choice(
            lang,
            "GitHub auth mode: ssh or api",
            "GitHub 认证模式：ssh 或 api",
            {"ssh": "ssh", "api": "api"},
            str(getattr(args, "github_auth_mode", "") or "ssh"),
        )
        if args.github_auth_mode == "ssh":
            args.github_ssh_key_path = _prompt_text(
                lang,
                "SSH key path (optional)",
                "SSH key 路径（可选）",
                str(getattr(args, "github_ssh_key_path", "") or "~/.ssh/id_ed25519"),
            )
            args.github_api_env_var = None
        else:
            args.github_api_env_var = _prompt_text(
                lang,
                "GitHub API token env var",
                "GitHub API Token 环境变量名",
                str(getattr(args, "github_api_env_var", "") or DEFAULT_GITHUB_API_ENV_VAR),
            )
            args.github_ssh_key_path = None
        runtime_confirmed = _prompt_confirm(
            lang,
            "Confirm that the target runtime is Codex with GPT-5.4 high reasoning effort only.",
            "请确认目标运行时仅为 Codex + GPT-5.4 high reasoning effort。",
            default=False,
        )
        if not runtime_confirmed:
            raise ValueError("wizard aborted because the supported runtime constraint was not accepted")
        github_risk_confirmed = _prompt_confirm(
            lang,
            "Confirm that you are using a fresh GitHub account or have already backed up and cleared the existing one.",
            "请确认你使用的是新的 GitHub 账户，或旧账户资产已完成备份并清空。",
            default=False,
        )
        if not github_risk_confirmed:
            raise ValueError("wizard aborted because the GitHub control risk warning was not accepted")
        args.acknowledge_github_control_risk = True
        args.runtime_target = SUPPORTED_RUNTIME_TARGET

    runtime_target = _require_supported_runtime_target(getattr(args, "runtime_target", None))
    github_binding = _build_github_binding(args, require_complete=True)
    codex_cli_strategy = _resolve_codex_cli_strategy(
        install_root,
        requested_mode=_normalize_codex_cli_mode(getattr(args, "codex_cli_mode", None)),
        provided_bin=getattr(args, "codex_cli_bin", None),
        execute_install=False,
    )
    plan = _build_plan(repo_root, install_root, workspace_root, github_binding, codex_cli_strategy)

    if not args.yes:
        _print_header(lang, "Install Plan", "安装计划")
        _print_plan_summary(lang, plan)

    allow_replace_workspace = args.allow_replace_workspace
    if plan["workspace_exists"] and not allow_replace_workspace:
        if args.yes:
            allow_replace_workspace = True
        else:
            allow_replace_workspace = _prompt_confirm(
                lang,
                "Allow replacing the existing workspace directory?",
                "允许替换现有工作区目录吗？",
                default=False,
            )
        if not allow_replace_workspace:
            raise ValueError("wizard aborted because workspace replacement approval was not granted")

    if not args.yes:
        confirmed = _prompt_confirm(
            lang,
            "Proceed with installation now?",
            "现在开始安装吗？",
            default=True,
        )
        if not confirmed:
            raise ValueError("wizard aborted by user")

    install_args = SimpleNamespace(
        repo_root=str(repo_root),
        install_root=str(install_root),
        codex_root=None,
        workspace_root=str(workspace_root),
        state_root=str(state_root),
        runtime_target=runtime_target,
        allow_replace_workspace=allow_replace_workspace,
        github_skill_repo=github_binding["repo"],
        github_auth_mode=github_binding["auth_mode"],
        github_ssh_key_path=github_binding.get("github_ssh_key_path"),
        github_api_env_var=github_binding.get("github_api_env_var"),
        codex_cli_mode=_normalize_codex_cli_mode(getattr(args, "codex_cli_mode", None)),
        codex_cli_bin=getattr(args, "codex_cli_bin", None),
        acknowledge_github_control_risk=True,
    )
    result = install_command(install_args)
    if not args.yes:
        print()
        print(_label(lang, "Installation finished.", "安装完成。"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Octopus OS product installer and cleanup entrypoint"
    )
    parser.add_argument("action", choices=["plan", "install", "uninstall", "wizard"])
    parser.add_argument("--repo-root")
    parser.add_argument("--install-root")
    parser.add_argument("--codex-root")
    parser.add_argument("--workspace-root")
    parser.add_argument("--state-root")
    parser.add_argument("--session-id")
    parser.add_argument("--runtime-target")
    parser.add_argument("--allow-replace-workspace", action="store_true")
    parser.add_argument("--github-skill-repo")
    parser.add_argument("--github-auth-mode", choices=["ssh", "api"])
    parser.add_argument("--github-ssh-key-path")
    parser.add_argument("--github-api-env-var")
    parser.add_argument("--codex-cli-mode", choices=["auto", "attach", "install"], default=DEFAULT_CODEX_CLI_MODE)
    parser.add_argument("--codex-cli-bin")
    parser.add_argument("--acknowledge-github-control-risk", action="store_true")
    parser.add_argument("--wizard-language", choices=["auto", "en", "zh", "bilingual"], default="auto")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    if args.action == "plan":
        return plan_command(args)
    if args.action == "install":
        return install_command(args)
    if args.action == "wizard":
        return wizard_command(args)
    return uninstall_command(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
