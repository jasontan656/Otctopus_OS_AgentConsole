from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class TestSkillProductionFormCliTests:
    def run_cli(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        merged_env = dict(os.environ)
        if env:
            merged_env.update(env)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
            env=merged_env,
        )

    def test_working_contract_reads_json_contract(self) -> None:
        result = self.run_cli("working-contract", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["status"] == "ok"
        assert payload["payload"]["skill_name"] == "SkillsManager-Production-Form"
        assert payload["payload"]["display_name"] == "SkillsManager-Production-Form"
        assert payload["payload"]["runtime_observability"]["skill_runtime_root"].endswith("/SkillsManager-Production-Form")

    def test_intent_snapshot_reads_markdown(self) -> None:
        result = self.run_cli("intent-snapshot", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert "console 产品意图" in payload["content"]
        assert "Skills/" in payload["content"]

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
                "Refine console product form",
                "--summary",
                "Locked the console productization boundary.",
                "--decision",
                "Keep the skill root as the mirror authoring source.",
                "--affected-path",
                "SkillsManager-Production-Form/SKILL.md",
                "--next-step",
                "Keep the registry and runtime contract aligned.",
            )

            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["status"] == "ok"
            text = log_path.read_text(encoding="utf-8")
            assert "Refine console product form" in text
            assert "SkillsManager-Production-Form/SKILL.md" in text

    def test_default_log_path_uses_runtime_root_and_seeds_legacy_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            result_root = Path(tmp) / "result"
            legacy_log_path = Path(tmp) / "legacy" / "ITERATION_LOG.md"
            legacy_log_path.parent.mkdir(parents=True)
            legacy_log_path.write_text(
                "# SkillsManager-Production-Form Iteration Log\n\n## 2026-03-11 00:00:00Z - Seed\n\n- summary: kept\n",
                encoding="utf-8",
            )
            result = self.run_cli(
                "append-iteration-log",
                "--json",
                "--title",
                "Migrate runtime log root",
                "--summary",
                "Moved the active iteration log into the governed runtime root.",
                env={
                    "CODEX_SKILL_RUNTIME_ROOT": str(runtime_root),
                    "CODEX_SKILLS_RESULT_ROOT": str(result_root),
                    "SKILL_PRODUCTION_FORM_LEGACY_LOG_PATH": str(legacy_log_path),
                },
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            expected_log_path = runtime_root / "SkillsManager-Production-Form" / "ITERATION_LOG.md"
            assert payload["log_path"] == str(expected_log_path)
            assert payload["runtime_root"] == str(runtime_root / "SkillsManager-Production-Form")
            assert payload["result_root"] == str(result_root / "SkillsManager-Production-Form")
            assert payload["migrated_legacy_log"]
            text = expected_log_path.read_text(encoding="utf-8")
            assert "Seed" in text
            assert "Migrate runtime log root" in text

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
