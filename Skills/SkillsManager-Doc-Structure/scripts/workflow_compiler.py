from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from doc_models import Issue, TargetProfile


ALLOWED_HOPS = {"entry", "next", "branch"}


def _parse_markdown(markdown_path: Path) -> tuple[dict[str, Any], str]:
    text = markdown_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    payload = yaml.safe_load(text[4:closing]) or {}
    body = text[closing + 5 :]
    return payload if isinstance(payload, dict) else {}, body


def lint_workflow(target_root: Path, profile: TargetProfile) -> list[Issue]:
    if profile.doc_topology != "workflow_path":
        return []
    path_root = target_root / "path"
    entry_docs = sorted(path_root.rglob("00_*.md"))
    if not entry_docs:
        return [Issue("workflow", "workflow_path target is missing 00_*.md entry documents")]
    issues: list[Issue] = []
    for markdown_path in sorted(path_root.rglob("*.md")):
        frontmatter, _body = _parse_markdown(markdown_path)
        chain = frontmatter.get("reading_chain")
        if not isinstance(chain, list):
            continue
        for item in chain:
            if not isinstance(item, dict):
                issues.append(Issue("workflow", f"invalid reading_chain item in {markdown_path.relative_to(target_root)}"))
                continue
            target = item.get("target")
            hop = item.get("hop")
            if not isinstance(target, str) or not isinstance(hop, str):
                issues.append(Issue("workflow", f"incomplete reading_chain item in {markdown_path.relative_to(target_root)}"))
                continue
            if hop not in ALLOWED_HOPS:
                issues.append(Issue("workflow", f"unsupported hop '{hop}' in {markdown_path.relative_to(target_root)}"))
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.is_file():
                issues.append(Issue("workflow", f"missing reading_chain target '{target}' from {markdown_path.relative_to(target_root)}"))
    return issues


def _compile_inline(target_root: Path) -> dict[str, object]:
    content = (target_root / "SKILL.md").read_text(encoding="utf-8")
    return {
        "status": "ok",
        "resolved_chain": ["SKILL.md"],
        "segments": [{"source": "SKILL.md", "content": content.strip()}],
        "compiled_markdown": content.strip(),
    }


def _compile_referenced(target_root: Path, entry: str | None) -> dict[str, object]:
    entry_key = entry or "routing"
    references_root = target_root / "references"
    entry_map: dict[str, list[Path]] = {
        "routing": [references_root / "routing" / "TASK_ROUTING.md"],
        "policy": sorted((references_root / "policies").glob("*.md")) or sorted((references_root / "governance").glob("*.md")),
        "runtime_contract": [references_root / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT_human.md"],
        "tooling": sorted((references_root / "tooling").rglob("*.md")),
    }
    selected = [path for path in entry_map.get(entry_key, []) if path.is_file()]
    if not selected:
        return {
            "status": "error",
            "error": "entry_not_found",
            "available_entries": sorted(entry_map.keys()),
        }
    segments = [{"source": "SKILL.md", "content": (target_root / "SKILL.md").read_text(encoding="utf-8").strip()}]
    resolved_chain = ["SKILL.md"]
    for path in selected:
        relative = path.relative_to(target_root).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "content": path.read_text(encoding="utf-8").strip()})
    return {
        "status": "ok",
        "entry": entry_key,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": "\n\n".join(segment["content"] for segment in segments if segment["content"]),
    }


def _workflow_entry_candidates(path_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for candidate in sorted(path_root.rglob("00_*.md")):
        if "steps" not in candidate.parts:
            candidates.append(candidate)
    return candidates or sorted(path_root.rglob("00_*.md"))


def _select_workflow_entry(path_root: Path, entry: str | None) -> tuple[Path | None, list[str]]:
    candidates = _workflow_entry_candidates(path_root)
    labels = [candidate.parent.name for candidate in candidates]
    if entry is None:
        return (candidates[0] if len(candidates) == 1 else None), labels
    for candidate in candidates:
        if candidate.parent.name == entry or candidate.stem == entry:
            return candidate, labels
    return None, labels


def _compile_workflow(target_root: Path, entry: str | None, selection: list[str]) -> dict[str, object]:
    path_root = target_root / "path"
    current, available_entries = _select_workflow_entry(path_root, entry)
    if current is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "available_entries": available_entries,
        }
    queue = list(selection)
    resolved_chain = ["SKILL.md"]
    segments = [{"source": "SKILL.md", "content": (target_root / "SKILL.md").read_text(encoding="utf-8").strip()}]
    while True:
        frontmatter, body = _parse_markdown(current)
        relative = current.relative_to(target_root).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "content": body.strip()})
        chain = frontmatter.get("reading_chain")
        if not isinstance(chain, list) or not chain:
            break
        if len(chain) > 1:
            if not queue:
                available_next = [item.get("key") for item in chain if isinstance(item, dict) and isinstance(item.get("key"), str)]
                return {
                    "status": "branch_selection_required",
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": available_next,
                    "current_source": relative,
                }
            selected_key = queue.pop(0)
            next_item = next(
                (
                    item
                    for item in chain
                    if isinstance(item, dict) and isinstance(item.get("key"), str) and item["key"] == selected_key
                ),
                None,
            )
            if next_item is None:
                return {
                    "status": "branch_selection_required",
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": [item.get("key") for item in chain if isinstance(item, dict)],
                    "current_source": relative,
                }
        else:
            next_item = chain[0] if isinstance(chain[0], dict) else None
        if not isinstance(next_item, dict) or not isinstance(next_item.get("target"), str):
            break
        current = (current.parent / next_item["target"]).resolve()
    return {
        "status": "ok",
        "entry": entry or current.parent.name,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": "\n\n".join(segment["content"] for segment in segments if segment["content"]),
    }


def compile_context(target_root: Path, profile: TargetProfile, entry: str | None, selection: list[str]) -> dict[str, object]:
    if profile.doc_topology == "inline":
        return _compile_inline(target_root)
    if profile.doc_topology == "referenced":
        return _compile_referenced(target_root, entry)
    return _compile_workflow(target_root, entry, selection)
