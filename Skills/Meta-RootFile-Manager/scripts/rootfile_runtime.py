from __future__ import annotations

import json
import os
import re
import shutil
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


SKILL_NAME = "Meta-RootFile-Manager"
HOOK_HEADER = "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]"
PART_A_OPEN = "<part_A>"
PART_A_CLOSE = "</part_A>"
PART_B_OPEN = "<part_B>"
PART_B_CLOSE = "</part_B>"
PAYLOAD_STRUCTURE_CONTRACT_RELATIVE_PATH = Path(
    "references/runtime_contracts/AGENTS_payload_structure.json"
)
REPO_ROOT_CANONICAL_NAME = "Otctopus_OS_AgentConsole"
SKILLS_DIR_NAME = "Skills"
REPO_ROOT_COMPAT_ALIASES = {
    "Codex_Skills_Mirror": REPO_ROOT_CANONICAL_NAME,
    REPO_ROOT_CANONICAL_NAME: REPO_ROOT_CANONICAL_NAME,
}
LEGACY_MANAGED_TARGET_DIRS = ("Codex_Skills_Mirror",)
LEGACY_OWNER_META_GLOB = "*__owner_meta.json"
RUNTIME_MANAGED_TARGETS_DIRNAME = "managed_targets"
ROOTFILE_MANAGER_NAME = "$Meta-RootFile-Manager"
SKILL_TOKEN_PATTERN = re.compile(r"\$[A-Za-z][A-Za-z0-9._-]*")
TEXT_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9._/-]+|[\u4e00-\u9fff]+")
EPHEMERAL_WORKSPACE_SEGMENT_PATTERN = re.compile(r"tmp[a-z0-9]{6,}$")
PARENT_DUPLICATE_MIN_TOKEN_WINDOW = 4
PARENT_DUPLICATE_MIN_EXACT_CHARS = 18
PARENT_DUPLICATE_EXCLUDED_PAYLOAD_KEYS = {"owner", "entry_role", "repo_name", "default_meta_skill_order"}
PARENT_DUPLICATE_EXCLUDED_PAYLOAD_PREFIXES = ("$.governed_container", "$.workflow_roots")
STANDARD_WRITE_EXEC_GOAL = "default to full-coverage edits for the intended change"
STANDARD_WRITE_EXEC_ACTION = (
    "Default to full-coverage edits, proactively explore to avoid omissions, "
    "and use the meta skill stack to strengthen the result."
)
SCAFFOLD_REPLACE_ME = "replace_me"
SCAFFOLD_NOT_APPLICABLE = "N/A"
PARENT_DUPLICATE_ALLOWED_NORMALIZED_STRINGS = {
    " ".join(TEXT_TOKEN_PATTERN.findall(_text)).lower()
    for _text in (STANDARD_WRITE_EXEC_GOAL, STANDARD_WRITE_EXEC_ACTION)
}


@dataclass(frozen=True)
class RuntimePaths:
    workspace_root: Path
    mirror_skill_root: Path
    installed_skill_root: Path
    runtime_root: Path
    managed_targets_root: Path
    scan_rules_path: Path


@dataclass(frozen=True)
class OwnerMetadata:
    owner: str


@dataclass(frozen=True)
class OwnerInjectedMachinePayload:
    owner: str
    payload: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        normalized = {"owner": self.owner}
        normalized.update(self.payload)
        return normalized


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
        workspace_root = repo_root.parent if repo_root is not None else (Path.home() / "AI_Projects")

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
            mirror_skill_root = next((candidate for candidate in candidates if candidate.exists()), candidates[0])

    installed_skill_root = _env_path("MDM_INSTALLED_SKILL_ROOT")
    if installed_skill_root is None:
        local_installed_root = (workspace_root / ".codex" / "skills" / SKILL_NAME).resolve()
        if local_installed_root.exists():
            installed_skill_root = local_installed_root
        else:
            codex_home = _env_path("CODEX_HOME")
            if codex_home is None:
                codex_home = (Path.home() / ".codex").resolve()
            installed_skill_root = (codex_home / "skills" / SKILL_NAME).resolve()

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


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str, dry_run: bool) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    ensure_parent(path, dry_run)
    if dry_run:
        return True
    path.write_text(content, encoding="utf-8")
    return True


def write_json(path: Path, payload: object, dry_run: bool) -> bool:
    return write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n", dry_run)


def sync_file_to_installed(paths: RuntimePaths, mirror_path: Path, dry_run: bool) -> bool:
    try:
        relative = mirror_path.relative_to(paths.mirror_skill_root)
    except ValueError:
        return False
    installed_path = paths.installed_skill_root / relative
    if mirror_path.exists():
        mirror_bytes = mirror_path.read_bytes()
        if installed_path.exists() and installed_path.read_bytes() == mirror_bytes:
            return False
        ensure_parent(installed_path, dry_run)
        if dry_run:
            return True
        shutil.copy2(mirror_path, installed_path)
        return True
    if installed_path.exists():
        if dry_run:
            return True
        installed_path.unlink()
        return True
    return False


def prune_legacy_managed_target_dirs(paths: RuntimePaths, dry_run: bool) -> list[str]:
    removed: list[str] = []
    for legacy_dir_name in LEGACY_MANAGED_TARGET_DIRS:
        for base_root in (paths.managed_targets_root, paths.installed_skill_root / "assets" / "managed_targets" / "AI_Projects"):
            legacy_dir = base_root / legacy_dir_name
            if not legacy_dir.exists():
                continue
            if any(legacy_dir.iterdir()):
                continue
            removed.append(str(legacy_dir))
            if not dry_run:
                legacy_dir.rmdir()
    return removed


