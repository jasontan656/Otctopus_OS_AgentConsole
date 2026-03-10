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
    registry_path,
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
        (workspace_root / "AGENTS.md").write_text("[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n<part_A>\nroot rule\n</part_A>\n", encoding="utf-8")
        return skill_root, workspace_root

    def test_target_contract_returns_managed_pair_and_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            collect_from_scan(skill_root)
            payload = load_target_contract(skill_root, ROOT_RELATIVE_PATH, "agents")
            self.assertEqual(payload["source_path"], str(workspace_root / "AGENTS.md"))
            self.assertEqual(payload["managed_human_path"], str(managed_human_path(skill_root)))
            self.assertEqual(payload["managed_machine_path"], str(managed_machine_path(skill_root)))
            self.assertEqual(payload["payload"]["active_scope_policy"]["current_phase"], "root_only_bootstrap")

    def test_scan_reports_forbidden_extra_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            extra = workspace_root / "Admin_UI" / "AGENTS.md"
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text("legacy", encoding="utf-8")
            payload = scan_agents_tree(skill_root, workspace_root / "Mother_Doc" / "docs")
            self.assertEqual(payload["managed_external_targets"], [str(workspace_root / "AGENTS.md")])
            self.assertEqual(payload["extra_agents"], [str(extra)])

    def test_collect_writes_single_registry_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            payload = collect_from_scan(skill_root)
            registry = json.loads(registry_path(skill_root).read_text(encoding="utf-8"))
            self.assertEqual(len(registry["entries"]), 1)
            self.assertEqual(registry["entries"][0]["relative_path"], ROOT_RELATIVE_PATH)
            self.assertEqual(payload["source_path"], str(workspace_root / "AGENTS.md"))

    def test_branch_contract_declares_registry_as_machine_index(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        payload = load_branch_runtime_contract(skill_root)
        self.assertEqual(payload["runtime_source_policy"]["machine_branch_index"], "registry_json")
        self.assertIn("mother-doc-agents-registry --json", payload["runtime_entry_commands"]["branch_registry_command"])
        self.assertIn("governance_mapping_template", payload["template_semantics"])

    def test_push_deletes_extra_agents_and_legacy_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root, workspace_root = self._prepare_workspace(tmp)
            legacy_extra = workspace_root / "Admin_UI" / "AGENTS.md"
            legacy_extra.parent.mkdir(parents=True, exist_ok=True)
            legacy_extra.write_text("legacy", encoding="utf-8")

            runtime_rules = skill_root / "assets" / "mother_doc_agents" / "runtime_rules"
            runtime_rules.mkdir(parents=True, exist_ok=True)
            (runtime_rules / "AGENT_AUDIT.md").write_text("legacy", encoding="utf-8")

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
            self.assertFalse(runtime_rules.exists())
            self.assertEqual(payload["pushed_root_agents"], str(workspace_root / "AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
