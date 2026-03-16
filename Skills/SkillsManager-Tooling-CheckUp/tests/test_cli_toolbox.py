from __future__ import annotations

import json
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


def run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(CLI_PATH), *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_contract_exposes_audit_entry() -> None:
    payload = run_cli("contract")
    assert payload["skill_role"] == "tooling_governor"
    assert "audit" in payload["tool_entry"]["commands"]


def test_audit_passes_for_creation_template() -> None:
    payload = run_cli(
        "audit",
        "--target-skill-root",
        str(SKILL_ROOT.parent / "SkillsManager-Creation-Template"),
    )
    assert payload["status"] == "ok"
    assert payload["tooling_surface"] == "automation_cli"


def test_audit_handles_no_tooling_surface(tmp_path: Path) -> None:
    skill_root = tmp_path / "Inline-Skill"
    skill_root.mkdir()
    (skill_root / "SKILL.md").write_text(
        "---\nname: Inline-Skill\ndescription: Inline.\n---\n\n# Inline-Skill\n\n## 1. 技能定位\n\n## 2. 技能正文\n",
        encoding="utf-8",
    )
    payload = run_cli("audit", "--target-skill-root", str(skill_root))
    assert payload["status"] == "ok"
    assert payload["tooling_surface"] == "none"


def test_audit_rejects_absolute_artifact_paths(tmp_path: Path) -> None:
    skill_root = tmp_path / "Bad-Artifact"
    runtime_root = skill_root / "references" / "runtime_contracts"
    runtime_root.mkdir(parents=True)
    (skill_root / "scripts").mkdir()
    (skill_root / "tests").mkdir()
    (skill_root / "references" / "tooling").mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        "---\nname: Bad-Artifact\ndescription: Bad artifact policy.\n---\n\n# Bad-Artifact\n\n## Runtime Entry\n\n## 1. 技能定位\n\n## 2. 必读顺序\n\n## 3. 分类入口\n",
        encoding="utf-8",
    )
    (skill_root / "scripts" / "Cli_Toolbox.py").write_text("# placeholder\n", encoding="utf-8")
    (skill_root / "tests" / "test_cli_toolbox.py").write_text("def test_placeholder():\n    assert True\n", encoding="utf-8")
    (skill_root / "references" / "tooling" / "Cli_Toolbox_USAGE.md").write_text("# usage\n", encoding="utf-8")
    payload = {
        "skill_name": "Bad-Artifact",
        "runtime_source_policy": {"runtime_rule_source": "CLI_JSON"},
        "tool_entry": {"commands": {"contract": "read contract"}},
        "artifact_policy": {"mode": "persisted", "root": "/home/jasontan656/AI_Projects/Codex_Skills_Result"}
    }
    (runtime_root / "SKILL_RUNTIME_CONTRACT.json").write_text(json.dumps(payload), encoding="utf-8")
    audit = run_cli("audit", "--target-skill-root", str(skill_root))
    assert audit["status"] == "error"
    assert any(issue["scope"] == "artifact_policy" for issue in audit["issues"])
