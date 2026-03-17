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
REPORT_INPUTS = {
    "research": [],
    "architect": ["research/001_research_report.md"],
    "preview": ["research/001_research_report.md", "architect/001_architecture_assessment_report.md"],
    "design": ["research/001_research_report.md", "architect/001_architecture_assessment_report.md", "preview/001_future_shape_preview.md"],
    "impact": [
        "research/001_research_report.md",
        "architect/001_architecture_assessment_report.md",
        "preview/001_future_shape_preview.md",
        "design/001_design_strategy.md",
    ],
    "validation": [
        "research/001_research_report.md",
        "architect/001_architecture_assessment_report.md",
        "preview/001_future_shape_preview.md",
        "design/001_design_strategy.md",
        "impact/001_impact_investigation.md",
        "plan/milestone_packages.yaml",
        "implementation/turn_ledger.yaml",
    ],
    "final_delivery": [
        "research/001_research_report.md",
        "architect/001_architecture_assessment_report.md",
        "preview/001_future_shape_preview.md",
        "design/001_design_strategy.md",
        "impact/001_impact_investigation.md",
        "plan/milestone_packages.yaml",
        "implementation/turn_ledger.yaml",
        "validation/001_acceptance_report.md",
    ],
}
REPORT_SECTIONS = {
    "research": [
        "调研目标与范围",
        "输入资产与当前前提",
        "问题框架与强制追问",
        "证据登记",
        "显式推导链",
        "阶段结论",
        "未收口问题与进入 architect 的门禁",
    ],
    "architect": [
        "阶段目标",
        "消费的前序产物",
        "关键架构问题框架",
        "should change",
        "should not change",
        "架构判断推导链",
        "阶段结论与进入 preview 的门禁",
    ],
    "preview": [
        "阶段目标",
        "消费的前序产物",
        "关键预演问题框架",
        "future shape",
        "behavior delta",
        "failure modes",
        "rollback triggers",
        "预演推导链与进入 design 的门禁",
    ],
    "design": [
        "阶段目标",
        "消费的前序产物",
        "关键设计问题框架",
        "候选路径与取舍",
        "设计推导链",
        "selected strategy",
        "写回对象与进入 impact 的门禁",
    ],
    "impact": [
        "阶段目标",
        "消费的前序产物",
        "关键影响面问题框架",
        "direct scope",
        "indirect scope",
        "latent related",
        "regression surface",
        "影响面推导链与进入 plan 的门禁",
    ],
    "validation": [
        "阶段目标",
        "消费的前序产物",
        "验收问题框架",
        "验收执行与成功反馈",
        "残余风险与可接受副作用",
        "验收推导链",
        "阶段结论与进入 final_delivery 的门禁",
    ],
    "final_delivery": [
        "交付目标",
        "消费的前序产物",
        "对人类的最终结论",
        "关键承接链摘要",
        "剩余风险与后续观察点",
    ],
}


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


def write_closed_task_runtime(task_dir: Path, task_id: str, workspace_root: Path) -> None:
    payload = {
        "task_id": task_id,
        "task_name": task_id,
        "task_slug": task_id.split("_", 1)[1],
        "task_status": "closed",
        "workspace_root": str(workspace_root),
        "created_at": "2026-03-17T00:00:00+00:00",
        "updated_at": "2026-03-17T00:00:00+00:00",
        "current_stage": "final_delivery",
        "current_step": "delivery_brief_archived",
        "ended_stage": "final_delivery",
        "ended_step": "delivery_brief_archived",
        "ended_reason": "completed",
        "resume_hint": "closed",
        "stages": {
            stage: {
                "status": "completed",
                "checklist": [],
            }
            for stage in (
                "research",
                "architect",
                "preview",
                "design",
                "impact",
                "plan",
                "implementation",
                "validation",
                "final_delivery",
            )
        },
    }
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "task_runtime.yaml").write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def write_stage_report(target: Path, stage: str) -> None:
    lines = [f"# {stage} report", ""]
    for section in REPORT_SECTIONS[stage]:
        lines.append(f"## {section}")
        if section == "消费的前序产物":
            lines.extend([f"- `{path}`" for path in REPORT_INPUTS[stage]])
        elif section == "未收口问题与进入 architect 的门禁":
            lines.append("- research 已锁定未收口问题，并把进入 architect 的门禁写清。")
        elif section == "阶段结论与进入 preview 的门禁":
            lines.append("- architect judgement 已完成，preview 可继续消费。")
        elif section == "预演推导链与进入 design 的门禁":
            lines.append("- preview 已把未来形态与失败模式写透，design 可继续消费。")
        elif section == "写回对象与进入 impact 的门禁":
            lines.append("- design 已完成 selected strategy 与对象写回，impact 可继续消费。")
        elif section == "影响面推导链与进入 plan 的门禁":
            lines.append("- impact 已完成 direct/indirect/latent/regression 写回，plan 可继续消费。")
        elif section == "阶段结论与进入 final_delivery 的门禁":
            lines.append("- validation 已形成正式验收结论，final_delivery 可继续消费。")
        else:
            lines.append(f"- {stage} 阶段该节已正式补齐。")
        lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")

