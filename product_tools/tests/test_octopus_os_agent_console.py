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
    supported_runtime_target = "codex-gpt-5.4-high"

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
            skills_root = repo_root / "Skills"
            codex_root = Path(tmp) / "codex"
            workspace_root = Path(tmp) / "workspace"
            (skills_root / "Meta-Impact-Investigation").mkdir(parents=True)
            (skills_root / "Meta-Impact-Investigation" / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (repo_root / "docs").mkdir()
            (repo_root / "docs" / "README.md").write_text("docs\n", encoding="utf-8")
            (skills_root / ".system").mkdir()
            (skills_root / ".system" / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")
            (skills_root / ".system" / "Skill-creator").mkdir()
            (skills_root / ".system" / "Skill-creator" / "SKILL.md").write_text("creator\n", encoding="utf-8")

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
            self.assertEqual(payload["plan"]["skills_root"], str(skills_root))
            self.assertEqual(
                [item["name"] for item in payload["plan"]["skills"]],
                [".system", "Meta-Impact-Investigation"],
            )

    def test_install_and_uninstall_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            skills_root = repo_root / "Skills"
            codex_root = Path(tmp) / ".codex" / "skills"
            workspace_root = Path(tmp) / "workspace"
            state_root = Path(tmp) / "state"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (repo_root / "README.md").write_text("product\n", encoding="utf-8")
            codex_root.parent.mkdir(parents=True)
            (codex_root / "AGENTS.md").parent.mkdir(parents=True, exist_ok=True)
            (codex_root / "AGENTS.md").write_text("stale\n", encoding="utf-8")

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
                "--runtime-target",
                self.supported_runtime_target,
            )
            install_payload = json.loads(install.stdout)
            self.assertEqual(install_payload["status"], "ok")
            self.assertEqual(install_payload["supported_runtime_target"], self.supported_runtime_target)
            self.assertEqual(install_payload["supported_host_env"], "Codex CLI + VS Code")
            self.assertTrue((codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists())
            self.assertFalse((codex_root / "AGENTS.md").exists())
            self.assertFalse((codex_root / "README.md").exists())
            self.assertTrue((workspace_root / "AGENTS.md").exists())
            self.assertTrue((workspace_root / "Skills" / "AGENTS.md").exists())
            self.assertTrue((workspace_root / "README.md").exists())
            self.assertIn('codex -C "', install_payload["codex_launch_command"])

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
            skills_root = repo_root / "Skills"
            codex_root = Path(tmp) / ".codex" / "skills"
            workspace_root = Path(tmp) / "workspace"
            state_root = Path(tmp) / "state"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            codex_root.parent.mkdir(parents=True)

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
                "--runtime-target",
                self.supported_runtime_target,
            )

            payload = json.loads(wizard.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertTrue((codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists())
            self.assertTrue(workspace_root.exists())
            self.assertTrue((workspace_root / "AGENTS.md").exists())
            self.assertTrue((workspace_root / "Skills" / "AGENTS.md").exists())

    def test_install_rejects_non_codex_root_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            skills_root = repo_root / "Skills"
            codex_root = Path(tmp) / "other-model" / "skills"
            workspace_root = Path(tmp) / "workspace"
            state_root = Path(tmp) / "state"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")

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
                "--runtime-target",
                self.supported_runtime_target,
                check=False,
            )

            self.assertNotEqual(install.returncode, 0)
            payload = json.loads(install.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("non-codex target", payload["error"])

    def test_install_requires_supported_runtime_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            skills_root = repo_root / "Skills"
            codex_root = Path(tmp) / ".codex" / "skills"
            workspace_root = Path(tmp) / "workspace"
            state_root = Path(tmp) / "state"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            codex_root.parent.mkdir(parents=True)

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
                check=False,
            )

            self.assertNotEqual(install.returncode, 0)
            payload = json.loads(install.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn(self.supported_runtime_target, payload["error"])


if __name__ == "__main__":
    unittest.main()
