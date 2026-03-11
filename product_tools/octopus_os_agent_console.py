#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
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
PRODUCT_NAME = "Octopus OS - Natural-Language-Driven Multi-Agent Console"
SUPPORTED_RUNTIME_TARGET = "codex-gpt-5.4-high"
SUPPORTED_RUNTIME_LABEL = "Codex + GPT-5.4 high reasoning effort"


def _resolve_repo_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def _resolve_codex_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    env_root = os.environ.get("CODEX_SKILLS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return (Path.home() / ".codex" / "skills").resolve()


def _resolve_workspace_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / "Octopus_OS_Agent_Console").resolve()


def _resolve_state_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".octopus-os-agent-console" / "install_sessions").resolve()


def _validate_codex_root_structure(codex_root: Path) -> None:
    if codex_root.name != "skills" or codex_root.parent.name != ".codex":
        raise ValueError(
            "codex root must be a Codex skills directory shaped like .../.codex/skills; "
            f"refusing install for non-codex target: {codex_root}"
        )


def _require_supported_runtime_target(runtime_target: str | None) -> str:
    normalized = str(runtime_target or "").strip()
    if normalized != SUPPORTED_RUNTIME_TARGET:
        raise ValueError(
            "installation is limited to Codex with GPT-5.4 high reasoning effort; "
            f"rerun with --runtime-target {SUPPORTED_RUNTIME_TARGET}"
        )
    return normalized


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


def _build_plan(repo_root: Path, codex_root: Path, workspace_root: Path) -> dict[str, object]:
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
    return {
        "repo_root": str(repo_root),
        "skills_root": str(_resolve_skills_root(repo_root)),
        "codex_root": str(codex_root),
        "workspace_root": str(workspace_root),
        "supported_runtime_target": SUPPORTED_RUNTIME_TARGET,
        "supported_runtime_label": SUPPORTED_RUNTIME_LABEL,
        "recommended_install_command": (
            "python3 product_tools/octopus_os_agent_console.py install "
            f"--runtime-target {SUPPORTED_RUNTIME_TARGET} "
            f"--codex-root {codex_root} "
            f"--workspace-root {workspace_root}"
        ),
        "skills": skills,
        "overwrite_skills": overwrite_skills,
        "workspace_exists": workspace_root.exists(),
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
    overwrite_skills = plan["overwrite_skills"]
    workspace_exists = plan["workspace_exists"]
    print(_label(lang, "Product:", "产品："), PRODUCT_NAME)
    print(_label(lang, "Supported runtime:", "受支持运行时："), SUPPORTED_RUNTIME_LABEL)
    print(_label(lang, "Codex root:", "Codex 根目录："), plan["codex_root"])
    print(_label(lang, "Workspace root:", "工作区根目录："), plan["workspace_root"])
    print(_label(lang, "Syncable skills:", "可同步技能："), len(skills))
    for skill in skills:
        print(f"  - {skill['name']} -> {skill['destination']}")
    print()
    if overwrite_skills:
        print(_label(lang, "Skills that will overwrite existing installs:", "将覆盖现有安装的技能："))
        for skill_name in overwrite_skills:
            print(f"  - {skill_name}")
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
        f"  - {_label(lang, 'Other models are unsupported, untested, and may behave differently.', '其他模型不受支持、未经测试，效果不可保证。')}"
    )
    print()


