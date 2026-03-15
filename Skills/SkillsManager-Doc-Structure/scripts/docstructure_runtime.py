from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SKILL_MODE_TO_SHAPE_KIND = {
    "guide_only": "facade_only",
    "guide_with_tool": "linear_path",
    "executable_workflow_skill": "compound_path",
}
SHAPE_KIND_OVERVIEW = {
    "facade_only": "最小门面型：所有内容留在 SKILL.md 内，不进入 path/。",
    "linear_path": "单线路径型：允许多个入口，但每个入口进入后必须单线到底。",
    "compound_path": "复合路径型：入口进入后允许 workflow index 与步骤子闭环继续下沉。",
}
ROOT_IGNORE_NAMES = {"__pycache__"}
ALLOWED_HOPS = {"entry", "next", "branch"}


@dataclass
class ChainEdge:
    key: str
    target: str
    hop: str
    reason: str
    source: Path

    @property
    def resolved(self) -> Path:
        return (self.source.parent / self.target).resolve()


def runtime_contract_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "skill_name": "SkillsManager-Doc-Structure",
        "runtime_entry": "./scripts/Cli_Toolbox.py",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "governed_scope": [
            "root shape",
            "SKILL.md facade scope",
            "reading-chain definition",
            "structural role alignment",
            "reading-chain compilation",
            "semantic review workflow",
        ],
        "target_shape_model": {
            "facade_only": SHAPE_KIND_OVERVIEW["facade_only"],
            "linear_path": SHAPE_KIND_OVERVIEW["linear_path"],
            "compound_path": SHAPE_KIND_OVERVIEW["compound_path"],
        },
        "skill_mode_mapping": SKILL_MODE_TO_SHAPE_KIND,
        "commands": [
            "runtime-contract",
            "inspect-target",
            "lint-root-shape",
            "lint-reading-chain",
            "compile-reading-chain",
            "read-contract-context",
            "read-path-context",
            "lint-docstructure",
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
    raw_frontmatter = text[4:closing]
    body = text[closing + 5 :]
    payload = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(payload, dict):
        return {}, body
    return payload, body


def _visible_root_entries(target_root: Path) -> list[str]:
    entries = []
    for child in target_root.iterdir():
        if child.name.startswith(".") or child.name in ROOT_IGNORE_NAMES:
            continue
        entries.append(child.name)
    return sorted(entries)


def _resolve_target_shape(target_root: Path) -> dict[str, Any]:
    skill_md = target_root / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"target skill is missing SKILL.md: {skill_md}")

    frontmatter, _ = _parse_frontmatter(skill_md)
    skill_mode = frontmatter.get("skill_mode")
    shape_kind = SKILL_MODE_TO_SHAPE_KIND.get(skill_mode)
    if shape_kind is None:
        if (target_root / "path").is_dir():
            path_root = target_root / "path"
            if any(path_root.rglob("20_WORKFLOW_INDEX.md")):
                shape_kind = "compound_path"
            else:
                shape_kind = "linear_path"
        else:
            shape_kind = "facade_only"
    return {
        "target_root": str(target_root),
        "skill_md": str(skill_md),
        "detected_skill_mode": skill_mode,
        "shape_kind": shape_kind,
        "shape_overview": SHAPE_KIND_OVERVIEW[shape_kind],
    }


def inspect_target(target_root: Path) -> dict[str, Any]:
    payload = _resolve_target_shape(target_root)
    payload["status"] = "ok"
    payload["root_entries"] = _visible_root_entries(target_root)
    return payload


def lint_root_shape(target_root: Path) -> dict[str, Any]:
    payload = _resolve_target_shape(target_root)
    actual_entries = set(_visible_root_entries(target_root))
    expected_entries = {"SKILL.md", "agents"} if payload["shape_kind"] == "facade_only" else {"SKILL.md", "path", "agents", "scripts"}
    missing = sorted(expected_entries - actual_entries)
    unexpected = sorted(actual_entries - expected_entries)
    errors: list[str] = []
    if missing:
        errors.append(f"missing root entries: {', '.join(missing)}")
    if unexpected:
        errors.append(f"unexpected root entries: {', '.join(unexpected)}")
    return {
        "status": "ok" if not errors else "error",
        "target_root": str(target_root),
        "shape_kind": payload["shape_kind"],
        "expected_root_entries": sorted(expected_entries),
        "actual_root_entries": sorted(actual_entries),
        "errors": errors,
    }


