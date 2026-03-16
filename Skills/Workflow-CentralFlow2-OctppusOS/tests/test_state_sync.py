from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from devflow_agents_support import scaffold_and_collect_devflow_agents
from target_runtime_support import resolve_target_runtime
from tests.support_cli import init_git_repo, run_cli, run_cli_raw
from tests.support_docs import fill_directory_placeholders, write_protocol_doc


class TestStateSync:
    def test_runtime_helpers_cover_workspace_and_agents(self, monkeypatch: pytest.MonkeyPatch) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir).resolve()
            octopus_root = workspace_root / "Octopus_OS"
            docs_root = octopus_root / "Development_Docs"
            docs_root.mkdir(parents=True, exist_ok=True)
            monkeypatch.setattr("target_runtime_support.WORKSPACE_ROOT", workspace_root)
            monkeypatch.setattr("target_runtime_support.ROOT_AGENTS_PATH", workspace_root / "AGENTS.md")
            runtime = resolve_target_runtime()
            root = Path(temp_dir).resolve()
            machine_path = root / "managed" / "AGENTS_machine.json"
            runtime_for_agents = {"target_root": root, "development_docs_root": docs_root, "codebase_root": root / "sample_repo", "module_dir": "sample_repo", "docs_root": docs_root, "mother_doc_root": docs_root / "mother_doc", "construction_plan_root": docs_root / "mother_doc" / "execution_atom_plan_validation_packs", "graph_runtime_root": docs_root / "graph", "acceptance_root": docs_root / "mother_doc" / "acceptance"}
            calls: list[list[str]] = []

            def fake_run(command: list[str]) -> dict[str, object]:
                calls.append(command)
                if command[1:].count("target-contract"):
                    return {"managed_files": {"human": str(root / "managed" / "AGENTS_human.md"), "machine": str(machine_path)}}
                if command[1:].count("collect") or command[1:].count("scaffold"):
                    return {"stage": "ok", "operation_count": 1}
                raise AssertionError(command)

            monkeypatch.setattr("devflow_agents_support._run_json_command", fake_run)
            payload = scaffold_and_collect_devflow_agents(runtime_for_agents)
        assert runtime["target_root"] == octopus_root
        assert payload["external_agents_path"].endswith("Development_Docs/AGENTS.md")
        assert any("collect" in command for command in calls)

    def test_mother_doc_sync_state_and_mark_modified(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "docs" / "mother_doc"
            run_cli("mother-doc-init", "--target", str(target))
            source = write_protocol_doc(target, "01_target_state.md", title="Target State", summary="定义目标态文档。", layer="capability", doc_id="sample.target_state")
            payload = run_cli("mother-doc-state-sync", "--path", str(target), "--doc-ref", "sample.target_state", "--from-state", "modified", "--to-state", "planned", "--pack-ref", "01_design_01")
            assert payload["status"] == "pass"
            payload = run_cli("mother-doc-mark-modified", "--path", str(target), "--doc-ref", "sample.target_state")
            assert payload["selected_doc_refs"] == ["01_target_state.md"]
            updated = source.read_text(encoding="utf-8")
            assert "doc_work_state: modified" in updated
            assert "doc_pack_refs: []" in updated

    def test_mother_doc_mark_modified_can_use_git_diff_as_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            mother_doc_root = repo_root / "Development_Docs" / "mother_doc"
            init_git_repo(repo_root)
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            write_protocol_doc(mother_doc_root, "01_target_state/00_index.md", title="Target State", summary="定义目标态章节根。", layer="capability", doc_id="sample.target_state.index")
            subprocess = __import__("subprocess")
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo_root, check=True)
            run_cli("mother-doc-state-sync", "--path", str(mother_doc_root), "--doc-ref", "01_target_state/00_index.md", "--from-state", "modified", "--to-state", "planned", "--pack-ref", "01_design_01")
            write_protocol_doc(mother_doc_root, "01_target_state/10_scope.md", title="Scope Slice", summary="定义子范围文档。", layer="capability", doc_id="sample.target_state.scope", state="planned", pack_refs=["01_design_01"], body_lines=["# Scope", "", "## 当前职责", "changed"])
            payload = run_cli("mother-doc-mark-modified", "--path", str(mother_doc_root), "--repo-root", str(repo_root), "--auto-from-git")
            assert "01_target_state/10_scope.md" in payload["git_direct_doc_refs"]
            assert "01_target_state/00_index.md" in payload["git_impact_doc_refs"]

    def test_mother_doc_mark_modified_ignores_pack_docs_and_requires_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            mother_doc_root = repo_root / "Development_Docs" / "mother_doc"
            pack_root = mother_doc_root / "execution_atom_plan_validation_packs" / "01_pack"
            init_git_repo(repo_root)
            run_cli("mother-doc-init", "--target", str(mother_doc_root))
            fill_directory_placeholders(mother_doc_root)
            pack_root.mkdir(parents=True, exist_ok=True)
            (pack_root / "00_index.md").write_text("# Pack\n", encoding="utf-8")
            subprocess = __import__("subprocess")
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo_root, check=True)
            (pack_root / "00_index.md").write_text("# Changed Pack\n", encoding="utf-8")
            payload = json.loads(run_cli_raw("mother-doc-mark-modified", "--path", str(mother_doc_root), "--repo-root", str(repo_root), "--auto-from-git").stdout)
            assert payload["reason"] == "no_doc_refs_selected_for_modified_mark"
            completed = run_cli_raw("mother-doc-mark-modified", "--path", str(mother_doc_root))
            assert json.loads(completed.stdout)["reason"] == "no_doc_refs_selected_for_modified_mark"
