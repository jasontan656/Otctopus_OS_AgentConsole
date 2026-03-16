from __future__ import annotations

from pathlib import Path

from doc_models import Issue, TargetProfile


def lint_facade(target_root: Path, profile: TargetProfile) -> list[Issue]:
    skill_md = target_root / "SKILL.md"
    if not skill_md.is_file():
        return [Issue("facade", "missing SKILL.md")]
    body = skill_md.read_text(encoding="utf-8")
    issues: list[Issue] = []
    required_sections = ["## 1. 技能定位"]
    if profile.doc_topology == "inline":
        required_sections.append("## 2. 技能正文")
    else:
        required_sections.extend(["## Runtime Entry", "## 2. 必读顺序", "## 3. 分类入口"])
    for section in required_sections:
        if section not in body:
            issues.append(Issue("facade", f"missing section: {section}"))
    if profile.doc_topology == "workflow_path" and "`path/" not in body:
        issues.append(Issue("facade", "workflow_path facade should route to path/"))
    return issues
