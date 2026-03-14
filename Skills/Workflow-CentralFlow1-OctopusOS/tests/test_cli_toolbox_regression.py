from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from devflow_agents_support import scaffold_and_collect_devflow_agents


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


def create_runtime_layout(root: Path) -> dict[str, Path | str]:
    repo_root = root.resolve()
    codebase_root = repo_root / "sample_repo"
    docs_root = codebase_root / "Development_Docs"
    docs_root.mkdir(parents=True, exist_ok=True)
    return {
        "target_root": repo_root,
        "codebase_root": codebase_root,
        "development_docs_root": docs_root,
        "docs_root": docs_root,
        "module_dir": "sample_repo",
    }


def workspace_tempdir() -> tempfile.TemporaryDirectory[str]:
    return tempfile.TemporaryDirectory(dir="/home/jasontan656/AI_Projects")


def runtime_scope(layout: dict[str, Path | str]) -> tuple[str, ...]:
    return (
        "--target-root",
        str(layout["target_root"]),
        "--development-docs-root",
        str(layout["development_docs_root"]),
        "--docs-root",
        str(layout["docs_root"]),
        "--module-dir",
        str(layout["module_dir"]),
        "--codebase-root",
        str(layout["codebase_root"]),
    )


def init_git_repo(repo_root: Path) -> None:
    repo_root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "Codex"], cwd=repo_root, check=True)
    subprocess.run(["git", "config", "user.email", "codex@example.com"], cwd=repo_root, check=True)


