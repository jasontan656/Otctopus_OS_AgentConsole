from __future__ import annotations


PART_B_MARKER = "[PART B]"


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


def compose_external_agents(part_a_text: str) -> str:
    return normalize_text(part_a_text)
