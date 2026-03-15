from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml

ROOT_IGNORE_NAMES = {"__pycache__"}


def runtime_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "skill_name": "SkillsManager-Tooling-CheckUp",
        "runtime_entry": "./scripts/Cli_Toolbox.py",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "governed_scope": [
            "techstack baseline overlap",
            "output governance",
            "CLI surface contract",
            "tooling responsibility boundaries",
            "behavior-preserving remediation",
        ],
        "commands": [
            "runtime-contract",
            "read-contract-context",
            "read-path-context",
            "govern-target",
        ],
        "notes": [
            "documents remain the source of truth",
            "CLI payloads are compiled reading views or audit views",
            "read-contract-context is the preferred shortcut when the model wants one compiled contract context for a selected function entry",
            "this skill does not govern target root shape or reading-chain design itself",
        ],
    }


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, Any], str]:
    text = _read_text(markdown_path)
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    payload = yaml.safe_load(text[4:closing]) or {}
    body = text[closing + 5 :]
    return payload if isinstance(payload, dict) else {}, body


def _reading_chain(markdown_path: Path) -> list[dict[str, str]]:
    frontmatter, _ = _parse_frontmatter(markdown_path)
    if markdown_path.name == "SKILL.md":
        return _facade_entries(markdown_path)
    else:
        raw_chain = frontmatter.get("reading_chain")
    if not isinstance(raw_chain, list):
        return []
    chain: list[dict[str, str]] = []
    for item in raw_chain:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        target = item.get("target")
        hop = item.get("hop")
        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):
            chain.append({"key": key, "target": target, "hop": hop})
    return chain


def _facade_entries(markdown_path: Path) -> list[dict[str, str]]:
    _frontmatter, body = _parse_frontmatter(markdown_path)
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_entries = False
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if stripped == "## 2. 功能入口":
            in_entries = True
            continue
        if in_entries and stripped.startswith("## "):
            break
        if not in_entries:
            continue
        match = re.match(r"^- \[(?P<label>[^\]]+)\][：:]\s*`(?P<target>[^`]+)`", stripped)
        if match:
            current = {
                "key": match.group("label").strip(),
                "target": match.group("target").strip(),
                "hop": "entry",
            }
            items.append(current)
            continue
        if current is None:
            continue
        command_match = re.search(r"--entry\s+([A-Za-z0-9_.-]+)", stripped)
        if command_match:
            current["key"] = command_match.group(1).strip()
    return items


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _select_edge(edges: list[dict[str, str]], key: str | None) -> tuple[dict[str, str] | None, list[str]]:
    if not edges:
        return None, []
    if key is None:
        return (edges[0], []) if len(edges) == 1 else (None, [edge["key"] for edge in edges])
    for edge in edges:
        if edge["key"] == key:
            return edge, []
    return None, [edge["key"] for edge in edges]


def compile_reading_chain(target_root: Path, entry_key: str, selection_keys: list[str]) -> dict[str, Any]:
    skill_md = target_root / "SKILL.md"
    if not skill_md.is_file():
        return {
            "status": "error",
            "error": "missing_skill_md",
            "target_root": str(target_root),
        }

    skill_edges = _reading_chain(skill_md)
    first_edge, available = _select_edge(skill_edges, entry_key)
    if first_edge is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "entry": entry_key,
            "available_entries": available,
            "target_root": str(target_root),
        }

    selection_queue = list(selection_keys)
    current = (skill_md.parent / first_edge["target"]).resolve()
    resolved_chain = ["SKILL.md"]
    segments: list[dict[str, str]] = []

    _skill_frontmatter, skill_body = _parse_frontmatter(skill_md)
    segments.append({"source": "SKILL.md", "title": _extract_title(skill_body), "content": skill_body.strip()})

    while True:
        frontmatter, body = _parse_frontmatter(current)
        relative = current.relative_to(target_root).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "title": _extract_title(body), "content": body.strip()})
        edges = _reading_chain(current)
        if not edges:
            break
        if len(edges) > 1:
            requested = selection_queue.pop(0) if selection_queue else None
            next_edge, available = _select_edge(edges, requested)
            if next_edge is None:
                return {
                    "status": "branch_selection_required",
                    "target_root": str(target_root),
                    "entry": entry_key,
                    "resolved_chain": resolved_chain,
                    "available_next": available,
                    "current_source": relative,
                    "segments": segments,
                }
            current = (current.parent / next_edge["target"]).resolve()
            continue
        current = (current.parent / edges[0]["target"]).resolve()

    compiled_markdown = "\n\n".join(segment["content"] for segment in segments if segment["content"])
    return {
        "status": "ok",
        "target_root": str(target_root),
        "entry": entry_key,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": compiled_markdown,
    }


def _parse_skill_mode(skill_root: Path) -> str | None:
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        return None
    frontmatter, _ = _parse_frontmatter(skill_md)
    mode = frontmatter.get("skill_mode")
    return mode if isinstance(mode, str) else None


def _detect_cli_entry(scripts_dir: Path) -> Path | None:
    if not scripts_dir.is_dir():
        return None
    for name in ("Cli_Toolbox.py", "Cli_Toolbox.ts", "Cli_Toolbox.js"):
        candidate = scripts_dir / name
        if candidate.exists():
            return candidate
    return None