class TestCliToolboxRegression:
    def test_scaffold_and_collect_devflow_agents_accepts_managed_files_machine_contract(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir).resolve()
            docs_root = root / "Development_Docs"
            docs_root.mkdir(parents=True, exist_ok=True)
            machine_path = root / "managed" / "AGENTS_machine.json"
            runtime = {
                "target_root": root,
                "development_docs_root": docs_root,
                "codebase_root": root / "sample_repo",
                "module_dir": "sample_repo",
                "docs_root": docs_root,
                "mother_doc_root": docs_root / "mother_doc",
                "construction_plan_root": docs_root / "mother_doc" / "execution_atom_plan_validation_packs",
                "graph_runtime_root": docs_root / "graph",
                "acceptance_root": docs_root / "mother_doc" / "acceptance",
            }
            calls: list[list[str]] = []

            def fake_run(command: list[str]) -> dict[str, object]:
                calls.append(command)
                if command[1:].count("target-contract"):
                    return {
                        "managed_files": {
                            "human": str(root / "managed" / "AGENTS_human.md"),
                            "machine": str(machine_path),
                        }
                    }
                if command[1:].count("collect"):
                    return {"stage": "collect", "operation_count": 1}
                if command[1:].count("scaffold"):
                    return {"stage": "scaffold", "operation_count": 1}
                raise AssertionError(command)

            monkeypatch.setattr("devflow_agents_support._run_json_command", fake_run)
            payload = scaffold_and_collect_devflow_agents(runtime)

            assert payload["external_agents_path"].endswith("Development_Docs/AGENTS.md")
            assert machine_path.exists()
            machine_payload = json.loads(machine_path.read_text(encoding="utf-8"))
            assert machine_payload["governed_container"]["module_docs_root"].endswith("Development_Docs")
            assert any("collect" in command for command in calls)

    def test_workflow_contract_uses_docs_root_as_single_work_root(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("workflow-contract", *runtime_scope(layout))
        assert payload["stage_order"] == ["mother_doc", "construction_plan", "implementation", "acceptance"]
        assert "mother-doc-mark-modified" in payload["stage_specific_contract_tools"]
        assert payload["target_runtime_contract"]["docs_root"].endswith("/sample_repo/Development_Docs")
        assert payload["target_runtime_contract"]["development_docs_root"].endswith(
            "/sample_repo/Development_Docs"
        )
        assert (
            payload["target_runtime_contract"]["module_dir_role"]
            == "optional_logical_topic_identifier_not_used_as_filesystem_segment"
        )
        assert payload["construction_plan_root"].endswith(
            "sample_repo/Development_Docs/mother_doc/execution_atom_plan_validation_packs"
        )

    def test_target_runtime_contract_resolves_docs_root_without_extra_module_layer(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("target-runtime-contract", *runtime_scope(layout))
        assert payload["status"] == "pass"
        assert payload["docs_root"].endswith("/sample_repo/Development_Docs")
        assert payload["development_docs_root"] == payload["docs_root"]
        assert payload["codebase_root"].endswith("/sample_repo")
        assert payload["mother_doc_root"].endswith("/sample_repo/Development_Docs/mother_doc")
        assert "single governed Development_Docs root" in payload["docs_root_resolution_rule"]

    def test_stage_checklist_for_construction_plan_references_docs_root(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("stage-checklist", "--stage", "construction_plan", *runtime_scope(layout))
        assert payload["stage"] == "construction_plan"
        assert "<docs_root>/mother_doc/execution_atom_plan_validation_packs/ directory" in payload[
            "required_outputs"
        ][0]
        assert "<docs_root>/mother_doc/08_dev_execution_plan.md" in payload["stage_docs"]
        assert payload["resolved_paths"]["docs_root"].endswith("/sample_repo/Development_Docs")

    def test_stage_doc_command_and_graph_contracts_are_stage_scoped(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            doc_payload = run_cli("stage-doc-contract", "--stage", "implementation", *runtime_scope(layout))
            command_payload = run_cli("stage-command-contract", "--stage", "construction_plan", *runtime_scope(layout))
            graph_payload = run_cli("stage-graph-contract", "--stage", "mother_doc", *runtime_scope(layout))
        assert "<docs_root>/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*" in doc_payload[
            "stage_docs"
        ]
        assert "<docs_root>/mother_doc/<source_mother_doc_refs declared by active_pack>" in doc_payload[
            "stage_docs"
        ]
        assert "mother-doc-mark-modified" in command_payload["optional_commands"][2]
        assert "graph-preflight" in graph_payload["recommended_commands"][0]

    def test_target_scaffold_creates_docs_root_artifacts(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("target-scaffold", *runtime_scope(layout))
            assert payload["status"] == "pass"
            assert any(item.endswith("Development_Docs/AGENTS.md") for item in payload["created_or_verified"])
            assert (Path(layout["docs_root"]) / "mother_doc" / "00_index.md").exists()
            assert (
                Path(layout["docs_root"])
                / "mother_doc"
                / "execution_atom_plan_validation_packs"
                / "00_index.md"
            ).exists()
            preview_registry = (
                Path(layout["docs_root"])
                / "mother_doc"
                / "execution_atom_plan_validation_packs"
                / "pack_registry.yaml"
            ).read_text(encoding="utf-8")
            assert "plan_kind: preview_skeleton" in preview_registry

    def test_official_construction_plan_requires_ready_mother_doc(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            completed = run_cli_raw(
                "construction-plan-init",
                "--target",
                str(pack_root),
                "--design-plan",
                str(mother_doc_root / "08_dev_execution_plan.md"),
            )
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["reason"] == "mother_doc_not_ready_for_construction_plan"

    def test_preview_skeleton_is_not_execution_eligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            plan_root = Path(temp_dir) / "packs"
            design_plan = Path(temp_dir) / "08_dev_execution_plan.md"
            completed = run_cli_raw(
                "construction-plan-init",
                "--target",
                str(plan_root),
                "--design-plan",
                str(design_plan),
                "--plan-kind",
                "preview_skeleton",
            )
            assert completed.returncode == 0
            lint_completed = run_cli_raw(
                "construction-plan-lint",
                "--path",
                str(plan_root),
                "--require-execution-eligible",
            )
            assert lint_completed.returncode != 0
            payload = json.loads(lint_completed.stdout)
            assert "execution-eligible lint requires execution_eligible=true" in payload[
                "execution_eligibility_violations"
            ][0]

    def test_construction_plan_lint_detects_design_step_coverage_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            fill_directory_placeholders(mother_doc_root)
            design_plan = mother_doc_root / "08_dev_execution_plan.md"
            design_plan.write_text(
                "\n".join(
                    [
                        "---",
                        "doc_work_state: modified",
                        "doc_pack_refs: []",
                        "doc_id: sample.dev_execution_plan",
                        "doc_type: example_doc",
                        "topic: 08 Design Phase Plan",
                        "anchors: []",
                        "---",
                        "",
                        "# 08 Design Phase Plan",
                        "",
                        "## 1. 阶段总览",
                        "本节明确阶段断言、阶段测试与阶段验收。",
                        "",
                        "| stage_id | stage_goal | stage_assertions | stage_tests | stage_exit_evidence |",
                        "|---|---|---|---|---|",
                        "| `mother_doc` | `shape doc` | `doc passes lint` | `mother-doc-lint` | `lint pass` |",
                        "| `construction_plan` | `write official packs` | `packs cover design steps` | `construction-plan-lint` | `lint pass` |",
                        "| `implementation` | `consume official packs` | `code matches pack` | `tests` | `phase ledger` |",
                        "| `acceptance` | `close delivery` | `evidence linked` | `acceptance-lint` | `report` |",
                        "",
                        "## 2. 设计阶段步骤",
                        "| design_step_id | target_requirement_atoms | dependencies | implementation_actions | stage_assertions | stage_tests | stage_acceptance | live_delivery_witness | rollback_or_risk |",
                        "|---|---|---|---|---|---|---|---|---|",
                        "| `DESIGN-01` | `REQ-01` | none | action 1 | assert 1 | test 1 | accept 1 | witness 1 | risk 1 |",
                        "| `DESIGN-02` | `REQ-02` | DESIGN-01 | action 2 | assert 2 | test 2 | accept 2 | witness 2 | risk 2 |",
                        "",
                        "## 3. 进入 construction_plan 的要求",
                        "- construction_plan_must_separate_from_design_plan: yes",
                        "- construction_plan_expected_focus: official plan only",
                        "- construction_plan_pack_shape_expectation: numbered packs",
                        "- construction_plan_evidence_backfill_expectation: later phase ledgers",
                        "",
                        "## 4. 上线可交付收口",
                        "- delivery_path: local runtime",
                        "- live_witness_expectations: real witness",
                        "- remaining_risk_threshold: explicit only",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            completed = run_cli_raw(
                "construction-plan-init",
                "--target",
                str(pack_root),
                "--design-plan",
                str(design_plan),
                "--plan-kind",
                "official_plan",
            )
            assert completed.returncode == 0
            registry_path = pack_root / "pack_registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["design_step_ids"] = ["DESIGN-01"]
            registry["packs"] = [registry["packs"][0]]
            registry_path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8")
            lint_completed = run_cli_raw("construction-plan-lint", "--path", str(pack_root))
            assert lint_completed.returncode != 0
            payload = json.loads(lint_completed.stdout)
            assert any(
                "official plan missing design steps ['DESIGN-02']" in item
                for item in payload["design_coverage_violations"]
            )

    def test_mother_doc_lint_accepts_tree_first_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            source = target / "01_target_state.md"
            content = source.read_text(encoding="utf-8")
            source.unlink()
            chapter_dir = target / "01_target_state"
            chapter_dir.mkdir()
            (chapter_dir / "00_index.md").write_text(content, encoding="utf-8")
            fill_directory_placeholders(target)
            completed = run_cli_raw("mother-doc-lint", "--path", str(target))
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "pass"

    def test_mother_doc_state_sync_transitions_doc_and_adds_pack_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            fill_directory_placeholders(target)
            payload = run_cli(
                "mother-doc-state-sync",
                "--path",
                str(target),
                "--doc-ref",
                "01_target_state.md",
                "--from-state",
                "modified",
                "--to-state",
                "planned",
                "--pack-ref",
                "01_design_01",
            )
            assert payload["status"] == "pass"
            updated = (target / "01_target_state.md").read_text(encoding="utf-8")
            assert "doc_work_state: planned" in updated
            assert "01_design_01" in updated

    def test_mother_doc_mark_modified_resets_state_and_clears_pack_refs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            fill_directory_placeholders(target)
            run_cli(
                "mother-doc-state-sync",
                "--path",
                str(target),
                "--doc-ref",
                "01_target_state.md",
                "--from-state",
                "modified",
                "--to-state",
                "planned",
                "--pack-ref",
                "01_design_01",
            )
            payload = run_cli(
                "mother-doc-mark-modified",
                "--path",
                str(target),
                "--doc-ref",
                "01_target_state.md",
            )
            assert payload["status"] == "pass"
            updated = (target / "01_target_state.md").read_text(encoding="utf-8")
            assert "doc_work_state: modified" in updated
            assert "doc_pack_refs: []" in updated

    def test_mother_doc_mark_modified_accepts_doc_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            fill_directory_placeholders(target)
            source = target / "01_target_state.md"
            content = source.read_text(encoding="utf-8").replace(
                "doc_id: workflow_centralflow1_octopusos.assets_templates_mother_doc_01_target_state",
                "doc_id: sample.target_state",
            )
            source.write_text(content, encoding="utf-8")
            run_cli(
                "mother-doc-state-sync",
                "--path",
                str(target),
                "--doc-ref",
                "sample.target_state",
                "--from-state",
                "modified",
                "--to-state",
                "planned",
                "--pack-ref",
                "01_design_01",
            )
            payload = run_cli(
                "mother-doc-mark-modified",
                "--path",
                str(target),
                "--doc-ref",
                "sample.target_state",
            )
            assert payload["status"] == "pass"
            assert payload["selected_doc_refs"] == ["01_target_state.md"]
            updated = source.read_text(encoding="utf-8")
            assert "doc_work_state: modified" in updated
            assert "doc_pack_refs: []" in updated

    def test_mother_doc_mark_modified_can_use_git_diff_as_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            docs_root = repo_root / "Development_Docs"
            mother_doc_root = docs_root / "mother_doc"
            init_git_repo(repo_root)
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            fill_directory_placeholders(mother_doc_root)
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo_root, check=True)

            chapter_dir = mother_doc_root / "01_target_state"
            source = mother_doc_root / "01_target_state.md"
            content = source.read_text(encoding="utf-8")
            source.unlink()
            chapter_dir.mkdir()
            (chapter_dir / "00_index.md").write_text(content, encoding="utf-8")
            fill_directory_placeholders(mother_doc_root)
            run_cli(
                "mother-doc-state-sync",
                "--path",
                str(mother_doc_root),
                "--doc-ref",
                "01_target_state/00_index.md",
                "--from-state",
                "modified",
                "--to-state",
                "planned",
                "--pack-ref",
                "01_design_01",
            )
            section_doc = chapter_dir / "10_scope.md"
            section_doc.write_text(
                "\n".join(
                    [
                        "---",
                        "doc_work_state: planned",
                        "doc_pack_refs:",
                        "  - 01_design_01",
                        "---",
                        "# Scope",
                        "",
                        "changed",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = run_cli(
                "mother-doc-mark-modified",
                "--path",
                str(mother_doc_root),
                "--repo-root",
                str(repo_root),
                "--auto-from-git",
            )
            assert payload["status"] == "pass"
            assert "01_target_state/10_scope.md" in payload["git_direct_doc_refs"]
            assert "01_target_state/00_index.md" in payload["git_impact_doc_refs"]
            updated_section = section_doc.read_text(encoding="utf-8")
            updated_index = (chapter_dir / "00_index.md").read_text(encoding="utf-8")
            assert "doc_work_state: modified" in updated_section
            assert "doc_pack_refs: []" in updated_section
            assert "doc_work_state: modified" in updated_index

    def test_mother_doc_mark_modified_ignores_pack_docs_from_git_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            mother_doc_root = repo_root / "Development_Docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs" / "01_pack"
            init_git_repo(repo_root)
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            fill_directory_placeholders(mother_doc_root)
            pack_root.mkdir(parents=True, exist_ok=True)
            (pack_root / "00_index.md").write_text("# Pack\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo_root, check=True)

            (pack_root / "00_index.md").write_text("# Changed Pack\n", encoding="utf-8")
            completed = run_cli_raw(
                "mother-doc-mark-modified",
                "--path",
                str(mother_doc_root),
                "--repo-root",
                str(repo_root),
                "--auto-from-git",
            )
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "fail"
            assert payload["reason"] == "no_doc_refs_selected_for_modified_mark"

    def test_mother_doc_mark_modified_fails_when_no_docs_selected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            fill_directory_placeholders(target)
            completed = run_cli_raw("mother-doc-mark-modified", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["reason"] == "no_doc_refs_selected_for_modified_mark"
