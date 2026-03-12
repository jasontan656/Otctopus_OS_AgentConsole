from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class TestProductionFormCliTests:
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_working_contract_reads_json_contract(self) -> None:
        result = self.run_cli("working-contract", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["status"] == "ok"
        assert payload["payload"]["skill_name"] == "production-form"

    def test_intent_snapshot_reads_markdown(self) -> None:
        result = self.run_cli("intent-snapshot", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert "Octopus OS" in payload["content"]
        assert "自然语言驱动的多 Agent 控制台" in payload["content"]

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

            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["status"] == "ok"
            text = log_path.read_text(encoding="utf-8")
            assert "Refine current form" in text
            assert "production-form/SKILL.md" in text

    def test_latest_log_reads_latest_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "ITERATION_LOG.md"
            log_path.write_text(
                "# Log\n\n## 2026-03-10 00:00:00Z - First\n\n- summary: old\n\n## 2026-03-11 00:00:00Z - Second\n\n- summary: new\n",
                encoding="utf-8",
            )
            result = self.run_cli("latest-log", "--json", "--log-path", str(log_path))
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["entry_count"] == 1
            assert "Second" in payload["entries"][0]

