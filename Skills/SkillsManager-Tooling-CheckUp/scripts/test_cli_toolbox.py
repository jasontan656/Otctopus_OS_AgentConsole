from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "Cli_Toolbox.py"
DOCSTRUCTURE_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "SkillsManager-Doc-Structure"
    / "scripts"
    / "Cli_Toolbox.py"
)
SKILL_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


class CliToolboxTests(unittest.TestCase):
    def test_runtime_contract_returns_new_shape_payload(self) -> None:
        completed = run_cli("runtime-contract", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["skill_name"], "SkillsManager-Tooling-CheckUp")
        self.assertEqual(payload["root_shape"], ["SKILL.md", "path", "agents", "scripts"])
        self.assertIn("read-contract-context", payload["commands"])
        self.assertIn("read-path-context", payload["commands"])

    def test_read_path_context_compiles_local_entry(self) -> None:
        completed = run_cli("read-path-context", "--entry", "cli_surface", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["entry"], "cli_surface")
        self.assertIn("path/cli_surface/00_CLI_SURFACE_ENTRY.md", payload["resolved_chain"])
        self.assertIn("compiled_markdown", payload)

    def test_read_contract_context_compiles_local_entry(self) -> None:
        completed = run_cli("read-contract-context", "--entry", "cli_surface", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["entry"], "cli_surface")
        self.assertIn("path/cli_surface/10_CONTRACT.md", payload["resolved_chain"])

    def test_govern_target_reports_no_tooling_surface_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "No-Tooling-Skill"
            target_root.mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: No Tooling\ndescription: example\n---\n\n# No Tooling\n",
                encoding="utf-8",
            )

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertTrue(payload["compliant"])
            self.assertFalse(payload["audit"]["tooling_surface_detected"])

    def test_govern_target_reports_non_compliant_target_without_cli_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "Example-Skill"
            (target_root / "scripts").mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: Example Skill\ndescription: example\n---\n\n# Example Skill\n",
                encoding="utf-8",
            )
            (target_root / "scripts" / "runner.py").write_text("print('tooling')\n", encoding="utf-8")

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["compliant"])
            self.assertFalse(payload["audit"]["cli_entry_present"])

    def test_govern_target_requires_read_path_context_for_path_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "Path-Skill"
            (target_root / "scripts").mkdir(parents=True)
            (target_root / "path" / "primary_flow").mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: Path Skill\ndescription: example\nskill_mode: guide_with_tool\n---\n\n# Path Skill\n\n## 1. 模型立刻需要知道的事情\n### 1. 总览\n- example\n\n### 2. 技能约束\n- example\n\n### 3. 顶层常驻合同\n- example\n\n## 2. 功能入口\n- [primary_flow]：`path/primary_flow/00_PRIMARY_FLOW_ENTRY.md`\n  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry primary_flow --json`\n\n## 3. 目录结构图\n",
                encoding="utf-8",
            )
            (target_root / "path" / "primary_flow" / "00_PRIMARY_FLOW_ENTRY.md").write_text(
                "---\nreading_chain:\n- key: contract\n  target: 10_CONTRACT.md\n  hop: next\n  reason: contract\n---\n\n# Entry\n\n## 下一跳列表\n- [contract]：`10_CONTRACT.md`\n",
                encoding="utf-8",
            )
            (target_root / "path" / "primary_flow" / "10_CONTRACT.md").write_text("# Contract\n", encoding="utf-8")
            (target_root / "scripts" / "Cli_Toolbox.py").write_text("print('tooling')\n", encoding="utf-8")

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["compliant"])
            self.assertTrue(payload["audit"]["chain_reader_required"])
            self.assertFalse(payload["audit"]["chain_reader_present"])

    def test_govern_target_accepts_working_read_path_context_for_path_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "Path-Skill"
            (target_root / "scripts").mkdir(parents=True)
            (target_root / "path" / "primary_flow").mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: Path Skill\ndescription: example\nskill_mode: guide_with_tool\n---\n\n# Path Skill\n\n## 1. 模型立刻需要知道的事情\n### 1. 总览\n- example\n\n### 2. 技能约束\n- example\n\n### 3. 顶层常驻合同\n- example\n\n## 2. 功能入口\n- [primary_flow]：`path/primary_flow/00_PRIMARY_FLOW_ENTRY.md`\n  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry primary_flow --json`\n\n## 3. 目录结构图\n",
                encoding="utf-8",
            )
            (target_root / "path" / "primary_flow" / "00_PRIMARY_FLOW_ENTRY.md").write_text(
                "---\nreading_chain:\n- key: contract\n  target: 10_CONTRACT.md\n  hop: next\n  reason: contract\n---\n\n# Entry\n\n## 下一跳列表\n- [contract]：`10_CONTRACT.md`\n",
                encoding="utf-8",
            )
            (target_root / "path" / "primary_flow" / "10_CONTRACT.md").write_text("# Contract\n", encoding="utf-8")
            (target_root / "scripts" / "Cli_Toolbox.py").write_text(
                "import json,sys\n"
                "if __name__ == '__main__':\n"
                "    print(json.dumps({'status':'ok','resolved_chain':['SKILL.md','path/primary_flow/00_PRIMARY_FLOW_ENTRY.md','path/primary_flow/10_CONTRACT.md'],'segments':[{'source':'SKILL.md','content':'# Path Skill'},{'source':'path/primary_flow/00_PRIMARY_FLOW_ENTRY.md','content':'# Entry'},{'source':'path/primary_flow/10_CONTRACT.md','content':'# Contract'}],'compiled_markdown':'# Path Skill\\n\\n# Entry\\n\\n# Contract'}))\n",
                encoding="utf-8",
            )

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertTrue(payload["compliant"])
            self.assertTrue(payload["audit"]["chain_reader_present"])

    def test_docstructure_lint_accepts_rewritten_skill_shape(self) -> None:
        completed = subprocess.run(
            [
                "python3",
                str(DOCSTRUCTURE_SCRIPT),
                "lint-docstructure",
                "--target",
                str(SKILL_ROOT),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")


if __name__ == "__main__":
    unittest.main()
