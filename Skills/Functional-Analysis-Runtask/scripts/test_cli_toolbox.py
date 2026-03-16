from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return run_cli_with_env(*args)


def run_cli_with_env(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=SKILL_ROOT,
        check=False,
        capture_output=True,
        text=True,
        env={**dict(__import__("os").environ), **(env or {})},
    )


class CliToolboxRegressionTest(unittest.TestCase):
    def test_runtime_contract_exposes_workflow_mode(self) -> None:
        result = run_cli("runtime-contract", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["skill_mode"], "executable_workflow_skill")
        self.assertIn("stage-lint", payload["commands"])
        self.assertIn("task-runtime-scaffold", payload["commands"])
        self.assertEqual(payload["stage_order"], ["research", "design", "plan", "implementation", "validation"])

    def test_read_contract_context_can_descend_to_plan(self) -> None:
        result = run_cli("read-contract-context", "--entry", "analysis_loop", "--selection", "plan", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("path/analysis_loop/steps/plan/00_PLAN_ENTRY.md", payload["resolved_chain"])

    def test_workspace_scaffold_and_stage_lint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            workspace_root = managed_root / "Temporary_Files" / "sample_runtask"
            env = {"FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root)}
            scaffold = run_cli_with_env("workspace-scaffold", "--workspace-root", str(workspace_root), "--json", env=env)
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)

            (workspace_root / "sources").mkdir()
            (workspace_root / "outputs").mkdir()
            (workspace_root / "reports").mkdir()
            (workspace_root / "sources" / "legacy_report.md").write_text("legacy", encoding="utf-8")
            (workspace_root / "sources" / "evidence_note.md").write_text("evidence", encoding="utf-8")
            (workspace_root / "outputs" / "changed_file.md").write_text("changed", encoding="utf-8")
            (workspace_root / "reports" / "methodology.md").write_text("report", encoding="utf-8")
            (workspace_root / "reports" / "convergence.md").write_text("plan", encoding="utf-8")

            manifest_path = workspace_root / "workspace_manifest.yaml"
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            manifest["analysis_id"] = "far-001"
            manifest["intent_summary"] = "升级为单技能多阶段 workflow"
            manifest["current_stage"] = "validation"
            manifest["source_assets"] = [
                {
                    "asset_id": "legacy_report",
                    "path": "sources/legacy_report.md",
                    "role": "existing_methodology",
                }
            ]
            manifest["target_scope"] = {
                "external_target": "Functional-Analysis-Runtask",
                "local_target": "Otctopus_OS_AgentConsole/Skills/Functional-Analysis-Runtask",
            }
            manifest["stage_status"] = {stage: "completed" for stage in manifest["stage_status"]}
            manifest["writeback_status"] = {
                "analysis_summary": "reports/methodology.md",
                "convergence_plan": "reports/convergence.md",
                "last_synced_at": "2026-03-16T00:00:00Z",
                "notes": "synced",
            }
            manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")

            evidence_path = workspace_root / "research" / "evidence_registry.yaml"
            evidence = {
                "evidence_items": [
                    {
                        "evidence_id": "ev_001",
                        "kind": "document",
                        "location": "sources/evidence_note.md",
                        "relevance": "支撑新 workflow 设计",
                        "supports": ["decision_workflow_shape"],
                    }
                ]
            }
            evidence_path.write_text(yaml.safe_dump(evidence, sort_keys=False, allow_unicode=True), encoding="utf-8")

            decisions_path = workspace_root / "design" / "architecture_decisions.yaml"
            decisions = {
                "decisions": [
                    {
                        "decision_id": "decision_workflow_shape",
                        "inherited_asset_refs": ["legacy_report"],
                        "evidence_refs": ["ev_001"],
                        "current_baseline_delta": "从 guide_only 升级到 executable workflow",
                        "target_shape": "单技能多阶段",
                        "phase_gate": {
                            "entry_requirements": ["旧资产已锁定"],
                            "exit_signal": "阶段入口与 lint 面已定义",
                        },
                        "status": "completed",
                    }
                ]
            }
            decisions_path.write_text(yaml.safe_dump(decisions, sort_keys=False, allow_unicode=True), encoding="utf-8")

            slices_path = workspace_root / "plan" / "slices.yaml"
            slices = {
                "slices": [
                    {
                        "slice_id": "slice_001",
                        "borrowed_design_refs": ["decision_workflow_shape"],
                        "current_baseline_delta": "新增 path 与 scripts",
                        "expected_effect": "技能具备阶段入口与 lint",
                        "validation_method": "执行 CLI 与测试",
                        "required_evidence": ["ev_001"],
                        "writeback_targets": ["implementation/turn_ledger.yaml"],
                        "exit_signal": "CLI 与测试通过",
                        "status": "completed",
                    }
                ]
            }
            slices_path.write_text(yaml.safe_dump(slices, sort_keys=False, allow_unicode=True), encoding="utf-8")

            ledger_path = workspace_root / "implementation" / "turn_ledger.yaml"
            ledger = {
                "entries": [
                    {
                        "entry_id": "entry_001",
                        "slice_id": "slice_001",
                        "action_types": ["implementation", "validation", "state_writeback"],
                        "summary": "写入 workflow skill 文件并执行验证",
                        "changed_paths": ["outputs/changed_file.md"],
                        "validation_runs": [
                            {
                                "command": "python3 ./scripts/Cli_Toolbox.py runtime-contract --json",
                                "result": "pass",
                            }
                        ],
                        "evidence_refs": ["ev_001"],
                        "status_updates": ["slice_001 completed", "validation completed"],
                        "residual_issues": [],
                    }
                ]
            }
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True), encoding="utf-8")

            result = run_cli_with_env("stage-lint", "--workspace-root", str(workspace_root), "--stage", "all", "--json", env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")

    def test_workspace_scaffold_rejects_skill_local_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            forbidden_root = SKILL_ROOT / "tmp_artifacts"
            result = run_cli_with_env(
                "workspace-scaffold",
                "--workspace-root",
                str(forbidden_root),
                "--json",
                env={"FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root)},
            )
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["reason"], "workspace_root_forbidden_under_skill_root")

    def test_task_runtime_scaffold_blocks_new_task_until_previous_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            runtime_root = Path(tmp_dir) / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
            env = {
                "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
                "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
            }
            workspace_root = managed_root / "Temporary_Files" / "sample_task"

            first = run_cli_with_env(
                "task-runtime-scaffold",
                "--task-name",
                "sample task",
                "--workspace-root",
                str(workspace_root),
                "--json",
                env=env,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            runtime_file = Path(first_payload["task_runtime_file"])
            self.assertTrue(runtime_file.exists())

            gate = run_cli_with_env("task-gate-check", "--json", env=env)
            self.assertNotEqual(gate.returncode, 0)
            gate_payload = json.loads(gate.stdout)
            self.assertEqual(gate_payload["reason"], "unfinished_task_exists")
            self.assertEqual(len(gate_payload["open_tasks"]), 1)

            payload = yaml.safe_load(runtime_file.read_text(encoding="utf-8"))
            payload["task_status"] = "closed"
            payload["current_stage"] = "validation"
            payload["ended_stage"] = "validation"
            payload["ended_step"] = "final_validation"
            payload["ended_reason"] = "completed"
            for stage in payload["stages"].values():
                stage["status"] = "completed"
            runtime_file.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")

            second = run_cli_with_env(
                "task-runtime-scaffold",
                "--task-name",
                "follow up task",
                "--workspace-root",
                str(managed_root / "Temporary_Files" / "follow_up_task"),
                "--json",
                env=env,
            )
            self.assertEqual(second.returncode, 0, second.stderr)


if __name__ == "__main__":
    unittest.main()
