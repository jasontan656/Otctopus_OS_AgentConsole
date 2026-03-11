from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
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


class CreateSkillFromTemplateRegressionTest(unittest.TestCase):
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

            self.assertIn("## 1. 技能定位", skill_md)
            self.assertIn("## 2. 必读顺序", skill_md)
            self.assertIn("## 6. 读取原则", skill_md)
            self.assertIn("## 7. 结构索引", skill_md)
            self.assertIn("metadata:", skill_md)
            self.assertTrue((skill_dir / "references" / "routing" / "TASK_ROUTING.md").exists())
            self.assertTrue((skill_dir / "references" / "governance" / "SKILL_DOCSTRUCTURE_POLICY.md").exists())
            self.assertTrue((skill_dir / "references" / "governance" / "SKILL_EXECUTION_RULES.md").exists())
            self.assertTrue((skill_dir / "tests").exists())
            self.assertFalse((skill_dir / "references" / "runtime").exists())

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
                (skill_dir / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.json").read_text(encoding="utf-8")
            )

            self.assertEqual(runtime_contract["skill_profile"], "staged_cli_first")
            self.assertEqual(runtime_contract["doc_structure_governance"]["mandatory_skill"], "skill-doc-structure")
            self.assertIn("stage-checklist", runtime_contract["stage_contract_policy"]["required_contracts"])
            self.assertTrue((skill_dir / "references" / "routing" / "TASK_ROUTING.md").exists())
            self.assertTrue((skill_dir / "references" / "governance" / "SKILL_DOCSTRUCTURE_POLICY.md").exists())
            self.assertTrue(
                (skill_dir / "assets" / "templates" / "stages" / "STAGE_TEMPLATE" / "CHECKLIST.json").exists()
            )
            self.assertTrue(
                (skill_dir / "assets" / "templates" / "stages" / "STAGE_TEMPLATE" / "COMMAND_CONTRACT.json").exists()
            )
            self.assertTrue((skill_dir / "references" / "stages" / "00_STAGE_INDEX.md").exists())


if __name__ == "__main__":
    unittest.main()
