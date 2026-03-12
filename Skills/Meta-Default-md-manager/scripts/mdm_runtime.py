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
PART_A_OPEN = "<part_A>"
PART_A_CLOSE = "</part_A>"
PART_B_OPEN = "<part_B>"
PART_B_CLOSE = "</part_B>"
PAYLOAD_STRUCTURE_CONTRACT_RELATIVE_PATH = Path("references/runtime_contracts/AGENTS_payload_structure.json")
REPO_ROOT_CANONICAL_NAME = "octopus-os-agent-console"
SKILLS_DIR_NAME = "Skills"
REPO_ROOT_COMPAT_ALIASES = {
    "Codex_Skills_Mirror": REPO_ROOT_CANONICAL_NAME,
    REPO_ROOT_CANONICAL_NAME: REPO_ROOT_CANONICAL_NAME,
}


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


def _detect_repo_root_from_skill_root(skill_root: Path) -> Path | None:
    skill_parent = skill_root.parent
    if skill_parent.name == SKILLS_DIR_NAME and skill_parent.parent.name in REPO_ROOT_COMPAT_ALIASES:
        return skill_parent.parent.resolve()
    if skill_parent.name in REPO_ROOT_COMPAT_ALIASES:
        return skill_parent.resolve()
    return None


def detect_paths(script_file: str) -> RuntimePaths:
    script_path = Path(script_file).resolve()
    script_dir = script_path.parent
    skill_root = script_dir.parent
    repo_root = _detect_repo_root_from_skill_root(skill_root)

    workspace_root = _env_path("MDM_WORKSPACE_ROOT")
    if workspace_root is None:
        if repo_root is not None:
            workspace_root = repo_root.parent
        else:
            workspace_root = (Path.home() / "AI_Projects").resolve()

    mirror_skill_root = _env_path("MDM_MIRROR_SKILL_ROOT")
    if mirror_skill_root is None:
        if repo_root is not None:
            mirror_skill_root = skill_root
        else:
            candidates = [
                workspace_root / REPO_ROOT_CANONICAL_NAME / SKILLS_DIR_NAME / SKILL_NAME,
                workspace_root / REPO_ROOT_CANONICAL_NAME / SKILL_NAME,
                workspace_root / "Codex_Skills_Mirror" / SKILLS_DIR_NAME / SKILL_NAME,
                workspace_root / "Codex_Skills_Mirror" / SKILL_NAME,
            ]
            existing = next((candidate for candidate in candidates if candidate.exists()), candidates[0])
            mirror_skill_root = existing.resolve()

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


def load_payload_structure_contract(paths: RuntimePaths) -> dict[str, Any]:
    return read_json(paths.mirror_skill_root / PAYLOAD_STRUCTURE_CONTRACT_RELATIVE_PATH)


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
    relative = _canonical_relative_path(paths, source_path)
    parent = relative.parent
    if str(parent) == ".":
        return paths.managed_targets_root
    return paths.managed_targets_root / parent


def ensure_within_workspace(paths: RuntimePaths, target_path: Path) -> Path:
    resolved = target_path.expanduser().resolve()
    resolved.relative_to(paths.workspace_root)
    return resolved


def _extract_tag_block(text: str, open_tag: str, close_tag: str) -> str | None:
    if open_tag not in text or close_tag not in text:
        return None
    return text.split(open_tag, 1)[1].split(close_tag, 1)[0].strip()


def _extract_header_prefix(text: str) -> str:
    if PART_A_OPEN in text:
        prefix = text.split(PART_A_OPEN, 1)[0].rstrip()
        return prefix + "\n"
    return (
        f"{HOOK_HEADER}\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n"
    )


def extract_external_agents_part_a_body(text: str) -> str:
    tagged = _extract_tag_block(text, PART_A_OPEN, PART_A_CLOSE)
    if tagged is not None:
        return tagged
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
        f"{PART_B_OPEN}\n\n"
        f"```json\n{payload}\n```\n"
        f"{PART_B_CLOSE}\n"
    )


def extract_internal_part_a(human_text: str) -> str:
    if PART_B_OPEN in human_text:
        return human_text.split(PART_B_OPEN, 1)[0].rstrip() + "\n"
    return human_text.rstrip() + "\n"


def load_machine_payload(machine_path: Path) -> Any:
    if machine_path.exists():
        return read_json(machine_path)
    return {}


