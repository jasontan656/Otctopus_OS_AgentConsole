from __future__ import annotations

from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"


def render_template(relative_path: str, replacements: dict[str, str]) -> str:
    content = (TEMPLATE_ROOT / relative_path).read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content
