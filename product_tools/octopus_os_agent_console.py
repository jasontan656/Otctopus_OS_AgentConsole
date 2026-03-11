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
DEFAULT_WORKSPACE_DIR_NAME = "octopus-os-agent-console"
CODEX_HOME_DIR_NAME = ".codex"
CODEX_CLI_PACKAGE = "@openai/codex@latest"
CODEX_CLI_INSTALL_MODE_ENV = "OCTOPUS_OS_CODEX_INSTALL_MODE"
DEFAULT_GITHUB_API_ENV_VAR = "GITHUB_TOKEN"
PRODUCT_NAME = "Octopus OS - Natural-Language-Driven Multi-Agent Console"
SUPPORTED_RUNTIME_TARGET = "codex-gpt-5.4-high"
SUPPORTED_RUNTIME_LABEL = "Codex + GPT-5.4 high reasoning effort"
SUPPORTED_HOST_ENV_LABEL = "Codex CLI + VS Code"
FORBIDDEN_CODEX_ROOT_FILES = ("AGENTS.md",)
ALLOWED_CLEAN_CODEX_ROOT_ENTRIES = {SYSTEM_SKILL_NAMESPACE}


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


def _resolve_workspace_root(raw: str | None, install_root: Path) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (install_root.parent / DEFAULT_WORKSPACE_DIR_NAME).resolve()


def _resolve_state_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".octopus-os-agent-console" / "install_sessions").resolve()


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


def _build_codex_cli_install_command(install_root: Path) -> str:
    return _shell_join(["npm", "install", "-g", CODEX_CLI_PACKAGE, "--prefix", str(install_root)])


