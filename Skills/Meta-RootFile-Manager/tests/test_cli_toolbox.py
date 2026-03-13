from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_external_agents(part_a_body: str) -> str:
    return (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n"
    )


def render_internal_human(part_a_body: str, payload: dict) -> str:
    return (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n\n"
        "<part_B>\n\n"
        "```json\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
        "```\n"
        "</part_B>\n"
    )


def payload() -> dict:
    return {
        "entry_role": "repo_runtime_entry",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
        },
    }


class TestCliToolbox:
    def setup_method(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.workspace = self.root / "AI_Projects"
        self.repo_root = self.workspace / "Otctopus_OS_AgentConsole"
        self.skill_root = self.repo_root / "Skills" / "Meta-RootFile-Manager"
        self.installed = self.root / ".codex" / "skills" / "Meta-RootFile-Manager"
        self.runtime = self.workspace / "Codex_Skill_Runtime" / "Meta-RootFile-Manager"

        self._copy_skill_tree()
        self._seed_workspace()
        self._seed_managed_agents()

    def teardown_method(self) -> None:
        self.tempdir.cleanup()

    def _copy_skill_tree(self) -> None:
        src = SCRIPT.parents[1]
        for path in src.rglob("*"):
            if "__pycache__" in path.parts:
                continue
            relative = path.relative_to(src)
            target = self.skill_root / relative
            if path.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                write(target, path.read_text(encoding="utf-8"))

    def _seed_workspace(self) -> None:
        write(self.workspace / "AGENTS.md", render_external_agents("workspace root"))
        write(self.repo_root / "AGENTS.md", render_external_agents("repo root"))
        write(self.repo_root / "README.md", "# Console\n")
        write(self.workspace / "Octopus_OS" / "README.md", "# Octopus\n")
        write(self.repo_root / "CHANGELOG.md", "## 0.1.0\n")
        write(self.repo_root / "CONTRIBUTING.md", "贡献说明\n")
        write(self.repo_root / "SECURITY.md", "security\n")
        write(self.repo_root / "CODE_OF_CONDUCT.md", "be nice\n")
        write(self.repo_root / "LICENSE", "MIT\n")
        write(self.repo_root / ".gitignore", ".venv/\n")
        write(self.workspace / "Octopus_OS" / ".gitignore", ".cache/\n")
        write(self.repo_root / "pytest.ini", "[pytest]\n")
        write(self.repo_root / "requirements-backend_skills.lock.txt", "pytest==8.0.0\n")

    def _seed_managed_agents(self) -> None:
        root_assets = self.skill_root / "assets" / "managed_targets" / "AI_Projects"
        write(root_assets / "AGENTS_human.md", render_internal_human("workspace root", payload()))
        write(root_assets / "AGENTS_machine.json", json.dumps(payload(), ensure_ascii=False, indent=2) + "\n")
        write(
            root_assets / "Otctopus_OS_AgentConsole" / "AGENTS_human.md",
            render_internal_human("repo root", payload()),
        )
        write(
            root_assets / "Otctopus_OS_AgentConsole" / "AGENTS_machine.json",
            json.dumps(payload(), ensure_ascii=False, indent=2) + "\n",
        )

    def _seed_legacy_alias_dir(self) -> None:
        (self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror").mkdir(
            parents=True, exist_ok=True
        )
        (self.installed / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror").mkdir(
            parents=True, exist_ok=True
        )

    def run_cli(self, *args: str, expect_ok: bool = True) -> dict:
        env = os.environ.copy()
        env["MDM_WORKSPACE_ROOT"] = str(self.workspace)
        env["MDM_MIRROR_SKILL_ROOT"] = str(self.skill_root)
        env["MDM_INSTALLED_SKILL_ROOT"] = str(self.installed)
        env["MDM_RUNTIME_ROOT"] = str(self.runtime)
        result = subprocess.run(
            ["python3", str(self.skill_root / "scripts" / "Cli_Toolbox.py"), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        if expect_ok and result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        if not expect_ok and result.returncode == 0:
            raise AssertionError("expected failure")
        return json.loads(result.stdout)

    def test_scan_returns_multiple_channels(self) -> None:
        result = self.run_cli("scan", "--json", "--write-runtime-report")
        channels = {entry["channel_id"] for entry in result["entries"]}
        assert "AGENTS_MD" in channels
        assert "README_MD" in channels
        assert "GITIGNORE" in channels
        assert (self.runtime / "scan" / "latest.json").exists()

    def test_collect_syncs_plain_mapping_and_installed_copy(self) -> None:
        result = self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        assert result["operation_count"] == 1
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        installed = (
            self.installed
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        assert managed.read_text(encoding="utf-8") == "# Console\n"
        assert installed.read_text(encoding="utf-8") == "# Console\n"

    def test_push_writes_plain_mapping_back_to_external(self) -> None:
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        write(managed, "# Updated\n")
        result = self.run_cli("push", "--json", "--source-path", str(self.repo_root / "README.md"))
        assert result["operation_count"] == 1
        assert (self.repo_root / "README.md").read_text(encoding="utf-8") == "# Updated\n"

    def test_target_contract_returns_channel_metadata_for_plain_file(self) -> None:
        self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        result = self.run_cli("target-contract", "--source-path", str(self.repo_root / "README.md"), "--json")
        assert result["channel_id"] == "README_MD"
        assert result["mapping_mode"] == "plain_copy"
        assert result["managed_files"]["mapped"].endswith("README_MD__governed_external.md")

    def test_scaffold_can_open_non_agents_channel(self) -> None:
        target_dir = self.workspace / "NewRepo"
        result = self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "package.json",
        )
        assert result["operation_count"] == 1
        assert (target_dir / "package.json").exists()
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "NewRepo"
            / "PACKAGE_JSON__governed_external.json"
        )
        assert managed.exists()

    def test_lint_detects_plain_mapping_drift(self) -> None:
        self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        write(managed, "# Drift\n")
        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(self.repo_root / "README.md"),
            expect_ok=False,
        )
        assert result["failed_count"] == 1
        assert "managed_mapping_content_drift" in result["failures"][0]["errors"]

    def test_target_contract_keeps_agents_payload(self) -> None:
        result = self.run_cli("target-contract", "--source-path", str(self.repo_root / "AGENTS.md"), "--json")
        assert result["channel_id"] == "AGENTS_MD"
        assert "payload" in result

    def test_collect_prunes_legacy_alias_dir(self) -> None:
        self._seed_legacy_alias_dir()
        result = self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        assert any(item.endswith("Codex_Skills_Mirror") for item in result["removed_legacy_dirs"])
        assert not (
            self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror"
        ).exists()
        assert not (
            self.installed / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror"
        ).exists()
