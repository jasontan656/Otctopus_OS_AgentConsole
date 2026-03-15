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
from target_runtime_support import resolve_target_runtime


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


def write_protocol_doc(
    root: Path,
    relative_path: str,
    *,
    title: str,
    summary: str,
    layer: str,
    doc_id: str | None = None,
    doc_role: str | None = None,
    doc_kind: str | None = None,
    content_family: str | None = None,
    branch_family: str | None = None,
    state: str = "modified",
    pack_refs: list[str] | None = None,
    always_read: bool = False,
    anchors_down: list[str] | None = None,
    anchors_support: list[str] | None = None,
    body_lines: list[str] | None = None,
) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    inferred_doc_kind = doc_kind
    inferred_content_family = content_family
    inferred_branch_family = branch_family
    if doc_role == "root_index":
        inferred_doc_kind = inferred_doc_kind or "trunk_node"
        inferred_content_family = inferred_content_family or "root_index_auto"
    else:
        if layer == "overview":
            inferred_doc_kind = inferred_doc_kind or "trunk_node"
            inferred_content_family = inferred_content_family or "overview_narrative"
        elif layer == "entry":
            inferred_doc_kind = inferred_doc_kind or "branch_root"
            inferred_content_family = inferred_content_family or "branch_overview"
            inferred_branch_family = inferred_branch_family or "domain_branch"
        elif layer == "resolution":
            inferred_doc_kind = inferred_doc_kind or "branch_root"
            inferred_content_family = inferred_content_family or "layer_taxonomy_root"
            inferred_branch_family = inferred_branch_family or "framework_branch"
        elif layer == "capability":
            inferred_doc_kind = inferred_doc_kind or "trunk_node"
            inferred_content_family = inferred_content_family or "layer_item_doc"
        else:
            inferred_doc_kind = inferred_doc_kind or "trunk_node"
            inferred_content_family = inferred_content_family or "container_item_doc"

    frontmatter_lines = [
        "---",
        f"doc_work_state: {state}",
        f"doc_pack_refs: {json.dumps(pack_refs or [], ensure_ascii=False)}",
    ]
    if doc_id is not None:
        frontmatter_lines.append(f"doc_id: {doc_id}")
    if doc_role is not None:
        frontmatter_lines.append(f"doc_role: {doc_role}")
    frontmatter_lines.append(f"doc_kind: {inferred_doc_kind}")
    frontmatter_lines.append(f"content_family: {inferred_content_family}")
    if inferred_branch_family is not None:
        frontmatter_lines.append(f"branch_family: {inferred_branch_family}")
    frontmatter_lines.extend(
        [
            f"thumb_title: {title}",
            f"thumb_summary: {summary}",
            f"display_layer: {layer}",
            f"always_read: {'true' if always_read else 'false'}",
            f"anchors_down: {json.dumps(anchors_down or [], ensure_ascii=False)}",
            f"anchors_support: {json.dumps(anchors_support or [], ensure_ascii=False)}",
            "---",
            "",
        ]
    )
    if inferred_content_family == "root_index_auto":
        default_body = [
            f"# {title}",
            "",
            "## 当前职责",
            "- 作为测试 fixture 的根入口。",
            "",
            "## 自动目录结构图",
            "```text",
            "mother_doc/",
            "```",
            "",
            "## 自动目录清单",
            "- `fixture/`",
            "",
            "## 根入口约束",
            "- `doc_role` 必须为 `root_index`。",
            "",
        ]
    else:
        default_body = [
            f"# {title}",
            "",
            "## 来源",
            "- `test_fixture`",
            "",
            "## 当前节点职责",
            f"- {summary}",
            "",
            "## 当前内容",
            f"- {summary}",
            "",
            "## 当前延伸规则",
            "- 当前 fixture 允许继续按注册规则扩展。",
            "",
            "## 当前延伸边界",
            "- 当前 fixture 不跨同层互连。",
            "",
            "## 当前承载边界",
            "- 当前 fixture 只承载本节点语义。",
            "",
            "## 当前规则",
            f"- {summary}",
            "",
            "## 当前配置",
            "- `fixture: true`",
            "",
        ]
    path.write_text(
        "\n".join(frontmatter_lines + (body_lines or default_body)) + "\n",
        encoding="utf-8",
    )
    return path


