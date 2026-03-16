from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from tests.support_cli import create_runtime_layout, run_cli, runtime_scope, workspace_tempdir


sys_path_ready = True


class TestRuntimeContracts:
    def test_workflow_contract_uses_docs_root_as_single_work_root(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("workflow-contract", *runtime_scope(layout))
        assert payload["stage_order"] == [
            "mother_doc_audit",
            "mother_doc",
            "construction_plan",
            "implementation",
            "acceptance",
        ]
        assert "mother-doc-refresh-root-index" in payload["stage_specific_contract_tools"]
        assert "mother-doc-audit" in payload["stage_specific_contract_tools"]
        assert "mother-doc-mark-modified" in payload["stage_specific_contract_tools"]
        assert payload["target_runtime_contract"]["docs_root"].endswith("/sample_repo/Development_Docs")
        assert payload["top_level_resident_docs"][0] == "path/development_loop/10_CONTRACT.md"

    def test_runtime_contract_and_read_contract_context_follow_new_skill_shape(self) -> None:
        payload = run_cli("contract")
        assert payload["skill_profile"]["tooling_surface"] == "automation_cli"
        assert "references" in payload["root_shape"]
        compiled = run_cli(
            "read-contract-context",
            "--entry",
            "development_loop",
            "--selection",
            "mother_doc,scope_and_runtime",
        )
        assert compiled["status"] == "ok"
        assert "path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md" in compiled["resolved_chain"]
        assert any(item.endswith("path/development_loop/steps/mother_doc/10_CONTRACT.md") for item in compiled["resolved_chain"])

    def test_target_runtime_contract_resolves_docs_root_without_extra_module_layer(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("target-runtime-contract", *runtime_scope(layout))
        assert payload["status"] == "pass"
        assert payload["development_docs_root"] == payload["docs_root"]
        assert payload["client_mother_doc_root"].endswith("/sample_repo/Client_Applications/mother_doc")

    def test_stage_checklist_and_contracts_are_stage_scoped(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            checklist = run_cli("stage-checklist", "--stage", "mother_doc_audit", *runtime_scope(layout))
            doc_payload = run_cli("stage-doc-contract", "--stage", "implementation", *runtime_scope(layout))
            command_payload = run_cli("stage-command-contract", "--stage", "mother_doc", *runtime_scope(layout))
            graph_payload = run_cli("stage-graph-contract", "--stage", "mother_doc", *runtime_scope(layout))
        assert checklist["stage"] == "mother_doc_audit"
        assert any("mother-doc-audit" in item for item in checklist["stage_entry_actions"])
        assert "<docs_root>/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*" in doc_payload["stage_docs"]
        assert any("mother-doc-refresh-root-index" in command for command in command_payload["optional_commands"])
        assert "graph-preflight" in graph_payload["recommended_commands"][0]

    def test_graph_preflight_exposes_stable_graph_consumer_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "code_repo"
            repo.mkdir()
            for index in range(5):
                (repo / f"mod_{index}.py").write_text("print('ok')\n", encoding="utf-8")
            payload = run_cli("graph-preflight", "--repo", str(repo), "--allow-missing-index")
        assert payload["graph_consumer_contract_version"] == "1.0"
        assert "--direction upstream" in payload["impact_command"]
