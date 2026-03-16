#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re

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

DEFAULT_TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "references" / "templates" / "intent_clarify_template_v1.txt"
HEADER_PATTERN = re.compile(r"^([A-Za-z_ /&\-]+|[\u4e00-\u9fff]+)\s*:\s*(.*)$")
LEGACY_HEADER_PATTERN = re.compile(r"(?mi)^(?:GOAL|REPO_CONTEXT_AND_IMPACT|INPUTS|OUTPUTS|BOUNDARIES|VALIDATION)\s*:")
SESSION_REF_PATTERN = re.compile(r"(?i)\b(codex|session|resume)\s*id\s*[:：]\s*([A-Za-z0-9][A-Za-z0-9._:-]*)")
PROMPT_MARKER_PATTERNS = (
    re.compile(r"(?is)(?:帮我|请|请先.*?后)?(?:强化|增强|加强|优化|澄清|改写)\s*(?:如下|以下|下面(?:的)?)?\s*prompt\s*[:：]\s*(.+)$"),
    re.compile(r'(?is)(?:help me |please )?(?:enhance|strengthen|clarify|rewrite|refine)\s+(?:the\s+)?(?:following\s+)?prompt\s*[:：]\s*(.+)$'),
)
SECTION_ALIASES = {
    "intent": {"intent", "user intent", "task intent", "clarified intent", "需求意图", "意图", "真实意图", "目标意图"},
    "goal": {"goal", "目标"},
    "repo_context": {"repo_context_and_impact", "repo_context", "repo context", "repo context and impact", "仓库上下文", "影响面", "覆盖面"},
    "inputs": {"inputs", "input", "输入"},
    "outputs": {"outputs", "output", "输出"},
    "boundaries": {"boundaries", "boundary", "constraints", "边界", "约束"},
    "validation": {"validation", "acceptance", "acceptance checks", "验证", "验收"},
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


def _join_lines(lines: list[str]) -> str:
    joined: list[str] = []
    for line in lines:
        if not line:
            if joined and joined[-1] != "":
                joined.append("")
            continue
        joined.append(line)
    while joined and not joined[0]:
        joined.pop(0)
    while joined and not joined[-1]:
        joined.pop()
    return "\n".join(joined).strip()


def _unwrap_enclosing_pairs(text: str) -> str:
    cleaned = str(text or "").strip()
    wrapper_pairs = (
        ("(", ")"),
        ("（", "）"),
        ("[", "]"),
        ("【", "】"),
        ("{", "}"),
        ('"', '"'),
        ("'", "'"),
        ("“", "”"),
        ("‘", "’"),
        ("`", "`"),
    )
    changed = True
    while cleaned and changed:
        changed = False
        for left, right in wrapper_pairs:
            if cleaned.startswith(left) and cleaned.endswith(right):
                inner = cleaned[len(left) : len(cleaned) - len(right)].strip()
                if inner:
                    cleaned = inner
                    changed = True
                    break
    return cleaned


def collect_context_session_refs(text: str) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for match in SESSION_REF_PATTERN.finditer(text):
        session_kind = str(match.group(1) or "").strip().lower()
        session_id = str(match.group(2) or "").strip()
        key = (session_kind, session_id)
        if not session_id or key in seen:
            continue
        refs.append({"kind": session_kind, "id": session_id})
        seen.add(key)
    return refs


def preprocess_prompt_request(text: str) -> tuple[str, dict[str, object]]:
    raw_text = str(text or "")
    metadata: dict[str, object] = {
        "context_session_refs": collect_context_session_refs(raw_text),
        "context_request_detected": False,
        "target_prompt_detected": False,
        "target_prompt_source": "raw_input",
    }
    for pattern in PROMPT_MARKER_PATTERNS:
        match = pattern.search(raw_text)
        if not match:
            continue
        candidate = _unwrap_enclosing_pairs(str(match.group(1) or "").strip())
        metadata["context_request_detected"] = bool(metadata["context_session_refs"])
        metadata["target_prompt_detected"] = bool(candidate)
        metadata["target_prompt_source"] = "embedded_prompt_wrapper"
        return candidate, metadata
    return raw_text, metadata


def parse_intent_source(text: str) -> tuple[dict[str, list[str] | str], dict[str, object]]:
    normalized_text, metadata = preprocess_prompt_request(text)
    parsed: dict[str, list[str] | str] = {"intent_lines": [], "goal": "", "fallback_lines": []}
    current = ""
    saw_structured_header = False
    for raw in normalized_text.splitlines():
        stripped = raw.strip()
        if not stripped:
            if current == "intent":
                intent_lines = parsed["intent_lines"]
                assert isinstance(intent_lines, list)
                if intent_lines and intent_lines[-1] != "":
                    intent_lines.append("")
            continue

        header_match = HEADER_PATTERN.match(stripped)
        if header_match:
            key = _section_key(str(header_match.group(1) or "").strip())
            remainder = sanitize_inline(str(header_match.group(2) or ""))
            if key:
                saw_structured_header = True
                current = key
                if key == "intent" and remainder:
                    intent_lines = parsed["intent_lines"]
                    assert isinstance(intent_lines, list)
                    intent_lines.append(remainder)
                elif key == "goal" and remainder:
                    goal = str(parsed["goal"]).strip()
                    parsed["goal"] = f"{goal} {remainder}".strip() if goal else remainder
                continue
            current = ""
            continue

        bullet_match = re.match(r"^[-*]\s+(.+)$", stripped)
        cleaned = sanitize_inline(bullet_match.group(1) if bullet_match else stripped)
        if not cleaned:
            continue
        rendered_line = f"- {cleaned}" if bullet_match else cleaned

        if current == "intent":
            intent_lines = parsed["intent_lines"]
            assert isinstance(intent_lines, list)
            intent_lines.append(rendered_line)
        elif current == "goal":
            goal = str(parsed["goal"]).strip()
            parsed["goal"] = f"{goal} {cleaned}".strip() if goal else cleaned
        elif not saw_structured_header:
            fallback_lines = parsed["fallback_lines"]
            assert isinstance(fallback_lines, list)
            fallback_lines.append(rendered_line)
    return parsed, metadata


def resolve_intent_body(parsed: dict[str, list[str] | str]) -> str:
    intent_lines = parsed["intent_lines"]
    fallback_lines = parsed["fallback_lines"]
    goal = str(parsed["goal"]).strip()
    assert isinstance(intent_lines, list)
    assert isinstance(fallback_lines, list)
    if intent_lines:
        return _join_lines(intent_lines)
    if goal:
        return goal
    return _join_lines(fallback_lines)


def missing_required_sections(intent_body: str) -> list[str]:
    return [] if str(intent_body).strip() else ["INTENT"]


def load_template(template_file: pathlib.Path) -> str:
    if not template_file.exists():
        raise FileNotFoundError(str(template_file))
    template = template_file.read_text(encoding="utf-8")
    if "{{INTENT_BODY}}" not in template:
        raise ValueError("template_missing_required_tokens")
    return template


def render_intent_output(template: str, intent_body: str) -> str:
    return template.replace("{{INTENT_BODY}}", str(intent_body).strip()).strip() + "\n"


def validate_final_shape(text: str) -> bool:
    lowered = text.lower()
    return text.startswith("INTENT:") and "{{INTENT_BODY}}" not in text and not LEGACY_HEADER_PATTERN.search(text) and not any(
        token.lower() in lowered for token in FORBIDDEN_TOKENS
    )
