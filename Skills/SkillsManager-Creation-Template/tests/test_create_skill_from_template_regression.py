from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "create_skill_from_template.py"


def run_generator(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


class TestCreateSkillFromTemplateRegressionTest:
    def test_basic_profile_generates_standard_section_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "basic-sandbox",
                "--target-root",
                temp_dir,
                "--profile",
                "basic",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

            assert "## 1. 技能定位" in skill_md
            assert "## 2. 必读顺序" in skill_md
            assert "## 6. 读取原则" in skill_md
            assert "## 7. 结构索引" in skill_md
            assert "metadata:" in skill_md
            assert (skill_dir / "references" / "routing" / "TASK_ROUTING.md").exists()
            assert (skill_dir / "references" / "governance" / "SKILL_DOCSTRUCTURE_POLICY.md").exists()
            assert (skill_dir / "references" / "governance" / "SKILL_EXECUTION_RULES.md").exists()
            assert (skill_dir / "tests").exists()
            assert not (skill_dir / "references" / "runtime").exists()

    def test_staged_profile_generates_stage_contract_kit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "staged-sandbox",
                "--target-root",
                temp_dir,
                "--profile",
                "staged_cli_first",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            runtime_contract = json.loads(
                (skill_dir / "references" / "runtime" / "SKILL_RUNTIME_OVERVIEW.json").read_text(encoding="utf-8")
            )

            assert runtime_contract["skill_profile"] == "staged_cli_first"
            assert runtime_contract["doc_structure_governance"]["mandatory_skill"] == "SkillsManager-Doc-Structure"
            assert "stage-checklist" in runtime_contract["stage_contract_policy"]["required_contracts"]
            assert (skill_dir / "references" / "routing" / "TASK_ROUTING.md").exists()
            assert (skill_dir / "references" / "governance" / "SKILL_DOCSTRUCTURE_POLICY.md").exists()
            assert (skill_dir / "assets" / "templates" / "stages" / "STAGE_TEMPLATE" / "CHECKLIST.json").exists()
            assert (skill_dir / "assets" / "templates" / "stages" / "STAGE_TEMPLATE" / "COMMAND_CONTRACT.json").exists()
            assert (skill_dir / "references" / "stages" / "00_STAGE_INDEX.md").exists()
