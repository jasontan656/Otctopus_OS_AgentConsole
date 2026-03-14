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
    def test_guide_only_mode_generates_single_file_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "guide-only-sandbox",
                "--target-root",
                temp_dir,
                "--skill-mode",
                "guide_only",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

            assert payload["skill_mode"] == "guide_only"
            assert payload["resources_created"] == []
            assert "skill_mode: guide_only" in skill_md
            assert "## 4. 执行规则" in skill_md
            assert not (skill_dir / "agents").exists()
            assert not (skill_dir / "references").exists()
            assert not (skill_dir / "tests").exists()

    def test_guide_with_tool_mode_generates_standard_section_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "guide-with-tool-sandbox",
                "--target-root",
                temp_dir,
                "--skill-mode",
                "guide_with_tool",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

            assert payload["skill_mode"] == "guide_with_tool"
            assert "skill_mode: guide_with_tool" in skill_md
            assert "## 1. Immediate Contract" in skill_md
            assert "## 2. Structured Entry" in skill_md
            assert "## 3. 分类入口" not in skill_md
            assert "metadata:" in skill_md
            assert (skill_dir / "references" / "routing" / "TASK_ROUTING.md").exists()
            assert (skill_dir / "references" / "governance" / "SKILL_DOCSTRUCTURE_POLICY.md").exists()
            assert (skill_dir / "references" / "governance" / "SKILL_EXECUTION_RULES.md").exists()
            assert (skill_dir / "tests").exists()
            assert not (skill_dir / "references" / "runtime").exists()

    def test_executable_workflow_mode_generates_stage_contract_kit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "workflow-sandbox",
                "--target-root",
                temp_dir,
                "--skill-mode",
                "executable_workflow_skill",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            runtime_contract = json.loads(
                (skill_dir / "references" / "runtime" / "SKILL_RUNTIME_OVERVIEW.json").read_text(encoding="utf-8")
            )

            assert payload["skill_mode"] == "executable_workflow_skill"
            assert "## 1. Immediate Contract" in skill_md
            assert "## 2. Structured Entry" in skill_md
            assert "## 3. 分类入口" not in skill_md
            assert runtime_contract["skill_mode"] == "executable_workflow_skill"
            assert runtime_contract["doc_structure_governance"]["mandatory_skill"] == "SkillsManager-Doc-Structure"
            assert "stage-checklist" in runtime_contract["stage_contract_policy"]["required_contracts"]
            assert (skill_dir / "references" / "routing" / "TASK_ROUTING.md").exists()
            assert (skill_dir / "references" / "governance" / "SKILL_DOCSTRUCTURE_POLICY.md").exists()
            assert (skill_dir / "assets" / "templates" / "stages" / "STAGE_TEMPLATE" / "CHECKLIST.json").exists()
            assert (skill_dir / "assets" / "templates" / "stages" / "STAGE_TEMPLATE" / "COMMAND_CONTRACT.json").exists()
            assert (skill_dir / "references" / "stages" / "00_STAGE_INDEX.md").exists()
