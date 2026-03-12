from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "octopus_os_agent_console.py"


class TestOctopusOSAgentConsoleTests:
    supported_runtime_target = "codex-gpt-5.4-high"

    def run_cli(
        self,
        *args: str,
        check: bool = True,
        env_overrides: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "OCTOPUS_OS_CODEX_INSTALL_MODE": "stub",
        }
        if env_overrides:
            env.update(env_overrides)
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
            env=env,
        )

    def make_fake_codex_cli(self, root: Path) -> Path:
        codex_bin = root / "bin" / "codex"
        codex_bin.parent.mkdir(parents=True, exist_ok=True)
        codex_bin.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = \"--version\" ]; then\n"
            "  echo 'codex fake 1.0.0'\n"
            "  exit 0\n"
            "fi\n"
            "exit 0\n",
            encoding="utf-8",
        )
        codex_bin.chmod(codex_bin.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return codex_bin

    def write_meta_agent_browser_dependency_manifest(self, skill_root: Path) -> None:
        manifest_path = (
            skill_root / "references" / "runtime_contracts" / "EXTERNAL_RUNTIME_DEPENDENCIES.json"
        )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "dependency_contract_name": "meta_agent_browser_external_runtime_dependencies",
                    "contract_version": "1.0.0",
                    "skill_name": "__SKILL_NAME__",
                    "dependencies": [
                        {
                            "dependency_id": "agent-browser",
                            "display_name": "agent-browser",
                            "install_type": "npm_global_package",
                            "install_root": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser",
                            "binary_name": "agent-browser",
                            "binary_path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
                            "runtime_env": {
                                "PATH_prepend": [
                                    "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin"
                                ],
                                "PLAYWRIGHT_BROWSERS_PATH": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/ms-playwright",
                                "HOME": "__PRODUCT_ROOT__",
                            },
                            "install_commands": [
                                {
                                    "argv": [
                                        "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
                                        "install",
                                    ]
                                }
                            ],
                            "validate_commands": [
                                {
                                    "argv": [
                                        "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
                                        "--version",
                                    ]
                                }
                            ],
                            "required_artifacts": [
                                {
                                    "path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser",
                                    "kind": "dir",
                                },
                                {
                                    "path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
                                    "kind": "file",
                                },
                                {
                                    "path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/ms-playwright",
                                    "kind": "nonempty_dir",
                                },
                            ],
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_plan_derives_install_root_codex_home_and_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            workspace_root = install_root / "console"
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
                "--codex-cli-mode",
                "install",
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
            )

            payload = json.loads(completed.stdout)
            assert payload["status"] == "ok"
            assert payload["plan"]["install_root"] == str(install_root)
            assert payload["plan"]["codex_home"] == str(install_root / ".codex")
            assert payload["plan"]["codex_root"] == str(install_root / ".codex" / "skills")
            assert payload["plan"]["codex_cli_mode"] == "install"
            assert payload["plan"]["console_root"] == str(workspace_root)
            assert payload["plan"]["workspace_root"] == str(workspace_root)
            assert payload["plan"]["skill_runtime_root"] == str(install_root / "Codex_Skill_Runtime")
            assert payload["plan"]["skill_result_root"] == str(install_root / "Codex_Skills_Result")
            assert payload["plan"]["octopus_os_root"] == str(install_root / "Octopus_OS")
            assert [item["name"] for item in payload["plan"]["skills"]] == [
                ".system",
                "Meta-Impact-Investigation",
            ]
            assert payload["plan"]["external_runtime_dependencies"] == []

    def test_plan_lists_product_managed_external_runtime_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Agent-Browser"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            self.write_meta_agent_browser_dependency_manifest(skill_root)

            completed = self.run_cli(
                "plan",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--codex-cli-mode",
                "install",
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
            )

            payload = json.loads(completed.stdout)
            dependencies = payload["plan"]["external_runtime_dependencies"]
            assert len(dependencies) == 1
            dependency = dependencies[0]
            assert dependency["dependency_id"] == "agent-browser"
            assert dependency["required_by_skills"] == ["Meta-Agent-Browser"]
            assert dependency["install_root"] == str(
                install_root / ".product_runtime" / "external_runtime_dependencies" / "agent-browser"
            )

    def test_install_and_uninstall_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            workspace_root = install_root / "console"
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
                "--codex-cli-mode",
                "install",
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
            )
            install_payload = json.loads(install.stdout)
            assert install_payload["status"] == "ok"
            assert install_payload["supported_runtime_target"] == self.supported_runtime_target
            assert install_payload["supported_host_env"] == "Codex CLI + VS Code"
            assert install_payload["codex_cli_mode"] == "install"
            assert (install_root / "bin" / "codex").exists()
            assert (codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists()
            assert not (codex_root / "AGENTS.md").exists()
            assert (install_root / "Codex_Skill_Runtime").is_dir()
            assert (install_root / "Codex_Skills_Result").is_dir()
            assert (install_root / "Octopus_OS").is_dir()
            assert (workspace_root / "AGENTS.md").exists()
            assert (workspace_root / "Skills" / "AGENTS.md").exists()
            assert (workspace_root / ".product_runtime" / "github_skill_repo_binding.json").exists()
            assert install_payload["console_root"] == str(workspace_root)
            assert install_payload["skill_runtime_root"] == str(install_root / "Codex_Skill_Runtime")
            assert install_payload["skill_result_root"] == str(install_root / "Codex_Skills_Result")
            assert install_payload["octopus_os_root"] == str(install_root / "Octopus_OS")
            assert "HOME=" in install_payload["codex_launch_command"]

            uninstall = self.run_cli(
                "uninstall",
                "--state-root",
                str(state_root),
                "--session-id",
                install_payload["session_id"],
            )
            uninstall_payload = json.loads(uninstall.stdout)
            assert uninstall_payload["status"] == "ok"
            assert not (codex_root / "Meta-Impact-Investigation").exists()
            assert not (install_root / "bin" / "codex").exists()
            assert not (install_root / "Codex_Skill_Runtime").exists()
            assert not (install_root / "Codex_Skills_Result").exists()
            assert not (install_root / "Octopus_OS").exists()
            assert not (workspace_root.exists())

    def test_install_and_uninstall_manage_external_runtime_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Agent-Browser"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            self.write_meta_agent_browser_dependency_manifest(skill_root)
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (repo_root / "README.md").write_text("product\n", encoding="utf-8")
            (codex_root / ".system").mkdir(parents=True)
            (codex_root / ".system" / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--codex-cli-mode",
                "install",
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
                env_overrides={"OCTOPUS_OS_EXTERNAL_DEPENDENCY_MODE": "stub"},
            )

            payload = json.loads(install.stdout)
            dependency_root = install_root / ".product_runtime" / "external_runtime_dependencies" / "agent-browser"
            assert payload["status"] == "ok"
            assert payload["external_runtime_dependencies"][0]["dependency_id"] == "agent-browser"
            assert (dependency_root / "npm" / "bin" / "agent-browser").exists()
            assert (dependency_root / "ms-playwright").is_dir()

            uninstall = self.run_cli(
                "uninstall",
                "--state-root",
                str(state_root),
                "--session-id",
                payload["session_id"],
            )
            uninstall_payload = json.loads(uninstall.stdout)
            assert uninstall_payload["status"] == "ok"
            assert str(dependency_root) in uninstall_payload["removed_external_runtime_dependencies"]
            assert not dependency_root.exists()

    def test_wizard_supports_bilingual_non_interactive_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            workspace_root = install_root / "console"
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
                "--codex-cli-mode",
                "install",
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
            )

            payload = json.loads(wizard.stdout)
            assert payload["status"] == "ok"
            assert (codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists()
            assert workspace_root.exists()
            assert (workspace_root / "AGENTS.md").exists()
            assert (workspace_root / "Skills" / "AGENTS.md").exists()

    def test_install_attaches_existing_codex_cli_without_local_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            codex_root = install_root / ".codex" / "skills"
            workspace_root = install_root / "console"
            state_root = Path(tmp) / "state"
            fake_root = Path(tmp) / "existing-codex"
            fake_codex_bin = self.make_fake_codex_cli(fake_root)
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (repo_root / "README.md").write_text("product\n", encoding="utf-8")
            (codex_root / ".system").mkdir(parents=True)
            (codex_root / ".system" / ".codex-system-skills.marker").write_text("marker\n", encoding="utf-8")

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--codex-cli-mode",
                "attach",
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
                env_overrides={"PATH": f"{fake_codex_bin.parent}:{os.environ['PATH']}"},
            )

            payload = json.loads(install.stdout)
            assert payload["status"] == "ok"
            assert payload["codex_cli_mode"] == "attach"
            assert payload["codex_cli_bin"] == str(fake_codex_bin)
            assert payload["codex_cli_install_command"] is None
            assert payload["codex_cli_version"] == "codex fake 1.0.0"
            assert not (install_root / "bin" / "codex").exists()
            assert (codex_root / "Meta-Impact-Investigation" / "SKILL.md").exists()
            assert workspace_root.exists()
            assert f"HOME={install_root}" in payload["codex_launch_command"]
            assert str(fake_codex_bin) in payload["codex_launch_command"]

            uninstall = self.run_cli(
                "uninstall",
                "--state-root",
                str(state_root),
                "--session-id",
                payload["session_id"],
            )
            uninstall_payload = json.loads(uninstall.stdout)
            assert uninstall_payload["status"] == "ok"
            assert fake_codex_bin.exists()
            assert not workspace_root.exists()

    def test_uninstall_removes_target_local_codex_runtime_when_created_by_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            install_root = Path(tmp) / "codex-home"
            state_root = Path(tmp) / "state"
            skills_root = repo_root / "Skills"
            skill_root = skills_root / "Meta-Impact-Investigation"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skills_root / "AGENTS.md").write_text("skills agents\n", encoding="utf-8")
            (repo_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (repo_root / "README.md").write_text("product\n", encoding="utf-8")

            install = self.run_cli(
                "install",
                "--repo-root",
                str(repo_root),
                "--install-root",
                str(install_root),
                "--state-root",
                str(state_root),
                "--codex-cli-mode",
                "install",
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
            )

            payload = json.loads(install.stdout)
            assert payload["status"] == "ok"
            assert (install_root / "bin" / "codex").exists()
            assert (install_root / ".codex" / "skills" / "Meta-Impact-Investigation" / "SKILL.md").exists()

            uninstall = self.run_cli(
                "uninstall",
                "--state-root",
                str(state_root),
                "--session-id",
                payload["session_id"],
            )
            uninstall_payload = json.loads(uninstall.stdout)
            assert uninstall_payload["status"] == "ok"
            assert not install_root.exists()
            assert str(install_root) in uninstall_payload["removed_runtime_roots"]

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
                "--codex-cli-mode",
                "install",
                "--runtime-target",
                self.supported_runtime_target,
                "--github-skill-repo",
                "git@github.com:test/octopus-os-skills.git",
                "--github-auth-mode",
                "ssh",
                "--acknowledge-github-control-risk",
                check=False,
            )

            assert install.returncode != 0
            payload = json.loads(install.stdout)
            assert payload["status"] == "error"
            assert "not clean" in payload["error"]

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

            assert install.returncode != 0
            payload = json.loads(install.stdout)
            assert payload["status"] == "error"
            assert self.supported_runtime_target in payload["error"]

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

            assert install.returncode != 0
            payload = json.loads(install.stdout)
            assert payload["status"] == "error"
            assert "--github-skill-repo" in payload["error"]
