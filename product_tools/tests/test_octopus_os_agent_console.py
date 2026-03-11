from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1] / "octopus_os_agent_console.py"
)


class OctopusOSAgentConsoleTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_plan_only_targets_skill_roots_for_codex(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            codex_root = Path(tmp) / "codex"
            workspace_root = Path(tmp) / "workspace"
            (repo_root / "Meta-Impact-Investigation").mkdir(parents=True)
            (repo_root / "Meta-Impact-Investigation" / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (repo_root / "docs").mkdir()
            (repo_root / "docs" / "README.md").write_text("docs\n", encoding="utf-8")
            (repo_root / ".system").mkdir()
            (repo_root / ".system" / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")
            (repo_root / ".system" / "Skill-creator").mkdir()
            (repo_root / ".system" / "Skill-creator" / "SKILL.md").write_text("creator\n", encoding="utf-8")

            completed = self.run_cli(
                "plan",
                "--repo-root",
                str(repo_root),
                "--codex-root",
                str(codex_root),
                "--workspace-root",
                str(workspace_root),
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["product_name"], "Octopus OS - Natural-Language-Driven Multi-Agent Console")
            self.assertEqual(
                [item["name"] for item in payload["plan"]["skills"]],
                [".system", "Meta-Impact-Investigation"],
            )

    def test_install_and_uninstall_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            codex_root = Path(tmp) / "codex"
            workspace_root = Path(tmp) / "workspace"
            state_root = Path(tmp) / "state"
            skill_root = repo_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (repo_root / "README.md").write_text("product\n", encoding="utf-8")
            codex_root.mkdir()

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--codex-root",
                str(codex_root),
                "--workspace-root",
                str(workspace_root),
                "--state-root",
                str(state_root),
            )
            install_payload = json.loads(install.stdout)
            self.assertEqual(install_payload["status"], "ok")
            self.assertTrue((codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists())
            self.assertFalse((codex_root / "README.md").exists())
            self.assertTrue((workspace_root / "README.md").exists())

            uninstall = self.run_cli(
                "uninstall",
                "--state-root",
                str(state_root),
                "--session-id",
                install_payload["session_id"],
            )
            uninstall_payload = json.loads(uninstall.stdout)
            self.assertEqual(uninstall_payload["status"], "ok")
            self.assertFalse((codex_root / "Meta-Impact-Investigation").exists())
            self.assertFalse(workspace_root.exists())

    def test_wizard_supports_bilingual_non_interactive_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            codex_root = Path(tmp) / "codex"
            workspace_root = Path(tmp) / "workspace"
            state_root = Path(tmp) / "state"
            skill_root = repo_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            codex_root.mkdir()

            wizard = self.run_cli(
                "wizard",
                "--yes",
                "--wizard-language",
                "bilingual",
                "--repo-root",
                str(repo_root),
                "--codex-root",
                str(codex_root),
                "--workspace-root",
                str(workspace_root),
                "--state-root",
                str(state_root),
            )

            payload = json.loads(wizard.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertTrue((codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists())
            self.assertTrue(workspace_root.exists())


if __name__ == "__main__":
    unittest.main()
