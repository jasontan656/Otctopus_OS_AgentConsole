from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from governed_type_registry import governed_type_definition
from runstate_models import InspectPayload, ProfilePayload


RUNSTATE_CONTRACT_PATH = Path("references/runstates/RUNSTATE_METHOD_CONTRACT.json")
ORCHESTRATOR_MARKERS = [
    "下游治理链",
    "必须显式应用",
    "显式启用相关治理技能",
    "技能编排",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, Any], str]:
    text = _read_text(markdown_path)
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    payload = yaml.safe_load(text[4:closing]) or {}
    if not isinstance(payload, dict):
        return {}, text
    return payload, text[closing + 5 :]


def _detect_profile(target_root: Path) -> ProfilePayload:
    skill_md = target_root / "SKILL.md"
    frontmatter, _body = _parse_frontmatter(skill_md)
    metadata = frontmatter.get("metadata", {})
    if isinstance(metadata, dict):
        profile = metadata.get("skill_profile", {})
        if isinstance(profile, dict):
            doc_topology = profile.get("doc_topology")
            tooling_surface = profile.get("tooling_surface")
            workflow_control = profile.get("workflow_control")
            if all(isinstance(value, str) for value in (doc_topology, tooling_surface, workflow_control)):
                return {
                    "doc_topology": doc_topology,
                    "tooling_surface": tooling_surface,
                    "workflow_control": workflow_control,
                }
    return {
        "doc_topology": "workflow_path" if (target_root / "path").exists() else "referenced" if (target_root / "references").exists() else "inline",
        "tooling_surface": "automation_cli" if (target_root / "scripts" / "Cli_Toolbox.py").exists() else "none",
        "workflow_control": "compiled" if (target_root / "path").exists() else "guardrailed" if (target_root / "references").exists() else "advisory",
    }


def _read_runstate_contract(target_root: Path) -> dict[str, Any] | None:
    path = target_root / RUNSTATE_CONTRACT_PATH
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _combined_markdown_text(target_root: Path) -> str:
    parts: list[str] = []
    for markdown_path in sorted(target_root.rglob("*.md")):
        try:
            parts.append(_read_text(markdown_path))
        except OSError:
            continue
    return "\n".join(parts)


def inspect_target(target_root: Path) -> InspectPayload:
    target_root = target_root.resolve()
    skill_md = target_root / "SKILL.md"
    if not skill_md.exists():
        return {
            "status": "error",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "profile": {"doc_topology": "inline", "tooling_surface": "none", "workflow_control": "advisory"},
            "governed_type": "not_applicable",
            "applicability": "not_applicable",
            "detection_source": "missing_skill_md",
            "reasons": ["SKILL.md is missing under the target root."],
            "required_checklists": [],
            "template_files": [],
            "success_criteria": [],
        }
    profile = _detect_profile(target_root)
    reasons: list[str] = []
    explicit_contract = _read_runstate_contract(target_root)
    if explicit_contract is not None:
        governed_type = explicit_contract.get("governed_type")
        if isinstance(governed_type, str) and governed_type in {"not_applicable", "workflow_runtime", "skill_flow_orchestrator"}:
            definition = governed_type_definition(governed_type)
            reasons.append("Existing RUNSTATE_METHOD_CONTRACT.json provides the governed_type.")
            return {
                "status": "ok",
                "target_skill_root": str(target_root),
                "skill_name": target_root.name,
                "profile": profile,
                "governed_type": governed_type,
                "applicability": definition["applicability"],
                "detection_source": "explicit_runstate_contract",
                "reasons": reasons,
                "required_checklists": definition["required_checklists"],
                "template_files": definition["template_files"],
                "success_criteria": definition["success_criteria"],
            }

    if profile["doc_topology"] != "workflow_path":
        definition = governed_type_definition("not_applicable")
        reasons.append("The target skill is not workflow_path and is treated as not workflow-bearing.")
        return {
            "status": "ok",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "profile": profile,
            "governed_type": "not_applicable",
            "applicability": definition["applicability"],
            "detection_source": "profile_inference",
            "reasons": reasons,
            "required_checklists": definition["required_checklists"],
            "template_files": definition["template_files"],
            "success_criteria": definition["success_criteria"],
        }

    combined_text = _combined_markdown_text(target_root)
    skill_name_mentions = re.findall(r"`([A-Za-z0-9_.-]+-[A-Za-z0-9_.-]+)`", combined_text)
    if any(marker in combined_text for marker in ORCHESTRATOR_MARKERS) or len({name for name in skill_name_mentions if "-" in name}) >= 3:
        definition = governed_type_definition("skill_flow_orchestrator")
        reasons.append("Workflow-bearing target also shows downstream skill orchestration markers.")
        detection_source = "workflow_plus_orchestration_markers"
        governed_type = "skill_flow_orchestrator"
    else:
        definition = governed_type_definition("workflow_runtime")
        reasons.append("Workflow-bearing target does not show stable skill-flow orchestration markers.")
        detection_source = "workflow_profile_inference"
        governed_type = "workflow_runtime"
    return {
        "status": "ok",
        "target_skill_root": str(target_root),
        "skill_name": target_root.name,
        "profile": profile,
        "governed_type": governed_type,
        "applicability": definition["applicability"],
        "detection_source": detection_source,
        "reasons": reasons,
        "required_checklists": definition["required_checklists"],
        "template_files": definition["template_files"],
        "success_criteria": definition["success_criteria"],
    }
