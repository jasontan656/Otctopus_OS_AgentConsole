#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re

EXIT_SUCCESS = 0
EXIT_INVALID_OUTPUT = 11
EXIT_EMPTY_AFTER_FILTER = 12
EXIT_SKILL_SOURCE_MISSING = 13
DEFAULT_SKILL_NAME = "Meta-Enhance-Prompt"


def sanitize_inline(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip()).strip()


def skills_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[2]


def toolbox_command(skill_name: str, command: str) -> str:
    return f"./.venv_backend_skills/bin/python Skills/{skill_name}/scripts/Cli_Toolbox.py {command} --json"


def extract_explicit_skill_names(text: str) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    patterns = [
        re.compile(r"\$([A-Za-z0-9][A-Za-z0-9._-]*)"),
        re.compile(r"<name>\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*</name>", flags=re.IGNORECASE),
    ]
    for pattern in patterns:
        for match in pattern.finditer(text):
            skill_name = str(match.group(1) or "").strip()
            if skill_name and skill_name not in seen:
                ordered.append(skill_name)
                seen.add(skill_name)
    return ordered


def resolve_skill_file(skill_name: str) -> pathlib.Path | None:
    normalized = str(skill_name or "").strip()
    if not normalized:
        return None
    root = skills_root()
    direct = (root / normalized / "SKILL.md").resolve()
    if direct.exists():
        return direct
    lowered = normalized.lower()
    for child in root.iterdir():
        if child.is_dir() and child.name.lower() == lowered:
            candidate = child / "SKILL.md"
            if candidate.exists():
                return candidate.resolve()
    return None


def summarize_intent(text: str, *, limit: int = 220) -> str:
    cleaned = sanitize_inline(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def build_skill_directive(raw_text: str) -> tuple[int, str, dict[str, object]]:
    intent_summary = summarize_intent(raw_text)
    if not intent_summary:
        return EXIT_EMPTY_AFTER_FILTER, "empty_after_filter", {}

    skill_names = extract_explicit_skill_names(raw_text) or [DEFAULT_SKILL_NAME]
    directives: list[str] = []
    resolved_skills: list[dict[str, str]] = []
    missing: list[str] = []
    for skill_name in skill_names:
        skill_file = resolve_skill_file(skill_name)
        if skill_file is None:
            missing.append(skill_name)
            continue
        purpose = (
            f"explicitly requested handling for `{intent_summary}`"
            if skill_name != DEFAULT_SKILL_NAME
            else f"prompt/instruction/workflow routing for `{intent_summary}`"
        )
        contract_command = toolbox_command(skill_name, "contract")
        active_invoke_command = toolbox_command(skill_name, "directive --topic active-invoke")
        output_governance_command = toolbox_command(skill_name, "directive --topic output-governance")
        directives.append(
            "\n".join(
                [
                    f"call `{contract_command}` for {purpose}.",
                    "then continue with the runtime payload instead of reading SKILL.md as the primary source:",
                    f"- `{active_invoke_command}`",
                    f"- `{output_governance_command}`",
                ]
            )
        )
        resolved_skills.append(
            {
                "skill_name": skill_name,
                "skill_file": str(skill_file),
                "purpose": purpose,
                "contract_command": contract_command,
                "active_invoke_command": active_invoke_command,
                "output_governance_command": output_governance_command,
            }
        )

    if missing:
        return EXIT_SKILL_SOURCE_MISSING, f"skill_source_missing: {', '.join(missing)}", {
            "intent_summary": intent_summary,
            "missing_skills": missing,
        }
    if not directives:
        return EXIT_INVALID_OUTPUT, "invalid_output: no_skill_directive_generated", {}
    return EXIT_SUCCESS, "success_skill_directive", {
        "intent_summary": intent_summary,
        "resolved_skills": resolved_skills,
        "final_skill_read_directive": "\n\n".join(directives).strip() + "\n",
    }
