from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"
SKILL_ROOT = Path(__file__).resolve().parents[1]


class MetaSkillDocStructureCliTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_runtime_contract_returns_expected_name(self) -> None:
        completed = self.run_cli("runtime-contract", "--json")
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["contract_name"], "META_SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT")

    def test_lint_self_skill_passes(self) -> None:
        completed = self.run_cli("lint-doc-anchors", "--target", str(SKILL_ROOT), "--json")
        payload = json.loads(completed.stdout)
        self.assertIn(payload["status"], {"pass", "pass_with_warnings"})

    def test_missing_anchor_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skill"
            root.mkdir()
            (root / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: "temp-skill"
                    description: "temporary skill"
                    metadata:
                      doc_structure:
                        doc_id: "skill.entry"
                        doc_type: "skill_facade"
                        topic: "temp facade"
                        anchors:
                          - target: "docs/guide.md"
                            relation: "details"
                            direction: "downstream"
                            reason: "guide expands facade"
                    ---

                    # Temp
                    """
                ),
                encoding="utf-8",
            )
            docs = root / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    doc_id: "docs.guide"
                    doc_type: "guide"
                    topic: "guide"
                    anchors: []
                    ---

                    # Guide
                    """
                ),
                encoding="utf-8",
            )

            completed = self.run_cli(
                "lint-doc-anchors",
                "--target",
                str(root),
                "--json",
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "fail")

    def test_split_warning_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skill"
            root.mkdir()
            (root / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: "temp-skill"
                    description: "temporary skill"
                    metadata:
                      doc_structure:
                        doc_id: "skill.entry"
                        doc_type: "skill_facade"
                        topic: "temp facade"
                        anchors:
                          - target: "docs/definition-and-flow.md"
                            relation: "details"
                            direction: "downstream"
                            reason: "details"
                    ---

                    # Temp
                    """
                ),
                encoding="utf-8",
            )
            docs = root / "docs"
            docs.mkdir()
            (docs / "definition-and-flow.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    doc_id: "docs.definition_flow"
                    doc_type: "guide"
                    topic: "definition and flow mixed doc"
                    anchors:
                      - target: "../SKILL.md"
                        relation: "expands"
                        direction: "upstream"
                        reason: "expands root"
                    ---

                    # 定义和流程

                    这里同时写定义、流程、脚本、lint、模板。
                    """
                ),
                encoding="utf-8",
            )

            completed = self.run_cli("build-anchor-graph", "--target", str(root), "--json")
            payload = json.loads(completed.stdout)
            self.assertGreaterEqual(len(payload["warnings"]), 1)


if __name__ == "__main__":
    unittest.main()