def write_design_plan_doc(root: Path, relative_path: str = "08_design_plan.md") -> Path:
    return write_protocol_doc(
        root,
        relative_path,
        title="Design Plan",
        summary="定义阶段目标与 design_step 的官方设计计划文档。",
        layer="design",
        doc_role="design_plan",
        body_lines=[
            "# Design Plan",
            "",
            "## 1. 阶段总览",
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
        ],
    )


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
    def test_resolve_target_runtime_defaults_to_octopus_os_repo_root_when_present(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir).resolve()
            octopus_root = workspace_root / "Octopus_OS"
            docs_root = octopus_root / "Development_Docs"
            docs_root.mkdir(parents=True, exist_ok=True)
            monkeypatch.setattr("target_runtime_support.WORKSPACE_ROOT", workspace_root)
            monkeypatch.setattr("target_runtime_support.ROOT_AGENTS_PATH", workspace_root / "AGENTS.md")

            runtime = resolve_target_runtime()

        assert runtime["target_root"] == octopus_root
        assert runtime["codebase_root"] == octopus_root
        assert runtime["docs_root"] == docs_root
        assert runtime["development_docs_root"] == docs_root
        assert runtime["mother_doc_root"] == docs_root / "mother_doc"
        assert runtime["client_mother_doc_root"] == octopus_root / "Client_Applications" / "mother_doc"
        assert runtime["acceptance_root"] == docs_root / "mother_doc" / "acceptance"

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
        assert "mother-doc-refresh-root-index" in payload["stage_specific_contract_tools"]
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
        assert payload["top_level_resident_docs"][0] == "path/development_loop/10_CONTRACT.md"

    def test_runtime_contract_and_read_contract_context_follow_new_skill_shape(self) -> None:
        payload = run_cli("runtime-contract")
        assert payload["root_shape"] == ["SKILL.md", "path", "agents", "scripts"]
        compiled = run_cli("read-contract-context", "--entry", "development_loop", "--selection", "mother_doc,scope_and_runtime")
        assert compiled["status"] == "ok"
        assert "path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md" in compiled["resolved_chain"]
        assert any(item.endswith("path/development_loop/steps/mother_doc/10_CONTRACT.md") for item in compiled["resolved_chain"])

    def test_target_runtime_contract_resolves_docs_root_without_extra_module_layer(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("target-runtime-contract", *runtime_scope(layout))
        assert payload["status"] == "pass"
        assert payload["docs_root"].endswith("/sample_repo/Development_Docs")
        assert payload["development_docs_root"] == payload["docs_root"]
        assert payload["codebase_root"].endswith("/sample_repo")
        assert payload["mother_doc_root"].endswith("/sample_repo/Development_Docs/mother_doc")
        assert payload["client_mother_doc_root"].endswith("/sample_repo/Client_Applications/mother_doc")
        assert "single governed Development_Docs root" in payload["docs_root_resolution_rule"]

    def test_mother_doc_sync_client_copy_brutally_overwrites_viewer_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "Octopus_OS"
            docs_root = repo_root / "Development_Docs"
            mother_doc_root = docs_root / "mother_doc"
            client_mother_doc_root = repo_root / "Client_Applications" / "mother_doc"
            docs_root.mkdir(parents=True, exist_ok=True)
            write_protocol_doc(
                mother_doc_root,
                "00_index.md",
                title="Root Index",
                summary="root placeholder",
                layer="overview",
                doc_role="root_index",
                always_read=True,
            )
            write_protocol_doc(
                mother_doc_root,
                "10_flow.md",
                title="Flow Entry",
                summary="source truth doc",
                layer="entry",
            )
            write_protocol_doc(
                client_mother_doc_root,
                "99_stale.md",
                title="Stale Node",
                summary="should be removed",
                layer="legacy",
            )

            payload = run_cli(
                "mother-doc-sync-client-copy",
                "--target-root",
                str(repo_root),
                "--development-docs-root",
                str(docs_root),
                "--docs-root",
                str(docs_root),
                "--codebase-root",
                str(repo_root),
            )

            assert payload["status"] == "pass"
            assert payload["source_root"] == str(mother_doc_root)
            assert payload["mirror_root"] == str(client_mother_doc_root)
            assert (client_mother_doc_root / "00_index.md").exists()
            assert (client_mother_doc_root / "10_flow.md").exists()
            assert not (client_mother_doc_root / "99_stale.md").exists()

    def test_stage_checklist_for_construction_plan_references_docs_root(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("stage-checklist", "--stage", "construction_plan", *runtime_scope(layout))
        assert payload["stage"] == "construction_plan"
        assert "<docs_root>/mother_doc/execution_atom_plan_validation_packs/ directory" in payload[
            "required_outputs"
        ][0]
        assert any("doc_work_state=modified|planned|ref" in item for item in payload["stage_docs"])
        assert payload["resolved_paths"]["docs_root"].endswith("/sample_repo/Development_Docs")

    def test_stage_doc_command_and_graph_contracts_are_stage_scoped(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            doc_payload = run_cli("stage-doc-contract", "--stage", "implementation", *runtime_scope(layout))
            command_payload = run_cli("stage-command-contract", "--stage", "construction_plan", *runtime_scope(layout))
            mother_doc_command_payload = run_cli("stage-command-contract", "--stage", "mother_doc", *runtime_scope(layout))
            graph_payload = run_cli("stage-graph-contract", "--stage", "mother_doc", *runtime_scope(layout))
        assert "<docs_root>/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*" in doc_payload[
            "stage_docs"
        ]
        assert "<docs_root>/mother_doc/<source_mother_doc_refs declared by active_pack>" in doc_payload[
            "stage_docs"
        ]
        assert any("mother-doc-mark-modified" in command for command in command_payload["optional_commands"])
        assert any(
            "mother-doc-refresh-root-index" in command
            for command in mother_doc_command_payload["optional_commands"]
        )
        assert "graph-preflight" in graph_payload["recommended_commands"][0]

    def test_target_scaffold_creates_docs_root_artifacts(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("target-scaffold", *runtime_scope(layout))
            assert payload["status"] == "pass"
            assert any(item.endswith("Development_Docs/AGENTS.md") for item in payload["created_or_verified"])
            assert (Path(layout["docs_root"]) / "mother_doc" / "00_index.md").exists()
            assert not (
                Path(layout["docs_root"])
                / "mother_doc"
                / "execution_atom_plan_validation_packs"
            ).exists()

    def test_official_construction_plan_requires_ready_mother_doc(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            completed = run_cli_raw(
                "construction-plan-init",
                "--target",
                str(pack_root),
            )
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["reason"] == "modified_doc_missing"

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
            assert any(
                "execution_eligible=true" in item for item in payload["execution_eligibility_violations"]
            )

    def test_construction_plan_lint_detects_design_step_coverage_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            write_protocol_doc(
                mother_doc_root,
                "00_index.md",
                title="Root Index",
                summary="root placeholder",
                layer="overview",
                doc_role="root_index",
                always_read=True,
                state="ref",
                pack_refs=["00_done"],
            )
            write_protocol_doc(
                mother_doc_root,
                "10_entry_layer/00_http_entry.md",
                title="HTTP Entry",
                summary="处理 HTTP 入口。",
                layer="resolution",
                anchors_down=["20_resolution_layer/00_access_resolution.md"],
            )
            write_protocol_doc(
                mother_doc_root,
                "20_resolution_layer/00_access_resolution.md",
                title="Access Resolution",
                summary="处理入口后的首站解析。",
                layer="capability",
            )
            write_protocol_doc(
                mother_doc_root,
                "30_support_layer/00_delivery.md",
                title="Delivery Node",
                summary="独立的交付支撑节点。",
                layer="support",
            )
            run_cli("mother-doc-refresh-root-index", "--path", str(mother_doc_root))
            completed = run_cli_raw(
                "construction-plan-init",
                "--target",
                str(pack_root),
                "--plan-kind",
                "official_plan",
            )
            assert completed.returncode == 0
            registry_path = pack_root / "pack_registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["design_step_ids"] = [registry["design_step_ids"][0]]
            registry["packs"] = [registry["packs"][0]]
            registry_path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8")
            lint_completed = run_cli_raw("construction-plan-lint", "--path", str(pack_root))
            assert lint_completed.returncode != 0
            payload = json.loads(lint_completed.stdout)
            assert any(
                "registry missing pack entries for directories" in item
                or "registry missing pack entries for design_step_ids" in item
                for item in payload["design_coverage_violations"]
            )

    def test_mother_doc_lint_accepts_tree_first_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            chapter_dir = target / "01_target_state"
            chapter_dir.mkdir()
            write_protocol_doc(
                target,
                "01_target_state/00_index.md",
                title="Target State",
                summary="定义当前目标态的章节根。",
                layer="capability",
                doc_id="sample.target_state.index",
                body_lines=[
                    "# Target State",
                    "",
                    "## 来源",
                    "- `test_fixture`",
                    "",
                    "## 当前节点职责",
                    "- 定义目标态。",
                    "",
                    "## 当前内容",
                    "- 这是目标态章节根。",
                    "",
                    "## 当前延伸边界",
                    "- 当前 fixture 不跨同层互连。",
                    "",
                ],
            )
            run_cli("mother-doc-refresh-root-index", "--path", str(target))
            completed = run_cli_raw("mother-doc-lint", "--path", str(target))
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "pass"

    def test_mother_doc_lint_rejects_legacy_directional_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            legacy_doc = target / "10_entry_layer" / "10_backend_overview.md"
            legacy_doc.parent.mkdir(parents=True, exist_ok=True)
            legacy_doc.write_text(
                "\n".join(
                    [
                        "---",
                        "doc_work_state: modified",
                        "doc_pack_refs: []",
                        "thumb_title: Backend Overview",
                        "thumb_summary: 后端总览。",
                        "display_layer: entry",
                        "layer: legacy_entry",
                        "always_read: false",
                        "anchors_up: []",
                        "anchors_right: []",
                        "anchors_down: []",
                        "anchors_left: []",
                        "anchors_support: []",
                        "---",
                        "",
                        "# Backend Overview",
                        "",
                        "## 当前职责",
                        "后端总览。",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            run_cli("mother-doc-refresh-root-index", "--path", str(target))

            completed = run_cli_raw("mother-doc-lint", "--path", str(target))

            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            violations = payload["frontmatter_violations"]["10_entry_layer/10_backend_overview.md"]
            assert any("forbidden_frontmatter_fields_present" in item for item in violations)

    def test_mother_doc_lint_rejects_multi_parent_traversal_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(
                target,
                "10_entry_layer/00_frontend_overview.md",
                title="Frontend Overview",
                summary="前端总览。",
                layer="entry",
                anchors_down=["20_resolution_layer/00_frontend_layers.md"],
            )
            write_protocol_doc(
                target,
                "10_entry_layer/10_backend_overview.md",
                title="Backend Overview",
                summary="后端总览。",
                layer="entry",
                anchors_down=["20_resolution_layer/00_frontend_layers.md"],
            )
            write_protocol_doc(
                target,
                "20_resolution_layer/00_frontend_layers.md",
                title="Frontend Layers",
                summary="前端层级定义。",
                layer="resolution",
            )
            run_cli("mother-doc-refresh-root-index", "--path", str(target))

            completed = run_cli_raw("mother-doc-lint", "--path", str(target))

            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["traversal_violations"]
            assert any(
                "multi_parent_target_forbidden=20_resolution_layer/00_frontend_layers.md" in item
                for violations in payload["traversal_violations"].values()
                for item in violations
            )

    def test_mother_doc_refresh_root_index_renders_folder_only_structure_graph(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(
                target,
                "10_entry_layer/10_backend_overview.md",
                title="Backend Overview",
                summary="后端总览。",
                layer="entry",
            )
            write_protocol_doc(
                target,
                "20_resolution_layer/10_backend_layer_definition.md",
                title="Backend Layers",
                summary="后端层级定义。",
                layer="resolution",
            )

            payload = run_cli("mother-doc-refresh-root-index", "--path", str(target))

            assert payload["status"] == "pass"
            assert payload["folder_refs"] == ["10_entry_layer/", "20_resolution_layer/"]
            index_content = (target / "00_index.md").read_text(encoding="utf-8")
            assert "## 自动目录结构图" in index_content
            assert "mother_doc/" in index_content
            assert "10_entry_layer/" in index_content
            assert "20_resolution_layer/" in index_content
            assert "10_backend_overview.md" not in index_content

    def test_mother_doc_lint_fails_when_root_index_is_out_of_sync_with_folder_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(
                target,
                "10_entry_layer/10_backend_overview.md",
                title="Backend Overview",
                summary="后端总览。",
                layer="entry",
            )

            completed = run_cli_raw("mother-doc-lint", "--path", str(target))

            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert "root_index_out_of_sync_with_folder_structure" in payload["root_index_violations"]

    def test_official_construction_plan_groups_modified_docs_without_single_design_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            write_protocol_doc(
                mother_doc_root,
                "10_entry_layer/00_backend_overview.md",
                title="Backend Overview",
                summary="后端总览。",
                layer="entry",
                anchors_down=["10_entry_layer/10_http_entry.md"],
            )
            write_protocol_doc(
                mother_doc_root,
                "10_entry_layer/10_http_entry.md",
                title="HTTP Entry",
                summary="HTTP 请求入口。",
                layer="resolution",
            )
            write_protocol_doc(
                mother_doc_root,
                "40_support_layer/00_delivery_contract.md",
                title="Delivery Contract",
                summary="交付支撑节点。",
                layer="support",
            )
            run_cli("mother-doc-refresh-root-index", "--path", str(mother_doc_root))
            completed = run_cli_raw(
                "construction-plan-init",
                "--target",
                str(pack_root),
                "--plan-kind",
                "official_plan",
            )
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["design_plan_path"] is None
            assert payload["modified_doc_refs"] == [
                "10_entry_layer/00_backend_overview.md",
                "10_entry_layer/10_http_entry.md",
                "40_support_layer/00_delivery_contract.md",
            ]
            registry = yaml.safe_load((pack_root / "pack_registry.yaml").read_text(encoding="utf-8"))
            assert registry["design_plan_path"] is None
            assert len(registry["packs"]) == 2
            first_pack_manifest = yaml.safe_load(
                (pack_root / registry["packs"][0]["pack_dir"] / "pack_manifest.yaml").read_text(encoding="utf-8")
            )
            assert "10_entry_layer/00_backend_overview.md" in first_pack_manifest["source_mother_doc_refs"]
            assert "10_entry_layer/10_http_entry.md" in first_pack_manifest["source_mother_doc_refs"]

    def test_mother_doc_state_sync_transitions_doc_and_adds_pack_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(
                target,
                "01_target_state.md",
                title="Target State",
                summary="定义目标态文档。",
                layer="capability",
                doc_id="sample.target_state",
            )
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
            write_protocol_doc(
                target,
                "01_target_state.md",
                title="Target State",
                summary="定义目标态文档。",
                layer="capability",
                doc_id="sample.target_state",
            )
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
            source = write_protocol_doc(
                target,
                "01_target_state.md",
                title="Target State",
                summary="定义目标态文档。",
                layer="capability",
                doc_id="sample.target_state",
            )
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
            write_protocol_doc(
                mother_doc_root,
                "01_target_state/00_index.md",
                title="Target State",
                summary="定义目标态章节根。",
                layer="capability",
                doc_id="sample.target_state.index",
            )
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo_root, check=True)

            chapter_dir = mother_doc_root / "01_target_state"
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
            write_protocol_doc(
                mother_doc_root,
                "01_target_state/10_scope.md",
                title="Scope Slice",
                summary="定义子范围文档。",
                layer="capability",
                doc_id="sample.target_state.scope",
                state="planned",
                pack_refs=["01_design_01"],
                body_lines=["# Scope", "", "## 当前职责", "changed"],
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
            updated_index = (chapter_dir / "00_index.md").read_text(encoding="utf-8")
            updated_section = section_doc.read_text(encoding="utf-8")
            assert "doc_work_state: modified" in updated_index
            assert "doc_work_state: modified" in updated_section
            assert "doc_pack_refs: []" in updated_section

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