def plan_command(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    codex_root = _resolve_codex_root(args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root)
    payload = {
        "status": "ok",
        "action": "plan",
        "product_name": PRODUCT_NAME,
        "plan": _build_plan(repo_root, codex_root, workspace_root),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def install_command(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    codex_root = _resolve_codex_root(args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root)
    state_root = _resolve_state_root(args.state_root)
    runtime_target = _require_supported_runtime_target(getattr(args, "runtime_target", None))
    _validate_codex_root_structure(codex_root)
    plan = _build_plan(repo_root, codex_root, workspace_root)

    if plan["overwrite_skills"] and not args.allow_overwrite_skills:
        raise ValueError(
            "overwrite required for existing codex skills; rerun with --allow-overwrite-skills"
        )
    if workspace_root.exists() and any(workspace_root.iterdir()) and not args.allow_replace_workspace:
        raise ValueError(
            "workspace root already exists and is not empty; rerun with --allow-replace-workspace"
        )

    session_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    session_root = state_root / session_id
    backup_root = session_root / "backups"
    codex_root.mkdir(parents=True, exist_ok=True)

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

    workspace_marker = workspace_root / WORKSPACE_MARKER
    _write_json(
        workspace_marker,
        {
            "session_id": session_id,
            "repo_root": str(repo_root),
            "workspace_root": str(workspace_root),
        },
    )

    manifest = {
        "session_id": session_id,
        "product_name": PRODUCT_NAME,
        "supported_runtime_target": runtime_target,
        "repo_root": str(repo_root),
        "codex_root": str(codex_root),
        "workspace_root": str(workspace_root),
        "installed_entries": installed_entries,
        "workspace_marker": str(workspace_marker),
    }
    manifest_path = session_root / "install_manifest.json"
    _write_json(manifest_path, manifest)

    payload = {
        "status": "ok",
        "action": "install",
        "manifest_path": str(manifest_path),
        "session_id": session_id,
        "supported_runtime_target": runtime_target,
        "overwrite_skills": plan["overwrite_skills"],
        "workspace_root": str(workspace_root),
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
    codex_root = _resolve_codex_root(args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root)
    state_root = _resolve_state_root(args.state_root)

    if not args.yes:
        _print_header(lang, "Octopus OS Installation Wizard", "章鱼 OS 安装向导")
        codex_root = Path(
            _prompt_text(
                lang,
                "Codex skills root",
                "Codex 技能根目录",
                str(codex_root),
            )
        ).expanduser().resolve()
        workspace_root = Path(
            _prompt_text(
                lang,
                "Workspace root",
                "工作区根目录",
                str(workspace_root),
            )
        ).expanduser().resolve()
        runtime_confirmed = _prompt_confirm(
            lang,
            "Confirm that the target runtime is Codex with GPT-5.4 high reasoning effort only.",
            "请确认目标运行时仅为 Codex + GPT-5.4 high reasoning effort。",
            default=False,
        )
        if not runtime_confirmed:
            raise ValueError("wizard aborted because the supported runtime constraint was not accepted")
        args.runtime_target = SUPPORTED_RUNTIME_TARGET

    runtime_target = _require_supported_runtime_target(getattr(args, "runtime_target", None))
    _validate_codex_root_structure(codex_root)
    plan = _build_plan(repo_root, codex_root, workspace_root)
    if not args.yes:
        _print_header(lang, "Install Plan", "安装计划")
        _print_plan_summary(lang, plan)

    allow_overwrite = args.allow_overwrite_skills
    if plan["overwrite_skills"] and not allow_overwrite:
        if args.yes:
            allow_overwrite = True
        else:
            allow_overwrite = _prompt_confirm(
                lang,
                "Allow overwriting existing codex skill directories?",
                "允许覆盖已有的 codex 技能目录吗？",
                default=False,
            )
        if not allow_overwrite:
            raise ValueError("wizard aborted because overwrite approval was not granted")

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
        codex_root=str(codex_root),
        workspace_root=str(workspace_root),
        state_root=str(state_root),
        runtime_target=runtime_target,
        allow_overwrite_skills=allow_overwrite,
        allow_replace_workspace=allow_replace_workspace,
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
    parser.add_argument("--codex-root")
    parser.add_argument("--workspace-root")
    parser.add_argument("--state-root")
    parser.add_argument("--session-id")
    parser.add_argument("--runtime-target")
    parser.add_argument("--allow-overwrite-skills", action="store_true")
    parser.add_argument("--allow-replace-workspace", action="store_true")
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
