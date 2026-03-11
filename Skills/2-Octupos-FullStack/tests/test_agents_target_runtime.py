from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "scripts")))

from agents_target_runtime import (
    ROOT_RELATIVE_PATH,
    build_default_machine_payload,
    load_target_contract,
    managed_human_path,
    managed_machine_path,
    render_internal_agents_human,
)
from mother_doc_agents_manager import (
    collect_from_scan,
    load_runtime_contract as load_branch_runtime_contract,
    push_agents_tree,
    scan_agents_tree,
)


class AgentsTargetRuntimeTests(unittest.TestCase):
    def _prepare_workspace(self, tmp: str) -> tuple[Path, Path]:
        skill_root = Path(tmp) / "skill"
        workspace_root = Path(tmp) / "Octopus_OS"
        (workspace_root / "Mother_Doc" / "docs").mkdir(parents=True, exist_ok=True)
        (workspace_root / "AGENTS.md").write_text(
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n<part_A>\nroot rule\n</part_A>\n",
            encoding="utf-8",
        )
        return skill_root, workspace_root

    def test_target_contract_returns_managed_pair_and_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            collect_from_scan(skill_root)
            payload = load_target_contract(skill_root, ROOT_RELATIVE_PATH, "agents")
            self.assertEqual(payload["source_path"], str(workspace_root / "AGENTS.md"))
            self.assertEqual(payload["managed_human_path"], str(managed_human_path(skill_root)))
            self.assertEqual(payload["managed_machine_path"], str(managed_machine_path(skill_root)))
            self.assertNotIn("branch_registry_cli", payload["payload_navigation"])

    def test_scan_reports_forbidden_extra_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            extra = workspace_root / "Admin_UI" / "AGENTS.md"
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text("legacy", encoding="utf-8")
            payload = scan_agents_tree(skill_root, workspace_root / "Mother_Doc" / "docs")
            self.assertEqual(payload["managed_external_target"], str(workspace_root / "AGENTS.md"))
            self.assertEqual(payload["extra_agents"], [str(extra)])

    def test_collect_removes_registry_and_index_governance_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            obsolete_dir = skill_root / "assets" / "mother_doc_agents"
            obsolete_dir.mkdir(parents=True, exist_ok=True)
            (obsolete_dir / "registry.json").write_text("{}", encoding="utf-8")
            (obsolete_dir / "index.md").write_text("legacy", encoding="utf-8")
            payload = collect_from_scan(skill_root)
            self.assertFalse((obsolete_dir / "registry.json").exists())
            self.assertFalse((obsolete_dir / "index.md").exists())
            self.assertEqual(payload["source_path"], str(workspace_root / "AGENTS.md"))

    def test_branch_contract_no_longer_declares_registry_or_index(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        payload = load_branch_runtime_contract(skill_root)
        self.assertNotIn("machine_branch_index", payload["runtime_source_policy"])
        self.assertNotIn("branch_registry_command", payload["runtime_entry_commands"])
        self.assertEqual(payload["managed_asset_model"]["managed_human_path"], "assets/managed_targets/Octopus_OS/AGENTS_human.md")

    def test_push_deletes_extra_agents_and_obsolete_branch_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            legacy_extra = workspace_root / "Admin_UI" / "AGENTS.md"
            legacy_extra.parent.mkdir(parents=True, exist_ok=True)
            legacy_extra.write_text("legacy", encoding="utf-8")

            obsolete_dir = skill_root / "assets" / "mother_doc_agents"
            obsolete_dir.mkdir(parents=True, exist_ok=True)
            (obsolete_dir / "registry.json").write_text("{}", encoding="utf-8")

            machine_payload = build_default_machine_payload()
            managed_machine_path(skill_root).parent.mkdir(parents=True, exist_ok=True)
            managed_machine_path(skill_root).write_text(
                json.dumps(machine_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            managed_human_path(skill_root).write_text(
                render_internal_agents_human("root rule", machine_payload),
                encoding="utf-8",
            )

            payload = push_agents_tree(skill_root, workspace_root / "Mother_Doc" / "docs", dry_run=False)
            self.assertFalse(legacy_extra.exists())
            self.assertFalse((obsolete_dir / "registry.json").exists())
            self.assertEqual(payload["pushed_root_agents"], str(workspace_root / "AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
