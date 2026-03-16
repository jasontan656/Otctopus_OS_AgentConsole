from __future__ import annotations

import json
import tempfile
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT.parents[0] / "_shared" / "octopus_os_workflow_runtime" / "tests_support"))

from workflow_doc_support import write_protocol_doc
from workflow_test_support import run_cli, run_cli_raw



def test_contract_and_read_context_are_stage_local() -> None:
    payload = run_cli(SKILL_ROOT, "contract")
    assert payload["active_stage"] == "mother_doc"
    compiled = run_cli(SKILL_ROOT, "read-contract-context", "--entry", "stage_flow")
    assert compiled["status"] == "ok"
    assert "path/stage_flow/00_STAGE_FLOW_ENTRY.md" in compiled["resolved_chain"]


def test_skill_maintenance_entry_compiles() -> None:
    compiled = run_cli(SKILL_ROOT, "read-contract-context", "--entry", "skill_maintenance")
    assert compiled["status"] == "ok"
    assert "path/skill_maintenance/00_SKILL_MAINTENANCE_ENTRY.md" in compiled["resolved_chain"]


def test_mother_doc_lint_and_audit_follow_current_skill_cli() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir) / "docs" / "mother_doc"
        run_cli(SKILL_ROOT, "mother-doc-init", "--target", str(target))
        write_protocol_doc(
            target,
            "10_entry_layer/00_frontend_overview.md",
            title="Frontend Overview",
            summary="前端入口。",
            layer="entry",
        )
        run_cli(SKILL_ROOT, "mother-doc-refresh-root-index", "--path", str(target))
        assert run_cli_raw(SKILL_ROOT, "mother-doc-lint", "--path", str(target)).returncode == 0
        payload = run_cli(SKILL_ROOT, "mother-doc-audit", "--path", str(target))
        assert payload["status"] == "pass"
