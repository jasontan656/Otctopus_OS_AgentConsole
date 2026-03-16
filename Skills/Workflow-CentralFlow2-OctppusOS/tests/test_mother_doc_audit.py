from __future__ import annotations

import json
import tempfile
from pathlib import Path

from tests.support_cli import run_cli, run_cli_raw
from tests.support_docs import write_protocol_doc


class TestMotherDocAudit:
    def test_mother_doc_lint_accepts_tree_first_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            (target / "01_target_state").mkdir()
            write_protocol_doc(
                target,
                "01_target_state/00_index.md",
                title="Target State",
                summary="定义当前目标态的章节根。",
                layer="capability",
                doc_id="sample.target_state.index",
                body_lines=["# Target State", "", "## 来源", "- `test_fixture`", "", "## 当前节点职责", "- 定义目标态。", "", "## 当前内容", "- 这是目标态章节根。", "", "## 当前延伸边界", "- 当前 fixture 不跨同层互连。", ""],
            )
            run_cli("mother-doc-refresh-root-index", "--path", str(target))
            assert run_cli_raw("mother-doc-lint", "--path", str(target)).returncode == 0

    def test_mother_doc_audit_passes_clean_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(target, "10_entry_layer/00_frontend_overview.md", title="Frontend Overview", summary="前端入口。", layer="entry", body_lines=["# Frontend Overview", "", "## 来源", "- `test_fixture`", "", "## 当前节点职责", "- 说明前端入口是什么。", "", "## 当前内容", "- 当前只保留一个单一入口语义。", "", "## 当前延伸规则", "- 后续继续沿已注册分支扩展。", ""])
            run_cli("mother-doc-refresh-root-index", "--path", str(target))
            payload = run_cli("mother-doc-audit", "--path", str(target))
            assert payload["status"] == "pass"
            assert payload["audit_gate_allowed"] is True

    def test_mother_doc_audit_detects_overload_and_soft_fail_stays_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(target, "00_overview/00_product_intent.md", title="Product Intent", summary="故意过载的总览节点。", layer="overview", always_read=True, body_lines=["# Product Intent", "", "## 来源", "- `test_fixture`", "", "## 当前节点职责", "- 定义统一产品对象。", "- 定义外部用户主工作台。", "- 定义管理员治理入口。", "", "## 当前内容", "- 外部用户任务流必须在同一壳层完成。", "- 管理员需要查看文档图、代码图与协作入口。", "- `menu / workspace / panel / projection adapter / service boundary` 必须一起成立。", "- `GSAP Flip / Vue Move / View Transitions` 都要被继续消费。", "", "## 非目标", "- 不恢复 legacy UI。", "- 不降级成纯文档浏览器。", ""])
            run_cli("mother-doc-refresh-root-index", "--path", str(target))
            completed = run_cli_raw("mother-doc-audit", "--path", str(target))
            assert completed.returncode != 0
            payload = json.loads(completed.stdout)
            assert payload["status"] == "fail"
            assert payload["shadow_split_proposals"]
            soft_fail = run_cli_raw("mother-doc-audit", "--path", str(target), "--soft-fail-exit")
            assert soft_fail.returncode == 0

    def test_mother_doc_audit_short_circuits_when_lint_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            legacy_doc = target / "10_entry_layer" / "10_backend_overview.md"
            legacy_doc.parent.mkdir(parents=True, exist_ok=True)
            legacy_doc.write_text("\n".join(["---", "doc_work_state: modified", "doc_pack_refs: []", "thumb_title: Backend Overview", "thumb_summary: 故意同时制造 lint fail 和 semantic overload。", "display_layer: entry", "layer: legacy_entry", "always_read: false", "anchors_up: []", "anchors_right: []", "anchors_down: []", "anchors_left: []", "anchors_support: []", "---", "", "# Backend Overview", "", "## 来源", "- `test_fixture`", "", "## 当前节点职责", "- 定义统一产品对象。", "- 定义外部用户主工作台。", "- 定义管理员治理入口。", "", "## 当前内容", "- `menu / workspace / panel / projection adapter / service boundary` 必须一起成立。", "- `GSAP Flip / Vue Move / View Transitions` 都要被继续消费。", ""]), encoding="utf-8")
            run_cli("mother-doc-refresh-root-index", "--path", str(target))
            payload = json.loads(run_cli_raw("mother-doc-audit", "--path", str(target)).stdout)
            assert payload["reason"] == "mother_doc_lint_failed"

    def test_mother_doc_lint_rejects_legacy_traversal_and_root_index_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            legacy_doc = target / "10_entry_layer" / "10_backend_overview.md"
            legacy_doc.parent.mkdir(parents=True, exist_ok=True)
            legacy_doc.write_text("\n".join(["---", "doc_work_state: modified", "doc_pack_refs: []", "thumb_title: Backend Overview", "thumb_summary: 后端总览。", "display_layer: entry", "layer: legacy_entry", "always_read: false", "anchors_up: []", "anchors_right: []", "anchors_down: []", "anchors_left: []", "anchors_support: []", "---", "", "# Backend Overview", "", "## 当前职责", "后端总览。", ""]), encoding="utf-8")
            payload = json.loads(run_cli_raw("mother-doc-lint", "--path", str(target)).stdout)
            assert payload["frontmatter_violations"]
            write_protocol_doc(target, "10_entry_layer/00_frontend_overview.md", title="Frontend Overview", summary="前端总览。", layer="entry", anchors_down=["20_resolution_layer/00_frontend_layers.md"])
            write_protocol_doc(target, "10_entry_layer/20_backend_overview.md", title="Backend Overview", summary="后端总览。", layer="entry", anchors_down=["20_resolution_layer/00_frontend_layers.md"])
            write_protocol_doc(target, "20_resolution_layer/00_frontend_layers.md", title="Frontend Layers", summary="前端层级定义。", layer="resolution")
            run_cli("mother-doc-refresh-root-index", "--path", str(target))
            traversal = json.loads(run_cli_raw("mother-doc-lint", "--path", str(target)).stdout)
            assert traversal["traversal_violations"]

    def test_mother_doc_refresh_root_index_is_folder_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            write_protocol_doc(target, "10_entry_layer/10_backend_overview.md", title="Backend Overview", summary="后端总览。", layer="entry")
            write_protocol_doc(target, "20_resolution_layer/10_backend_layer_definition.md", title="Backend Layers", summary="后端层级定义。", layer="resolution")
            payload = run_cli("mother-doc-refresh-root-index", "--path", str(target))
            assert payload["folder_refs"] == ["10_entry_layer/", "20_resolution_layer/"]
            index_content = (target / "00_index.md").read_text(encoding="utf-8")
            assert "10_backend_overview.md" not in index_content
