from __future__ import annotations

import json


PART_B_MARKER = "[PART B]"
JSON_FENCE = "```json"
CODE_FENCE_END = "```"


def is_agents_target_kind(target_kind: str) -> bool:
    return target_kind == "AGENTS.md"


def normalize_text(text: str) -> str:
    cleaned = text.rstrip()
    return f"{cleaned}\n" if cleaned else ""


def extract_part_a(text: str) -> str:
    marker_index = text.find(PART_B_MARKER)
    if marker_index < 0:
        return normalize_text(text)
    return normalize_text(text[:marker_index])


def render_part_b_markdown(payload: dict[str, object]) -> str:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    return "\n".join([PART_B_MARKER, "", JSON_FENCE, rendered, CODE_FENCE_END]) + "\n"


def compose_managed_agents(part_a_text: str, payload: dict[str, object]) -> str:
    part_a = extract_part_a(part_a_text)
    part_b = render_part_b_markdown(payload)
    if not part_a:
        return part_b
    return f"{part_a}\n{part_b}"


def compose_external_agents(human_text: str) -> str:
    return extract_part_a(human_text)
