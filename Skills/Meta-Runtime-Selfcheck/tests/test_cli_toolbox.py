from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TOOLBOX = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
BATCH_SCRIPT = SKILL_ROOT / "scripts" / "runtime_pain_batch.py"


class TestMetaRuntimeSelfcheckSmoke:
    def run_python(
        self,
        script: Path,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged_env = dict(os.environ)
        if env is not None:
            merged_env.update(env)
        return subprocess.run(
            [sys.executable, str(script), *args],
            text=True,
            capture_output=True,
            check=False,
            env=merged_env,
        )

    def test_runtime_pain_batch_help_starts(self) -> None:
        result = self.run_python(BATCH_SCRIPT, "--help")
        assert result.returncode == 0, result.stderr
        assert "Post-task runtime selfcheck" in result.stdout
        assert "--memory-runtime" in result.stdout

    def test_runtime_pain_batch_reports_missing_provider_as_json(self) -> None:
        env = dict(os.environ)
        env.pop("CODEX_RUNTIME_PAIN_PROVIDER", None)
        result = self.run_python(BATCH_SCRIPT, ">", env=env)
        assert result.returncode == 1
        payload = json.loads(result.stdout)
        assert payload["status"] == "error"
        assert payload["error"] == "pain_source_not_configured"

    def test_paths_reports_governed_runtime_root(self) -> None:
        result = self.run_python(TOOLBOX, "paths", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        runtime_root = Path(payload["resolved_paths"]["runtime_root"])
        assert runtime_root.name == "Meta-Runtime-Selfcheck"
        assert runtime_root.parent.name == "Codex_Skill_Runtime"

    def test_runtime_contract_returns_cli_first_payload(self) -> None:
        result = self.run_python(TOOLBOX, "runtime-contract", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["skill_name"] == "Meta-Runtime-Selfcheck"
        assert "runtime-contract" in payload["tool_entry"]["commands"]

    def test_observability_logs_follow_runtime_root_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            env = {"CODEX_SKILL_RUNTIME_ROOT": str(runtime_root)}
            script = (
                "import json\n"
                "from runtime_pain_observability import attach_observability_logs\n"
                "payload = {\n"
                "  'status': 'ok',\n"
                "  'runtime_pain_batch_selfcheck_v1': {\n"
                "    'queue_summary': {'total_items': 1, 'pending_items': 1, 'resolved_items': 0},\n"
                "    'group_summary': {'group_count': 1, 'pending_group_count': 1}\n"
                "  }\n"
                "}\n"
                "print(json.dumps(attach_observability_logs(run_id='smoke-run', mode='diagnose', output=payload)))\n"
            )
            result = subprocess.run(
                [sys.executable, "-c", script],
                cwd=str(SKILL_ROOT / "scripts"),
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, **env},
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            machine_log_path = Path(payload["machine_log_path"])
            assert machine_log_path.parent.parent.parent.name == "logs"
            assert machine_log_path.is_relative_to(runtime_root)
            assert machine_log_path.parts[-5:-1] == (
                "Meta-Runtime-Selfcheck",
                "logs",
                "runtime_pain_batch",
                "smoke-run",
            )
            assert machine_log_path.exists()
