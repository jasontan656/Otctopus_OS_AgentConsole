from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


SKILL_NAME = "Meta-Default-md-manager"
HOOK_HEADER = "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]"
LEGACY_PART_A_MARKER = "[PART A]"
LEGACY_PART_B_MARKER = "[PART B]"
PART_A_OPEN = "<part_A>"
PART_A_CLOSE = "</part_A>"
PART_B_OPEN = "<part_B>"
PART_B_CLOSE = "</part_B>"


@dataclass(frozen=True)
class RuntimePaths:
    workspace_root: Path
    mirror_skill_root: Path
    installed_skill_root: Path
    runtime_root: Path
    managed_targets_root: Path
    scan_rules_path: Path


def _env_path(name: str) -> Path | None:
    value = os.environ.get(name)
    if not value:
        return None
    return Path(value).expanduser().resolve()


def detect_paths(script_file: str) -> RuntimePaths:
    script_path = Path(script_file).resolve()
    script_dir = script_path.parent
    skill_root = script_dir.parent

    workspace_root = _env_path("MDM_WORKSPACE_ROOT")
    if workspace_root is None:
        if skill_root.parent.name == "Codex_Skills_Mirror":
            workspace_root = skill_root.parent.parent
        else:
            workspace_root = (Path.home() / "AI_Projects").resolve()

    mirror_skill_root = _env_path("MDM_MIRROR_SKILL_ROOT")
    if mirror_skill_root is None:
        if skill_root.parent.name == "Codex_Skills_Mirror":
            mirror_skill_root = skill_root
        else:
            mirror_skill_root = (
                workspace_root / "Codex_Skills_Mirror" / SKILL_NAME
            ).resolve()

    installed_skill_root = _env_path("MDM_INSTALLED_SKILL_ROOT")
    if installed_skill_root is None:
        installed_skill_root = (
            Path.home() / ".codex" / "skills" / SKILL_NAME
        ).resolve()

    runtime_root = _env_path("MDM_RUNTIME_ROOT")
    if runtime_root is None:
        runtime_root = (workspace_root / "Codex_Skill_Runtime" / SKILL_NAME).resolve()

    return RuntimePaths(
        workspace_root=workspace_root.resolve(),
        mirror_skill_root=mirror_skill_root.resolve(),
        installed_skill_root=installed_skill_root.resolve(),
        runtime_root=runtime_root.resolve(),
        managed_targets_root=(mirror_skill_root / "assets" / "managed_targets" / "AI_Projects").resolve(),
        scan_rules_path=(mirror_skill_root / "rules" / "scan_rules.json").resolve(),
    )


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str, dry_run: bool) -> None:
    ensure_parent(path, dry_run)
    if dry_run:
        return
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Any, dry_run: bool) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n", dry_run)


def sync_file_to_installed(paths: RuntimePaths, mirror_path: Path, dry_run: bool) -> None:
    relative = mirror_path.relative_to(paths.mirror_skill_root)
    installed_path = paths.installed_skill_root / relative
    ensure_parent(installed_path, dry_run)
    if dry_run:
        return
    if mirror_path.exists():
        shutil.copy2(mirror_path, installed_path)
    elif installed_path.exists():
        installed_path.unlink()


def sync_tree_to_installed(paths: RuntimePaths, relative_paths: list[Path], dry_run: bool) -> None:
    for relative in relative_paths:
        mirror_path = paths.mirror_skill_root / relative
        if mirror_path.is_dir():
            installed_dir = paths.installed_skill_root / relative
            if dry_run:
                continue
            installed_dir.mkdir(parents=True, exist_ok=True)
            continue
        sync_file_to_installed(paths, mirror_path, dry_run)


def load_scan_rules(paths: RuntimePaths) -> dict[str, Any]:
    return read_json(paths.scan_rules_path)


def iter_workspace_files(paths: RuntimePaths):
    skip_roots = {
        paths.mirror_skill_root.resolve(),
        paths.runtime_root.resolve(),
        (paths.workspace_root / "Codex_Skill_Runtime").resolve(),
    }
    for file_path in paths.workspace_root.rglob("*"):
        if not file_path.is_file():
            continue
        resolved = file_path.resolve()
        if any(root == resolved or root in resolved.parents for root in skip_roots):
            continue
        if ".git" in resolved.parts:
            continue
        yield resolved


