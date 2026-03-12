from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestConstitutionQueryTests:
    def test_query_contract_is_query_only_after_python_lint_migration(self) -> None:
        output = subprocess.check_output(
            [
                "python3",
                str(ROOT / "scripts/constitution_keyword_query.py"),
                "--keywords-zh",
                "会话,权限",
                "--keywords-en",
                "session,permission",
            ],
            text=True,
        ).splitlines()
        rows = [json.loads(line) for line in output]
        contract = next(row for row in rows if row["record"] == "constitution_enforcement_contract")
        assert contract["required_gates"] == []
        assert contract["execution_owner_hint"] == "specialized skill or repo-local contract"

    def test_common_fat_file_is_removed_from_query_surface(self) -> None:
        registry = (ROOT / "references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml").read_text(encoding="utf-8")
        graph = (ROOT / "references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md").read_text(encoding="utf-8")
        machine = (ROOT / "references/anchor_docs_machine/anchor_docs_machine_v1.jsonl").read_text(encoding="utf-8")
        assert "common_fat_file" not in registry
        assert "common_fat_file" not in graph
        assert "common_fat_file" not in machine

    def test_python_lint_entry_is_not_owned_by_constitution_skill(self) -> None:
        skill_doc = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        tooling_usage = (ROOT / "references/tooling/Cli_Toolbox_USAGE.md").read_text(encoding="utf-8")
        assert "run_constitution_lints" not in skill_doc
        assert "run_constitution_lints" not in tooling_usage