def _invoke_chain_reader(cli_path: Path, target_root: Path, entry: str, selection: list[str]) -> tuple[bool, dict[str, Any] | None, str | None]:
    import json
    import subprocess

    cmd = ["python3", str(cli_path), "read-contract-context", "--entry", entry]
    if selection:
        cmd.extend(["--selection", ",".join(selection)])
    cmd.append("--json")
    completed = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        cwd=target_root,
    )
    if completed.returncode != 0:
        fallback_cmd = ["python3", str(cli_path), "read-path-context", "--entry", entry]
        if selection:
            fallback_cmd.extend(["--selection", ",".join(selection)])
        fallback_cmd.append("--json")
        completed = subprocess.run(
            fallback_cmd,
            check=False,
            capture_output=True,
            text=True,
            cwd=target_root,
        )
        if completed.returncode != 0:
            return False, None, "command_failed"
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return False, None, "invalid_json"
    if not isinstance(payload, dict):
        return False, None, "invalid_json"
    status = payload.get("status")
    return True, payload, status if isinstance(status, str) else None


def _run_chain_reader(cli_path: Path, target_root: Path) -> tuple[bool, str | None]:
    skill_md = target_root / "SKILL.md"
    root_chain = _reading_chain(skill_md)
    if not root_chain:
        return False, None
    entry = root_chain[0]["key"]
    selection: list[str] = []
    for _ in range(8):
        ok, payload, status = _invoke_chain_reader(cli_path, target_root, entry, selection)
        if not ok or payload is None or status is None:
            return False, status
        if status == "ok":
            required_fields = {"resolved_chain", "segments", "compiled_markdown"}
            return required_fields.issubset(payload.keys()), status
        if status != "branch_selection_required":
            return False, status
        available_next = payload.get("available_next")
        if not (isinstance(available_next, list) and available_next and isinstance(available_next[0], str)):
            return False, "branch_selection_required"
        selection.append(available_next[0])
    return False, "branch_selection_required"


def govern_target(target_root: Path) -> dict[str, Any]:
    skill_path = target_root / "SKILL.md"
    if not target_root.exists() or not target_root.is_dir():
        return {
            "status": "error",
            "error": "target_skill_root_not_found",
            "target_skill_root": str(target_root),
        }
    if not skill_path.exists():
        return {
            "status": "error",
            "error": "target_skill_root_missing_skill_md",
            "target_skill_root": str(target_root),
        }

    skill_mode = _parse_skill_mode(target_root)
    scripts_dir = target_root / "scripts"
    path_dir = target_root / "path"
    scripts_dir_exists = scripts_dir.is_dir()
    path_dir_exists = path_dir.is_dir()
    cli_entry = _detect_cli_entry(scripts_dir)
    tooling_surface_detected = scripts_dir_exists
    chain_reader_required = scripts_dir_exists and path_dir_exists and skill_mode != "guide_only"

    notes: list[str] = []
    chain_reader_present = False
    chain_reader_status: str | None = None

    if tooling_surface_detected and cli_entry is None:
        notes.append("scripts/ exists but no explicit Cli_Toolbox entry was detected")
    elif cli_entry is not None and chain_reader_required:
        chain_reader_present, chain_reader_status = _run_chain_reader(cli_entry, target_root)
        if not chain_reader_present:
            notes.append("path-based tooling skill is missing a working read-contract-context/read-path-context entry")

    if not tooling_surface_detected:
        notes.append("no governed tooling surface was detected under the target skill root")

    compliant = (not tooling_surface_detected) or (
        cli_entry is not None and (not chain_reader_required or chain_reader_present)
    )
    recommended_entries: list[str] = []
    if scripts_dir_exists:
        recommended_entries.append("cli_surface")
    if path_dir_exists:
        recommended_entries.append("output_governance")
    recommended_entries.extend(["techstack_baseline", "tooling_boundary"])
    if not compliant:
        recommended_entries.append("remediation")

    recommended_actions: list[str] = []
    if not tooling_surface_detected:
        recommended_actions.append("stop at tooling-surface absence; do not reinterpret this target as a shape-governance problem")
    else:
        if cli_entry is None:
            recommended_actions.append("review scripts/ and expose one explicit Cli_Toolbox entry if this target intends a governed CLI surface")
        if chain_reader_required and not chain_reader_present:
            recommended_actions.append("add a working read-contract-context command, and keep read-path-context as an equivalent alias when needed, so the target can compile one governed reading chain into JSON context output")
        if not recommended_actions:
            recommended_actions.append("target skill already satisfies the governed tooling surface checks covered by this CLI")

    return {
        "status": "ok",
        "action": "govern_target_skill_tooling",
        "target_skill_root": str(target_root),
        "audit": {
            "tooling_surface_detected": tooling_surface_detected,
            "scripts_dir_exists": scripts_dir_exists,
            "path_dir_exists": path_dir_exists,
            "skill_mode": skill_mode,
            "cli_entry_present": cli_entry is not None,
            "chain_reader_required": chain_reader_required,
            "chain_reader_present": chain_reader_present,
            "chain_reader_status": chain_reader_status,
            "notes": notes,
        },
        "compliant": compliant,
        "recommended_entries": recommended_entries,
        "recommended_actions": recommended_actions,
    }
