from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))


def run_cli(*args: str) -> dict:
    completed = subprocess.run(
        ["python3", str(CLI), *args, "--json"],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


def run_cli_raw(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(CLI), *args, "--json"],
        text=True,
        capture_output=True,
        check=False,
    )


def fill_directory_placeholders(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            content = re.sub(r"```python\n.*?```\n\n", "", content, flags=re.S)
        content = content.replace("replace_me", "resolved_value")
        path.write_text(content + "\n", encoding="utf-8")


class TestCliToolboxRegressionTest:
    def test_workflow_contract_exposes_construction_plan_model(self) -> None:
        payload = run_cli("workflow-contract")
        assert payload["stage_order"] == ["mother_doc", "construction_plan", "implementation", "acceptance"]
        assert "rules/OCTOPUS_SKILL_HARD_RULES.md" in payload["top_level_resident_docs"]
        assert "/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md" in payload["top_level_resident_docs"]
        assert payload["stage_specific_contract_tools"] == [
            "stage-checklist",
            "stage-doc-contract",
            "stage-command-contract",
            "stage-graph-contract",
            "template-index",
        ]
        assert payload["discovery_scope_policy"]["required_startup_sequence"] == [
            "read_mother_doc_index_or_directory",
            "inspect_latest_archived_mother_doc_if_present",
            "run_mother_doc_lint",
            "read_graph_context_for_current_code_reality_when_available",
            "only_then_read_concrete_codebase_files_if_construction_plan_or_implementation_requires_them",
        ]
        assert (
            payload["phase_read_policy"]["single_stage_rule"]
            == "read only the current stage checklist and the artifacts required by that stage"
        )
        assert payload["stage_switch_protocol"][0] == "keep only top_level_resident_docs across stage switches"
        assert "resident_docs" in payload["stage_read_boundaries"]["implementation"]
        assert "stage_docs" in payload["stage_read_boundaries"]["implementation"]
        assert "graph_role" in payload["stage_read_boundaries"]["implementation"]
        assert "drop_on_stage_switch" in payload["stage_read_boundaries"]["implementation"]
        assert "reconcile existing code reality" in payload["stage_graph_roles"]["mother_doc"]["read_policy"]
        assert "decompose execution atom packs" in payload["stage_graph_roles"]["construction_plan"]["read_policy"]
        assert (
            payload["stage_graph_roles"]["implementation"]["read_policy"]
            == "do_not_read_graph_as_a_stage_artifact; implementation must read concrete code directly"
        )
        assert "run graph-postflight" in payload["stage_graph_roles"]["acceptance"]["update_policy"]
        assert "08_dev_execution_plan.md" in payload["mother_doc_required_files"]
        assert "阶段断言" in payload["mother_doc_required_signals"]
        assert "requirement_atom_id" in payload["requirement_atom_required_fields"]
        assert "design_step_id" in payload["design_phase_plan_required_sections"]
        assert "00_index.md" in payload["construction_plan_required_sections"]
        assert "phase_status.jsonl" in payload["construction_plan_required_sections"]
        assert "plan_step_id" in payload["acceptance_required_fields"]
        assert payload["construction_plan_root"].endswith("docs/mother_doc/execution_atom_plan_validation_packs")
        assert payload["construction_plan_index"].endswith("docs/mother_doc/execution_atom_plan_validation_packs/00_index.md")
        assert payload["required_templates"]["mother_doc_root"].endswith("assets/templates/mother_doc")
        assert payload["required_templates"]["construction_plan_root"].endswith(
            "assets/templates/execution_atom_plan_validation_packs"
        )

    def test_stage_checklist_for_construction_plan_focuses_on_separate_execution_plan(self) -> None:
        payload = run_cli("stage-checklist", "--stage", "construction_plan")
        assert payload["stage"] == "construction_plan"
        assert "docs/mother_doc/execution_atom_plan_validation_packs/ directory" in payload["required_outputs"][0]
        assert "rules/OCTOPUS_SKILL_HARD_RULES.md" in payload["resident_docs"]
        assert "docs/mother_doc/08_dev_execution_plan.md" in payload["stage_docs"]
        assert "graph context" in payload["graph_role"]["read_policy"]
        assert any("construction-plan-init" in item for item in payload["stage_entry_actions"])
        assert "separate from mother doc design plan" in payload["stage_exit_gate"][0]
        assert "machine files" in payload["stage_exit_gate"][1]
        assert "mother_doc drafting focus" in payload["drop_on_stage_switch"][0]

    def test_stage_doc_command_and_graph_contracts_are_stage_scoped(self) -> None:
        doc_payload = run_cli("stage-doc-contract", "--stage", "implementation")
        command_payload = run_cli("stage-command-contract", "--stage", "acceptance")
        graph_payload = run_cli("stage-graph-contract", "--stage", "mother_doc")
        assert doc_payload["stage"] == "implementation"
        assert "docs/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*" in doc_payload["stage_docs"]
        assert "acceptance-lint" in command_payload["gate_commands"][0]
        assert "mother-doc-archive" in command_payload["gate_commands"][2]
        assert "read 07_env_and_deploy.md" in command_payload["required_runtime_actions"][0]
        assert "resolve env values and local config from ignored env files" in command_payload["required_runtime_actions"][1]
        assert "simulate at least one human interaction" in command_payload["required_runtime_actions"][4]
        assert (
            "only after local config, build or preview readiness checks, connectivity checks, and simulated human usage"
            in command_payload["needs_real_env_threshold"][0]
        )
        assert "reconcile existing code reality" in graph_payload["graph_role"]["read_policy"]
        assert "graph-preflight" in graph_payload["recommended_commands"][0]

    def test_mother_doc_contracts_require_latest_archive_review_before_refill(self) -> None:
        doc_payload = run_cli("stage-doc-contract", "--stage", "mother_doc")
        command_payload = run_cli("stage-command-contract", "--stage", "mother_doc")
        checklist_payload = run_cli("stage-checklist", "--stage", "mother_doc")
        assert "docs/<latest_NN_slug>/* when present" in checklist_payload["stage_docs"]
        assert "iteration_context_root" in doc_payload
        assert doc_payload["iteration_context_root"] is None
        assert "if a numbered archived mother_doc iteration exists" in command_payload["required_iteration_actions"][0]
        assert "extract inherited target state" in command_payload["required_iteration_actions"][1]
        assert "read graph context after archive review" in command_payload["required_iteration_actions"][2]

    def test_acceptance_lint_defaults_to_mother_doc_acceptance_container(self) -> None:
        import cli_support  # type: ignore

        assert str(cli_support.ACCEPTANCE_ROOT).endswith("docs/mother_doc/acceptance")
        assert str(cli_support.ACCEPTANCE_MATRIX_PATH).endswith(
            "docs/mother_doc/acceptance/acceptance_matrix.md"
        )
        assert str(cli_support.ACCEPTANCE_REPORT_PATH).endswith(
            "docs/mother_doc/acceptance/acceptance_report.md"
        )

    def test_template_index_lists_directory_templates(self) -> None:
        payload = run_cli("template-index")
        assert payload["mother_doc_root"].endswith("assets/templates/mother_doc")
        assert payload["mother_doc_index"].endswith("00_index.md")
        assert payload["mother_doc_dev_execution_plan"].endswith("08_dev_execution_plan.md")
        assert payload["construction_plan_root"].endswith("execution_atom_plan_validation_packs")
        assert payload["execution_atom_pack_template_root"].endswith("PACK_TEMPLATE")
        assert payload["adr_record"].endswith("12_adrs/ADR_TEMPLATE.md")
        assert payload["acceptance_report"].endswith("ACCEPTANCE_REPORT_TEMPLATE.md")

    def test_mother_doc_init_creates_directory_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            payload = run_cli("mother-doc-init", "--target", str(target))
            assert payload["status"] == "pass"
            assert (target / "00_index.md").exists()
            assert (target / "08_dev_execution_plan.md").exists()
            assert (target / "12_adrs" / "ADR_TEMPLATE.md").exists()

    def test_construction_plan_init_creates_plan_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc" / "execution_atom_plan_validation_packs"
            payload = run_cli("construction-plan-init", "--target", str(target))
            assert payload["status"] == "pass"
            assert (target / "00_index.md").exists()
            assert (target / "pack_registry.yaml").exists()
            assert (target / "01_design_01").exists()

    def test_construction_plan_lint_passes_for_filled_directory_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc" / "execution_atom_plan_validation_packs"
            run_cli("construction-plan-init", "--target", str(target))
            fill_directory_placeholders(target)
            completed = run_cli_raw("construction-plan-lint", "--path", str(target))
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "pass"
            assert payload["construction_plan_gate_allowed"]

    def test_construction_plan_lint_fails_for_invalid_pack_manifest_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc" / "execution_atom_plan_validation_packs"
            run_cli("construction-plan-init", "--target", str(target))
            fill_directory_placeholders(target)
            manifest = target / "01_design_01" / "pack_manifest.yaml"
            manifest.write_text(
                "\n".join(
                    [
                        "pack_id: INVALID",
                        "design_step_id: DESIGN-01",
                        "pack_goal: resolved_value",
                        "design_plan_refs:",
                        "  - DESIGN-01",
                        "target_requirement_atoms:",
                        "  - resolved_value",
                        "implementation_actions:",
                        "  - resolved_value",
                        "changed_files_boundary:",
                        "  - resolved_value",
                        "stage_acceptance_target:",
                        "  - resolved_value",
                        "machine_files:",
                        "  inner_phase_plan: wrong.json",
                        "  phase_status_ledger: phase_status.jsonl",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            completed = run_cli_raw("construction-plan-lint", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "fail"
            assert payload["machine_schema_violations"]
            assert "pack_id must match PACK-NN" in "\n".join(payload["machine_schema_violations"])
            assert "machine_files missing keys ['evidence_registry']" in "\n".join(payload["machine_schema_violations"])

    def test_construction_plan_lint_fails_for_invalid_inner_phase_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc" / "execution_atom_plan_validation_packs"
            run_cli("construction-plan-init", "--target", str(target))
            fill_directory_placeholders(target)
            phase_plan = target / "01_design_01" / "inner_phase_plan.json"
            phase_plan.write_text(
                json.dumps(
                    {
                        "pack_id": "PACK-01",
                        "design_step_id": "DESIGN-01",
                        "inner_phases": [
                            {
                                "inner_phase_id": "PHASE-01",
                                "phase_goal": "",
                                "implementation_slice": ["resolved_value"],
                                "validation_slice": ["resolved_value"],
                                "evidence_writeback_slice": ["unknown.txt"],
                                "phase_exit_signal": "resolved_value",
                            },
                            {
                                "inner_phase_id": "PHASE-01",
                                "phase_goal": "resolved_value",
                                "implementation_slice": [],
                                "validation_slice": ["resolved_value"],
                                "evidence_writeback_slice": ["phase_status.jsonl"],
                                "phase_exit_signal": "resolved_value",
                            },
                        ],
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            completed = run_cli_raw("construction-plan-lint", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "fail"
            assert payload["machine_schema_violations"]
            violations = "\n".join(payload["machine_schema_violations"])
            assert "phase_goal must be a non-empty string" in violations
            assert "evidence_writeback_slice has unsupported refs ['unknown.txt']" in violations
            assert "inner_phase_id must be unique" in violations
            assert "implementation_slice must be a non-empty string list" in violations

    def test_mother_doc_archive_renames_to_next_sequence_and_reinits(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_root = Path(temp_dir) / "docs"
            active_root = docs_root / "mother_doc"
            archived_root = docs_root / "01_existing"
            archived_root.mkdir(parents=True)
            run_cli("mother-doc-init", "--target", str(active_root))
            fill_directory_placeholders(active_root)
            payload = run_cli("mother-doc-archive", "--target", str(active_root), "--archive-slug", "demo-project")
            assert payload["status"] == "pass"
            assert (docs_root / "02_demo_project").exists()
            assert (active_root / "00_index.md").exists()

    def test_mother_doc_lint_fails_when_replace_me_or_guidance_remains(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            completed = run_cli_raw("mother-doc-lint", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "fail"
            assert "00_index.md" in payload["files_with_replace_me"]
            assert "08_dev_execution_plan.md" in payload["files_with_replace_me"]

    def test_mother_doc_lint_passes_for_filled_directory_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            fill_directory_placeholders(target)
            completed = run_cli_raw("mother-doc-lint", "--path", str(target))
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "pass"
            assert payload["construction_plan_gate_allowed"]

    def test_mother_doc_lint_rejects_single_file_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "mother_doc.md"
            target.write_text("# single file\n", encoding="utf-8")
            completed = run_cli_raw("mother-doc-lint", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["single_file_input_detected"]
            assert "single-file mother_doc.md is not accepted" in payload["single_file_rejection_hint"]

    def test_mother_doc_lint_detects_forbidden_terms_even_after_fill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            fill_directory_placeholders(target)
            problem_file = target / "01_target_state.md"
            content = problem_file.read_text(encoding="utf-8")
            problem_file.write_text(content + "\n这是一个 mvp。\n", encoding="utf-8")
            completed = run_cli_raw("mother-doc-lint", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert "mvp" in payload["forbidden_term_hits"]

    def test_graph_preflight_skips_missing_index_for_empty_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "empty_repo"
            repo.mkdir()
            payload = run_cli("graph-preflight", "--repo", str(repo), "--allow-missing-index")
            assert not (payload["indexed"])
            assert not (payload["substantial_codebase"])
            assert payload["recommended_action"] == "skip_non_blocking"
            assert payload["default_baseline_mode"] == "empty_baseline"
            assert payload["implementation_source_scope"] == "current_worktree_only"
            assert "reading non-worktree source artifacts as implementation material" in payload[
                "forbidden_non_worktree_actions"
            ]

    def test_graph_preflight_recommends_analyze_for_existing_codebase(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "code_repo"
            repo.mkdir()
            for index in range(5):
                (repo / f"mod_{index}.py").write_text("print('ok')\n", encoding="utf-8")
            payload = run_cli("graph-preflight", "--repo", str(repo), "--allow-missing-index")
            assert not (payload["indexed"])
            assert payload["substantial_codebase"]
            assert payload["recommended_action"] == "run_analyze"
            assert payload["default_baseline_mode"] == "real_codebase"

    def test_acceptance_lint_fails_when_docs_claim_success_before_files_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            matrix = root / "acceptance_matrix.md"
            report = root / "acceptance_report.md"
            matrix.write_text(
                "\n".join(
                    [
                        "# Acceptance Matrix",
                        "",
                        "| requirement_atom_id | implemented | tested | witnessed | blocked_state | evidence_refs | notes |",
                        "|---|---|---|---|---|---|---|",
                        "| `RA-01` | `true` | `true` | `false` | `needs_real_env` | `tests/test_route_shell.tsx`, `src/routes/route_shell.tsx` | invalid |",
                    ]
                ),
                encoding="utf-8",
            )
            report.write_text(
                "\n".join(
                    [
                        "# Acceptance Report",
                        "",
                        "## 2. Plan Step Results",
                        "| plan_step_id | implemented_files | tests_run | real_witnesses | residual_risks |",
                        "|---|---|---|---|---|",
                        "| `STEP-01` | `src/routes/route_shell.tsx` | `tests/test_route_shell.tsx` | `pending` | `pending` |",
                    ]
                ),
                encoding="utf-8",
            )
            completed = run_cli_raw("acceptance-lint", "--matrix-path", str(matrix), "--report-path", str(report))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "fail"
            reasons = {item["reason"] for item in payload["violations"]}
            assert "implemented_true_without_existing_non_doc_evidence" in reasons
            assert "tested_true_without_existing_test_evidence" in reasons

    def test_acceptance_lint_passes_when_paths_exist_and_states_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            frontend_dir = root / "src" / "routes"
            tests_dir = root / "tests"
            frontend_dir.mkdir(parents=True)
            tests_dir.mkdir(parents=True)
            (frontend_dir / "route_shell.tsx").write_text("export const RouteShell = () => null;\n", encoding="utf-8")
            (tests_dir / "test_route_shell.tsx").write_text("export const ok = true;\n", encoding="utf-8")
            matrix = root / "acceptance_matrix.md"
            report = root / "acceptance_report.md"
            matrix.write_text(
                "\n".join(
                    [
                        "# Acceptance Matrix",
                        "",
                        "| requirement_atom_id | implemented | tested | witnessed | blocked_state | evidence_refs | notes |",
                        "|---|---|---|---|---|---|---|",
                        f"| `RA-01` | `true` | `true` | `false` | `clear_to_proceed` | `{frontend_dir / 'route_shell.tsx'}`, `{tests_dir / 'test_route_shell.tsx'}` | valid |",
                    ]
                ),
                encoding="utf-8",
            )
            report.write_text(
                "\n".join(
                    [
                        "# Acceptance Report",
                        "",
                        "## 2. Plan Step Results",
                        "| plan_step_id | implemented_files | tests_run | real_witnesses | residual_risks |",
                        "|---|---|---|---|---|",
                        f"| `STEP-01` | `{frontend_dir / 'route_shell.tsx'}` | `{tests_dir / 'test_route_shell.tsx'}` | `pending` | `pending` |",
                    ]
                ),
                encoding="utf-8",
            )
            completed = run_cli_raw("acceptance-lint", "--matrix-path", str(matrix), "--report-path", str(report))
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "pass"
            assert payload["acceptance_gate_allowed"]
