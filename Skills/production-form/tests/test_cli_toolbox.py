from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class ProductionFormCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_working_contract_reads_json_contract(self) -> None:
        result = self.run_cli("working-contract", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["payload"]["skill_name"], "production-form")

    def test_intent_snapshot_reads_markdown(self) -> None:
        result = self.run_cli("intent-snapshot", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("Octopus OS", payload["content"])
        self.assertIn("自然语言驱动的多 Agent 控制台", payload["content"])

    def test_append_iteration_log_appends_structured_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "ITERATION_LOG.md"
            log_path.write_text("# Log\n", encoding="utf-8")

            result = self.run_cli(
                "append-iteration-log",
                "--json",
                "--log-path",
                str(log_path),
                "--title",
                "Refine current form",
                "--summary",
                "Locked the temporary skill role.",
                "--decision",
                "Use a local markdown log during the transition stage.",
                "--affected-path",
                "production-form/SKILL.md",
                "--next-step",
                "Keep the log updated after each real product decision.",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            text = log_path.read_text(encoding="utf-8")
            self.assertIn("Refine current form", text)
            self.assertIn("production-form/SKILL.md", text)

    def test_latest_log_reads_latest_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "ITERATION_LOG.md"
            log_path.write_text(
                "# Log\n\n## 2026-03-10 00:00:00Z - First\n\n- summary: old\n\n## 2026-03-11 00:00:00Z - Second\n\n- summary: new\n",
                encoding="utf-8",
            )
            result = self.run_cli("latest-log", "--json", "--log-path", str(log_path))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["entry_count"], 1)
            self.assertIn("Second", payload["entries"][0])


if __name__ == "__main__":
    unittest.main()
