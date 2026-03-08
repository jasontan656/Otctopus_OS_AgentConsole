from __future__ import annotations

import json
from pathlib import Path


STAGES = ("scan", "collect", "push")


def runtime_contract_json_path(skill_root: Path) -> Path:
    return skill_root / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.json"


def runtime_contract_md_path(skill_root: Path) -> Path:
    return skill_root / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.md"


def stage_directive_json_path(skill_root: Path, stage: str) -> Path:
    return skill_root / "references" / "stages" / stage / "DIRECTIVE.json"


def stage_instruction_md_path(skill_root: Path, stage: str) -> Path:
    return skill_root / "references" / "stages" / stage / "INSTRUCTION.md"


def stage_workflow_md_path(skill_root: Path, stage: str) -> Path:
    return skill_root / "references" / "stages" / stage / "WORKFLOW.md"


def stage_rules_md_path(skill_root: Path, stage: str) -> Path:
    return skill_root / "references" / "stages" / stage / "RULES.md"


def _load_json(path: Path, label: str) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"{label} missing: {path}")
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ValueError(f"{label} file is empty: {path}")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return payload


def load_runtime_contract(skill_root: Path) -> dict[str, object]:
    payload = _load_json(runtime_contract_json_path(skill_root), "runtime contract")
    if not payload.get("skill_name"):
        raise ValueError("runtime contract missing skill_name")
    return payload


def load_stage_directive(skill_root: Path, stage: str) -> dict[str, object]:
    if stage not in STAGES:
        raise ValueError(f"unsupported stage: {stage}")
    payload = _load_json(stage_directive_json_path(skill_root, stage), f"{stage} directive")
    if payload.get("stage") != stage:
        raise ValueError(f"{stage} directive stage mismatch")
    return payload


def _render_bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def _render_numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, start=1)]


def _render_runtime_contract_md(payload: dict[str, object]) -> str:
    lines = [
        "# Skill Runtime Contract",
        "",
        "> Audit copy generated from `references/runtime/SKILL_RUNTIME_CONTRACT.json`.",
        "> Runtime models must call `python3 scripts/Cli_Toolbox.py contract --json` instead of reading this markdown for guidance.",
        "",
        f"- skill_name: `{payload['skill_name']}`",
        f"- version: `{payload['version']}`",
        f"- description: {payload['description']}",
        "",
        "## Runtime Access Policy",
    ]
    access_policy = payload.get("runtime_access_policy", {})
    lines.extend(_render_bullets([f"{key}: `{value}`" for key, value in access_policy.items()]))
    lines.extend(["", "## Command Map"])
    command_map = payload.get("command_map", {})
    lines.extend(_render_bullets([f"`{name}`: {description}" for name, description in command_map.items()]))
    lines.extend(["", "## Sync Policy"])
    sync_policy = payload.get("sync_policy", {})
    lines.extend(_render_bullets([f"{key}: {value}" for key, value in sync_policy.items()]))
    return "\n".join(lines) + "\n"


def _render_stage_instruction_md(stage_payload: dict[str, object]) -> str:
    stage = str(stage_payload["stage"])
    lines = [
        f"# {stage.capitalize()} Instruction",
        "",
        f"> Audit copy generated from `references/stages/{stage}/DIRECTIVE.json`.",
        f"> Runtime models must call `python3 scripts/Cli_Toolbox.py directive --stage {stage} --json` instead of reading this markdown for guidance.",
        "",
    ]
    lines.extend(_render_bullets([str(item) for item in stage_payload.get("instruction", [])]))
    return "\n".join(lines) + "\n"


def _render_stage_workflow_md(stage_payload: dict[str, object]) -> str:
    lines = [f"# {str(stage_payload['stage']).capitalize()} Workflow", ""]
    lines.extend(_render_numbered([str(item) for item in stage_payload.get("workflow", [])]))
    return "\n".join(lines) + "\n"


def _render_stage_rules_md(stage_payload: dict[str, object]) -> str:
    lines = [f"# {str(stage_payload['stage']).capitalize()} Rules", ""]
    lines.extend(_render_bullets([str(item) for item in stage_payload.get("rules", [])]))
    return "\n".join(lines) + "\n"


def render_audit_docs(skill_root: Path) -> dict[str, object]:
    runtime_payload = load_runtime_contract(skill_root)
    runtime_md_target = runtime_contract_md_path(skill_root)
    runtime_md_target.parent.mkdir(parents=True, exist_ok=True)
    runtime_md_target.write_text(_render_runtime_contract_md(runtime_payload), encoding="utf-8")

    written_files = [str(runtime_md_target)]
    for stage in STAGES:
        payload = load_stage_directive(skill_root, stage)
        for path, text in (
            (stage_instruction_md_path(skill_root, stage), _render_stage_instruction_md(payload)),
            (stage_workflow_md_path(skill_root, stage), _render_stage_workflow_md(payload)),
            (stage_rules_md_path(skill_root, stage), _render_stage_rules_md(payload)),
        ):
            path.write_text(text, encoding="utf-8")
            written_files.append(str(path))

    return {
        "status": "ok",
        "action": "render_audit_docs",
        "count": len(written_files),
        "entries": written_files,
    }
