from __future__ import annotations

import tempfile
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT.parents[0] / "_shared" / "octopus_os_workflow_runtime" / "tests_support"))

from workflow_test_support import run_cli, run_cli_raw


def test_contract_and_read_context_are_stage_local() -> None:
    payload = run_cli(SKILL_ROOT, "contract")
    assert payload["active_stage"] == "construction_plan"
    compiled = run_cli(SKILL_ROOT, "read-contract-context", "--entry", "stage_flow")
    assert compiled["status"] == "ok"


def test_construction_plan_init_and_lint_work_from_current_skill() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        pack_root = Path(temp_dir) / "docs" / "mother_doc" / "execution_atom_plan_validation_packs"
        run_cli(SKILL_ROOT, "construction-plan-init", "--target", str(pack_root), "--plan-kind", "preview_skeleton")
        lint_completed = run_cli_raw(SKILL_ROOT, "construction-plan-lint", "--path", str(pack_root))
        assert lint_completed.returncode == 0
