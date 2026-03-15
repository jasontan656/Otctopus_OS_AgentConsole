from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "Cli_Toolbox.py"


def run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
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


class CliToolboxTests(unittest.TestCase):
    def test_runtime_contract_returns_new_shape_payload(self) -> None:
        result = run_cli("runtime-contract", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["skill_name"], "SkillsManager-Production-Form")
        self.assertEqual(payload["root_shape"], ["SKILL.md", "path", "agents", "scripts"])
        self.assertIn("read-contract-context", payload["commands"])

    def test_working_contract_reads_json_contract(self) -> None:
        result = run_cli("working-contract", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["payload"]["skill_name"], "SkillsManager-Production-Form")
        self.assertEqual(payload["payload"]["display_name"], "SkillsManager-Production-Form")
        self.assertTrue(
            payload["payload"]["runtime_observability"]["skill_runtime_root"].endswith("/SkillsManager-Production-Form")
        )

    def test_intent_snapshot_reads_markdown(self) -> None:
        result = run_cli("intent-snapshot", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("console 产品意图", payload["content"])
        self.assertIn("Skills/", payload["content"])

    def test_read_contract_context_compiles_current_intent(self) -> None:
        result = run_cli("read-contract-context", "--entry", "current_intent", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("path/current_intent/20_EXECUTION.md", payload["resolved_chain"])

    def test_append_iteration_log_appends_structured_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "ITERATION_LOG.md"
            log_path.write_text("# Log\n", encoding="utf-8")

            result = run_cli(
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

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            text = log_path.read_text(encoding="utf-8")
            self.assertIn("Refine console product form", text)
            self.assertIn("SkillsManager-Production-Form/SKILL.md", text)

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
            result = run_cli(
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
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            expected_log_path = runtime_root / "SkillsManager-Production-Form" / "ITERATION_LOG.md"
            self.assertEqual(payload["log_path"], str(expected_log_path))
            self.assertEqual(payload["runtime_root"], str(runtime_root / "SkillsManager-Production-Form"))
            self.assertEqual(payload["result_root"], str(result_root / "SkillsManager-Production-Form"))
            self.assertTrue(payload["migrated_legacy_log"])
            text = expected_log_path.read_text(encoding="utf-8")
            self.assertIn("Seed", text)
            self.assertIn("Migrate runtime log root", text)

    def test_latest_log_reads_latest_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "ITERATION_LOG.md"
            log_path.write_text(
                "# Log\n\n## 2026-03-10 00:00:00Z - First\n\n- summary: old\n\n## 2026-03-11 00:00:00Z - Second\n\n- summary: new\n",
                encoding="utf-8",
            )
            result = run_cli("latest-log", "--json", "--log-path", str(log_path))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["entry_count"], 1)
            self.assertIn("Second", payload["entries"][0])


if __name__ == "__main__":
    unittest.main()