def add_governed_source_path(paths: RuntimePaths, source_path: Path, dry_run: bool) -> None:
    rules = load_scan_rules(paths)
    relative = str(source_path.resolve().relative_to(paths.workspace_root))
    governed = list(rules.get("governed_source_paths", []))
    if relative not in governed:
        governed.append(relative)
        governed.sort()
        rules["governed_source_paths"] = governed
        write_json(paths.scan_rules_path, rules, dry_run)
        sync_file_to_installed(paths, paths.scan_rules_path, dry_run)


def scaffold_external_agents(external_path: Path) -> str:
    command = (
        "python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/"
        "Skills/Meta-Default-md-manager/scripts/Cli_Toolbox.py "
        f'target-contract --source-path "{external_path}" --json'
    )
    return (
        f"{HOOK_HEADER}\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        f"{PART_A_OPEN}\n"
        "1. 根入口命令\n"
        "- 在处理当前目录路径规则之前，必须先运行：\n"
        f"- `{command}`\n\n"
        "2. 待治理骨架\n"
        "- 该目录已进入治理范围。\n"
        "- 用户后续应补全该目录所需的具体治理内容。\n"
        "\n"
        "3. 治理链约束\n"
        "- 更新本文件时及相关内容时,必须使用 $Meta-Default-md-manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.\n"
        f"{PART_A_CLOSE}\n"
    )


def scaffold_internal_agents_human(external_path: Path) -> str:
    return render_internal_agents_human(scaffold_external_agents(external_path), {})


def _relative_source_key(paths: RuntimePaths, source_path: Path) -> str:
    return str(_canonical_relative_path(paths, source_path))


def _canonicalize_relative_path(relative_path: Path) -> Path:
    parts = list(relative_path.parts)
    if not parts:
        return relative_path
    first = REPO_ROOT_COMPAT_ALIASES.get(parts[0], parts[0])
    if len(parts) == 1:
        return Path(first)
    return Path(first, *parts[1:])


def _canonical_relative_path(paths: RuntimePaths, source_path: Path) -> Path:
    relative = source_path.resolve().relative_to(paths.workspace_root)
    return _canonicalize_relative_path(relative)


def _payload_schema_for_source(paths: RuntimePaths, source_path: Path) -> dict[str, Any] | None:
    contract = load_payload_structure_contract(paths)
    targets = contract.get("targets", {})
    return targets.get(_relative_source_key(paths, source_path))


def _validate_tag_wrapper(text: str, open_tag: str, close_tag: str, label: str) -> list[str]:
    errors: list[str] = []
    if text.count(open_tag) != 1 or text.count(close_tag) != 1:
        errors.append(f"{label}_wrapper_count_invalid")
        return errors
    if text.index(open_tag) > text.index(close_tag):
        errors.append(f"{label}_wrapper_order_invalid")
    return errors


def _extract_fenced_json_payload(block: str) -> tuple[Any | None, list[str]]:
    stripped = block.strip()
    if not stripped.startswith("```json\n") or not stripped.endswith("\n```"):
        return None, ["part_b_json_fence_invalid"]
    if stripped.count("```json") != 1 or stripped.count("```") != 2:
        return None, ["part_b_json_fence_count_invalid"]
    payload_text = stripped[len("```json\n") : -len("\n```")]
    try:
        return json.loads(payload_text), []
    except json.JSONDecodeError as exc:
        return None, [f"part_b_invalid_json:{exc.msg}"]


def _validate_payload_value(payload: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
    }
    if expected_type not in type_map:
        return [f"payload_schema_type_unsupported:{path}:{expected_type}"]
    if not isinstance(payload, type_map[expected_type]):
        return [f"payload_type_mismatch:{path}:{expected_type}"]
    if expected_type == "object":
        expected_keys = schema.get("key_order", [])
        actual_keys = list(payload.keys())
        if actual_keys != expected_keys:
            errors.append(f"payload_key_order_mismatch:{path}")
        for key in expected_keys:
            if key not in payload:
                errors.append(f"payload_missing_key:{path}.{key}")
        for key in actual_keys:
            if key not in expected_keys:
                errors.append(f"payload_extra_key:{path}.{key}")
        for key in expected_keys:
            if key in payload:
                errors.extend(
                    _validate_payload_value(payload[key], schema["properties"][key], f"{path}.{key}")
                )
        return errors
    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema is None:
            return [f"payload_schema_items_missing:{path}"]
        for index, item in enumerate(payload):
            errors.extend(_validate_payload_value(item, item_schema, f"{path}[{index}]"))
    return errors


