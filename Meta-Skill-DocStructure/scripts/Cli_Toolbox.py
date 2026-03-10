#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_CONTRACT_PATH = SKILL_ROOT / "references" / "runtime" / "SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json"
MATRIX_PATH = SKILL_ROOT / "assets" / "runtime" / "anchor_query_matrix.json"
SELF_GRAPH_PATH = SKILL_ROOT / "assets" / "runtime" / "self_anchor_graph.json"
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


class DocStructureError(Exception):
    pass


def emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for key, value in payload.items():
        if isinstance(value, (dict, list)):
            print(f"{key}:")
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            print(f"{key}: {value}")
    return 0


def ensure_skill_root(path: Path) -> Path:
    resolved = path.resolve()
    if not (resolved / "SKILL.md").exists():
        raise DocStructureError(f"target is not a skill root: {resolved}")
    return resolved


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DocStructureError(f"missing json file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DocStructureError(f"invalid json file: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DocStructureError(f"json payload must be an object: {path}")
    return payload


def collect_markdown_docs(target_root: Path) -> list[Path]:
    return sorted(
        path
        for path in target_root.rglob("*.md")
        if ".git" not in path.parts and "Codex_Skill_Runtime" not in path.parts
    )


def parse_frontmatter(doc_path: Path) -> tuple[dict[str, Any], str]:
    text = doc_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise DocStructureError(f"missing frontmatter: {doc_path}")
    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise DocStructureError(f"invalid frontmatter yaml: {doc_path}: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise DocStructureError(f"frontmatter must be a yaml object: {doc_path}")
    return frontmatter, text[match.end():]


def extract_heading(body: str, doc_path: Path) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return doc_path.stem


def extract_doc_contract(doc_path: Path, frontmatter: dict[str, Any]) -> dict[str, Any]:
    if doc_path.name == "SKILL.md":
        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict):
            raise DocStructureError(f"SKILL.md metadata must be a dict: {doc_path}")
        contract = metadata.get("doc_structure")
    else:
        contract = frontmatter
    if not isinstance(contract, dict):
        raise DocStructureError(f"missing doc structure contract: {doc_path}")

    required_fields = ("doc_id", "doc_type", "topic", "anchors")
    for field in required_fields:
        if field not in contract:
            raise DocStructureError(f"missing '{field}' in {doc_path}")

    anchors = contract["anchors"]
    if not isinstance(anchors, list) or not anchors:
        raise DocStructureError(f"anchors must be a non-empty list in {doc_path}")

    topic = contract["topic"]
    if not isinstance(topic, str) or not topic.strip():
        raise DocStructureError(f"topic must be a non-empty string in {doc_path}")

    return {
        "doc_id": contract["doc_id"],
        "doc_type": contract["doc_type"],
        "topic": topic.strip(),
        "anchors": anchors,
    }


def normalize_anchor_target(doc_path: Path, raw_target: str, target_root: Path) -> str:
    target = (doc_path.parent / raw_target).resolve()
    try:
        relative = target.relative_to(target_root.resolve())
    except ValueError as exc:
        raise DocStructureError(f"anchor target escapes skill root: {doc_path} -> {raw_target}") from exc
    if not target.exists():
        raise DocStructureError(f"anchor target does not exist: {doc_path} -> {raw_target}")
    if target.suffix.lower() != ".md":
        raise DocStructureError(f"anchor target must be markdown: {doc_path} -> {raw_target}")
    return relative.as_posix()


def apply_split_rules(title: str, body: str, doc_path: Path, matrix: dict[str, Any]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for rule in matrix.get("split_keyword_rules", []):
        scope = rule.get("scope")
        haystack = title if scope == "title" else body
        keywords = rule.get("keywords", [])
        hits = 0
        lowered = haystack.casefold()
        for keyword in keywords:
            if str(keyword).casefold() in lowered:
                hits += 1
        threshold = int(rule.get("threshold", 1))
        if hits >= threshold:
            warnings.append(
                {
                    "doc": doc_path.as_posix(),
                    "rule_id": rule.get("rule_id"),
                    "severity": rule.get("severity", "warn"),
                    "message": rule.get("message", "split signal matched"),
                    "hits": hits,
                }
            )
    return warnings


def build_anchor_graph(target_root: Path) -> dict[str, Any]:
    skill_root = ensure_skill_root(target_root)
    matrix = load_json(MATRIX_PATH)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []

    for doc_path in collect_markdown_docs(skill_root):
        relative_path = doc_path.relative_to(skill_root).as_posix()
        try:
            frontmatter, body = parse_frontmatter(doc_path)
            contract = extract_doc_contract(doc_path, frontmatter)
            title = extract_heading(body, doc_path)
            record = {
                "path": relative_path,
                "title": title,
                "body": body,
                **contract,
            }
            records.append(record)
            nodes.append(
                {
                    "path": relative_path,
                    "doc_id": contract["doc_id"],
                    "doc_type": contract["doc_type"],
                    "topic": contract["topic"],
                    "title": title,
                    "anchor_count": len(contract["anchors"]),
                }
            )
            warnings.extend(apply_split_rules(title, body, Path(relative_path), matrix))
        except DocStructureError as exc:
            errors.append({"doc": relative_path, "error": str(exc)})

    for record in records:
        source_path = record["path"]
        source_doc_path = skill_root / source_path
        for anchor in record["anchors"]:
            if not isinstance(anchor, dict):
                errors.append({"doc": source_path, "error": "anchor entry must be an object"})
                continue
            missing = [
                field
                for field in matrix.get("required_anchor_fields", [])
                if field not in anchor or not str(anchor[field]).strip()
            ]
            if missing:
                errors.append(
                    {
                        "doc": source_path,
                        "error": f"anchor missing fields: {', '.join(missing)}",
                    }
                )
                continue
            direction = str(anchor["direction"]).strip()
            if direction not in matrix.get("allowed_directions", []):
                errors.append(
                    {
                        "doc": source_path,
                        "error": f"invalid anchor direction: {direction}",
                    }
                )
                continue
            try:
                target_path = normalize_anchor_target(
                    source_doc_path,
                    str(anchor["target"]).strip(),
                    skill_root,
                )
            except DocStructureError as exc:
                errors.append({"doc": source_path, "error": str(exc)})
                continue
            edges.append(
                {
                    "source": source_path,
                    "target": target_path,
                    "relation": str(anchor["relation"]).strip(),
                    "direction": direction,
                    "reason": str(anchor["reason"]).strip(),
                }
            )

    status = "fail" if errors else "pass"
    if not errors and warnings:
        status = "pass_with_warnings"

    return {
        "status": status,
        "target_root": str(skill_root),
        "matrix_path": str(MATRIX_PATH),
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "error_count": len(errors),
            "warning_count": len(warnings),
        },
        "nodes": nodes,
        "edges": edges,
        "errors": errors,
        "warnings": warnings,
    }


def cmd_runtime_contract(args: argparse.Namespace) -> int:
    contract = load_json(RUNTIME_CONTRACT_PATH)
    return emit(contract, args.json)


def cmd_build_anchor_graph(args: argparse.Namespace) -> int:
    payload = build_anchor_graph(Path(args.target))
    return emit(payload, args.json)


def cmd_lint_doc_anchors(args: argparse.Namespace) -> int:
    payload = build_anchor_graph(Path(args.target))
    emit(payload, args.json)
    return 1 if payload["status"] == "fail" else 0


def cmd_rebuild_self_graph(args: argparse.Namespace) -> int:
    payload = build_anchor_graph(SKILL_ROOT)
    if payload["status"] == "fail":
        emit(payload, args.json)
        return 1
    SELF_GRAPH_PATH.write_text(json.dumps(
        {
            "graph_name": "META_SKILL_DOCSTRUCTURE_SELF_ANCHOR_GRAPH",
            "graph_version": "v1",
            "source_skill": "Meta-Skill-DocStructure",
            "summary": payload["summary"],
            "nodes": payload["nodes"],
            "edges": payload["edges"],
            "warnings": payload["warnings"],
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n", encoding="utf-8")
    result = {
        "status": "written",
        "written_graph_path": str(SELF_GRAPH_PATH),
        "summary": payload["summary"],
        "warnings": payload["warnings"],
    }
    return emit(result, args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meta-Skill-DocStructure toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    runtime_contract = subparsers.add_parser("runtime-contract")
    runtime_contract.add_argument("--json", action="store_true")
    runtime_contract.set_defaults(func=cmd_runtime_contract)

    build_graph = subparsers.add_parser("build-anchor-graph")
    build_graph.add_argument("--target", required=True)
    build_graph.add_argument("--json", action="store_true")
    build_graph.set_defaults(func=cmd_build_anchor_graph)

    lint = subparsers.add_parser("lint-doc-anchors")
    lint.add_argument("--target", required=True)
    lint.add_argument("--json", action="store_true")
    lint.set_defaults(func=cmd_lint_doc_anchors)

    rebuild = subparsers.add_parser("rebuild-self-graph")
    rebuild.add_argument("--json", action="store_true")
    rebuild.set_defaults(func=cmd_rebuild_self_graph)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except DocStructureError as exc:
        payload = {"status": "error", "error": str(exc)}
        if getattr(args, "json", False):
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
