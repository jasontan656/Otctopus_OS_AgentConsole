from __future__ import annotations

import re
from pathlib import Path
from typing import Literal
from typing import NotRequired
from typing import TypedDict

import yaml


class RuntimePayload(TypedDict):
    status: Literal["ok"]
    skill_name: str
    skill_mode: str
    runtime_entry: str
    root_shape: list[str]
    governed_scope: list[str]
    commands: list[str]
    notes: list[str]


class FrontmatterEdge(TypedDict):
    key: str
    target: str
    hop: str


class CompiledSegment(TypedDict):
    source: str
    title: str
    content: str


class ReadingChainMissingSkill(TypedDict):
    status: Literal["error"]
    error: Literal["missing_skill_md"]
    target_root: str


class ReadingChainEntryNotFound(TypedDict):
    status: Literal["error"]
    error: Literal["entry_not_found"]
    entry: str
    available_entries: list[str]
    target_root: str


class ReadingChainBranchRequired(TypedDict):
    status: Literal["branch_selection_required"]
    target_root: str
    entry: str
    resolved_chain: list[str]
    available_next: list[str]
    current_source: str
    segments: list[CompiledSegment]


class ReadingChainSuccess(TypedDict):
    status: Literal["ok"]
    target_root: str
    entry: str
    resolved_chain: list[str]
    segments: list[CompiledSegment]
    compiled_markdown: str


ReadingChainResult = ReadingChainMissingSkill | ReadingChainEntryNotFound | ReadingChainBranchRequired | ReadingChainSuccess


def runtime_payload() -> RuntimePayload:
    return {
        "status": "ok",
        "skill_name": "SkillsManager-Mirror-To-Codex",
        "skill_mode": "guide_with_tool",
        "runtime_entry": "./scripts/Cli_Toolbox.py",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "governed_scope": [
            "auto routing between push and install",
            "push sync semantics",
            "install route semantics",
            "rename sync semantics",
            "mirror root and sync boundary",
        ],
        "commands": [
            "runtime-contract",
            "contract",
            "read-contract-context",
            "read-path-context",
        ],
        "notes": [
            "documents remain the source of truth",
            "SKILL.md exposes function entries directly in section 2",
            "downstream path documents continue with frontmatter reading_chain",
        ],
    }


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, object], str]:
    text = _read_text(markdown_path)
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    payload = yaml.safe_load(text[4:closing]) or {}
    body = text[closing + 5 :]
    return payload if isinstance(payload, dict) else {}, body


def _facade_entries(markdown_path: Path) -> list[FrontmatterEdge]:
    _frontmatter, body = _parse_frontmatter(markdown_path)
    items: list[FrontmatterEdge] = []
    current: FrontmatterEdge | None = None
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


def _reading_chain(markdown_path: Path) -> list[FrontmatterEdge]:
    if markdown_path.name == "SKILL.md":
        return _facade_entries(markdown_path)
    frontmatter, _ = _parse_frontmatter(markdown_path)
    raw_chain = frontmatter.get("reading_chain")
    if not isinstance(raw_chain, list):
        return []
    chain: list[FrontmatterEdge] = []
    for item in raw_chain:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        target = item.get("target")
        hop = item.get("hop")
        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):
            chain.append({"key": key, "target": target, "hop": hop})
    return chain


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _select_edge(edges: list[FrontmatterEdge], key: str | None) -> tuple[FrontmatterEdge | None, list[str]]:
    if not edges:
        return None, []
    if key is None:
        return (edges[0], []) if len(edges) == 1 else (None, [edge["key"] for edge in edges])
    for edge in edges:
        if edge["key"] == key:
            return edge, []
    return None, [edge["key"] for edge in edges]


def compile_reading_chain(target_root: Path, entry_key: str, selection_keys: list[str]) -> ReadingChainResult:
    skill_md = target_root / "SKILL.md"
    if not skill_md.is_file():
        return {"status": "error", "error": "missing_skill_md", "target_root": str(target_root)}

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
    segments: list[CompiledSegment] = []

    _skill_frontmatter, skill_body = _parse_frontmatter(skill_md)
    segments.append({"source": "SKILL.md", "title": _extract_title(skill_body), "content": skill_body.strip()})

    while True:
        _frontmatter, body = _parse_frontmatter(current)
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

    return {
        "status": "ok",
        "target_root": str(target_root),
        "entry": entry_key,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": "\n\n".join(segment["content"] for segment in segments if segment["content"]),
    }