def prune_legacy_owner_meta_files(paths: RuntimePaths, dry_run: bool) -> list[str]:
    removed: list[str] = []
    candidate_roots = [
        paths.managed_targets_root,
        paths.installed_skill_root / "assets" / "managed_targets" / "AI_Projects",
        runtime_managed_targets_root(paths),
    ]
    for root in candidate_roots:
        if not root.exists():
            continue
        for path in root.rglob(LEGACY_OWNER_META_GLOB):
            removed.append(str(path))
            if not dry_run:
                path.unlink()
    return removed


def load_scan_rules(paths: RuntimePaths) -> dict[str, object]:
    return read_json(paths.scan_rules_path)


def load_agents_structure_contract(paths: RuntimePaths) -> dict[str, object]:
    return read_json(paths.mirror_skill_root / PAYLOAD_STRUCTURE_CONTRACT_RELATIVE_PATH)


def _default_agents_payload_schema(paths: RuntimePaths) -> dict[str, object] | None:
    contract = load_agents_structure_contract(paths)
    targets = contract.get("targets", {})
    default_schema = targets.get("AGENTS.md")
    return default_schema if isinstance(default_schema, dict) else None


def _root_agents_template_human_path(paths: RuntimePaths) -> Path:
    return paths.managed_targets_root / "AGENTS_human.md"


def _root_agents_template_machine_path(paths: RuntimePaths) -> Path:
    return paths.managed_targets_root / "AGENTS_machine.json"


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
    return f"{HOOK_HEADER}\n\n`HOOK_LOAD`: Apply this AGENTS contract.\n"


def extract_external_agents_part_a_body(text: str) -> str:
    tagged = _extract_tag_block(text, PART_A_OPEN, PART_A_CLOSE)
    if tagged is not None:
        return tagged
    return text.strip()


def render_external_agents(part_a_body: str, prefix_text: str | None = None) -> str:
    prefix = (prefix_text or _extract_header_prefix("")).rstrip()
    body = part_a_body.strip()
    return f"{prefix}\n\n{PART_A_OPEN}\n{body}\n{PART_A_CLOSE}\n"


def extract_external_agents_part_a(text: str) -> str:
    body = extract_external_agents_part_a_body(text)
    prefix = _extract_header_prefix(text)
    return render_external_agents(body, prefix)


def render_internal_agents_human(part_a_text: str, machine_payload: object) -> str:
    part_a = extract_external_agents_part_a(part_a_text).rstrip()
    payload = json.dumps(machine_payload, indent=2, ensure_ascii=False)
    return f"{part_a}\n\n{PART_B_OPEN}\n\n```json\n{payload}\n```\n{PART_B_CLOSE}\n"


def extract_internal_part_a(human_text: str) -> str:
    if PART_B_OPEN in human_text:
        return human_text.split(PART_B_OPEN, 1)[0].rstrip() + "\n"
    return human_text.rstrip() + "\n"


def load_machine_payload(machine_path: Path) -> object:
    if machine_path.exists():
        return read_json(machine_path)
    return {}


