from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class MetaSkillMirrorCliTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_push_mode_accepts_nested_system_skill_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            source_skill = mirror_root / ".system" / "Skill-creator"
            destination_skill = codex_root / ".system" / "skill-creator"
            source_skill.mkdir(parents=True)
            destination_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("mirror\n", encoding="utf-8")
            (destination_skill / "SKILL.md").write_text("installed\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "skill",
                "--skill-name",
                ".system/skill-creator",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
                "--dry-run",
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["resolved_mode"], "push")
            self.assertEqual(payload["skill_name"], ".system/skill-creator")
            self.assertEqual(payload["source_skill_name"], ".system/Skill-creator")
            self.assertEqual(payload["destination_skill_name"], ".system/skill-creator")
            self.assertEqual(payload["source"], str(source_skill))
            self.assertEqual(payload["destination"], str(destination_skill))

    def test_install_mode_routes_nested_system_skill_to_lowercase_codex_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            source_skill = mirror_root / ".system" / "Skill-installer"
            source_skill.mkdir(parents=True)
            codex_root.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("mirror\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "skill",
                "--skill-name",
                ".system/skill-installer",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "route_required")
            self.assertEqual(payload["resolved_mode"], "install")
            self.assertEqual(payload["source_skill_name"], ".system/Skill-installer")
            self.assertEqual(payload["destination_skill_name"], ".system/skill-installer")
            self.assertEqual(payload["destination"], str(codex_root / ".system" / "skill-installer"))

    def test_nested_non_system_skill_path_keeps_original_destination_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            source_skill = mirror_root / "families" / "Custom-Skill"
            destination_skill = codex_root / "families" / "Custom-Skill"
            source_skill.mkdir(parents=True)
            destination_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("mirror\n", encoding="utf-8")
            (destination_skill / "SKILL.md").write_text("installed\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "skill",
                "--skill-name",
                "families/Custom-Skill",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
                "--dry-run",
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["resolved_mode"], "push")
            self.assertEqual(payload["source_skill_name"], "families/Custom-Skill")
            self.assertEqual(payload["destination_skill_name"], "families/Custom-Skill")

    def test_rejects_path_traversal_skill_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            mirror_root.mkdir()
            codex_root.mkdir()

            completed = self.run_cli(
                "--scope",
                "skill",
                "--skill-name",
                ".system/../skill-creator",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("dot traversal", payload["error"])


if __name__ == "__main__":
    unittest.main()
