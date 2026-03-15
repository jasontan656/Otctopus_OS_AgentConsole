#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import TypedDict

import yaml

from skill_blueprints import GUIDE_WITH_TOOL_MODE, SKILL_MODE_CHOICES, runtime_contract_payload

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent


class TextAssetPayload(TypedDict):
    status: str
    asset: str
    path: str
    content: str


def emit(payload: object, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if isinstance(payload, dict):
        for key, value in payload.items():
            print(f"{key}: {value}")
        return 0
    print(payload)
    return 0


def text_payload(path: Path, asset_name: str) -> TextAssetPayload:
    return {
        "status": "ok",
        "asset": asset_name,
        "path": str(path),
        "content": path.read_text(encoding="utf-8"),
    }


def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, object], str]:
    text = markdown_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    payload = yaml.safe_load(text[4:closing]) or {}
    if not isinstance(payload, dict):
        payload = {}
    return payload, text[closing + 5 :]


def _chain(markdown_path: Path) -> list[dict[str, str]]:
    frontmatter, _ = _parse_frontmatter(markdown_path)
    if markdown_path.name == "SKILL.md":
        metadata = frontmatter.get("metadata")
        doc_structure = metadata.get("doc_structure", {}) if isinstance(metadata, dict) else {}
        raw = doc_structure.get("reading_chain")
    else:
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
            items.append(
                {
                    "key": key,
                    "target": target,
                    "hop": hop,
                    "reason": str(item.get("reason", "")),
                }
            )
    return items


def _title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def compile_context(entry: str, selection: list[str]) -> dict[str, object]:
    skill_md = SKILL_ROOT / "SKILL.md"
    root_items = _chain(skill_md)
    chosen = next((item for item in root_items if item["key"] == entry), None)
    if chosen is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "entry": entry,
            "available_entries": [item["key"] for item in root_items],
        }

    _frontmatter, skill_body = _parse_frontmatter(skill_md)
    segments = [{"source": "SKILL.md", "title": _title(skill_body), "content": skill_body.strip()}]
    resolved_chain = ["SKILL.md"]
    queue = list(selection)
    current = (skill_md.parent / chosen["target"]).resolve()

    while True:
        _frontmatter, body = _parse_frontmatter(current)
        relative = current.relative_to(SKILL_ROOT).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "title": _title(body), "content": body.strip()})
        items = _chain(current)
        if not items:
            break
        if len(items) > 1:
            if not queue:
                return {
                    "status": "branch_selection_required",
                    "entry": entry,
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": [item["key"] for item in items],
                    "current_source": relative,
                }
            wanted = queue.pop(0)
            chosen = next((item for item in items if item["key"] == wanted), None)
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


def cmd_create_skill_from_template(args: argparse.Namespace) -> int:
    cmd = [
        "python3",
        str(SCRIPT_DIR / "create_skill_from_template.py"),
        "--skill-name",
        args.skill_name,
        "--target-root",
        args.target_root,
        "--description",
        args.description,
    ]
    if args.skill_mode:
        cmd.extend(["--skill-mode", args.skill_mode])
    if args.overwrite:
        cmd.append("--overwrite")
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "create_skill_from_template failed")
    print(completed.stdout.strip())
    return 0


def cmd_guide_only_template(args: argparse.Namespace) -> int:
    return emit(text_payload(SKILL_ROOT / "path" / "template_creation" / "guide_only" / "12_TEMPLATE.md", "guide_only_template"), args.json)


def cmd_guide_with_tool_template(args: argparse.Namespace) -> int:
    return emit(text_payload(SKILL_ROOT / "path" / "template_creation" / "guide_with_tool" / "12_TEMPLATE.md", "guide_with_tool_template"), args.json)


def cmd_executable_workflow_template(args: argparse.Namespace) -> int:
    return emit(text_payload(SKILL_ROOT / "path" / "template_creation" / "executable_workflow_skill" / "12_TEMPLATE.md", "executable_workflow_template"), args.json)


def cmd_template_registry(args: argparse.Namespace) -> int:
    return emit(text_payload(SKILL_ROOT / "path" / "maintenance" / "template_registry" / "00_TEMPLATE_REGISTRY.md", "template_registry"), args.json)


def cmd_runtime_contract(args: argparse.Namespace) -> int:
    return emit(runtime_contract_payload("SkillsManager-Creation-Template", GUIDE_WITH_TOOL_MODE), args.json)


def cmd_read_path_context(args: argparse.Namespace) -> int:
    selection = [item.strip() for item in args.selection.split(",") if item.strip()]
    return emit(compile_context(args.entry, selection), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Creation-Template unified toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_skill = subparsers.add_parser("create-skill-from-template")
    create_skill.add_argument("--skill-name", required=True)
    create_skill.add_argument("--target-root", required=True)
    create_skill.add_argument("--description", default="")
    create_skill.add_argument("--skill-mode", choices=SKILL_MODE_CHOICES)
    create_skill.add_argument("--overwrite", action="store_true")
    create_skill.set_defaults(func=cmd_create_skill_from_template)

    for name, func in (
        ("guide-only-template", cmd_guide_only_template),
        ("guide-with-tool-template", cmd_guide_with_tool_template),
        ("executable-workflow-template", cmd_executable_workflow_template),
        ("skill-template", cmd_guide_with_tool_template),
        ("staged-skill-template", cmd_executable_workflow_template),
        ("template-registry", cmd_template_registry),
        ("runtime-contract", cmd_runtime_contract),
    ):
        sub = subparsers.add_parser(name)
        sub.add_argument("--json", action="store_true")
        sub.set_defaults(func=func)

    read_context = subparsers.add_parser("read-path-context")
    read_context.add_argument("--entry", required=True)
    read_context.add_argument("--selection", default="")
    read_context.add_argument("--json", action="store_true")
    read_context.set_defaults(func=cmd_read_path_context)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