def _build_codex_launch_command(install_root: Path, workspace_root: Path) -> str:
    command = _shell_join(
        [
            str(_derive_codex_cli_bin(install_root)),
            "-C",
            str(workspace_root),
            "-m",
            "gpt-5.4",
            "-c",
            'model_reasoning_effort="high"',
        ]
    )
    return f"HOME={shlex.quote(str(install_root))} {command}"


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
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "failed to install Codex CLI")
    if not codex_bin.exists():
        raise FileNotFoundError(f"Codex CLI install completed but binary is missing: {codex_bin}")

    version_completed = subprocess.run(
        [str(codex_bin), "--version"],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(install_root)},
    )
    version = version_completed.stdout.strip() or version_completed.stderr.strip() or "unknown"
    return {
        "mode": "npm",
        "command": command,
        "codex_cli_bin": str(codex_bin),
        "codex_cli_install_command": _build_codex_cli_install_command(install_root),
        "version": version,
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
    shutil.copytree(source, destination)


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
) -> dict[str, object]:
    codex_root = _derive_codex_root(install_root)
    codex_cli_bin = _derive_codex_cli_bin(install_root)
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
    install_command = _build_recommended_install_command(install_root, github_binding)
    return {
        "repo_root": str(repo_root),
        "skills_root": str(_resolve_skills_root(repo_root)),
        "install_root": str(install_root),
        "codex_home": str(_derive_codex_home(install_root)),
        "codex_root": str(codex_root),
        "codex_cli_bin": str(codex_cli_bin),
        "workspace_root": str(workspace_root),
        "supported_host_env": SUPPORTED_HOST_ENV_LABEL,
        "supported_runtime_target": SUPPORTED_RUNTIME_TARGET,
        "supported_runtime_label": SUPPORTED_RUNTIME_LABEL,
        "codex_cli_install_command": _build_codex_cli_install_command(install_root),
        "codex_launch_command": _build_codex_launch_command(install_root, workspace_root),
        "recommended_install_command": install_command,
        "recommended_install_and_launch_command": (
            f"{install_command} && {_build_codex_launch_command(install_root, workspace_root)}"
        ),
        "codex_root_cleanliness": cleanliness,
        "skills": skills,
        "overwrite_skills": overwrite_skills,
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
    workspace_exists = plan["workspace_exists"]
    cleanliness = plan["codex_root_cleanliness"]
    github_binding = plan["github_binding"]
    print(_label(lang, "Product:", "产品："), PRODUCT_NAME)
    print(_label(lang, "Supported host:", "受支持宿主："), SUPPORTED_HOST_ENV_LABEL)
    print(_label(lang, "Supported runtime:", "受支持运行时："), SUPPORTED_RUNTIME_LABEL)
    print(_label(lang, "Install root:", "安装根目录："), plan["install_root"])
    print(_label(lang, "Codex home:", "Codex Home："), plan["codex_home"])
    print(_label(lang, "Codex skills root:", "Codex 技能根目录："), plan["codex_root"])
    print(_label(lang, "Workspace root:", "工作区根目录："), plan["workspace_root"])
    print(_label(lang, "Codex CLI install command:", "Codex CLI 安装命令："), plan["codex_cli_install_command"])
    print(_label(lang, "Launch command:", "启动命令："), plan["codex_launch_command"])
    print(_label(lang, "Codex root clean state:", "Codex 根目录洁净状态："), cleanliness["state"])
    print(_label(lang, "Unexpected codex root entries:", "Codex 根目录异常项："), cleanliness["unexpected_root_entries"])
    print(_label(lang, "GitHub skill repo:", "GitHub 技能仓库："), github_binding.get("repo"))
    print(_label(lang, "GitHub auth mode:", "GitHub 认证模式："), github_binding.get("auth_mode"))
    print(_label(lang, "Syncable skills:", "可同步技能："), len(skills))
    for skill in skills:
        print(f"  - {skill['name']} -> {skill['destination']}")
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
    payload = {
        "status": "ok",
        "action": "plan",
        "product_name": PRODUCT_NAME,
        "plan": _build_plan(repo_root, install_root, workspace_root, github_binding),
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
    codex_install = _install_codex_cli_latest(install_root)
    codex_root = _derive_codex_root(install_root)
    clean_summary, removed_forbidden_codex_root_files = _assert_clean_codex_root(codex_root)
    plan = _build_plan(repo_root, install_root, workspace_root, github_binding)

    if workspace_root.exists() and any(workspace_root.iterdir()) and not args.allow_replace_workspace:
        raise ValueError(
            "workspace root already exists and is not empty; rerun with --allow-replace-workspace"
        )

    session_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    session_root = state_root / session_id
    backup_root = session_root / "backups"

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
        "codex_home": str(_derive_codex_home(install_root)),
        "codex_root": str(codex_root),
        "codex_cli_bin": codex_install["codex_cli_bin"],
        "codex_cli_install": codex_install,
        "workspace_root": str(workspace_root),
        "installed_entries": installed_entries,
        "workspace_marker": str(workspace_marker),
        "github_binding_path": str(github_binding_path),
        "github_binding": github_binding,
        "codex_root_cleanliness": clean_summary,
        "removed_forbidden_codex_root_files": removed_forbidden_codex_root_files,
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
        "workspace_root": str(workspace_root),
        "supported_host_env": SUPPORTED_HOST_ENV_LABEL,
        "supported_runtime_target": runtime_target,
        "codex_cli_bin": codex_install["codex_cli_bin"],
        "codex_cli_version": codex_install["version"],
        "codex_cli_install_command": codex_install["codex_cli_install_command"],
        "codex_launch_command": _build_codex_launch_command(install_root, workspace_root),
        "recommended_install_and_launch_command": plan["recommended_install_and_launch_command"],
        "removed_forbidden_codex_root_files": removed_forbidden_codex_root_files,
        "codex_root_cleanliness": clean_summary,
        "github_binding_path": str(github_binding_path),
        "github_binding": github_binding,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def uninstall_command(args: argparse.Namespace) -> int:
    state_root = _resolve_state_root(args.state_root)
    manifest_path, manifest = _load_manifest(state_root, args.session_id)
    workspace_root = Path(str(manifest["workspace_root"]))

    restored_backups: list[str] = []
    removed_entries: list[str] = []

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

    workspace_removed = False
    marker_path = workspace_root / WORKSPACE_MARKER
    if workspace_root.exists() and marker_path.exists():
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        if marker.get("session_id") == manifest.get("session_id"):
            shutil.rmtree(workspace_root)
            workspace_removed = True

    payload = {
        "status": "ok",
        "action": "uninstall",
        "manifest_path": str(manifest_path),
        "session_id": manifest["session_id"],
        "removed_entries": removed_entries,
        "restored_backups": restored_backups,
        "workspace_removed": workspace_removed,
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
    plan = _build_plan(repo_root, install_root, workspace_root, github_binding)

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
