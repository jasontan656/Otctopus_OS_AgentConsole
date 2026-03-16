from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from doc_models import TargetProfile


def _parse_frontmatter(markdown_path: Path) -> dict[str, Any]:
    if not markdown_path.is_file():
        return {}
    text = markdown_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}
    payload = yaml.safe_load(text[4:closing]) or {}
    return payload if isinstance(payload, dict) else {}


def detect_profile(target_root: Path) -> TargetProfile:
    frontmatter = _parse_frontmatter(target_root / "SKILL.md")
    metadata = frontmatter.get("metadata")
    if isinstance(metadata, dict):
        skill_profile = metadata.get("skill_profile")
        if isinstance(skill_profile, dict):
            doc_topology = skill_profile.get("doc_topology")
            tooling_surface = skill_profile.get("tooling_surface")
            workflow_control = skill_profile.get("workflow_control")
            if all(isinstance(value, str) for value in (doc_topology, tooling_surface, workflow_control)):
                return TargetProfile(doc_topology, tooling_surface, workflow_control, "metadata.skill_profile")

    has_path = (target_root / "path").is_dir() and any((target_root / "path").rglob("00_*.md"))
    has_references = (target_root / "references").is_dir()
    has_scripts = (target_root / "scripts").is_dir()
    doc_topology = "workflow_path" if has_path else "referenced" if has_references else "inline"
    tooling_surface = "none"
    if has_scripts:
        cli_path = target_root / "scripts" / "Cli_Toolbox.py"
        runtime_contract = target_root / "references" / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT.json"
        tooling_surface = "contract_cli" if cli_path.is_file() and runtime_contract.is_file() else "automation_cli"
    workflow_control = "compiled" if doc_topology == "workflow_path" else "guardrailed" if doc_topology == "referenced" else "advisory"
    return TargetProfile(doc_topology, tooling_surface, workflow_control, "filesystem_inference")
