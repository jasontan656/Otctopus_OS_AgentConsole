from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]


def runtime_contract_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "skill_name": "Workflow-CentralFlow2-OctppusOS",
        "skill_mode": "executable_workflow_skill",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "entry_doc": "path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md",
        "commands": [
            "runtime-contract",
            "read-contract-context",
            "read-path-context",
            "workflow-contract",
            "target-runtime-contract",
            "stage-checklist",
            "stage-doc-contract",
            "stage-command-contract",
            "stage-graph-contract",
            "graph-preflight",
            "graph-postflight",
            "target-scaffold",
            "template-index",
            "mother-doc-init",
            "mother-doc-archive",
            "construction-plan-init",
            "construction-plan-lint",
            "mother-doc-lint",
            "mother-doc-refresh-root-index",
            "mother-doc-state-sync",
            "mother-doc-mark-modified",
            "mother-doc-sync-client-copy",
            "acceptance-lint",
        ],
        "layout_rule": "Folder layout mirrors reading order. Static docs live under path, runtime helpers stay in scripts.",
        "compiler_rule": "SKILL.md section 2 exposes function entries; downstream markdown uses reading_chain to compile one contract context.",
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
    raw_frontmatter = text[4:closing]
    body = text[closing + 5 :]
    payload = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(payload, dict):
        return {}, body
    return payload, body


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


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


def _reading_chain(markdown_path: Path) -> list[dict[str, str]]:
    if markdown_path.name == "SKILL.md":
        return _facade_entries(markdown_path)
    frontmatter, _body = _parse_frontmatter(markdown_path)
    raw = frontmatter.get("reading_chain")
    if not isinstance(raw, list):
        return []
    items: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        target = item.get("target")
        hop = item.get("hop")
        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):
            items.append({"key": key, "target": target, "hop": hop})
    return items


def compile_reading_chain(entry: str, selection: list[str]) -> dict[str, Any]:
    skill_md = SKILL_ROOT / "SKILL.md"
    resolved_chain = ["SKILL.md"]
    _frontmatter, skill_body = _parse_frontmatter(skill_md)
    segments: list[dict[str, str]] = [
        {"source": "SKILL.md", "title": _extract_title(skill_body), "content": skill_body.strip()}
    ]
    root_items = _reading_chain(skill_md)
    chosen = next((item for item in root_items if item["key"] == entry), None)
    if chosen is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "entry": entry,
            "available_entries": [item["key"] for item in root_items],
        }
    queue = list(selection)
    current = (skill_md.parent / chosen["target"]).resolve()
    while True:
        _frontmatter, body = _parse_frontmatter(current)
        relative = current.relative_to(SKILL_ROOT).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "title": _extract_title(body), "content": body.strip()})
        items = _reading_chain(current)
        if not items:
            break
        if len(items) > 1:
            requested = queue.pop(0) if queue else None
            if requested is None:
                return {
                    "status": "branch_selection_required",
                    "entry": entry,
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": [item["key"] for item in items],
                    "current_source": relative,
                }
            chosen = next((item for item in items if item["key"] == requested), None)
            if chosen is None:
                return {
                    "status": "branch_selection_required",
                    "entry": entry,
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": [item["key"] for item in items],
                    "current_source": relative,
                }
        else:
            chosen = items[0]
        current = (current.parent / chosen["target"]).resolve()
    return {
        "status": "ok",
        "entry": entry,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": "\n\n".join(item["content"] for item in segments if item["content"]),
    }
