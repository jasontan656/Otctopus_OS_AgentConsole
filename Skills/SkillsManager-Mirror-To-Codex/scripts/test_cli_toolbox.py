from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "Cli_Toolbox.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


class CliToolboxTests(unittest.TestCase):
    def test_runtime_contract_returns_new_shape_payload(self) -> None:
        completed = run_cli("runtime-contract", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["skill_name"], "SkillsManager-Mirror-To-Codex")
        self.assertEqual(payload["root_shape"], ["SKILL.md", "path", "agents", "scripts"])
        self.assertIn("read-contract-context", payload["commands"])

    def test_read_contract_context_compiles_push_chain(self) -> None:
        completed = run_cli("read-contract-context", "--entry", "push_sync", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("path/push_sync/15_TOOLS.md", payload["resolved_chain"])

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

            completed = run_cli(
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

            completed = run_cli(
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

            completed = run_cli(
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

            completed = run_cli(
                "--scope",
                "skill",
                "--skill-name",
                ".system/../skill-creator",
                "--mirror-root",
                str(mirror_root),
                "--codex-root",
                str(codex_root),
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

            completed = run_cli(
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
            self.assertEqual(payload["removed_forbidden_entries"], [str(codex_root / "AGENTS.md")])

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

            completed = run_cli(
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
            self.assertEqual(payload["removed_forbidden_entries"], [str(codex_root / "AGENTS.md")])

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

            completed = run_cli(
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
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["resolved_mode"], "rename")
            self.assertEqual(payload["rename_from"], "Meta-browser-operation")
            self.assertEqual(payload["destination"], str(new_destination))
            self.assertTrue(payload["renamed_path"])
            self.assertFalse(old_destination.exists())
            self.assertTrue(new_destination.exists())
            self.assertEqual((new_destination / "SKILL.md").read_text(encoding="utf-8"), "new-skill\n")
            self.assertFalse((new_destination / "stale.txt").exists())

    def test_rename_mode_requires_rename_from(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_root = Path(tmp) / "mirror"
            codex_root = Path(tmp) / "codex"
            source_skill = mirror_root / "Skills" / "WorkFlow-RealState-Posting-Web"
            source_skill.mkdir(parents=True)
            codex_root.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("new-skill\n", encoding="utf-8")

            completed = run_cli(
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
            )

            self.assertNotEqual(completed.returncode, 0)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("--rename-from", payload["error"])


if __name__ == "__main__":
    unittest.main()
