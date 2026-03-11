from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "octopus_os_agent_console.py"


class OctopusOSAgentConsoleTests(unittest.TestCase):
    supported_runtime_target = "codex-gpt-5.4-high"

    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "OCTOPUS_OS_CODEX_INSTALL_MODE": "stub",
        }
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
            env=env,
        )

    def test_plan_derives_install_root_codex_home_and_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            workspace_root = install_root.parent / "octopus-os-agent-console"
            skills_root = repo_root / "Skills"
            (skills_root / "Meta-Impact-Investigation").mkdir(parents=True)
            (skills_root / "Meta-Impact-Investigation" / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / ".system").mkdir()
            (skills_root / ".system" / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")
            (skills_root / ".system" / "Skill-creator").mkdir()
            (skills_root / ".system" / "Skill-creator" / "SKILL.md").write_text("creator\n", encoding="utf-8")

            completed = self.run_cli(
                "plan",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["plan"]["install_root"], str(install_root))
            self.assertEqual(payload["plan"]["codex_home"], str(install_root / ".codex"))
            self.assertEqual(payload["plan"]["codex_root"], str(install_root / ".codex" / "skills"))
            self.assertEqual(payload["plan"]["workspace_root"], str(workspace_root))
            self.assertEqual(
                [item["name"] for item in payload["plan"]["skills"]],
                [".system", "Meta-Impact-Investigation"],
            )

    def test_install_and_uninstall_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            workspace_root = install_root.parent / "octopus-os-agent-console"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (repo_root / "README.md").write_text("product\n", encoding="utf-8")
            (codex_root / ".system").mkdir(parents=True)
            (codex_root / ".system" / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")
            (codex_root / "AGENTS.md").write_text("stale\n", encoding="utf-8")

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
            )
            install_payload = json.loads(install.stdout)
            self.assertEqual(install_payload["status"], "ok")
            self.assertEqual(install_payload["supported_runtime_target"], self.supported_runtime_target)
            self.assertEqual(install_payload["supported_host_env"], "Codex CLI + VS Code")
            self.assertTrue((install_root / "bin" / "codex").exists())
            self.assertTrue((codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists())
            self.assertFalse((codex_root / "AGENTS.md").exists())
            self.assertTrue((workspace_root / "AGENTS.md").exists())
            self.assertTrue((workspace_root / "Skills" / "AGENTS.md").exists())
            self.assertTrue((workspace_root / ".product_runtime" / "github_skill_repo_binding.json").exists())
            self.assertIn("HOME=", install_payload["codex_launch_command"])

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
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            workspace_root = install_root.parent / "octopus-os-agent-console"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (codex_root / ".system").mkdir(parents=True)

            wizard = self.run_cli(
                "wizard",
                "--yes",
                "--wizard-language",
                "bilingual",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
            )

            payload = json.loads(wizard.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertTrue((codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists())
            self.assertTrue(workspace_root.exists())
            self.assertTrue((workspace_root / "AGENTS.md").exists())
            self.assertTrue((workspace_root / "Skills" / "AGENTS.md").exists())

    def test_install_rejects_dirty_codex_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (codex_root / ".system").mkdir(parents=True)
            (codex_root / "Already-Installed").mkdir(parents=True)

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
                check=False,
            )

            self.assertNotEqual(install.returncode, 0)
            payload = json.loads(install.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("not clean", payload["error"])

    def test_install_requires_supported_runtime_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
                check=False,
            )

            self.assertNotEqual(install.returncode, 0)
            payload = json.loads(install.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn(self.supported_runtime_target, payload["error"])

    def test_install_requires_github_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--runtime-target",
                self.supported_runtime_target,
                check=False,
            )

            self.assertNotEqual(install.returncode, 0)
            payload = json.loads(install.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("--github-skill-repo", payload["error"])


if __name__ == "__main__":
    unittest.main()