def _reading_chain(markdown_path: Path) -> list[ChainEdge]:
    frontmatter, _ = _parse_frontmatter(markdown_path)
    if markdown_path.name == "SKILL.md":
        metadata = frontmatter.get("metadata")
        doc_structure = metadata.get("doc_structure", {}) if isinstance(metadata, dict) else {}
        raw_chain = doc_structure.get("reading_chain")
    else:
        raw_chain = frontmatter.get("reading_chain")
    if not isinstance(raw_chain, list):
        return []
    edges: list[ChainEdge] = []
    for index, item in enumerate(raw_chain, start=1):
        if not isinstance(item, dict):
            continue
        target = item.get("target")
        hop = item.get("hop")
        if not isinstance(target, str) or not isinstance(hop, str):
            continue
        key = item.get("key")
        if not isinstance(key, str) or not key.strip():
            key = f"hop_{index}"
        reason = item.get("reason")
        edges.append(
            ChainEdge(
                key=key.strip(),
                target=target,
                hop=hop.strip(),
                reason=reason if isinstance(reason, str) else "",
                source=markdown_path,
            )
        )
    return edges


def _markdown_files(target_root: Path) -> list[Path]:
    return sorted(path for path in target_root.rglob("*.md") if "__pycache__" not in path.parts)


