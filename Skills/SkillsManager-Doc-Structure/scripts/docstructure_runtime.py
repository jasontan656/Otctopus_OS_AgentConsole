from __future__ import annotations

import re
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
BACKTICK_MD_PATH_RE = re.compile(r"`([^`\n]+\.md)`")


def runtime_contract_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "skill_name": "SkillsManager-Doc-Structure",
        "runtime_entry": "./scripts/Cli_Toolbox.py",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "governed_scope": [
            "root shape",
            "SKILL.md facade scope",
            "path chaining",
            "structural role alignment",
            "anchor target resolution",
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
            "build-anchor-graph",
            "lint-anchor-graph",
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


def _resolve_target_shape(target_root: Path) -> dict[str, Any]:
    skill_md = target_root / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"target skill is missing SKILL.md: {skill_md}")

    frontmatter, _body = _parse_frontmatter(skill_md)
    skill_mode = frontmatter.get("skill_mode")
    shape_kind = SKILL_MODE_TO_SHAPE_KIND.get(skill_mode)

    if shape_kind is None:
        if (target_root / "path").is_dir():
            entry_dirs = _discover_entry_dirs(target_root / "path")
            if any((entry / "20_WORKFLOW_INDEX.md").is_file() or (entry / "steps").is_dir() for entry in entry_dirs):
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


def _visible_root_entries(target_root: Path) -> list[str]:
    entries = []
    for child in target_root.iterdir():
        if child.name.startswith(".") or child.name in ROOT_IGNORE_NAMES:
            continue
        entries.append(child.name)
    return sorted(entries)


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


