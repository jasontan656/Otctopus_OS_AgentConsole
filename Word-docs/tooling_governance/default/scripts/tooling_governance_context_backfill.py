#!/usr/bin/env python3
"""Context-aware autofill for governance instance docs and structured runtime files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

import mstg_yaml as yaml


PLACEHOLDER_LINE = re.compile(r"(?m)^- replace_me$")


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_yaml(path: Path) -> Any:
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_yaml(path: Path, payload: Any) -> None:
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def scan_target_stats(target_skill_dir: Path) -> dict[str, Any]:
    scripts = sorted(p for p in (target_skill_dir / "scripts").rglob("*") if p.is_file()) if (target_skill_dir / "scripts").is_dir() else []
    script_files = [p for p in scripts if p.suffix.lower() in {".py", ".sh"}]
    md_files = sorted(p for p in target_skill_dir.rglob("*.md") if p.is_file())
    return {
        "target_skill_dir": str(target_skill_dir),
        "script_count": len(script_files),
        "script_examples": [str(p.relative_to(target_skill_dir)).replace("\\", "/") for p in script_files[:12]],
        "markdown_count": len(md_files),
        "has_skill_md": (target_skill_dir / "SKILL.md").is_file(),
    }


def replace_placeholders(text: str, replacements: list[str], fallback: str) -> tuple[str, int]:
    replaced = 0
    for row in replacements:
        if not PLACEHOLDER_LINE.search(text):
            break
        text = PLACEHOLDER_LINE.sub(f"- {row}", text, count=1)
        replaced += 1
    while PLACEHOLDER_LINE.search(text):
        text = PLACEHOLDER_LINE.sub(f"- {fallback}", text, count=1)
        replaced += 1
    return text, replaced


def doc_replacements(
    *,
    managed_skill: str,
    target_skill_dir: Path,
    instance_name: str,
    stats: dict[str, Any],
) -> dict[str, list[str]]:
    tg = str(target_skill_dir)
    toolbox_dir = f"tooling_governance/{instance_name}/scripts"
    return {
        "L1/README.md": [
            f"governance toolbox scripts are injected under tooling_governance/{instance_name}/scripts and coexist with target scripts.",
            "L1 must keep one parent milestone chain one document under docs/L1/chains/*.md.",
        ],
        "L2/README.md": [
            "tool registry, structured docs, ledger, and state must stay synchronized by tool_id and event_id.",
            "L2 must split each L1 chain into an independent chain packet doc under docs/L2/chains/<chain>/README.md.",
        ],
        "L3/README.md": [
            "reuse shared tooling runtime when possible and avoid creating parallel bespoke dependencies.",
        ],
        "L4/README.md": [
            "default policy: governance toolbox scripts do not require secrets; use explicit env vars only when human-approved.",
        ],
        "L5/README.md": [
            "state files are maintained under runtime/ with append-only ledger and timestamped status updates.",
        ],
        "L6/README.md": [
            f"mandatory change flow: docs_pre_update -> script_update -> ops_post_docs_update -> ledger_append -> full_gate_lint (includes target outcome lint) via {toolbox_dir}/tooling_governance_apply_change.py.",
        ],
        "L7/README.md": [
            "triage priority: parse gate output -> locate affected tool_id -> update structured docs -> rerun full gate.",
        ],
        "L8/README.md": [
            "record governance objective/process/result in governance_audit artifacts and include run_id in command output.",
        ],
        "L9/README.md": [
            f"minimum checks per change: tooling_governance_lint + mstg_l0_l13_full_gate_lint (with mstg_target_governance_outcome_lint) at {tg}/tooling_governance/{instance_name}.",
        ],
        "L10/README.md": [
            "each script-affecting change must append TOOL_CHANGE_LEDGER.jsonl with changed_paths and docs_updated.",
        ],
        "L11/README.md": [
            "operators should use the unified apply-change entrypoint and avoid direct script mutation without pre-doc update.",
        ],
        "L12/README.md": [
            "exceptions are human-approved only; default action is fix-forward until full gate PASS.",
        ],
        "L13/README.md": [
            f"release requires full gate PASS and traceable governance records for {managed_skill}.",
            f"target context snapshot: scripts={stats['script_count']} markdown={stats['markdown_count']} at {tg}.",
        ],
    }


def backfill_docs(
    *,
    instance_root: Path,
    managed_skill: str,
    target_skill_dir: Path,
    instance_name: str,
    stats: dict[str, Any],
) -> dict[str, Any]:
    docs_dir = instance_root / "docs"
    if not docs_dir.is_dir():
        return {"status": "FAIL", "error": "DOCS_DIR_MISSING", "docs_dir": str(docs_dir)}

    rep_map = doc_replacements(
        managed_skill=managed_skill,
        target_skill_dir=target_skill_dir,
        instance_name=instance_name,
        stats=stats,
    )
    touched: list[str] = []
    replaced_total = 0

    for doc_name, replacements in rep_map.items():
        doc = docs_dir / doc_name
        if not doc.is_file():
            continue
        before = doc.read_text(encoding="utf-8")
        after, count = replace_placeholders(
            before,
            replacements,
            f"context autofill: maintain governance docs for {managed_skill} with keyword-first replacement.",
        )
        if after != before:
            doc.write_text(after, encoding="utf-8")
            touched.append(str(doc))
        replaced_total += count

    return {
        "status": "PASS",
        "touched_doc_count": len(touched),
        "placeholder_replacements": replaced_total,
        "touched_docs": touched,
    }


def clean_placeholder_list(values: Any, fallback: list[str]) -> list[str]:
    if not isinstance(values, list):
        return fallback
    rows = [str(v).strip() for v in values if str(v).strip() and str(v).strip() != "replace_me"]
    return rows if rows else fallback


def infer_command(entrypoint: str) -> str:
    if entrypoint.endswith(".py"):
        return f"python3 {entrypoint} --help"
    if entrypoint.endswith(".sh"):
        return f"bash {entrypoint} --help"
    return entrypoint


def backfill_runtime_docs(
    *,
    instance_root: Path,
    managed_skill: str,
    instance_name: str,
) -> dict[str, Any]:
    runtime_dir = instance_root / "runtime"
    reg_path = runtime_dir / "TOOL_REGISTRY.yaml"
    docs_path = runtime_dir / "TOOL_DOCS_STRUCTURED.yaml"
    state_path = runtime_dir / "TOOLING_GOVERNANCE_STATE.yaml"

    reg = load_yaml(reg_path)
    docs = load_yaml(docs_path)
    if not isinstance(reg, dict) or not isinstance(docs, dict):
        return {"status": "FAIL", "error": "RUNTIME_DOCS_OR_REGISTRY_INVALID"}

    reg_tools = reg.get("tools", [])
    entrypoints: dict[str, str] = {}
    if isinstance(reg_tools, list):
        for row in reg_tools:
            if not isinstance(row, dict):
                continue
            tid = str(row.get("tool_id", "")).strip()
            ep = str(row.get("entrypoint", "")).strip()
            if tid:
                entrypoints[tid] = ep

    tools = docs.get("tools", [])
    if not isinstance(tools, list):
        return {"status": "FAIL", "error": "TOOL_DOCS_STRUCTURED_TOOLS_INVALID"}

    changed = 0
    for row in tools:
        if not isinstance(row, dict):
            continue
        tool_id = str(row.get("tool_id", "")).strip()
        if not tool_id:
            continue
        entrypoint = entrypoints.get(tool_id, "")
        usage = row.setdefault("usage", {})
        if not isinstance(usage, dict):
            usage = {}
            row["usage"] = usage

        summary = str(usage.get("summary", "")).strip()
        if not summary or summary == "replace_me":
            usage["summary"] = f"Autofilled governance tool contract for {tool_id}."
            changed += 1

        cmd_examples = clean_placeholder_list(usage.get("command_examples"), [infer_command(entrypoint) if entrypoint else f"python3 tooling_governance/{instance_name}/scripts/{tool_id}.py --help"])
        usage["command_examples"] = cmd_examples
        usage["inputs"] = clean_placeholder_list(usage.get("inputs"), ["structured args", "instance runtime context"])
        usage["outputs"] = clean_placeholder_list(usage.get("outputs"), ["json status payload", "runtime artifacts update"])

        mod = row.setdefault("modification", {})
        if not isinstance(mod, dict):
            mod = {}
            row["modification"] = mod
        workflow = clean_placeholder_list(
            mod.get("update_workflow"),
            ["docs_pre_update", "script_update", "ops_post_docs_update", "ledger_append", "full_gate_lint"],
        )
        mod["update_workflow"] = workflow
        mod["required_docs"] = clean_placeholder_list(
            mod.get("required_docs"),
            ["docs/L6/README.md", "docs/L11/README.md", "docs/L12/README.md", "docs/L1/chains", "docs/L2/chains"],
        )
        notes = mod.get("notes")
        if not isinstance(notes, list):
            mod["notes"] = []

        dev = row.setdefault("development", {})
        if not isinstance(dev, dict):
            dev = {}
            row["development"] = dev
        if not str(dev.get("owner", "")).strip():
            dev["owner"] = "ai_maintained"
        records = dev.get("records")
        if not isinstance(records, list):
            dev["records"] = []

    docs["managed_skill"] = managed_skill
    save_yaml(docs_path, docs)

    state = load_yaml(state_path)
    if not isinstance(state, dict):
        state = {}
    state["governance_status"] = "active"
    state["last_updated_at_utc"] = now_utc()
    state["last_changed_tool_id"] = state.get("last_changed_tool_id", "context_backfill")
    save_yaml(state_path, state)

    return {
        "status": "PASS",
        "docs_path": str(docs_path),
        "tool_count": len(tools),
        "changed_items": changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Context-aware backfill for tooling governance instance")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--target-skill-dir", required=True)
    parser.add_argument("--managed-skill", default="")
    parser.add_argument("--instance-name", default="default")
    args = parser.parse_args()

    instance_root = Path(args.instance_root).expanduser().resolve()
    target_skill_dir = Path(args.target_skill_dir).expanduser().resolve()
    managed_skill = args.managed_skill.strip() or target_skill_dir.name

    if not instance_root.is_dir():
        print(json.dumps({"status": "FAIL", "error": "INSTANCE_ROOT_NOT_FOUND", "instance_root": str(instance_root)}, ensure_ascii=False, indent=2))
        return 1
    if not target_skill_dir.is_dir():
        print(json.dumps({"status": "FAIL", "error": "TARGET_SKILL_DIR_NOT_FOUND", "target_skill_dir": str(target_skill_dir)}, ensure_ascii=False, indent=2))
        return 1

    stats = scan_target_stats(target_skill_dir)
    docs_result = backfill_docs(
        instance_root=instance_root,
        managed_skill=managed_skill,
        target_skill_dir=target_skill_dir,
        instance_name=args.instance_name,
        stats=stats,
    )
    runtime_result = backfill_runtime_docs(
        instance_root=instance_root,
        managed_skill=managed_skill,
        instance_name=args.instance_name,
    )

    ok = docs_result.get("status") == "PASS" and runtime_result.get("status") == "PASS"
    out = {
        "status": "PASS" if ok else "FAIL",
        "instance_root": str(instance_root),
        "target_skill_dir": str(target_skill_dir),
        "managed_skill": managed_skill,
        "target_stats": stats,
        "docs_backfill": docs_result,
        "runtime_backfill": runtime_result,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