def file_contains_keyword(path: Path, keyword: str) -> bool:
    try:
        return keyword.lower() in path.read_text(encoding="utf-8").lower()
    except UnicodeDecodeError:
        return False


def derive_managed_dir(paths: RuntimePaths, source_path: Path) -> Path:
    relative = source_path.relative_to(paths.workspace_root)
    parent = relative.parent
    if str(parent) == ".":
        return paths.managed_targets_root
    return paths.managed_targets_root / parent


def _extract_tag_block(text: str, open_tag: str, close_tag: str) -> str | None:
    if open_tag not in text or close_tag not in text:
        return None
    return text.split(open_tag, 1)[1].split(close_tag, 1)[0].strip()


def _extract_legacy_part_a_body(text: str) -> str | None:
    if LEGACY_PART_A_MARKER not in text:
        return None
    body = text.split(LEGACY_PART_A_MARKER, 1)[1]
    if LEGACY_PART_B_MARKER in body:
        body = body.split(LEGACY_PART_B_MARKER, 1)[0]
    return body.strip()


def _extract_header_prefix(text: str) -> str:
    if PART_A_OPEN in text:
        prefix = text.split(PART_A_OPEN, 1)[0].rstrip()
        return prefix + "\n"
    if LEGACY_PART_A_MARKER in text:
        prefix = text.split(LEGACY_PART_A_MARKER, 1)[0].rstrip()
        return prefix + "\n"
    return (
        f"{HOOK_HEADER}\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n"
    )


def extract_external_agents_part_a_body(text: str) -> str:
    tagged = _extract_tag_block(text, PART_A_OPEN, PART_A_CLOSE)
    if tagged is not None:
        return tagged
    legacy = _extract_legacy_part_a_body(text)
    if legacy is not None:
        return legacy
    return text.strip()


def render_external_agents(part_a_body: str, prefix_text: str | None = None) -> str:
    prefix = (prefix_text or _extract_header_prefix("")).rstrip()
    body = part_a_body.strip()
    return (
        f"{prefix}\n\n"
        f"{PART_A_OPEN}\n"
        f"{body}\n"
        f"{PART_A_CLOSE}\n"
    )


def extract_external_agents_part_a(text: str) -> str:
    body = extract_external_agents_part_a_body(text)
    prefix = _extract_header_prefix(text)
    return render_external_agents(body, prefix)


def render_internal_agents_human(part_a_text: str, machine_payload: Any) -> str:
    part_a = extract_external_agents_part_a(part_a_text).rstrip()
    payload = json.dumps(machine_payload, indent=2, ensure_ascii=False)
    return (
        f"{part_a}\n\n"
        f"{PART_B_OPEN}\n"
        f"```json\n{payload}\n```\n"
        f"{PART_B_CLOSE}\n"
    )


def extract_internal_part_a(human_text: str) -> str:
    if PART_B_OPEN in human_text:
        return human_text.split(PART_B_OPEN, 1)[0].rstrip() + "\n"
    if LEGACY_PART_B_MARKER in human_text:
        return human_text.split(LEGACY_PART_B_MARKER, 1)[0].rstrip() + "\n"
    return human_text.rstrip() + "\n"


def load_machine_payload(machine_path: Path) -> Any:
    if machine_path.exists():
        return read_json(machine_path)
    return {}


def validate_external_agents(text: str) -> list[str]:
    errors: list[str] = []
    if HOOK_HEADER not in text:
        errors.append("missing_hook_header")
    if "`HOOK_LOAD`" not in text:
        errors.append("missing_hook_load")
    has_new_part_a = PART_A_OPEN in text and PART_A_CLOSE in text
    has_legacy_part_a = LEGACY_PART_A_MARKER in text
    if not has_new_part_a and not has_legacy_part_a:
        errors.append("missing_part_a")
    if PART_B_OPEN in text or PART_B_CLOSE in text or LEGACY_PART_B_MARKER in text:
        errors.append("external_agents_forbids_part_b")
    return errors


