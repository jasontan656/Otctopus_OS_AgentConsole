#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re

EXIT_TEMPLATE_MISSING = 10

FORBIDDEN_TOKENS = [
    "[ACTIVATION]",
    "[IMPACT_MATRIX]",
    "[FAILURE_MODES_AND_ROLLBACK]",
    "[MINIMUM_VALIDATION_PATH]",
    "[RECOMMENDATION]",
    "methodology_mode",
    "active_invoke_edit_mode",
    "mode_priority_applied",
    "风险矩阵",
    "复盘说明",
]

DEFAULT_TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "references" / "templates" / "active_invoke_prompt_template_v1.txt"
SECTION_ALIASES = {
    "goal": {"goal", "目标"},
    "repo_context": {"repo_context_and_impact", "repo_context", "repo context", "repo context and impact", "仓库上下文", "影响面", "覆盖面"},
    "inputs": {"inputs", "input", "输入"},
    "outputs": {"outputs", "output", "输出"},
    "boundaries": {"boundaries", "boundary", "constraints", "边界", "约束"},
    "validation": {"validation", "acceptance", "acceptance checks", "验证", "验收"},
}
DEFAULT_LINES = {
    "repo_context": ["- Survey the current repo and state the affected surfaces before execution."],
    "inputs": ["- User request", "- Relevant repository context and affected files"],
    "outputs": ["- A concrete task result aligned with the user goal"],
    "boundaries": ["- Preserve the user's real goal", "- Do not invent unrelated scope", "- Respect repository boundaries and existing contracts"],
    "validation": ["- Output matches the stated goal", "- Output is consistent with repository evidence", "- Acceptance can be checked directly"],
}


def sanitize_inline(text: str) -> str:
    cleaned = str(text or "").strip()
    for token in FORBIDDEN_TOKENS:
        cleaned = re.sub(re.escape(token), "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip()


def _normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _section_key(header: str) -> str:
    normalized = _normalize_header(header)
    for canonical, aliases in SECTION_ALIASES.items():
        if any(normalized == _normalize_header(alias) for alias in aliases):
            return canonical
    return ""


def parse_contract_sections(text: str) -> dict[str, list[str] | str]:
    sections: dict[str, list[str] | str] = {"goal": "", "repo_context": [], "inputs": [], "outputs": [], "boundaries": [], "validation": []}
    current = ""
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        header_match = re.match(r"^([A-Za-z_ /&\-]+|[\u4e00-\u9fff]+)\s*:\s*(.*)$", stripped)
        if header_match:
            key = _section_key(str(header_match.group(1) or "").strip())
            remainder = sanitize_inline(str(header_match.group(2) or ""))
            if key:
                current = key
                if key == "goal":
                    sections["goal"] = remainder
                elif remainder:
                    sections[key].append(f"- {remainder}")  # type: ignore[index]
                continue
        bullet_match = re.match(r"^[-*]\s+(.+)$", stripped)
        cleaned = sanitize_inline(bullet_match.group(1) if bullet_match else stripped)
        if not cleaned:
            continue
        if current == "goal":
            goal = str(sections["goal"] or "").strip()
            sections["goal"] = f"{goal} {cleaned}".strip() if goal else cleaned
        elif current:
            sections[current].append(f"- {cleaned}")  # type: ignore[index]
    if not str(sections["goal"] or "").strip():
        sections["goal"] = sanitize_inline(text)
    for key, default_lines in DEFAULT_LINES.items():
        if not sections[key]:
            sections[key] = list(default_lines)
    return sections


def load_template(template_file: pathlib.Path) -> str:
    if not template_file.exists():
        raise FileNotFoundError(str(template_file))
    template = template_file.read_text(encoding="utf-8")
    required = ["{{GOAL}}", "{{REPO_CONTEXT_LINES}}", "{{INPUT_LINES}}", "{{OUTPUT_LINES}}", "{{BOUNDARY_LINES}}", "{{VALIDATION_LINES}}"]
    if not all(token in template for token in required):
        raise ValueError("template_missing_required_tokens")
    return template


def render_contract(template: str, sections: dict[str, list[str] | str]) -> str:
    rendered = template.replace("{{GOAL}}", str(sections["goal"]).strip())
    rendered = rendered.replace("{{REPO_CONTEXT_LINES}}", "\n".join(sections["repo_context"]))  # type: ignore[arg-type]
    rendered = rendered.replace("{{INPUT_LINES}}", "\n".join(sections["inputs"]))  # type: ignore[arg-type]
    rendered = rendered.replace("{{OUTPUT_LINES}}", "\n".join(sections["outputs"]))  # type: ignore[arg-type]
    rendered = rendered.replace("{{BOUNDARY_LINES}}", "\n".join(sections["boundaries"]))  # type: ignore[arg-type]
    rendered = rendered.replace("{{VALIDATION_LINES}}", "\n".join(sections["validation"]))  # type: ignore[arg-type]
    return rendered.strip() + "\n"


def validate_final_shape(text: str) -> bool:
    required = ["GOAL:", "REPO_CONTEXT_AND_IMPACT:", "INPUTS:", "OUTPUTS:", "BOUNDARIES:", "VALIDATION:"]
    lowered = text.lower()
    return all(header in text for header in required) and not any(token.lower() in lowered for token in FORBIDDEN_TOKENS)
