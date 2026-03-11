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

    def test_all_scope_push_only_syncs_skill_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            skills_root = mirror_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            product_docs = mirror_root / "docs"
            product_tools = mirror_root / "product_tools"
            system_root = skills_root / ".system"

            skill_root.mkdir(parents=True)
            product_docs.mkdir(parents=True)
            product_tools.mkdir(parents=True)
            system_root.mkdir(parents=True)
            codex_root.mkdir(parents=True)
            (codex_root / "AGENTS.md").write_text("stale\n", encoding="utf-8")

            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (product_docs / "README.md").write_text("docs\n", encoding="utf-8")
            (product_tools / "installer.py").write_text("print('installer')\n", encoding="utf-8")
            (system_root / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")
            (system_root / "Skill-creator").mkdir()
            (system_root / "Skill-creator" / "SKILL.md").write_text("creator\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "all",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
                "--dry-run",
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["resolved_mode"], "push")
            self.assertEqual(payload["scope"], "all")
            self.assertEqual(payload["skills_root"], str(skills_root))
            self.assertEqual(
                [entry["root_name"] for entry in payload["synced_entries"]],
                [".system", "Meta-Impact-Investigation"],
            )
            self.assertTrue(all("docs" not in " ".join(command) for command in payload["commands"]))
            self.assertTrue(all("product_tools" not in " ".join(command) for command in payload["commands"]))
            self.assertEqual(
                payload["removed_forbidden_entries"],
                [str(codex_root / "AGENTS.md")],
            )

    def test_all_scope_push_removes_stale_codex_root_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            skills_root = mirror_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            codex_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (codex_root / "AGENTS.md").write_text("stale\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "all",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertFalse((codex_root / "AGENTS.md").exists())
            self.assertEqual(
                payload["removed_forbidden_entries"],
                [str(codex_root / "AGENTS.md")],
            )


if __name__ == "__main__":
    unittest.main()
