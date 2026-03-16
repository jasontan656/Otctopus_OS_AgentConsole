#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re

from filter_prompt_shape_helper import collect_context_session_refs

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
    session_context_refs = collect_context_session_refs(raw_text)
    session_context_detected = bool(session_context_refs)
    directives: list[str] = []
    resolved_skills: list[dict[str, object]] = []
    missing: list[str] = []
    for skill_name in skill_names:
        skill_file = resolve_skill_file(skill_name)
        if skill_file is None:
            missing.append(skill_name)
            continue
        purpose = (
            f"explicitly requested handling for `{intent_summary}`"
            if skill_name != DEFAULT_SKILL_NAME
            else f"intent clarification for `{intent_summary}`"
        )
        contract_command = toolbox_command(skill_name, "contract")
        intent_clarify_command = toolbox_command(skill_name, "directive --topic intent-clarify")
        active_invoke_command = toolbox_command(skill_name, "directive --topic active-invoke")
        session_context_directive_command = toolbox_command(skill_name, "directive --topic session-context-read")
        output_governance_command = toolbox_command(skill_name, "directive --topic output-governance")
        session_context_commands = [
            toolbox_command(
                skill_name,
                f"read-session-context --lookup-key {ref['kind']}_id --lookup-id {ref['id']}",
            )
            for ref in session_context_refs
        ]
        directives.append(
            "\n".join(
                [
                    f"call `{contract_command}` for {purpose}.",
                    "then continue with the runtime payload instead of reading SKILL.md as the primary source:",
                    *(
                        [
                            f"- pre-read workflow: `{session_context_directive_command}`",
                            *[f"- pre-read chat context now: `{command}`" for command in session_context_commands],
                            "- use the returned `focused_chat.user_prompt` + `focused_chat.assistant_reply` as context before continuing",
                        ]
                        if session_context_detected and skill_name == DEFAULT_SKILL_NAME
                        else []
                    ),
                    f"- canonical workflow: `{intent_clarify_command}`",
                    f"- runtime/result governance: `{output_governance_command}`",
                    f"- legacy alias only: `{active_invoke_command}`",
                    *(
                        ["- if the caller also provides `codex/session/resume id`, treat that id as pre-read context and not as part of the prompt that should be strengthened"]
                        if session_context_detected and skill_name == DEFAULT_SKILL_NAME
                        else []
                    ),
                ]
            )
        )
        resolved_skills.append(
            {
                "skill_name": skill_name,
                "skill_file": str(skill_file),
                "purpose": purpose,
                "contract_command": contract_command,
                "session_context_directive_command": session_context_directive_command,
                "intent_clarify_command": intent_clarify_command,
                "active_invoke_command": active_invoke_command,
                "output_governance_command": output_governance_command,
                "session_context_commands": session_context_commands,
                "session_context_policy": (
                    "when codex/session/resume id is present, call read-session-context first and treat the returned chat as pre-read context; do not strengthen the id-reading instruction itself"
                    if skill_name == DEFAULT_SKILL_NAME
                    else ""
                ),
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
        "session_context_detected": session_context_detected,
        "session_context_refs": session_context_refs,
        "resolved_skills": resolved_skills,
        "final_skill_read_directive": "\n\n".join(directives).strip() + "\n",
    }