def validate_internal_human_agents(text: str) -> list[str]:
    errors: list[str] = []
    if HOOK_HEADER not in text:
        errors.append("missing_hook_header")
    if "`HOOK_LOAD`" not in text:
        errors.append("missing_hook_load")
    has_new_part_a = PART_A_OPEN in text and PART_A_CLOSE in text
    has_legacy_part_a = LEGACY_PART_A_MARKER in text
    if not has_new_part_a and not has_legacy_part_a:
        errors.append("missing_part_a")
    has_new_part_b = PART_B_OPEN in text and PART_B_CLOSE in text
    has_legacy_part_b = LEGACY_PART_B_MARKER in text
    if not has_new_part_b and not has_legacy_part_b:
        errors.append("missing_part_b")
    if "```json" not in text:
        errors.append("missing_json_fence")
    return errors


def validate_machine_json(machine_path: Path) -> list[str]:
    if not machine_path.exists():
        return ["missing_machine_json"]
    try:
        read_json(machine_path)
    except json.JSONDecodeError as exc:
        return [f"invalid_machine_json:{exc.msg}"]
    return []


def report_path(paths: RuntimePaths, stage: str) -> Path:
    return paths.runtime_root / stage / "latest.json"


def write_stage_report(
    paths: RuntimePaths,
    stage: str,
    payload: Any,
    dry_run: bool,
    custom_report_path: str | None = None,
) -> Path:
    latest = report_path(paths, stage)
    stamped = paths.runtime_root / stage / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.json"
    custom_path = Path(custom_report_path).expanduser().resolve() if custom_report_path else None
    if not dry_run:
        latest.parent.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        stamped.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if custom_path is not None:
            custom_path.parent.mkdir(parents=True, exist_ok=True)
            custom_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return latest


def match_scan_rules(
    paths: RuntimePaths,
    only_filters: list[str] | None = None,
    source_paths: list[str] | None = None,
) -> list[dict[str, Any]]:
    rules = load_scan_rules(paths)
    disallowed = rules.get("disallowed_path_keywords", [])
    exact_names = set(rules.get("exact_filename_rules", []))
    keyword_rules = rules.get("keyword_rules", [])
    only_filters = only_filters or []
    source_paths = source_paths or []
    normalized_source_paths = {str(Path(item).expanduser().resolve()) for item in source_paths}

    results: list[dict[str, Any]] = []
    for file_path in iter_workspace_files(paths):
        text_path = str(file_path)
        if any(keyword in text_path for keyword in disallowed):
            continue
        if only_filters and not any(token in text_path for token in only_filters):
            continue
        if normalized_source_paths and text_path not in normalized_source_paths:
            continue

        reasons: list[str] = []
        if file_path.name in exact_names:
            reasons.append(f"exact_filename:{file_path.name}")

        for rule in keyword_rules:
            keyword = rule.get("keyword")
            file_ext = rule.get("file_ext")
            if keyword and file_ext and fnmatch(file_path.name, file_ext) and file_contains_keyword(file_path, keyword):
                reasons.append(f"keyword:{keyword}")

        if not reasons:
            continue

        managed_dir = derive_managed_dir(paths, file_path)
        results.append(
            {
                "source_path": str(file_path),
                "relative_path": str(file_path.relative_to(paths.workspace_root)),
                "managed_dir": str(managed_dir),
                "managed_human_path": str(managed_dir / "AGENTS_human.md"),
                "managed_machine_path": str(managed_dir / "AGENTS_machine.json"),
                "structure_template": rules["structure_template_map"].get(file_path.name),
                "match_reasons": reasons,
            }
        )
    return sorted(results, key=lambda item: item["relative_path"])


def lint_discovered_entry(paths: RuntimePaths, entry: dict[str, Any]) -> list[str]:
    source_path = Path(entry["source_path"])
    if source_path.name == "AGENTS.md":
        return validate_external_agents(source_path.read_text(encoding="utf-8"))
    return []
