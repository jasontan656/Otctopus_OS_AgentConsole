from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from subagent_support import runtask_validation_summary


def run_cli(*args: str, env: dict[str, str] | None = None) -> dict[str, object]:
    effective_env = os.environ.copy()
    if env:
        effective_env.update(env)
    completed = subprocess.run(
        ["python3", str(CLI_PATH), *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
        env=effective_env,
    )
    return json.loads(completed.stdout)


def scaffold_temp_octopus_root() -> Path:
    temp_dir = Path(tempfile.mkdtemp())
    (temp_dir / "Development_Docs").mkdir(parents=True)
    (temp_dir / "Client_Applications").mkdir(parents=True)
    return temp_dir


def scaffold_temp_runtask_env(tmp_path: Path) -> dict[str, str]:
    managed_root = tmp_path / "Human_Work_Zone"
    runtime_root = tmp_path / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
    managed_root.mkdir(parents=True, exist_ok=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    return {
        "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
        "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
    }


def test_contract_still_routes_self_governance_entry() -> None:
    payload = run_cli("contract")
    assert payload["entries"]["self_governance"]["path"] == "path/self_governance/00_SELF_GOVERNANCE_ENTRY.md"


def test_factory_intake_emits_dynamic_runtask_chain() -> None:
    payload = run_cli(
        "factory-intake",
        "--request-text",
        "把 Workflow-SiteMap-Creation 改造成 factory 后进入 Meta-Enhance-Prompt、tmux subagent 和 Functional-Analysis-Runtask。",
    )
    assert payload["primary_mode"] == "skill_governance"
    assert payload["factory_split"]["must_use_meta_enhance_prompt"] is True
    assert payload["factory_split"]["required_runtask_stages"][0] == "research"
    assert payload["factory_split"]["required_runtask_stages"][-1] == "final_delivery"


def test_intent_enhance_returns_single_intent_block() -> None:
    payload = run_cli(
        "intent-enhance",
        "--request-text",
        "把 Workflow-SiteMap-Creation 改造成 factory 后进入 Meta-Enhance-Prompt、tmux subagent 和 Functional-Analysis-Runtask。",
    )
    assert payload["enhanced_intent"]["final_intent_output"].startswith("INTENT:")
    assert "tmux background terminal" in payload["enhanced_intent"]["final_intent_output"]


def test_runtask_scaffold_initializes_workspace_under_managed_root(tmp_path: Path) -> None:
    env = scaffold_temp_runtask_env(tmp_path)
    payload = run_cli(
        "runtask-scaffold",
        "--request-text",
        "把 Workflow-SiteMap-Creation 改造成 runtask 九阶段闭环。",
        env=env,
    )
    workspace_root = Path(payload["workspace_root"])
    assert workspace_root.exists()
    assert str(workspace_root).startswith(env["FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT"])
    assert Path(payload["task_runtime_file"]).exists()


def test_artifact_refresh_writes_richer_framework_docs() -> None:
    target_root = scaffold_temp_octopus_root()
    snapshot = {
        "factory_payload": {
            "source_digest": "demo",
            "source_excerpt": "刷新实验产物",
        },
        "enhanced_intent": {
            "final_intent_output": "INTENT:\n刷新实验产物并保持九阶段闭环。\n",
        },
        "subagent_run": {"status": "pass"},
        "lint_audit": {"status": "pass"},
    }
    snapshot_file = target_root / "snapshot.json"
    snapshot_file.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
    payload = run_cli(
        "artifact-refresh",
        "--target-root",
        str(target_root),
        "--snapshot-file",
        str(snapshot_file),
    )
    assert payload["status"] == "pass"
    root_doc = target_root / "Development_Docs" / "mother_doc" / "00_governance" / "30_frontmatter_contract.md"
    content = root_doc.read_text(encoding="utf-8")
    assert "artifact_role" in content
    assert payload["lint_audit"]["status"] == "pass"


def test_artifact_refresh_deletes_legacy_manifest_managed_files() -> None:
    target_root = scaffold_temp_octopus_root()
    mother_doc_root = target_root / "Development_Docs" / "mother_doc"
    stale_doc = mother_doc_root / "00_governance" / "10_design_principles.md"
    stale_doc.parent.mkdir(parents=True, exist_ok=True)
    stale_doc.write_text("# stale\n", encoding="utf-8")
    legacy_manifest = mother_doc_root / "90_runtime_governance" / "50_artifact_manifest.json"
    legacy_manifest.parent.mkdir(parents=True, exist_ok=True)
    legacy_manifest.write_text(
        json.dumps(
            {
                "managed_markdown": ["00_governance/10_design_principles.md"],
                "managed_json": ["90_runtime_governance/30_artifact_manifest.json"],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    snapshot_file = target_root / "snapshot.json"
    snapshot_file.write_text(
        json.dumps(
            {
                "factory_payload": {"source_digest": "legacy", "source_excerpt": "refresh"},
                "enhanced_intent": {"final_intent_output": "INTENT:\nrefresh\n"},
                "subagent_run": {"status": "pass"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    payload = run_cli("artifact-refresh", "--target-root", str(target_root), "--snapshot-file", str(snapshot_file))
    assert payload["status"] == "pass"
    assert not stale_doc.exists()


def test_runtask_validation_summary_reads_nested_implementation_ledger(tmp_path: Path) -> None:
    env = scaffold_temp_runtask_env(tmp_path)
    payload = run_cli(
        "runtask-scaffold",
        "--request-text",
        "把 Workflow-SiteMap-Creation 改造成 runtask 九阶段闭环。",
        env=env,
    )
    workspace_root = Path(payload["workspace_root"])
    ledger_path = workspace_root / "implementation" / "turn_ledger.yaml"
    ledger_path.write_text("entries:\n- package_id: pkg_a\n", encoding="utf-8")
    summary = runtask_validation_summary(
        {
            "workspace_root": str(workspace_root),
            "task_runtime_file": payload["task_runtime_file"],
        }
    )
    assert summary["implementation_ledger"]["entries"][0]["package_id"] == "pkg_a"
    assert summary["stage_object_presence"]["implementation_ledger"] is True