class CliToolboxRegressionTest(unittest.TestCase):
    def test_runtime_contract_exposes_nine_stage_workflow(self) -> None:
        result = run_cli("runtime-contract", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["skill_mode"], "executable_workflow_skill")
        self.assertIn("task-runtime-scaffold", payload["commands"])
        self.assertEqual(
            payload["stage_order"],
            ["research", "architect", "preview", "design", "impact", "plan", "implementation", "validation", "final_delivery"],
        )
        self.assertIn("architect_assessment", payload["workspace_layout"])
        self.assertIn("final_delivery", payload["stage_artifacts"])

    def test_read_contract_context_can_descend_to_impact(self) -> None:
        result = run_cli("read-contract-context", "--entry", "analysis_loop", "--selection", "impact", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("path/analysis_loop/steps/impact/00_IMPACT_ENTRY.md", payload["resolved_chain"])

    def test_workspace_scaffold_and_stage_lint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            runtime_root = Path(tmp_dir) / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
            requested_workspace_root = managed_root / "Temporary_Files" / "sample_runtask"
            env = {
                "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
                "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
            }
            scaffold = run_cli_with_env(
                "workspace-scaffold",
                "--workspace-root",
                str(requested_workspace_root),
                "--json",
                env=env,
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
            scaffold_payload = json.loads(scaffold.stdout)
            workspace_root = Path(scaffold_payload["workspace_root"])
            self.assertEqual(workspace_root.name, "001_sample_runtask")
            self.assertEqual(scaffold_payload["requested_workspace_root"], str(requested_workspace_root))

            (workspace_root / "sources").mkdir()
            (workspace_root / "outputs").mkdir()
            (workspace_root / "sources" / "legacy_skill.md").write_text("legacy", encoding="utf-8")
            (workspace_root / "sources" / "evidence_note.md").write_text("evidence", encoding="utf-8")
            (workspace_root / "outputs" / "changed_file.md").write_text("changed", encoding="utf-8")

            manifest_path = workspace_root / "workspace_manifest.yaml"
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            manifest["analysis_id"] = "far-002"
            manifest["intent_summary"] = "九阶段显式闭环升级"
            manifest["current_stage"] = "final_delivery"
            manifest["source_assets"] = [
                {
                    "asset_id": "legacy_skill",
                    "path": "sources/legacy_skill.md",
                    "role": "legacy_skill_snapshot",
                }
            ]
            manifest["target_scope"] = {
                "external_target": "Functional-Analysis-Runtask",
                "local_target": "Otctopus_OS_AgentConsole/Skills/Functional-Analysis-Runtask",
            }
            manifest["stage_status"] = {stage: "completed" for stage in manifest["stage_status"]}
            manifest["writeback_status"] = {
                "current_sync_report": "validation/001_acceptance_report.md",
                "final_delivery_brief": "final_delivery/001_final_delivery_brief.md",
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
                        "relevance": "支撑九阶段升级",
                        "supports": ["research_report"],
                    }
                ]
            }
            evidence_path.write_text(yaml.safe_dump(evidence, sort_keys=False, allow_unicode=True), encoding="utf-8")

            architect_path = workspace_root / "architect" / "assessment.yaml"
            architect = {
                "consumed_stage_reports": ["research/001_research_report.md"],
                "question_framework": ["哪些结构必须改变", "哪些结构必须保留"],
                "judgement_chain": ["先消费 research report", "再收敛 should/should_not"],
                "should_change": ["新增 architect/preview/impact/final_delivery"],
                "should_not_change": ["保留 Human_Work_Zone 与 task runtime gate"],
                "open_questions": ["是否需要额外阶段 lint 约束"],
                "architecture_judgement": "采用单一九阶段主闭环。",
                "evidence_refs": ["ev_001"],
            }
            architect_path.write_text(yaml.safe_dump(architect, sort_keys=False, allow_unicode=True), encoding="utf-8")

            preview_path = workspace_root / "preview" / "projection.yaml"
            preview = {
                "consumed_stage_reports": ["research/001_research_report.md", "architect/001_architecture_assessment_report.md"],
                "question_framework": ["未来形态是什么", "失败模式是什么"],
                "reasoning_chain": ["承接 architect judgement", "推导 future shape 与 rollback triggers"],
                "future_shape": ["九阶段显式链"],
                "behavior_delta": ["新增四个正式阶段"],
                "failure_modes": ["stage_order 未切换"],
                "rollback_triggers": ["runtime-contract stage_order 非九阶段"],
                "evidence_refs": ["ev_001"],
            }
            preview_path.write_text(yaml.safe_dump(preview, sort_keys=False, allow_unicode=True), encoding="utf-8")

            design_path = workspace_root / "design" / "decisions.yaml"
            design = {
                "consumed_stage_reports": [
                    "research/001_research_report.md",
                    "architect/001_architecture_assessment_report.md",
                    "preview/001_future_shape_preview.md",
                ],
                "question_framework": ["应该选哪条设计路径", "为何拒绝其余路径"],
                "decision_mode": "rewrite",
                "seamless_state": "单一九阶段模型，无双轨别名。",
                "decision_chain": ["先消费 research/architect/preview", "再收敛 selected strategy"],
                "decision_items": [
                    {
                        "title": "rewrite runtime stage model",
                        "problem": "旧五阶段结构不足以承载九阶段显式链。",
                        "selected_because": "能够把问题驱动、推导链和重落盘合同迁移到九阶段。",
                        "rationale": "旧五阶段结构不足以承载九阶段显式链。",
                        "derives_from_stage_reports": [
                            "research/001_research_report.md",
                            "architect/001_architecture_assessment_report.md",
                            "preview/001_future_shape_preview.md",
                        ],
                        "rejected_options": ["继续沿用 generic 阶段合同", "只补 markdown 不补 lint"],
                        "blocked_by": [],
                        "evidence_refs": ["ev_001"],
                    }
                ],
                "evidence_refs": ["ev_001"],
            }
            design_path.write_text(yaml.safe_dump(design, sort_keys=False, allow_unicode=True), encoding="utf-8")

            impact_path = workspace_root / "impact" / "impact_map.yaml"
            impact = {
                "task_mode": "WRITE_INTENT",
                "consumed_stage_reports": [
                    "research/001_research_report.md",
                    "architect/001_architecture_assessment_report.md",
                    "preview/001_future_shape_preview.md",
                    "design/001_design_strategy.md",
                ],
                "question_framework": ["哪些对象直接受影响", "哪些对象潜在漏改"],
                "judgement_chain": ["承接 design strategy", "拆分 direct/indirect/latent/regression"],
                "direct_scope": ["SKILL.md", "runtime", "tests"],
                "indirect_scope": ["workflow docs"],
                "latent_related": ["stage artifacts"],
                "validation_or_evidence": ["pytest", "stage-lint"],
                "must_update": ["runtime", "docs", "tests"],
                "must_check_before_edit": ["old stage keywords"],
                "regression_surface": ["runtime-contract", "read-contract-context"],
                "evidence_refs": ["ev_001"],
                "confidence": "high",
                "evidence_gaps": [],
            }
            impact_path.write_text(yaml.safe_dump(impact, sort_keys=False, allow_unicode=True), encoding="utf-8")

            packages_path = workspace_root / "plan" / "milestone_packages.yaml"
            packages = {
                "planning_basis": {
                    "consumed_stage_reports": [
                        "research/001_research_report.md",
                        "architect/001_architecture_assessment_report.md",
                        "preview/001_future_shape_preview.md",
                        "design/001_design_strategy.md",
                        "impact/001_impact_investigation.md",
                    ],
                    "question_framework": ["如何拆 package 才不破坏证据链"],
                    "package_derivation_chain": ["先承接 design/impact", "再生成 implementation 可消费 package"],
                },
                "milestone_packages": [
                    {
                        "package_id": "package_001",
                        "goal": "落地九阶段链",
                        "consumes": ["research/001_research_report.md", "architect/001_architecture_assessment_report.md"],
                        "delivers": ["outputs/changed_file.md"],
                        "validation": ["pytest", "stage-lint"],
                        "derives_from_stage_reports": [
                            "research/001_research_report.md",
                            "architect/001_architecture_assessment_report.md",
                            "preview/001_future_shape_preview.md",
                            "design/001_design_strategy.md",
                            "impact/001_impact_investigation.md",
                        ],
                        "stage_gates": ["前序报告均已完成并可引用", "只允许修改 runtime/docs/tests"],
                        "writeback_targets": ["implementation/turn_ledger.yaml", "workspace_manifest.yaml"],
                        "evidence_expectations": ["至少一条 validation run", "至少一条 evidence ref"],
                        "exit_signals": ["stage-lint all pass", "pytest pass"],
                        "blocked_by": [],
                        "status": "completed",
                    }
                ]
            }
            packages_path.write_text(yaml.safe_dump(packages, sort_keys=False, allow_unicode=True), encoding="utf-8")

            ledger_path = workspace_root / "implementation" / "turn_ledger.yaml"
            ledger = {
                "entries": [
                    {
                        "entry_id": "entry_001",
                        "package_id": "package_001",
                        "action_types": ["implementation", "validation", "state_writeback"],
                        "summary": "重写 runtime 并完成验证",
                        "changed_paths": ["outputs/changed_file.md"],
                        "consumed_stage_reports": [
                            "research/001_research_report.md",
                            "architect/001_architecture_assessment_report.md",
                            "preview/001_future_shape_preview.md",
                            "design/001_design_strategy.md",
                            "impact/001_impact_investigation.md",
                            "plan/milestone_packages.yaml",
                        ],
                        "preflight_checks": ["只消费 active package", "所有前序正式产物已完成"],
                        "derivation_notes": ["实现严格承接 plan package 与前序 reports"],
                        "validation_runs": [
                            {
                                "command": "python3 ./scripts/Cli_Toolbox.py runtime-contract --json",
                                "result": "pass",
                            }
                        ],
                        "evidence_refs": ["ev_001"],
                        "writeback_targets": ["implementation/turn_ledger.yaml", "workspace_manifest.yaml"],
                        "status_updates": ["package_001 completed", "validation completed"],
                        "residual_issues": [],
                    }
                ]
            }
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True), encoding="utf-8")

            for stage, relative in (
                ("research", "research/001_research_report.md"),
                ("architect", "architect/001_architecture_assessment_report.md"),
                ("preview", "preview/001_future_shape_preview.md"),
                ("design", "design/001_design_strategy.md"),
                ("impact", "impact/001_impact_investigation.md"),
                ("validation", "validation/001_acceptance_report.md"),
                ("final_delivery", "final_delivery/001_final_delivery_brief.md"),
            ):
                write_stage_report(workspace_root / relative, stage)

            result = run_cli_with_env("stage-lint", "--workspace-root", str(workspace_root), "--stage", "all", "--json", env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")

    def test_workspace_scaffold_rejects_skill_local_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            runtime_root = Path(tmp_dir) / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
            forbidden_root = SKILL_ROOT / "tmp_artifacts"
            result = run_cli_with_env(
                "workspace-scaffold",
                "--workspace-root",
                str(forbidden_root),
                "--json",
                env={
                    "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
                    "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
                },
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
            requested_workspace_root = managed_root / "Temporary_Files" / "sample_task"

            first = run_cli_with_env(
                "task-runtime-scaffold",
                "--task-name",
                "sample task",
                "--workspace-root",
                str(requested_workspace_root),
                "--json",
                env=env,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            runtime_file = Path(first_payload["task_runtime_file"])
            self.assertTrue(runtime_file.exists())
            self.assertEqual(Path(first_payload["workspace_root"]).name, "001_sample_task")

            gate = run_cli_with_env("task-gate-check", "--json", env=env)
            self.assertNotEqual(gate.returncode, 0)
            gate_payload = json.loads(gate.stdout)
            self.assertEqual(gate_payload["reason"], "unfinished_task_exists")
            self.assertEqual(len(gate_payload["open_tasks"]), 1)

            payload = yaml.safe_load(runtime_file.read_text(encoding="utf-8"))
            payload["task_status"] = "closed"
            payload["current_stage"] = "final_delivery"
            payload["ended_stage"] = "final_delivery"
            payload["ended_step"] = "final_delivery_brief"
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
            second_payload = json.loads(second.stdout)
            self.assertEqual(Path(second_payload["task_root"]).name, "002_follow_up_task")
            self.assertEqual(Path(second_payload["workspace_root"]).name, "002_follow_up_task")

    def test_workspace_scaffold_reuses_existing_numbered_slot_for_same_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            runtime_root = Path(tmp_dir) / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
            workspace_container = managed_root / "Temporary_Files"
            reused_root = workspace_container / "002_stable_task"
            (workspace_container / "010_other_task").mkdir(parents=True)
            reused_root.mkdir(parents=True)
            env = {
                "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
                "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
            }

            first = run_cli_with_env(
                "workspace-scaffold",
                "--workspace-root",
                str(workspace_container / "stable task"),
                "--json",
                env=env,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            self.assertEqual(first_payload["workspace_root"], str(reused_root))

            second = run_cli_with_env(
                "workspace-scaffold",
                "--workspace-root",
                str(workspace_container / "stable task"),
                "--json",
                env=env,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            second_payload = json.loads(second.stdout)
            self.assertEqual(second_payload["workspace_root"], str(reused_root))

    def test_task_runtime_scaffold_reuses_existing_numbered_slot_by_numeric_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            runtime_root = Path(tmp_dir) / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
            workspace_container = managed_root / "Temporary_Files"
            existing_workspace_root = workspace_container / "002_stable_task"
            existing_workspace_root.mkdir(parents=True)
            write_closed_task_runtime(runtime_root / "010_other_task", "010_other_task", workspace_container / "010_other_task")
            env = {
                "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
                "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
            }

            first = run_cli_with_env(
                "task-runtime-scaffold",
                "--task-name",
                "stable task",
                "--workspace-root",
                str(workspace_container / "stable_task"),
                "--json",
                env=env,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            self.assertEqual(Path(first_payload["task_root"]).name, "002_stable_task")
            self.assertEqual(Path(first_payload["workspace_root"]).name, "002_stable_task")
            self.assertFalse(first_payload["reused_existing"])

            second = run_cli_with_env(
                "task-runtime-scaffold",
                "--task-name",
                "stable task",
                "--workspace-root",
                str(workspace_container / "stable_task"),
                "--json",
                env=env,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            second_payload = json.loads(second.stdout)
            self.assertEqual(Path(second_payload["task_root"]).name, "002_stable_task")
            self.assertTrue(second_payload["reused_existing"])

    def test_task_runtime_scaffold_allocates_next_slot_from_numeric_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            managed_root = Path(tmp_dir) / "Human_Work_Zone"
            runtime_root = Path(tmp_dir) / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
            workspace_container = managed_root / "Temporary_Files"
            write_closed_task_runtime(runtime_root / "010_old_task", "010_old_task", workspace_container / "010_old_task")
            (workspace_container / "002_other_task").mkdir(parents=True)
            env = {
                "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT": str(managed_root),
                "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT": str(runtime_root),
            }

            result = run_cli_with_env(
                "task-runtime-scaffold",
                "--task-name",
                "new task",
                "--workspace-root",
                str(workspace_container / "new task"),
                "--json",
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(Path(payload["task_root"]).name, "011_new_task")
            self.assertEqual(Path(payload["workspace_root"]).name, "011_new_task")


if __name__ == "__main__":
    unittest.main()
