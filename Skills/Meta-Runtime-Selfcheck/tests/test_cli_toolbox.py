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
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
VENV_PYTHON = Path("/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python")


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

    def make_codex_home(self, tmp_path: Path, *, command: str, output: str) -> Path:
        codex_home = tmp_path / ".codex"
        session_path = codex_home / "sessions" / "2026" / "03" / "17"
        session_path.mkdir(parents=True, exist_ok=True)
        session_file = session_path / "rollout-2026-03-17T00-08-52-019cf768-47cc-7882-bf9c-9d267e78188e.jsonl"
        entries = [
            {
                "timestamp": "2026-03-17T00:08:52.452Z",
                "type": "session_meta",
                "payload": {"cwd": "/home/jasontan656/AI_Projects"},
            },
            {
                "timestamp": "2026-03-17T00:08:53.000Z",
                "type": "event_msg",
                "payload": {"type": "task_started", "turn_id": "turn-001"},
            },
            {
                "timestamp": "2026-03-17T00:08:53.500Z",
                "type": "event_msg",
                "payload": {"type": "user_message", "message": "test runtime selfcheck"},
            },
            {
                "timestamp": "2026-03-17T00:08:54.000Z",
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "name": "exec_command",
                    "call_id": "call-001",
                    "arguments": json.dumps({"cmd": command}, ensure_ascii=False),
                },
            },
            {
                "timestamp": "2026-03-17T00:08:55.000Z",
                "type": "response_item",
                "payload": {
                    "type": "function_call_output",
                    "call_id": "call-001",
                    "output": output,
                },
            },
            {
                "timestamp": "2026-03-17T00:08:56.000Z",
                "type": "event_msg",
                "payload": {"type": "task_complete", "turn_id": "turn-001", "last_agent_message": "done"},
            },
        ]
        session_file.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in entries), encoding="utf-8")
        return codex_home

    def test_runtime_pain_batch_help_starts(self) -> None:
        result = self.run_python(BATCH_SCRIPT, "--help")
        assert result.returncode == 0, result.stderr
        assert "Turn hook runtime self-repair" in result.stdout
        assert "--memory-runtime" in result.stdout

    def test_runtime_pain_batch_falls_back_to_session_evidence(self, tmp_path: Path) -> None:
        command = (
            "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python "
            "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-github-operation/scripts/Cli_Toolbox.py "
            "push-contract --repo Octopus_OS"
        )
        output = (
            "Chunk ID: c7a699\n"
            "Wall time: 0.1769 seconds\n"
            "Process exited with code 2\n"
            "Output:\n"
            "Usage: Cli_Toolbox.py push-contract [OPTIONS]\n"
            "Try 'Cli_Toolbox.py push-contract --help' for help.\n"
            "No such option: --repo Did you mean --help?\n"
        )
        codex_home = self.make_codex_home(tmp_path, command=command, output=output)
        env = {"CODEX_HOME": str(codex_home), "CODEX_RUNTIME_PAIN_PROVIDER": ""}
        result = self.run_python(BATCH_SCRIPT, ">", "--thread-id", "turn-001", env=env)
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        report = payload["runtime_pain_batch_selfcheck_v1"]["pain_context_report_v2"]
        assert report["research_scope_v1"]["source_mode"] == "session_fallback"
        focus_group = report["focus_pain_context_v2"]["full_group_context_v2"]
        assert "cli_semantic_mismatch" in focus_group["kinds"]

    def test_paths_reports_governed_runtime_root(self) -> None:
        result = self.run_python(TOOLBOX, "paths", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        runtime_root = Path(payload["resolved_paths"]["runtime_root"])
        assert runtime_root.name == "Meta-Runtime-Selfcheck"
        assert runtime_root.parent.name == "Codex_Skill_Runtime"
        assert payload["resolved_paths"]["watcher_state_json"].endswith("OBSERVER_STATE.json")

    def test_runtime_contract_returns_cli_first_payload(self) -> None:
        result = self.run_python(TOOLBOX, "runtime-contract", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["skill_name"] == "Meta-Runtime-Selfcheck"
        assert "runtime-contract" in payload["tool_entry"]["commands"]
        assert payload["trigger_policy"]["default_trigger"] == "turn_hook"

    def test_turn_hook_directive_aliases_share_same_payload(self) -> None:
        new_result = self.run_python(TOOLBOX, "directive", "--topic", "turn-hook-self-repair", "--json")
        legacy_result = self.run_python(TOOLBOX, "directive", "--topic", "turn-end-selfcheck", "--json")
        assert new_result.returncode == 0, new_result.stderr
        assert legacy_result.returncode == 0, legacy_result.stderr
        new_payload = json.loads(new_result.stdout)
        legacy_payload = json.loads(legacy_result.stdout)
        assert new_payload["topic"] == "turn-hook-self-repair"
        assert legacy_payload["purpose"] == new_payload["purpose"]

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

    def test_execute_command_list_runs_argv_safe_command(self) -> None:
        safe_python = f'{sys.executable} -c "print(123)"'
        script = (
            "import json\n"
            "from runtime_pain_repair_exec import execute_command_list\n"
            f"result = execute_command_list(commands=['{safe_python}'], timeout_sec=5, workdir='.', change_detection_root='')\n"
            "print(json.dumps(result))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(SCRIPTS_ROOT),
            text=True,
            capture_output=True,
            check=False,
            env=os.environ.copy(),
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["success_commands"] == 1
        assert payload["failed_commands"] == 0
        assert payload["runs"][0]["stdout_preview"] == "123"

    def test_execute_command_list_blocks_shell_operator_command(self) -> None:
        script = (
            "import json\n"
            "from runtime_pain_repair_exec import execute_command_list\n"
            "result = execute_command_list(commands=['python -c \"print(1)\" && python -c \"print(2)\"'], timeout_sec=5, workdir='.', change_detection_root='')\n"
            "print(json.dumps(result))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(SCRIPTS_ROOT),
            text=True,
            capture_output=True,
            check=False,
            env=os.environ.copy(),
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["preflight_failed_commands"] == 1
        assert payload["runs"][0]["status"] == "preflight_blocked"
        assert payload["runs"][0]["preflight_reason_code"] == "preflight_shell_operator_unsupported"

    def test_execute_command_list_blocks_unknown_cli_option(self) -> None:
        command = (
            f"{VENV_PYTHON} "
            "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-github-operation/scripts/Cli_Toolbox.py "
            "push-contract --repo Octopus_OS"
        )
        script = (
            "import json\n"
            "from runtime_pain_repair_exec import execute_command_list\n"
            f"result = execute_command_list(commands=['{command}'], timeout_sec=5, workdir='.', change_detection_root='')\n"
            "print(json.dumps(result))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(SCRIPTS_ROOT),
            text=True,
            capture_output=True,
            check=False,
            env=os.environ.copy(),
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["preflight_failed_commands"] == 1
        assert payload["runs"][0]["preflight_reason_code"] == "preflight_unknown_option"

    def test_run_turn_hook_writes_audit_and_repairs_installed_copy_command(self, tmp_path: Path) -> None:
        command = (
            "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python "
            "/home/jasontan656/.codex/skills/Meta-github-operation/scripts/Cli_Toolbox.py "
            "baseline-contract --json"
        )
        output = (
            "Chunk ID: b7ceca\n"
            "Wall time: 0.0179 seconds\n"
            "Process exited with code 1\n"
            "Output:\n"
            "Traceback (most recent call last):\n"
            "RuntimeError: cannot resolve product root from Meta-github-operation script path\n"
        )
        codex_home = self.make_codex_home(tmp_path, command=command, output=output)
        runtime_root = tmp_path / "runtime"
        env = {
            "CODEX_HOME": str(codex_home),
            "CODEX_SKILL_RUNTIME_ROOT": str(runtime_root),
        }
        result = self.run_python(
            TOOLBOX,
            "run-turn-hook",
            "--mode",
            "repair",
            "--session-id",
            "019cf768-47cc-7882-bf9c-9d267e78188e",
            "--turn-id",
            "turn-001",
            "--json",
            env=env,
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["turn_hook_status"] == "repaired"
        assert payload["resolved_optimization_ids"]
        audit_path = Path(payload["turn_audit_path"])
        assert audit_path.exists()
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        assert audit["resolved_optimization_ids"]
        assert audit["hook_status"] == "repaired"