def _iter_replace_me_payload_paths(payload: object, path: str) -> Iterable[str]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield from _iter_replace_me_payload_paths(value, f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            yield from _iter_replace_me_payload_paths(item, f"{path}[{index}]")
        return
    if isinstance(payload, str) and SCAFFOLD_REPLACE_ME in payload:
        yield path


def validate_agents_writeback_completion(external_text: str, payload: object) -> list[str]:
    errors: list[str] = []
    part_a_body = extract_external_agents_part_a_body(external_text)
    for line_number, line in enumerate(part_a_body.splitlines(), start=1):
        if SCAFFOLD_REPLACE_ME in line:
            errors.append(f"external_replace_me_remaining:part_a[line={line_number}]")
    for path in _iter_replace_me_payload_paths(payload, "$"):
        errors.append(f"payload_replace_me_remaining:{path}")
    return errors


def _extract_part_a_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None
    for line in extract_external_agents_part_a_body(text).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^\d+\.\s+", stripped):
            current_heading = stripped
            sections.setdefault(current_heading, [])
            continue
        if current_heading is None:
            continue
        item = re.sub(r"^\s*[-*]\s*", "", stripped)
        if item:
            sections[current_heading].append(item)
    return sections


def _strip_inline_command_wrapper(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("`") and stripped.endswith("`") and stripped.count("`") == 2:
        return stripped[1:-1]
    return stripped


def _repo_root_for_runtime_paths(paths: RuntimePaths) -> Path:
    detected = _detect_repo_root_from_skill_root(paths.mirror_skill_root)
    if detected is not None:
        return detected
    return (paths.workspace_root / REPO_ROOT_CANONICAL_NAME).resolve()


def build_agents_payload_contract_command(paths: RuntimePaths, source_path: Path) -> str:
    repo_root = _repo_root_for_runtime_paths(paths)
    python_path = repo_root / ".venv_backend_skills" / "bin" / "python"
    script_path = paths.mirror_skill_root / "scripts" / "Cli_Toolbox.py"
    command = (
        f'{python_path} {script_path} agents-payload-contract --source-path "{source_path.resolve()}" --json'
    )
    if source_path.parts[-3:] == (".codex", "skills", "AGENTS.md"):
        return f"MDM_WORKSPACE_ROOT={source_path.resolve().parents[2]} {command}"
    try:
        source_path.resolve().relative_to(paths.workspace_root)
    except ValueError:
        command = f"MDM_WORKSPACE_ROOT={source_path.resolve().parents[2]} {command}"
    return command


def validate_source_specific_external_agents(
    paths: RuntimePaths,
    source_path: Path,
    text: str,
) -> list[str]:
    if source_path.parts[-3:] != (".codex", "skills", "AGENTS.md"):
        return []
    sections = _extract_part_a_sections(text)
    root_entry_items = sections.get("1. 根入口命令", [])
    if len(root_entry_items) != 1:
        return ["codex_skills_root_entry_command_count_invalid"]
    actual_command = _strip_inline_command_wrapper(root_entry_items[0])
    expected_command = build_agents_payload_contract_command(paths, source_path)
    if actual_command != expected_command:
        return [f"codex_skills_root_entry_command_invalid:{actual_command}"]
    return []


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


def _workspace_relative_path_or_none(paths: RuntimePaths, source_path: Path) -> Path | None:
    try:
        return source_path.resolve().relative_to(paths.workspace_root)
    except ValueError:
        return None


def _runtime_local_relative_path(paths: RuntimePaths, source_path: Path) -> Path:
    resolved = source_path.resolve()
    try:
        relative = resolved.relative_to(paths.runtime_root)
        return relative
    except ValueError:
        pass

    workspace_relative = _workspace_relative_path_or_none(paths, resolved)
    if workspace_relative is not None:
        return Path("ephemeral_workspace") / _canonicalize_relative_path(workspace_relative)

    parts = [part for part in resolved.parts if part not in (resolved.anchor, os.sep)]
    if not parts:
        return Path("external_source")
    return Path("external_source", *parts)


def is_ephemeral_workspace_source(paths: RuntimePaths, source_path: Path) -> bool:
    relative = _workspace_relative_path_or_none(paths, source_path)
    if relative is None or not relative.parts:
        return False
    first = relative.parts[0]
    return first in {"tmp", ".tmp", "temp", ".temp"} or EPHEMERAL_WORKSPACE_SEGMENT_PATTERN.fullmatch(first) is not None


def is_runtime_local_source(paths: RuntimePaths, source_path: Path) -> bool:
    resolved = source_path.resolve()
    try:
        resolved.relative_to(paths.runtime_root)
        return True
    except ValueError:
        pass
    if is_ephemeral_workspace_source(paths, resolved):
        return True
    if _workspace_relative_path_or_none(paths, resolved) is None:
        return True
    return False


def runtime_managed_targets_root(paths: RuntimePaths) -> Path:
    return paths.runtime_root / RUNTIME_MANAGED_TARGETS_DIRNAME


def derive_managed_dir(paths: RuntimePaths, source_path: Path) -> Path:
    if is_runtime_local_source(paths, source_path):
        relative = _runtime_local_relative_path(paths, source_path).parent
        if str(relative) == ".":
            return runtime_managed_targets_root(paths)
        return runtime_managed_targets_root(paths) / relative
    relative = _canonical_relative_path(paths, source_path)
    parent = relative.parent
    if str(parent) == ".":
        return paths.managed_targets_root
    return paths.managed_targets_root / parent


def _relative_source_key(paths: RuntimePaths, source_path: Path) -> str:
    if is_runtime_local_source(paths, source_path):
        return str(_runtime_local_relative_path(paths, source_path))
    return str(_canonical_relative_path(paths, source_path))


def describe_governed_container(paths: RuntimePaths, source_path: Path) -> str:
    if is_runtime_local_source(paths, source_path):
        runtime_relative = _runtime_local_relative_path(paths, source_path).parent
        if str(runtime_relative) == ".":
            return f"`{paths.runtime_root}` runtime-local root container"
        return f"`{runtime_relative.as_posix()}` runtime-local container"
    relative = _canonical_relative_path(paths, source_path)
    parent = relative.parent
    if str(parent) == ".":
        return "`AI_Projects` workspace root"
    if len(parent.parts) == 1:
        return f"`{parent.name}` repository root container"
    return f"`{parent.as_posix()}` container"


def derive_owner_text(
    paths: RuntimePaths,
    source_path: Path,
    channel_id: str,
    file_kind: str,
) -> str:
    container = describe_governed_container(paths, source_path)
    surface_map = {
        "README.md": "公共说明面",
        "CHANGELOG.md": "版本与迭代记录面",
        "CONTRIBUTING.md": "协作入口说明面",
        "SECURITY.md": "安全披露与响应面",
        "CODE_OF_CONDUCT.md": "协作行为边界面",
        "LICENSE": "授权与法律边界面",
        ".gitignore": "本地噪音过滤边界面",
        "pytest.ini": "Python 测试运行配置面",
        "Dockerfile": "容器构建入口面",
        ".dockerignore": "容器构建忽略边界面",
        ".env.example": "环境变量样例面",
        "requirements.txt": "Python 依赖声明面",
        "requirements-backend_skills.lock.txt": "skills Python 依赖锁定面",
        "pyproject.toml": "Python 项目集成配置面",
        "package.json": "Node package runtime 声明面",
        "package-lock.json": "Node package lock 面",
    }
    if file_kind == "AGENTS.md":
        return (
            f"由 `{ROOTFILE_MANAGER_NAME}` 作为 {container} 的 runtime entry owner 负责治理；"
            f"当前通过 `{channel_id}` 通道受管并同步这个入口文件。"
        )
    surface = surface_map.get(file_kind, f"`{file_kind}` 默认治理面")
    return (
        f"由 {container} 所代表的 {surface} 负责；"
        f"当前通过 `{ROOTFILE_MANAGER_NAME}` 的 `{channel_id}` 通道受管并同步。"
    )


def build_owner_payload(
    paths: RuntimePaths,
    source_path: Path,
    channel_id: str,
    file_kind: str,
) -> OwnerMetadata:
    return OwnerMetadata(owner=derive_owner_text(paths, source_path, channel_id, file_kind))


def _split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + len("\n---\n") :]


def extract_frontmatter_owner(text: str) -> str | None:
    frontmatter, _ = _split_frontmatter(text)
    if frontmatter is None:
        return None
    for line in frontmatter.splitlines():
        if line.startswith("owner:"):
            value = line.split(":", 1)[1].strip()
            if value.startswith('"') and value.endswith('"'):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value.strip('"')
            return value
    return None


def upsert_frontmatter_owner(text: str, owner: str) -> str:
    owner_line = f"owner: {json.dumps(owner, ensure_ascii=False)}"
    frontmatter, body = _split_frontmatter(text)
    if frontmatter is None:
        return f"---\n{owner_line}\n---\n{text}"
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("owner:"):
            lines[index] = owner_line
            break
    else:
        lines.append(owner_line)
    joined_lines = "\n".join(lines)
    return f"---\n{joined_lines}\n---\n{body}"


def strip_frontmatter_owner(text: str) -> str:
    frontmatter, body = _split_frontmatter(text)
    if frontmatter is None:
        return text
    lines = [line for line in frontmatter.splitlines() if not line.startswith("owner:")]
    if not lines:
        return body
    joined_lines = "\n".join(lines)
    return f"---\n{joined_lines}\n---\n{body}"


def _parse_json_object_text(text: str) -> dict[str, object] | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def managed_plain_copy_with_owner(external_text: str, owner: str) -> str:
    parsed = _parse_json_object_text(external_text)
    if parsed is not None:
        normalized = {"owner": owner}
        normalized.update({key: value for key, value in parsed.items() if key != "owner"})
        return json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
    return upsert_frontmatter_owner(external_text, owner)


def strip_owner_from_managed_plain_copy(managed_text: str) -> str:
    parsed = _parse_json_object_text(managed_text)
    if parsed is not None and "owner" in parsed:
        normalized = {key: value for key, value in parsed.items() if key != "owner"}
        return json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
    return strip_frontmatter_owner(managed_text)


def validate_owner_in_managed_plain_copy(managed_text: str, expected_owner: str) -> list[str]:
    parsed = _parse_json_object_text(managed_text)
    if parsed is not None:
        actual_owner = parsed.get("owner")
        if actual_owner is None:
            return ["missing_owner_field"]
        if actual_owner != expected_owner:
            return ["owner_field_mismatch"]
        return []
    owner = extract_frontmatter_owner(managed_text)
    if owner is None:
        return ["missing_owner_field"]
    if owner != expected_owner:
        return ["owner_field_mismatch"]
    return []


def inject_owner_into_machine_payload(payload: object, owner: str) -> OwnerInjectedMachinePayload:
    if not isinstance(payload, dict):
        return OwnerInjectedMachinePayload(owner=owner, payload={})
    normalized = {key: value for key, value in payload.items() if key != "owner"}
    return OwnerInjectedMachinePayload(owner=owner, payload=normalized)


def validate_markdown_owner(text: str, expected_owner: str) -> list[str]:
    owner = extract_frontmatter_owner(text)
    if owner is None:
        return ["missing_owner_field"]
    if owner != expected_owner:
        return ["owner_field_mismatch"]
    return []


def _payload_schema_for_source(paths: RuntimePaths, source_path: Path) -> dict[str, object] | None:
    contract = load_agents_structure_contract(paths)
    targets = contract.get("targets", {})
    schema = targets.get(_relative_source_key(paths, source_path))
    if isinstance(schema, dict):
        return schema
    default_schema = targets.get("AGENTS.md")
    return default_schema if isinstance(default_schema, dict) else None


def list_channels(paths: RuntimePaths) -> dict[str, dict[str, object]]:
    return load_scan_rules(paths).get("channels", {})


def find_channel_by_file_kind(paths: RuntimePaths, file_kind: str) -> tuple[str, dict[str, object]] | None:
    for channel_id, channel in list_channels(paths).items():
        if channel.get("file_kind") == file_kind:
            return channel_id, channel
    return None


def find_channel_for_source_path(paths: RuntimePaths, source_path: Path) -> tuple[str, dict[str, object]] | None:
    if is_runtime_local_source(paths, source_path):
        return find_channel_by_file_kind(paths, source_path.name)
    relative = _relative_source_key(paths, source_path)
    for channel_id, channel in list_channels(paths).items():
        governed = channel.get("governed_source_paths", [])
        if relative in governed:
            return channel_id, channel
    return None


def build_entry(
    paths: RuntimePaths,
    source_path: Path,
    channel_id: str,
    channel: dict[str, object],
) -> dict[str, object]:
    managed_dir = derive_managed_dir(paths, source_path)
    owner_payload = build_owner_payload(paths, source_path, channel_id, channel["file_kind"])
    managed_files = {
        key: str((managed_dir / filename).resolve())
        for key, filename in channel.get("managed_files", {}).items()
    }
    entry = {
        "source_path": str(source_path.resolve()),
        "relative_path": _relative_source_key(paths, source_path),
        "channel_id": channel_id,
        "file_kind": channel["file_kind"],
        "mapping_mode": channel.get("mapping_mode", "plain_copy"),
        "managed_dir": str(managed_dir),
        "managed_files": managed_files,
        "structure_template": channel.get("structure_template"),
        "match_reasons": [f"channel:{channel_id}"],
        "owner": owner_payload.owner,
    }
    if "human" in managed_files:
        entry["managed_human_path"] = managed_files["human"]
    if "machine" in managed_files:
        entry["managed_machine_path"] = managed_files["machine"]
    if "mapped" in managed_files:
        entry["managed_mapped_path"] = managed_files["mapped"]
    return entry


def match_scan_rules(
    paths: RuntimePaths,
    only_filters: list[str] | None = None,
    source_paths: list[str] | None = None,
    *,
    include_missing: bool = False,
) -> list[dict[str, object]]:
    rules = load_scan_rules(paths)
    disallowed = rules.get("disallowed_path_keywords", [])
    only_filters = only_filters or []
    normalized_source_paths = {
        str(Path(item).expanduser().resolve()) for item in (source_paths or [])
    }
    results: list[dict[str, object]] = []
    for channel_id, channel in list_channels(paths).items():
        for relative in channel.get("governed_source_paths", []):
            source_path = (paths.workspace_root / relative).resolve()
            source_text = str(source_path)
            if any(keyword in source_text for keyword in disallowed):
                continue
            if only_filters and not any(token in source_text for token in only_filters):
                continue
            if normalized_source_paths and source_text not in normalized_source_paths:
                continue
            if not include_missing and not source_path.exists():
                continue
            results.append(build_entry(paths, source_path, channel_id, channel))
    if normalized_source_paths:
        existing_sources = {item["source_path"] for item in results}
        for source_text in sorted(normalized_source_paths):
            source_path = Path(source_text).resolve()
            if source_text in existing_sources:
                continue
            if not is_runtime_local_source(paths, source_path):
                continue
            found = find_channel_for_source_path(paths, source_path)
            if found is None:
                continue
            if any(keyword in source_text for keyword in disallowed):
                continue
            if only_filters and not any(token in source_text for token in only_filters):
                continue
            if not include_missing and not source_path.exists():
                continue
            channel_id, channel = found
            results.append(build_entry(paths, source_path, channel_id, channel))
    return sorted(results, key=lambda item: item["relative_path"])


def _validate_tag_wrapper(text: str, open_tag: str, close_tag: str, label: str) -> list[str]:
    errors: list[str] = []
    if text.count(open_tag) != 1 or text.count(close_tag) != 1:
        errors.append(f"{label}_wrapper_count_invalid")
        return errors
    if text.index(open_tag) > text.index(close_tag):
        errors.append(f"{label}_wrapper_order_invalid")
    return errors


def _extract_fenced_json_payload(block: str) -> tuple[object | None, list[str]]:
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


def _validate_payload_value(payload: object, schema: dict[str, object], path: str) -> list[str]:
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


def _default_meta_skill_tokens(payload: object) -> set[str]:
    if not isinstance(payload, dict):
        return set()
    entries = payload.get("default_meta_skill_order")
    if not isinstance(entries, list):
        return set()
    tokens: set[str] = set()
    for item in entries:
        if isinstance(item, str):
            tokens.update(SKILL_TOKEN_PATTERN.findall(item))
    return tokens


def _iter_skill_tokens(payload: object, path: str) -> Iterable[tuple[str, str]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield from _iter_skill_tokens(value, f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            yield from _iter_skill_tokens(item, f"{path}[{index}]")
        return
    if isinstance(payload, str):
        for token in SKILL_TOKEN_PATTERN.findall(payload):
            yield path, token


def _validate_default_meta_skill_uniqueness(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return []
    default_tokens = _default_meta_skill_tokens(payload)
    if not default_tokens:
        return []
    errors: list[str] = []
    for key, value in payload.items():
        if key in {"owner", "default_meta_skill_order"}:
            continue
        for path, token in _iter_skill_tokens(value, f"$.{key}"):
            if token in default_tokens:
                errors.append(
                    "payload_skill_repeated_outside_default_meta_skill_order:"
                    f"{token}:{path}"
                )
    return errors


def _validate_standard_write_exec(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return []
    execution_modes = payload.get("execution_modes")
    if not isinstance(execution_modes, dict):
        return []
    write_exec = execution_modes.get("WRITE_EXEC")
    if not isinstance(write_exec, dict):
        return []

    errors: list[str] = []
    if write_exec.get("goal") != STANDARD_WRITE_EXEC_GOAL:
        errors.append("write_exec_goal_must_match_standard")
    default_actions = write_exec.get("default_actions")
    if default_actions != [STANDARD_WRITE_EXEC_ACTION]:
        errors.append("write_exec_default_actions_must_match_standard")
    return errors


def _normalize_duplicate_text(text: str) -> str:
    without_skills = SKILL_TOKEN_PATTERN.sub(" ", text)
    lowered = without_skills.lower()
    lowered = re.sub(r"[`*_>#\[\](){}\"'“”‘’]+", " ", lowered)
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff._/\-\s]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def _compact_duplicate_text(text: str) -> str:
    normalized = _normalize_duplicate_text(text)
    return re.sub(r"[\s._/\-]+", "", normalized)


def _tokenize_duplicate_text(text: str) -> list[str]:
    return TEXT_TOKEN_PATTERN.findall(_normalize_duplicate_text(text))


def _is_duplicate_comparable_text(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if (
        "Cli_Toolbox.py" in stripped
        or "target-contract --source-path" in stripped
        or ".venv_backend_skills/bin/python" in stripped
    ):
        return False
    if stripped.startswith("/home/") or stripped.startswith("<root>/"):
        return False
    if "/home/" in stripped or "<root>/" in stripped:
        return False
    if re.fullmatch(r"[A-Za-z0-9._/<>=:\"'` -]+", stripped) and "/" in stripped:
        return False
    return True


def _duplicate_phrase(child_text: str, parent_text: str) -> str | None:
    if not _is_duplicate_comparable_text(child_text):
        return None
    if not _is_duplicate_comparable_text(parent_text):
        return None
    child_normalized = _normalize_duplicate_text(child_text)
    parent_normalized = _normalize_duplicate_text(parent_text)
    if not child_normalized or not parent_normalized:
        return None
    if (
        child_normalized in PARENT_DUPLICATE_ALLOWED_NORMALIZED_STRINGS
        and parent_normalized == child_normalized
    ):
        return None
    if child_normalized == parent_normalized and len(child_normalized) >= PARENT_DUPLICATE_MIN_EXACT_CHARS:
        return child_normalized

    child_tokens = _tokenize_duplicate_text(child_text)
    parent_tokens = _tokenize_duplicate_text(parent_text)
    if len(child_tokens) >= PARENT_DUPLICATE_MIN_TOKEN_WINDOW and len(parent_tokens) >= PARENT_DUPLICATE_MIN_TOKEN_WINDOW:
        parent_windows = {
            tuple(parent_tokens[index : index + PARENT_DUPLICATE_MIN_TOKEN_WINDOW])
            for index in range(len(parent_tokens) - PARENT_DUPLICATE_MIN_TOKEN_WINDOW + 1)
        }
        for index in range(len(child_tokens) - PARENT_DUPLICATE_MIN_TOKEN_WINDOW + 1):
            window = tuple(child_tokens[index : index + PARENT_DUPLICATE_MIN_TOKEN_WINDOW])
            if window in parent_windows:
                return " ".join(window)
    return None


def _is_allowed_standard_write_exec_surface(path: str, text: str) -> bool:
    if not path.startswith("$.execution_modes.WRITE_EXEC."):
        return False
    normalized = _normalize_duplicate_text(text)
    if normalized in PARENT_DUPLICATE_ALLOWED_NORMALIZED_STRINGS:
        return True
    if normalized.startswith(_normalize_duplicate_text(STANDARD_WRITE_EXEC_GOAL)):
        return True
    return False


def _iter_part_a_strings(text: str) -> Iterable[tuple[str, str]]:
    body = extract_external_agents_part_a_body(text)
    for line_number, line in enumerate(body.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^\s*(?:[-*]|\d+\.)\s*", "", stripped)
        if stripped and _is_duplicate_comparable_text(stripped):
            yield f"part_a[line={line_number}]", stripped


def _iter_payload_strings(payload: object, path: str) -> Iterable[tuple[str, str]]:
    if any(path.startswith(prefix) for prefix in PARENT_DUPLICATE_EXCLUDED_PAYLOAD_PREFIXES):
        return
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in PARENT_DUPLICATE_EXCLUDED_PAYLOAD_KEYS:
                continue
            yield from _iter_payload_strings(value, f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            yield from _iter_payload_strings(item, f"{path}[{index}]")
        return
    if isinstance(payload, str) and _is_duplicate_comparable_text(payload):
        yield path, payload


def _parent_agents_source_path(paths: RuntimePaths, source_path: Path) -> Path | None:
    if is_runtime_local_source(paths, source_path):
        return None
    rules = load_scan_rules(paths)
    governed = {
        _canonicalize_relative_path(Path(item))
        for item in rules.get("channels", {}).get("AGENTS_MD", {}).get("governed_source_paths", [])
    }
    relative = _canonical_relative_path(paths, source_path)
    current = relative.parent
    while True:
        candidate = Path("AGENTS.md") if str(current) == "." else current / "AGENTS.md"
        if candidate != relative and candidate in governed:
            return paths.workspace_root / candidate
        if str(current) == ".":
            return None
        current = current.parent


def _validate_parent_agents_duplicates(
    paths: RuntimePaths,
    source_path: Path,
    external_text: str,
    payload: object,
) -> list[str]:
    if not isinstance(payload, dict):
        return []
    parent_source_path = _parent_agents_source_path(paths, source_path)
    if parent_source_path is None or not parent_source_path.exists():
        return []

    parent_entry = resolve_target_contract(paths, parent_source_path)
    if parent_entry.get("channel_id") != "AGENTS_MD":
        return []
    parent_machine_path = Path(str(parent_entry["managed_files"]["machine"]))
    if not parent_machine_path.exists():
        return []
    parent_payload = read_json(parent_machine_path)
    if not isinstance(parent_payload, dict):
        return []

    parent_strings = list(_iter_part_a_strings(parent_source_path.read_text(encoding="utf-8")))
    parent_strings.extend(_iter_payload_strings(parent_payload, "$"))
    child_strings = list(_iter_part_a_strings(external_text))
    child_strings.extend(_iter_payload_strings(payload, "$"))

    errors: list[str] = []
    parent_relative = _relative_source_key(paths, parent_source_path)
    for child_path, child_text in child_strings:
        for parent_path, parent_text in parent_strings:
            if _is_allowed_standard_write_exec_surface(child_path, child_text) and _is_allowed_standard_write_exec_surface(parent_path, parent_text):
                continue
            phrase = _duplicate_phrase(child_text, parent_text)
            if phrase is None:
                continue
            errors.append(
                "parent_agents_duplicate_phrase:"
                f"{parent_relative}:{child_path}:{parent_path}:{phrase}"
            )
            break
    return errors


def validate_external_agents(text: str, expected_owner: str) -> list[str]:
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
    errors.extend(validate_markdown_owner(text, expected_owner))
    return errors


def validate_internal_human_agents(
    text: str,
    expected_owner: str,
    payload_schema: dict[str, object] | None = None,
) -> list[str]:
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
    if payload is not None:
        errors.extend(_validate_default_meta_skill_uniqueness(payload))
        errors.extend(_validate_standard_write_exec(payload))
    errors.extend(validate_markdown_owner(text, expected_owner))
    return errors


def validate_machine_json(
    machine_path: Path,
    expected_owner: str,
    payload_schema: dict[str, object] | None = None,
) -> list[str]:
    if not machine_path.exists():
        return ["missing_machine_json"]
    try:
        payload = read_json(machine_path)
    except json.JSONDecodeError as exc:
        return [f"invalid_machine_json:{exc.msg}"]
    if not isinstance(payload, dict):
        return ["machine_payload_type_invalid"]
    if payload.get("owner") is None:
        return ["missing_owner_field"]
    if payload.get("owner") != expected_owner:
        return ["owner_field_mismatch"]
    errors = _validate_default_meta_skill_uniqueness(payload)
    errors.extend(_validate_standard_write_exec(payload))
    if payload_schema is None:
        return errors
    errors.extend(_validate_payload_value(payload, payload_schema, "$"))
    return errors


def validate_managed_agents_pair(
    paths: RuntimePaths,
    source_path: Path,
    human_path: Path,
    machine_path: Path,
) -> list[str]:
    errors: list[str] = []
    payload_schema = _payload_schema_for_source(paths, source_path)
    expected_owner = derive_owner_text(paths, source_path, "AGENTS_MD", "AGENTS.md")
    if payload_schema is None and not is_runtime_local_source(paths, source_path):
        return [f"missing_payload_structure_schema:{_relative_source_key(paths, source_path)}"]
    if not human_path.exists():
        errors.append("missing_managed_human")
    else:
        errors.extend(
            validate_internal_human_agents(
                human_path.read_text(encoding="utf-8"),
                expected_owner,
                payload_schema,
            )
        )
    errors.extend(validate_machine_json(machine_path, expected_owner, payload_schema))
    external_text = source_path.read_text(encoding="utf-8") if source_path.exists() else None
    if source_path.exists() and machine_path.exists():
        try:
            machine_payload = read_json(machine_path)
        except json.JSONDecodeError:
            machine_payload = None
        if isinstance(machine_payload, dict):
            if external_text is not None:
                errors.extend(validate_agents_writeback_completion(external_text, machine_payload))
            errors.extend(
                _validate_parent_agents_duplicates(
                    paths,
                    source_path,
                    external_text or "",
                    machine_payload,
                )
            )
    return errors


def validate_plain_mapping(entry: dict[str, object]) -> list[str]:
    source_path = Path(entry["source_path"])
    mapped_path = Path(entry["managed_mapped_path"])
    expected_owner = str(entry["owner"])
    errors: list[str] = []
    if not mapped_path.exists():
        return ["missing_managed_mapping"]
    if not source_path.exists():
        return ["missing_external_source"]
    managed_text = mapped_path.read_text(encoding="utf-8")
    errors.extend(validate_owner_in_managed_plain_copy(managed_text, expected_owner))
    managed_text = strip_owner_from_managed_plain_copy(managed_text)
    if managed_text != source_path.read_text(encoding="utf-8"):
        errors.append("managed_mapping_content_drift")
    return errors


def lint_external_entry(paths: RuntimePaths, entry: dict[str, object]) -> list[str]:
    source_path = Path(entry["source_path"])
    if not source_path.exists():
        return ["missing_external_source"]
    if entry["mapping_mode"] == "agents_ab":
        text = source_path.read_text(encoding="utf-8")
        errors = validate_external_agents(text, str(entry["owner"]))
        errors.extend(validate_source_specific_external_agents(paths, source_path, text))
        return errors
    return []


def lint_managed_entry(
    paths: RuntimePaths,
    entry: dict[str, object],
    *,
    include_external: bool = True,
) -> list[str]:
    source_path = Path(entry["source_path"])
    errors = lint_external_entry(paths, entry) if include_external else []
    if entry["mapping_mode"] == "agents_ab":
        errors.extend(
            validate_managed_agents_pair(
                paths,
                source_path,
                Path(entry["managed_human_path"]),
                Path(entry["managed_machine_path"]),
            )
        )
        return errors
    errors.extend(validate_plain_mapping(entry))
    return errors


def report_artifact_path(paths: RuntimePaths, stage: str) -> Path:
    return paths.runtime_root / "artifacts" / stage / "latest.json"


def report_log_dir(paths: RuntimePaths, stage: str) -> Path:
    return paths.runtime_root / "logs" / stage


def write_stage_report(
    paths: RuntimePaths,
    stage: str,
    payload: object,
    dry_run: bool,
    custom_report_path: str | None = None,
) -> Path:
    latest = report_artifact_path(paths, stage)
    stamped = report_log_dir(paths, stage) / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.json"
    custom_path = Path(custom_report_path).expanduser().resolve() if custom_report_path else None
    if not dry_run:
        serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        latest.parent.mkdir(parents=True, exist_ok=True)
        stamped.parent.mkdir(parents=True, exist_ok=True)
        latest.write_text(serialized, encoding="utf-8")
        stamped.write_text(serialized, encoding="utf-8")
        if custom_path is not None:
            custom_path.parent.mkdir(parents=True, exist_ok=True)
            custom_path.write_text(serialized, encoding="utf-8")
    return latest


def add_governed_source_path(
    paths: RuntimePaths,
    source_path: Path,
    file_kind: str,
    dry_run: bool,
) -> None:
    if is_runtime_local_source(paths, source_path):
        return
    found = find_channel_by_file_kind(paths, file_kind)
    if found is None:
        raise ValueError(f"unsupported_file_kind:{file_kind}")
    channel_id, channel = found
    relative = _relative_source_key(paths, source_path)
    rules = load_scan_rules(paths)
    governed = list(rules["channels"][channel_id].get("governed_source_paths", []))
    if relative not in governed:
        governed.append(relative)
        governed.sort()
        rules["channels"][channel_id]["governed_source_paths"] = governed
        write_json(paths.scan_rules_path, rules, dry_run)
        sync_file_to_installed(paths, paths.scan_rules_path, dry_run)


def _render_part_a_template_from_root(paths: RuntimePaths) -> str | None:
    template_path = _root_agents_template_human_path(paths)
    if not template_path.exists():
        return None
    template_text = template_path.read_text(encoding="utf-8")
    body = extract_external_agents_part_a_body(template_text)
    section_titles = [
        line.strip()
        for line in body.splitlines()
        if re.match(r"^\d+\.\s+", line.strip())
    ]
    if not section_titles:
        return None
    rendered_lines: list[str] = []
    for index, title in enumerate(section_titles):
        if index > 0:
            rendered_lines.append("")
        rendered_lines.append(title)
        rendered_lines.append("- replace_me")
    rendered = "\n".join(rendered_lines).strip()
    if rendered:
        return rendered
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            rendered_lines.append("")
            continue
        if re.match(r"^\d+\.\s+", stripped):
            rendered_lines.append(stripped)
            continue
        if stripped.startswith("- "):
            rendered_lines.append("- replace_me")
            continue
        rendered_lines.append("replace_me")
    return "\n".join(rendered_lines).strip()


def _scaffold_agents_string_value(path: str) -> str:
    if path == "$.entry_role":
        return SCAFFOLD_REPLACE_ME
    if path == "$.runtime_source_policy.runtime_rule_source":
        return "CLI_JSON"
    if path == "$.execution_modes.READ_EXEC.goal":
        return SCAFFOLD_REPLACE_ME
    if path == "$.execution_modes.WRITE_EXEC.goal":
        return STANDARD_WRITE_EXEC_GOAL
    if path.endswith(".repo_name"):
        return SCAFFOLD_NOT_APPLICABLE
    return SCAFFOLD_REPLACE_ME


def _scaffold_agents_value_from_root_template(value: object, path: str, owner: str) -> object:
    if path == "$.owner":
        return owner
    if path.startswith("$.runtime_source_policy"):
        return value
    if path.startswith("$.execution_modes.WRITE_EXEC"):
        return value
    if isinstance(value, dict):
        return {
            key: _scaffold_agents_value_from_root_template(item, f"{path}.{key}", owner)
            for key, item in value.items()
        }
    if isinstance(value, list):
        if path == "$.execution_modes.WRITE_EXEC.default_actions":
            return value
        if not value:
            return []
        return [
            _scaffold_agents_value_from_root_template(value[0], f"{path}[0]", owner)
        ]
    if isinstance(value, str):
        return _scaffold_agents_string_value(path)
    if isinstance(value, bool):
        return value
    return SCAFFOLD_NOT_APPLICABLE


def _scaffold_agents_value_from_schema(schema: dict[str, object], path: str, owner: str) -> object:
    schema_type = schema.get("type")
    if schema_type == "object":
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            return {}
        return {
            key: _scaffold_agents_value_from_schema(properties[key], f"{path}.{key}", owner)
            for key in schema.get("key_order", [])
            if key in properties
        }
    if schema_type == "array":
        if path == "$.execution_modes.WRITE_EXEC.default_actions":
            return [STANDARD_WRITE_EXEC_ACTION]
        return []
    if schema_type == "string":
        if path == "$.owner":
            return owner
        return _scaffold_agents_string_value(path)
    if schema_type == "boolean":
        if path in {
            "$.runtime_source_policy.audit_fields_are_not_primary_runtime_instructions",
            "$.runtime_source_policy.path_metadata_is_not_action_guidance",
        }:
            return True
        return False
    return SCAFFOLD_NOT_APPLICABLE


def scaffold_agents_machine_payload(paths: RuntimePaths, source_path: Path, owner: str) -> dict[str, object]:
    template_path = _root_agents_template_machine_path(paths)
    if template_path.exists():
        template_payload = read_json(template_path)
        if isinstance(template_payload, dict):
            payload = _scaffold_agents_value_from_root_template(template_payload, "$", owner)
            if isinstance(payload, dict):
                payload["owner"] = owner
                return payload
    schema = _payload_schema_for_source(paths, source_path) or _default_agents_payload_schema(paths)
    if schema is None:
        return {"owner": owner}
    payload = _scaffold_agents_value_from_schema(schema, "$", owner)
    if not isinstance(payload, dict):
        return {"owner": owner}
    payload["owner"] = owner
    return payload


def scaffold_external_agents(external_path: Path, owner: str) -> str:
    return upsert_frontmatter_owner(
        render_external_agents(_render_part_a_template_from_root(detect_paths(__file__)) or "1. 根入口命令\n- replace_me"),
        owner,
    )


def scaffold_internal_agents_human(
    paths: RuntimePaths,
    external_path: Path,
    owner: str,
    machine_payload: dict[str, object] | None = None,
) -> str:
    payload = machine_payload if machine_payload is not None else scaffold_agents_machine_payload(paths, external_path, owner)
    return render_internal_agents_human(scaffold_external_agents(external_path, owner), payload)


def scaffold_plain_external(_file_kind: str) -> str:
    return ""


def resolve_target_contract(paths: RuntimePaths, source_path: Path) -> dict[str, object]:
    found = find_channel_for_source_path(paths, source_path)
    if found is None:
        raise FileNotFoundError("governed_target_not_found")
    channel_id, channel = found
    entry = build_entry(paths, source_path, channel_id, channel)
    result = {
        "source_path": entry["source_path"],
        "relative_path": entry["relative_path"],
        "channel_id": entry["channel_id"],
        "file_kind": entry["file_kind"],
        "mapping_mode": entry["mapping_mode"],
        "owner": entry["owner"],
        "managed_dir": entry["managed_dir"],
        "managed_files": entry["managed_files"],
        "structure_template": entry.get("structure_template"),
    }
    if entry["mapping_mode"] == "agents_ab":
        machine_path = Path(entry["managed_machine_path"])
        if not machine_path.exists():
            raise FileNotFoundError("managed_machine_json_not_found")
        result["payload"] = read_json(machine_path)
    return result
