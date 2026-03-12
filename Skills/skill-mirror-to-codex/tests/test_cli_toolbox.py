from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class TestMetaSkillMirrorCliTests:
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
            assert payload["status"] == "ok"
            assert payload["resolved_mode"] == "push"
            assert payload["skill_name"] == ".system/skill-creator"
            assert payload["source_skill_name"] == ".system/Skill-creator"
            assert payload["destination_skill_name"] == ".system/skill-creator"
            assert payload["source"] == str(source_skill)
            assert payload["destination"] == str(destination_skill)

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
            assert payload["status"] == "route_required"
            assert payload["resolved_mode"] == "install"
            assert payload["source_skill_name"] == ".system/Skill-installer"
            assert payload["destination_skill_name"] == ".system/skill-installer"
            assert payload["destination"] == str(codex_root / ".system" / "skill-installer")

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
            assert payload["resolved_mode"] == "push"
            assert payload["source_skill_name"] == "families/Custom-Skill"
            assert payload["destination_skill_name"] == "families/Custom-Skill"

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

            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "error"
            assert "dot traversal" in payload["error"]

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
            assert payload["status"] == "ok"
            assert payload["resolved_mode"] == "push"
            assert payload["scope"] == "all"
            assert payload["skills_root"] == str(skills_root)
            assert [entry["root_name"] for entry in payload["synced_entries"]] == [
                ".system",
                "Meta-Impact-Investigation",
            ]
            assert all("docs" not in " ".join(command) for command in payload["commands"])
            assert all("product_tools" not in " ".join(command) for command in payload["commands"])
            assert payload["removed_forbidden_entries"] == [str(codex_root / "AGENTS.md")]

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
            assert payload["status"] == "ok"
            assert not (codex_root / "AGENTS.md").exists()
            assert payload["removed_forbidden_entries"] == [str(codex_root / "AGENTS.md")]

    def test_rename_mode_replaces_old_destination_and_renames_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            source_skill = mirror_root / "Skills" / "WorkFlow-RealState-Posting-Web"
            old_destination = codex_root / "Meta-browser-operation"
            source_skill.mkdir(parents=True)
            old_destination.mkdir(parents=True)
            codex_root.mkdir(parents=True, exist_ok=True)
            (source_skill / "SKILL.md").write_text("new-skill\n", encoding="utf-8")
            (source_skill / "new.txt").write_text("new\n", encoding="utf-8")
            (old_destination / "SKILL.md").write_text("old-skill\n", encoding="utf-8")
            (old_destination / "stale.txt").write_text("stale\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "skill",
                "--skill-name",
                "WorkFlow-RealState-Posting-Web",
                "--mode",
                "rename",
                "--rename-from",
                "Meta-browser-operation",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
            )

            payload = json.loads(completed.stdout)
            new_destination = codex_root / "WorkFlow-RealState-Posting-Web"
            assert payload["status"] == "ok"
            assert payload["resolved_mode"] == "rename"
            assert payload["rename_from"] == "Meta-browser-operation"
            assert payload["destination"] == str(new_destination)
            assert payload["renamed_path"]
            assert not (old_destination.exists())
            assert new_destination.exists()
            assert (new_destination / "SKILL.md").read_text(encoding="utf-8") == "new-skill\n"
            assert not (new_destination / "stale.txt").exists()

    def test_rename_mode_requires_rename_from(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            source_skill = mirror_root / "Skills" / "WorkFlow-RealState-Posting-Web"
            source_skill.mkdir(parents=True)
            codex_root.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("new-skill\n", encoding="utf-8")

            completed = self.run_cli(
                "--scope",
                "skill",
                "--skill-name",
                "WorkFlow-RealState-Posting-Web",
                "--mode",
                "rename",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
                check=False,
            )

            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "error"
            assert "--rename-from" in payload["error"]