def validate_external_agents(text: str) -> list[str]:
    errors: list[str] = []
    if HOOK_HEADER not in text:
        errors.append("missing_hook_header")
    if "`HOOK_LOAD`" not in text:
        errors.append("missing_hook_load")
    errors.extend(_validate_tag_wrapper(text, PART_A_OPEN, PART_A_CLOSE, "part_a"))
    if "[PART A]" in text:
        errors.append("legacy_part_a_marker_forbidden")
    if "[PART B]" in text:
        errors.append("legacy_part_b_marker_forbidden")
    if PART_B_OPEN in text or PART_B_CLOSE in text:
        errors.append("external_agents_forbids_part_b")
    return errors


def validate_internal_human_agents(text: str, payload_schema: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if HOOK_HEADER not in text:
        errors.append("missing_hook_header")
    if "`HOOK_LOAD`" not in text:
        errors.append("missing_hook_load")
    errors.extend(_validate_tag_wrapper(text, PART_A_OPEN, PART_A_CLOSE, "part_a"))
    errors.extend(_validate_tag_wrapper(text, PART_B_OPEN, PART_B_CLOSE, "part_b"))
    if "[PART A]" in text:
        errors.append("legacy_part_a_marker_forbidden")
    if "[PART B]" in text:
        errors.append("legacy_part_b_marker_forbidden")
    part_b_block = _extract_tag_block(text, PART_B_OPEN, PART_B_CLOSE)
    if part_b_block is None:
        errors.append("missing_part_b")
        return errors
    payload, payload_errors = _extract_fenced_json_payload(part_b_block)
    errors.extend(payload_errors)
    if payload_schema is not None and payload is not None:
        errors.extend(_validate_payload_value(payload, payload_schema, "$"))
    return errors


def validate_machine_json(machine_path: Path, payload_schema: dict[str, Any] | None = None) -> list[str]:
    if not machine_path.exists():
        return ["missing_machine_json"]
    try:
        payload = read_json(machine_path)
    except json.JSONDecodeError as exc:
        return [f"invalid_machine_json:{exc.msg}"]
    if payload_schema is None:
        return []
    return _validate_payload_value(payload, payload_schema, "$")


def validate_managed_agents_pair(
    paths: RuntimePaths,
    source_path: Path,
    human_path: Path,
    machine_path: Path,
) -> list[str]:
    errors: list[str] = []
    payload_schema = _payload_schema_for_source(paths, source_path)
    if payload_schema is None:
        return [f"missing_payload_structure_schema:{_relative_source_key(paths, source_path)}"]
    if not human_path.exists():
        errors.append("missing_managed_human")
    else:
        errors.extend(validate_internal_human_agents(human_path.read_text(encoding="utf-8"), payload_schema))
    errors.extend(validate_machine_json(machine_path, payload_schema))
    return errors


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
    governed_source_paths = {
        str((paths.workspace_root / item).resolve())
        for item in rules.get("governed_source_paths", [])
    }
    only_filters = only_filters or []
    source_paths = source_paths or []
    normalized_source_paths = {str(Path(item).expanduser().resolve()) for item in source_paths}

    candidate_files: list[Path]
    if normalized_source_paths:
        candidate_files = [Path(item) for item in sorted(normalized_source_paths)]
    else:
        candidate_files = list(iter_workspace_files(paths))

    results: list[dict[str, Any]] = []
    for file_path in candidate_files:
        if not file_path.exists() or not file_path.is_file():
            continue
        text_path = str(file_path)
        if governed_source_paths and text_path not in governed_source_paths:
            continue
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


def lint_external_entry(paths: RuntimePaths, entry: dict[str, Any]) -> list[str]:
    source_path = Path(entry["source_path"])
    if source_path.name == "AGENTS.md":
        return validate_external_agents(source_path.read_text(encoding="utf-8"))
    return []


def lint_managed_entry(paths: RuntimePaths, entry: dict[str, Any]) -> list[str]:
    source_path = Path(entry["source_path"])
    errors = lint_external_entry(paths, entry)
    if source_path.name != "AGENTS.md":
        return errors
    errors.extend(
        validate_managed_agents_pair(
            paths,
            source_path,
            Path(entry["managed_human_path"]),
            Path(entry["managed_machine_path"]),
        )
    )
    return errors