def _discover_entry_dirs(path_root: Path) -> list[Path]:
    if not path_root.is_dir():
        return []
    entry_dirs = []
    for child in sorted(path_root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if any(file.name.startswith("00_") and file.name.endswith("_ENTRY.md") for file in child.glob("00_*_ENTRY.md")):
            entry_dirs.append(child)
    return entry_dirs


def _discover_zero_docs(node_dir: Path) -> list[Path]:
    return sorted(path for path in node_dir.glob("00_*.md") if path.is_file())


def _classify_node_dir(node_dir: Path) -> str:
    zero_docs = _discover_zero_docs(node_dir)
    if not zero_docs:
        return "not_a_node"

    subdirs = sorted(child for child in node_dir.iterdir() if child.is_dir() and not child.name.startswith("."))
    markdown_names = {path.name for path in node_dir.glob("*.md")}
    linear_required = {"10_CONTRACT.md", "20_EXECUTION.md", "30_VALIDATION.md"}
    compound_required = {"10_CONTRACT.md", "15_TOOLS.md", "20_WORKFLOW_INDEX.md", "30_VALIDATION.md"}

    if compound_required.issubset(markdown_names) and (node_dir / "steps").is_dir():
        return "compound_loop"
    if linear_required.issubset(markdown_names) and not subdirs:
        return "linear_loop"
    if subdirs:
        return "branch_index"
    return "terminal_index"


def _markdown_targets(markdown_path: Path, frontmatter: dict[str, Any], body: str) -> list[str]:
    targets: list[str] = []
    anchors = frontmatter.get("anchors")
    if isinstance(anchors, list):
        for item in anchors:
            if isinstance(item, dict) and isinstance(item.get("target"), str):
                targets.append(item["target"])
    for match in BACKTICK_MD_PATH_RE.finditer(body):
        targets.append(match.group(1))
    deduped: list[str] = []
    seen: set[str] = set()
    for target in targets:
        if target in seen:
            continue
        seen.add(target)
        deduped.append(target)
    return deduped


def _lint_markdown_section(markdown_path: Path, body: str) -> list[str]:
    errors: list[str] = []
    name = markdown_path.name

    if name == "SKILL.md":
        return errors

    if name.startswith("00_") and "## 下一跳列表" not in body:
        errors.append(f"{markdown_path} is missing '## 下一跳列表'")
    return errors


def _lint_facade(target_root: Path, shape_kind: str) -> list[str]:
    errors: list[str] = []
    skill_md = target_root / "SKILL.md"
    text = _read_text(skill_md)
    if shape_kind == "facade_only":
        required_sections = [
            "## 1. 模型立刻需要知道的事情",
            "## 2. 技能正文",
            "## 3. 目录结构图",
        ]
    else:
        required_sections = [
            "## 1. 模型立刻需要知道的事情",
            "## 2. 唯一入口",
            "## 3. 目录结构图",
        ]
    for section in required_sections:
        if section not in text:
            errors.append(f"SKILL.md is missing section: {section}")
    if shape_kind != "facade_only" and "`path/00_SKILL_ENTRY.md`" not in text:
        errors.append("SKILL.md does not expose path/00_SKILL_ENTRY.md as the only root entry")
    return errors


def _lint_linear_entry(entry_dir: Path) -> list[str]:
    errors: list[str] = []
    expected_names = {"10_CONTRACT.md", "20_EXECUTION.md", "30_VALIDATION.md"}
    actual_names = {path.name for path in entry_dir.glob("*.md")}
    missing = sorted(expected_names - actual_names)
    if missing:
        errors.append(f"{entry_dir} is missing required linear docs: {', '.join(missing)}")
    subdirs = [child.name for child in entry_dir.iterdir() if child.is_dir()]
    if subdirs:
        errors.append(f"{entry_dir} must stay linear and cannot contain subdirectories: {', '.join(sorted(subdirs))}")
    return errors


def _lint_terminal_index(entry_dir: Path) -> list[str]:
    errors: list[str] = []
    zero_docs = _discover_zero_docs(entry_dir)
    if len(zero_docs) != 1:
        errors.append(f"{entry_dir} terminal index must contain exactly one 00_*.md file")
    extra_markdown = [path.name for path in entry_dir.glob("*.md") if not path.name.startswith("00_")]
    if extra_markdown:
        errors.append(f"{entry_dir} terminal index must not carry extra markdown files: {', '.join(sorted(extra_markdown))}")
    return errors


def _lint_branch_index(entry_dir: Path, target_root: Path) -> list[str]:
    errors: list[str] = []
    zero_docs = _discover_zero_docs(entry_dir)
    if len(zero_docs) != 1:
        errors.append(f"{entry_dir} branch index must contain exactly one 00_*.md file")
    child_dirs = sorted(child for child in entry_dir.iterdir() if child.is_dir() and not child.name.startswith("."))
    if not child_dirs:
        errors.append(f"{entry_dir} branch index must expose child node directories")
        return errors

    frontmatter, body = _parse_frontmatter(zero_docs[0])
    if not _markdown_targets(zero_docs[0], frontmatter, body):
        errors.append(f"{zero_docs[0].relative_to(target_root)} branch index entry does not expose any downstream targets")

    for child_dir in child_dirs:
        child_kind = _classify_node_dir(child_dir)
        if child_kind == "not_a_node":
            errors.append(f"{child_dir} is not a valid child node under branch index {entry_dir}")
            continue
        errors.extend(_lint_node_dir(child_dir, target_root))
    return errors


def _lint_compound_entry(entry_dir: Path) -> list[str]:
    errors: list[str] = []
    expected_names = {"10_CONTRACT.md", "15_TOOLS.md", "20_WORKFLOW_INDEX.md", "30_VALIDATION.md"}
    actual_names = {path.name for path in entry_dir.glob("*.md")}
    missing = sorted(expected_names - actual_names)
    if missing:
        errors.append(f"{entry_dir} is missing required compound docs: {', '.join(missing)}")
    steps_dir = entry_dir / "steps"
    if not steps_dir.is_dir():
        errors.append(f"{entry_dir} is missing steps/")
        return errors
    step_dirs = sorted(child for child in steps_dir.iterdir() if child.is_dir())
    if not step_dirs:
        errors.append(f"{entry_dir} has steps/ but no step directories")
        return errors
    expected_step_names = {"10_CONTRACT.md", "15_TOOLS.md", "20_EXECUTION.md", "30_VALIDATION.md"}
    for step_dir in step_dirs:
        step_files = {path.name for path in step_dir.glob("*.md")}
        missing_steps = sorted(expected_step_names - step_files)
        if missing_steps:
            errors.append(f"{step_dir} is missing required step docs: {', '.join(missing_steps)}")
        if not any(path.name.startswith("00_") and path.name.endswith("_ENTRY.md") for path in step_dir.glob("00_*_ENTRY.md")):
            errors.append(f"{step_dir} is missing its 00_*_ENTRY.md file")
    return errors


def _lint_node_dir(entry_dir: Path, target_root: Path) -> list[str]:
    node_kind = _classify_node_dir(entry_dir)
    if node_kind == "linear_loop":
        return _lint_linear_entry(entry_dir)
    if node_kind == "compound_loop":
        return _lint_compound_entry(entry_dir)
    if node_kind == "branch_index":
        return _lint_branch_index(entry_dir, target_root)
    if node_kind == "terminal_index":
        return _lint_terminal_index(entry_dir)
    return [f"{entry_dir} is not a valid node directory"]


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
    skill_entry = path_root / "00_SKILL_ENTRY.md"
    if not skill_entry.is_file():
        errors.append(f"missing path entry: {skill_entry}")
    entry_dirs = _discover_entry_dirs(path_root)
    if not entry_dirs:
        errors.append(f"{path_root} does not expose any entry directories")

    for markdown_path in sorted(target_root.rglob("*.md")):
        if markdown_path.parts[-2:-1] == ("agents",):
            continue
        if markdown_path.name == "SKILL.md":
            continue
        parent_kind = _classify_node_dir(markdown_path.parent)
        frontmatter, body = _parse_frontmatter(markdown_path)
        if parent_kind in {"linear_loop", "compound_loop", "branch_index"} and markdown_path.name.startswith("00_"):
            errors.extend(_lint_markdown_section(markdown_path.relative_to(target_root), body))
            targets = _markdown_targets(markdown_path, frontmatter, body)
            if not targets:
                errors.append(f"{markdown_path.relative_to(target_root)} does not expose any next-hop markdown target")

    for entry_dir in entry_dirs:
        errors.extend(_lint_node_dir(entry_dir, target_root))

    return {
        "status": "ok" if not errors else "error",
        "target_root": str(target_root),
        "shape_kind": payload["shape_kind"],
        "entry_dirs": [str(path.relative_to(target_root)) for path in entry_dirs],
        "errors": errors,
    }


def build_anchor_graph(target_root: Path) -> dict[str, Any]:
    nodes: list[str] = []
    edges: list[dict[str, Any]] = []
    for markdown_path in sorted(target_root.rglob("*.md")):
        relative_source = markdown_path.relative_to(target_root).as_posix()
        nodes.append(relative_source)
        frontmatter, _body = _parse_frontmatter(markdown_path)
        anchors = frontmatter.get("anchors")
        if not isinstance(anchors, list):
            continue
        for item in anchors:
            if not isinstance(item, dict):
                continue
            raw_target = item.get("target")
            if not isinstance(raw_target, str):
                continue
            resolved_target = (markdown_path.parent / raw_target).resolve()
            target_within_root = None
            try:
                target_within_root = resolved_target.relative_to(target_root.resolve()).as_posix()
            except ValueError:
                target_within_root = str(resolved_target)
            edges.append(
                {
                    "source": relative_source,
                    "target": raw_target,
                    "resolved_target": target_within_root,
                    "relation": item.get("relation"),
                    "direction": item.get("direction"),
                    "exists": resolved_target.exists(),
                }
            )
    return {
        "status": "ok",
        "target_root": str(target_root),
        "nodes": nodes,
        "edges": edges,
    }


def lint_anchor_graph(target_root: Path) -> dict[str, Any]:
    graph = build_anchor_graph(target_root)
    errors = []
    for edge in graph["edges"]:
        if not edge["exists"]:
            errors.append(
                f"{edge['source']} points to missing anchor target: {edge['target']} -> {edge['resolved_target']}"
            )
    return {
        "status": "ok" if not errors else "error",
        "target_root": str(target_root),
        "edge_count": len(graph["edges"]),
        "errors": errors,
        "graph": graph,
    }


def lint_docstructure(target_root: Path) -> dict[str, Any]:
    shape_payload = lint_root_shape(target_root)
    chain_payload = lint_reading_chain(target_root)
    anchor_payload = lint_anchor_graph(target_root)
    errors = [*shape_payload["errors"], *chain_payload["errors"], *anchor_payload["errors"]]
    inspected = inspect_target(target_root)
    return {
        "status": "ok" if not errors else "error",
        "target_root": str(target_root),
        "detected_skill_mode": inspected["detected_skill_mode"],
        "shape_kind": inspected["shape_kind"],
        "checks": {
            "root_shape": shape_payload,
            "reading_chain": chain_payload,
            "anchor_graph": anchor_payload,
        },
        "errors": errors,
    }
