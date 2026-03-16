from __future__ import annotations

import json
import tempfile
from pathlib import Path

import yaml

from tests.support_cli import create_runtime_layout, run_cli, run_cli_raw, runtime_scope, workspace_tempdir
from tests.support_docs import fill_directory_placeholders, write_protocol_doc


class TestConstructionPlanFlow:
    def test_target_scaffold_creates_docs_root_artifacts(self) -> None:
        with workspace_tempdir() as temp_dir:
            layout = create_runtime_layout(Path(temp_dir))
            payload = run_cli("target-scaffold", *runtime_scope(layout))
            assert payload["status"] == "pass"
            assert any(item.endswith("Development_Docs/AGENTS.md") for item in payload["created_or_verified"])
            assert (Path(layout["docs_root"]) / "mother_doc" / "00_index.md").exists()
            assert not ((Path(layout["docs_root"]) / "mother_doc" / "execution_atom_plan_validation_packs").exists())

    def test_official_construction_plan_requires_ready_mother_doc(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            completed = run_cli_raw("construction-plan-init", "--target", str(pack_root))
            assert completed.returncode != 0
            assert json.loads(completed.stdout)["reason"] == "modified_doc_missing"

    def test_preview_skeleton_is_not_execution_eligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            plan_root = Path(temp_dir) / "packs"
            design_plan = Path(temp_dir) / "08_dev_execution_plan.md"
            assert run_cli_raw(
                "construction-plan-init",
                "--target",
                str(plan_root),
                "--design-plan",
                str(design_plan),
                "--plan-kind",
                "preview_skeleton",
            ).returncode == 0
            lint_completed = run_cli_raw(
                "construction-plan-lint",
                "--path",
                str(plan_root),
                "--require-execution-eligible",
            )
            assert lint_completed.returncode != 0
            payload = json.loads(lint_completed.stdout)
            assert any("execution_eligible=true" in item for item in payload["execution_eligibility_violations"])

    def test_construction_plan_lint_detects_design_step_coverage_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            fill_directory_placeholders(mother_doc_root)
            write_protocol_doc(mother_doc_root, "00_index.md", title="Root Index", summary="root placeholder", layer="overview", doc_role="root_index", always_read=True, state="ref", pack_refs=["00_done"])
            write_protocol_doc(mother_doc_root, "10_entry_layer/00_http_entry.md", title="HTTP Entry", summary="处理 HTTP 入口。", layer="resolution", anchors_down=["20_resolution_layer/00_access_resolution.md"])
            write_protocol_doc(mother_doc_root, "20_resolution_layer/00_access_resolution.md", title="Access Resolution", summary="处理入口后的首站解析。", layer="capability")
            write_protocol_doc(mother_doc_root, "30_support_layer/00_delivery.md", title="Delivery Node", summary="独立的交付支撑节点。", layer="support")
            run_cli("mother-doc-refresh-root-index", "--path", str(mother_doc_root))
            assert run_cli_raw("construction-plan-init", "--target", str(pack_root), "--plan-kind", "official_plan").returncode == 0
            registry_path = pack_root / "pack_registry.yaml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["design_step_ids"] = [registry["design_step_ids"][0]]
            registry["packs"] = [registry["packs"][0]]
            registry_path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8")
            lint_completed = run_cli_raw("construction-plan-lint", "--path", str(pack_root))
            assert lint_completed.returncode != 0
            payload = json.loads(lint_completed.stdout)
            assert payload["design_coverage_violations"]

    def test_official_construction_plan_groups_modified_docs_without_single_design_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mother_doc_root = Path(temp_dir) / "docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs"
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            fill_directory_placeholders(mother_doc_root)
            write_protocol_doc(mother_doc_root, "10_entry_layer/00_backend_overview.md", title="Backend Overview", summary="后端总览。", layer="entry", anchors_down=["10_entry_layer/10_http_entry.md"])
            write_protocol_doc(mother_doc_root, "10_entry_layer/10_http_entry.md", title="HTTP Entry", summary="HTTP 请求入口。", layer="resolution")
            write_protocol_doc(mother_doc_root, "40_support_layer/00_delivery_contract.md", title="Delivery Contract", summary="交付支撑节点。", layer="support")
            run_cli("mother-doc-refresh-root-index", "--path", str(mother_doc_root))
            completed = run_cli_raw("construction-plan-init", "--target", str(pack_root), "--plan-kind", "official_plan")
            assert completed.returncode == 0
            payload = json.loads(completed.stdout)
            assert payload["design_plan_path"] is None
            assert len(yaml.safe_load((pack_root / "pack_registry.yaml").read_text(encoding="utf-8"))["packs"]) == 2