def _discover_entry_dirs(path_root: Path) -> list[Path]:
    if not path_root.is_dir():
        return []
    entry_dirs: list[Path] = []
    for child in sorted(path_root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if any(file.name.startswith("00_") and file.name.endswith(".md") for file in child.glob("00_*.md")):
            entry_dirs.append(child)
    return entry_dirs


def _discover_zero_docs(node_dir: Path) -> list[Path]:
    return sorted(path for path in node_dir.glob("00_*.md") if path.is_file())


def _classify_node_dir(node_dir: Path) -> str:
    zero_docs = _discover_zero_docs(node_dir)
    if not zero_docs:
        return "not_a_node"
    markdown_names = {path.name for path in node_dir.glob("*.md")}
    linear_required = {"10_CONTRACT.md", "20_EXECUTION.md", "30_VALIDATION.md"}
    compound_required = {"10_CONTRACT.md", "15_TOOLS.md", "20_WORKFLOW_INDEX.md", "30_VALIDATION.md"}
    if compound_required.issubset(markdown_names) and (node_dir / "steps").is_dir():
        return "compound_loop"
    if linear_required.issubset(markdown_names):
        return "linear_loop"
    if any(child.is_dir() and not child.name.startswith(".") for child in node_dir.iterdir()):
        return "branch_index"
    return "terminal_index"


def _lint_facade(target_root: Path, shape_kind: str) -> list[str]:
    skill_md = target_root / "SKILL.md"
    frontmatter, body = _parse_frontmatter(skill_md)
    errors: list[str] = []
    required_sections = [
        "## 1. 模型立刻需要知道的事情",
        "## 2. 技能正文" if shape_kind == "facade_only" else "## 2. 功能入口",
        "## 3. 目录结构图",
    ]
    for section in required_sections:
        if section not in body:
            errors.append(f"SKILL.md is missing section: {section}")
    if shape_kind != "facade_only":
        chain = _reading_chain(skill_md)
        if not chain:
            errors.append("SKILL.md does not expose any reading-chain entry")
        for edge in chain:
            if edge.hop != "entry":
                errors.append(f"SKILL.md reading_chain hop must be 'entry': {edge.target}")
    else:
        if "reading_chain" in frontmatter:
            errors.append("facade_only skills must not declare reading_chain in SKILL.md")
    return errors


def _lint_chain_field(markdown_path: Path, target_root: Path) -> list[str]:
    errors: list[str] = []
    for edge in _reading_chain(markdown_path):
        if edge.hop not in ALLOWED_HOPS:
            errors.append(f"{markdown_path.relative_to(target_root)} uses unsupported hop: {edge.hop}")
            continue
        if not edge.resolved.exists():
            errors.append(
                f"{markdown_path.relative_to(target_root)} points to missing reading-chain target: {edge.target}"
            )
        elif edge.resolved.suffix != ".md":
            errors.append(
                f"{markdown_path.relative_to(target_root)} points to non-markdown reading-chain target: {edge.target}"
            )
    return errors


def _lint_markdown_section(markdown_path: Path, target_root: Path) -> list[str]:
    _frontmatter, body = _parse_frontmatter(markdown_path)
    errors: list[str] = []
    if markdown_path.name.startswith("00_") and "## 下一跳列表" not in body:
        errors.append(f"{markdown_path.relative_to(target_root)} is missing '## 下一跳列表'")
    return errors


def _lint_node_dir(node_dir: Path, target_root: Path) -> list[str]:
    kind = _classify_node_dir(node_dir)
    errors: list[str] = []
    zero_docs = _discover_zero_docs(node_dir)
    if kind == "not_a_node":
        return [f"{node_dir.relative_to(target_root)} is not a valid node directory"]
    if len(zero_docs) != 1:
        errors.append(f"{node_dir.relative_to(target_root)} must contain exactly one 00_*.md file")
        return errors
    entry_doc = zero_docs[0]
    chain = _reading_chain(entry_doc)

    if kind == "linear_loop":
        expected_names = {"10_CONTRACT.md", "20_EXECUTION.md", "30_VALIDATION.md"}
        if "15_TOOLS.md" in {path.name for path in node_dir.glob("*.md")}:
            expected_names.add("15_TOOLS.md")
        missing = sorted(expected_names - {path.name for path in node_dir.glob("*.md")})
        if missing:
            errors.append(f"{node_dir.relative_to(target_root)} is missing linear docs: {', '.join(missing)}")
        if len(chain) != 1 or chain[0].hop != "next":
            errors.append(f"{entry_doc.relative_to(target_root)} must expose exactly one next hop")
    elif kind == "compound_loop":
        expected_names = {"10_CONTRACT.md", "15_TOOLS.md", "20_WORKFLOW_INDEX.md", "30_VALIDATION.md"}
        missing = sorted(expected_names - {path.name for path in node_dir.glob("*.md")})
        if missing:
            errors.append(f"{node_dir.relative_to(target_root)} is missing compound docs: {', '.join(missing)}")
        if not (node_dir / "steps").is_dir():
            errors.append(f"{node_dir.relative_to(target_root)} is missing steps/")
        if len(chain) != 1 or chain[0].hop != "next":
            errors.append(f"{entry_doc.relative_to(target_root)} must expose exactly one next hop")
    elif kind == "branch_index":
        if not chain:
            errors.append(f"{entry_doc.relative_to(target_root)} must expose branch options")
        elif len(chain) == 1 and chain[0].hop == "next":
            # Allow a pass-through index that only forwards into one terminal or nested node.
            pass
        else:
            for edge in chain:
                if edge.hop != "branch":
                    errors.append(f"{entry_doc.relative_to(target_root)} must use branch hops")
    elif kind == "terminal_index":
        if chain:
            errors.append(f"{entry_doc.relative_to(target_root)} terminal index must not expose downstream hops")

    return errors


def build_reading_chain(target_root: Path) -> dict[str, Any]:
    nodes: list[str] = []
    edges: list[dict[str, Any]] = []
    for markdown_path in _markdown_files(target_root):
        relative_source = markdown_path.relative_to(target_root).as_posix()
        nodes.append(relative_source)
        for edge in _reading_chain(markdown_path):
            resolved = edge.resolved
            try:
                resolved_target = resolved.relative_to(target_root.resolve()).as_posix()
            except ValueError:
                resolved_target = str(resolved)
            edges.append(
                {
                    "source": relative_source,
                    "key": edge.key,
                    "target": edge.target,
                    "resolved_target": resolved_target,
                    "hop": edge.hop,
                    "reason": edge.reason,
                    "exists": resolved.exists(),
                }
            )
    return {
        "status": "ok",
        "target_root": str(target_root),
        "nodes": nodes,
        "edges": edges,
    }


def lint_reading_chain(target_root: Path) -> dict[str, Any]:
    payload = _resolve_target_shape(target_root)
    errors = _lint_facade(target_root, payload["shape_kind"])
    if payload["shape_kind"] == "facade_only":
        return {
            "status": "ok" if not errors else "error",
            "target_root": str(target_root),
            "shape_kind": payload["shape_kind"],
            "errors": errors,
        }

    path_root = target_root / "path"
    entry_dirs = _discover_entry_dirs(path_root)
    if not entry_dirs:
        errors.append(f"{path_root} does not expose any node directories")

    for markdown_path in _markdown_files(target_root):
        if markdown_path.name == "SKILL.md" or "agents" in markdown_path.parts:
            continue
        errors.extend(_lint_chain_field(markdown_path, target_root))
        errors.extend(_lint_markdown_section(markdown_path, target_root))

    for entry_dir in entry_dirs:
        errors.extend(_lint_node_dir(entry_dir, target_root))

    return {
        "status": "ok" if not errors else "error",
        "target_root": str(target_root),
        "shape_kind": payload["shape_kind"],
        "entry_dirs": [str(path.relative_to(target_root)) for path in entry_dirs],
        "errors": errors,
        "chain": build_reading_chain(target_root),
    }


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _select_edge(edges: list[ChainEdge], key: str | None) -> tuple[ChainEdge | None, list[str]]:
    if not edges:
        return None, []
    if key is None:
        return (edges[0], []) if len(edges) == 1 else (None, [edge.key for edge in edges])
    for edge in edges:
        if edge.key == key:
            return edge, []
    return None, [edge.key for edge in edges]


def compile_reading_chain(target_root: Path, entry_key: str, selection_keys: list[str]) -> dict[str, Any]:
    shape = _resolve_target_shape(target_root)
    if shape["shape_kind"] == "facade_only":
        _frontmatter, body = _parse_frontmatter(target_root / "SKILL.md")
        return {
            "status": "ok",
            "target_root": str(target_root),
            "entry": "facade_only",
            "resolved_chain": ["SKILL.md"],
            "segments": [{"source": "SKILL.md", "title": _extract_title(body), "content": body.strip()}],
            "compiled_markdown": body.strip(),
        }

    skill_md = target_root / "SKILL.md"
    skill_edges = _reading_chain(skill_md)
    first_edge, available = _select_edge(skill_edges, entry_key)
    if first_edge is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "entry": entry_key,
            "available_entries": available,
        }

    selection_queue = list(selection_keys)
    current = first_edge.resolved
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
            current = next_edge.resolved
            continue
        current = edges[0].resolved

    compiled_markdown = "\n\n".join(segment["content"] for segment in segments if segment["content"])
    return {
        "status": "ok",
        "target_root": str(target_root),
        "entry": entry_key,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": compiled_markdown,
    }


def lint_docstructure(target_root: Path) -> dict[str, Any]:
    shape_payload = lint_root_shape(target_root)
    chain_payload = lint_reading_chain(target_root)
    errors = [*shape_payload["errors"], *chain_payload["errors"]]
    inspected = inspect_target(target_root)
    return {
        "status": "ok" if not errors else "error",
        "target_root": str(target_root),
        "detected_skill_mode": inspected["detected_skill_mode"],
        "shape_kind": inspected["shape_kind"],
        "checks": {
            "root_shape": shape_payload,
            "reading_chain": chain_payload,
        },
        "errors": errors,
    }
