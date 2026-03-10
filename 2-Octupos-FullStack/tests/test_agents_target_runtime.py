from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "scripts")))

from agents_target_runtime import load_target_contract
from mother_doc_agents_manager import load_runtime_contract as load_branch_runtime_contract


class AgentsTargetRuntimeTests(unittest.TestCase):
    def write_registry(self, skill_root: Path, workspace_root: Path) -> None:
        registry_path = skill_root / "assets" / "mother_doc_agents" / "registry.json"
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "entries": [
                {
                    "scope_branch": "octopus_os_root",
                    "relative_path": "octopus_os_root",
                    "scope_path": str(workspace_root),
                    "agents_source_path": str(workspace_root / "AGENTS.md"),
                    "readme_source_path": str(workspace_root / "README.md"),
                    "readme_management_mode": "template_managed",
                },
                {
                    "scope_branch": "container_roots",
                    "relative_path": "container_roots/Admin_UI",
                    "scope_path": str(workspace_root / "Admin_UI"),
                    "agents_source_path": str(workspace_root / "Admin_UI" / "AGENTS.md"),
                    "readme_source_path": str(workspace_root / "Admin_UI" / "README.md"),
                    "readme_management_mode": "template_managed",
                },
            ]
        }
        registry_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_octopus_root_keeps_only_constitution_lint_turn_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            workspace_root = Path(tmp) / "Octopus_OS"
            (workspace_root / "Admin_UI").mkdir(parents=True)
            self.write_registry(skill_root, workspace_root)

            payload = load_target_contract(skill_root, "octopus_os_root", "agents")
            self.assertEqual(payload["turn_contract"]["status"], "enforced")
            self.assertIn("Constitution lint", " ".join(payload["turn_contract"]["turn_end"]))
            self.assertNotIn("commit-and-push", " ".join(payload["turn_contract"]["turn_end"]))
            self.assertNotIn("Git traceability", " ".join(payload["turn_contract"]["turn_start"]))

    def test_container_root_stays_na(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            workspace_root = Path(tmp) / "Octopus_OS"
            (workspace_root / "Admin_UI").mkdir(parents=True)
            self.write_registry(skill_root, workspace_root)

            payload = load_target_contract(skill_root, "container_roots/Admin_UI", "agents")
            self.assertEqual(payload["turn_contract"]["status"], "n_a")
            self.assertEqual(payload["turn_contract"]["turn_end"], ["N/A"])

    def test_target_contract_exposes_machine_navigation_and_asset_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            workspace_root = Path(tmp) / "Octopus_OS"
            (workspace_root / "Admin_UI").mkdir(parents=True)
            self.write_registry(skill_root, workspace_root)

            payload = load_target_contract(skill_root, "container_roots/Admin_UI", "agents")
            self.assertEqual(payload["managed_asset_model"]["document_shape"]["external_shape"], "thin_runtime_entry_only")
            self.assertIn("branch_registry_cli", payload["payload_navigation"])
            self.assertTrue(payload["rule_source_policy"]["audit_fields_are_not_primary_runtime_instructions"])
            self.assertTrue(payload["managed_asset_model"]["governance_assets"]["runtime_json_path"].endswith("AGENTS.runtime.json"))
            self.assertTrue(payload["managed_asset_model"]["governance_assets"]["template_path"].endswith("templates/container_roots/Admin_UI/AGENTS.md"))

    def test_branch_contract_declares_registry_as_machine_index(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        payload = load_branch_runtime_contract(skill_root)
        self.assertEqual(payload["runtime_source_policy"]["machine_branch_index"], "registry_json")
        self.assertIn("mother-doc-agents-registry --json", payload["runtime_entry_commands"]["branch_registry_command"])
        self.assertIn("governance_mapping_template", payload["template_semantics"])


if __name__ == "__main__":
    unittest.main()
