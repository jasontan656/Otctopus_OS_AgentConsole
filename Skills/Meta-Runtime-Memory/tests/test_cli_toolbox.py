from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TOOLBOX = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


class TestMetaRuntimeMemoryCli:
    def run_python(
        self,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged_env = dict(os.environ)
        if env is not None:
            merged_env.update(env)
        return subprocess.run(
            [sys.executable, str(TOOLBOX), *args],
            text=True,
            capture_output=True,
            check=False,
            env=merged_env,
        )

    def make_env(self, tmpdir: str) -> dict[str, str]:
        return {
            "CODEX_SKILL_RUNTIME_ROOT": str(Path(tmpdir) / "runtime"),
            "CODEX_SKILL_RESULT_ROOT": str(Path(tmpdir) / "result"),
        }

    def write_session_file(
        self,
        codex_home: Path,
        session_id: str,
        turn_id: str,
        *,
        user_message: str,
        final_reply: str,
        changed_paths: list[str] | None = None,
        cwd: str = "/tmp",
    ) -> Path:
        session_file = codex_home / "sessions" / "2026" / "03" / "16" / f"rollout-2026-03-16T00-00-00-{session_id}.jsonl"
        session_file.parent.mkdir(parents=True, exist_ok=True)
        entries = [
            {
                "timestamp": "2026-03-16T00:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": session_id,
                    "timestamp": "2026-03-16T00:00:00Z",
                    "cwd": cwd,
                },
            },
            {
                "timestamp": "2026-03-16T00:00:01Z",
                "type": "event_msg",
                "payload": {"type": "task_started", "turn_id": turn_id},
            },
            {
                "timestamp": "2026-03-16T00:00:02Z",
                "type": "event_msg",
                "payload": {"type": "user_message", "message": user_message},
            },
        ]
        if changed_paths:
            entries.extend(
                [
                    {
                        "timestamp": "2026-03-16T00:00:03Z",
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "status": "completed",
                            "call_id": "call_patch",
                            "name": "apply_patch",
                            "input": "*** Begin Patch\n*** End Patch\n",
                        },
                    },
                    {
                        "timestamp": "2026-03-16T00:00:04Z",
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "call_patch",
                            "output": json.dumps(
                                {
                                    "output": "Success. Updated the following files:\n"
                                    + "\n".join(f"M {path}" for path in changed_paths),
                                    "metadata": {"exit_code": 0},
                                },
                                ensure_ascii=False,
                            ),
                        },
                    },
                    {
                        "timestamp": "2026-03-16T00:00:05Z",
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "call_id": "call_test",
                            "name": "exec_command",
                            "arguments": json.dumps({"cmd": "pytest -q", "workdir": "/tmp"}),
                        },
                    },
                    {
                        "timestamp": "2026-03-16T00:00:06Z",
                        "type": "response_item",
                        "payload": {
                            "type": "function_call_output",
                            "call_id": "call_test",
                            "output": "Chunk ID: ok\nWall time: 0.0 seconds\nProcess exited with code 0\nOutput:\n1 passed\n",
                        },
                    },
                ]
            )
        entries.extend(
            [
                {
                    "timestamp": "2026-03-16T00:00:07Z",
                    "type": "event_msg",
                    "payload": {"type": "agent_message", "message": final_reply, "phase": "final_answer"},
                },
                {
                    "timestamp": "2026-03-16T00:00:08Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "task_complete",
                        "turn_id": turn_id,
                        "last_agent_message": final_reply,
                    },
                },
            ]
        )
        session_file.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in entries) + "\n", encoding="utf-8")
        return session_file

    def test_runtime_contract_reports_turn_hook_policy(self) -> None:
        result = self.run_python("runtime-contract", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["skill_name"] == "Meta-Runtime-Memory"
        assert payload["trigger_policy"]["default_trigger"] == "turn_hook"

    def test_paths_use_governed_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_python("paths", "--json", env=self.make_env(tmp))
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["resolved_paths"]["runtime_root"].endswith("/Meta-Runtime-Memory")
            assert payload["resolved_paths"]["result_root"].endswith("/Meta-Runtime-Memory")

    def test_init_bind_upsert_compile_and_validate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = self.make_env(tmp)

            init_result = self.run_python("init-store", "--json", env=env)
            assert init_result.returncode == 0, init_result.stderr
            init_payload = json.loads(init_result.stdout)
            assert init_payload["result_root"].endswith("/Meta-Runtime-Memory")

            bind_result = self.run_python(
                "bind-task",
                "--task-id",
                "Memory Contract",
                "--title",
                "Memory Contract",
                "--goal",
                "落地 Meta-Runtime-Memory",
                "--json",
                env=env,
            )
            assert bind_result.returncode == 0, bind_result.stderr
            bind_payload = json.loads(bind_result.stdout)
            assert bind_payload["task_id"] == "memory-contract"

            user_patch = json.dumps(
                {
                    "top_layer": {
                        "communication_style": ["中文为主", "结论先行"],
                        "stable_constraints": ["不要保存完整聊天历史"],
                    }
                },
                ensure_ascii=False,
            )
            user_result = self.run_python(
                "upsert-user-memory",
                "--patch-json",
                user_patch,
                "--json",
                env=env,
            )
            assert user_result.returncode == 0, user_result.stderr
            assert json.loads(user_result.stdout)["status"] == "written"

            task_patch = json.dumps(
                {
                    "task_layer": {
                        "current_state": ["技能目录已创建", "CLI 已可用"],
                        "next_steps": ["补充测试", "完成镜像同步"],
                    }
                },
                ensure_ascii=False,
            )
            task_result = self.run_python(
                "upsert-task-memory",
                "--patch-json",
                task_patch,
                "--json",
                env=env,
            )
            assert task_result.returncode == 0, task_result.stderr

            delta_result = self.run_python(
                "append-turn-delta",
                "--summary",
                "完成第一轮技能落地",
                "--task-memory-update",
                "创建脚本与合同",
                "--next-action",
                "跑测试",
                "--json",
                env=env,
            )
            assert delta_result.returncode == 0, delta_result.stderr

            compile_result = self.run_python("compile-active-memory", "--json", env=env)
            assert compile_result.returncode == 0, compile_result.stderr
            compile_payload = json.loads(compile_result.stdout)
            assert compile_payload["active_task_id"] == "memory-contract"

            validate_result = self.run_python("validate-store", "--json", env=env)
            assert validate_result.returncode == 0, validate_result.stderr
            validate_payload = json.loads(validate_result.stdout)
            assert validate_payload["status"] == "ok"
            assert "memory-contract" in validate_payload["task_ids"]

    def test_upsert_user_memory_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = self.make_env(tmp)
            self.run_python("init-store", "--json", env=env)
            result_root = Path(env["CODEX_SKILL_RESULT_ROOT"]) / "Meta-Runtime-Memory"
            user_json = result_root / "user" / "USER_MEMORY.json"
            before_text = user_json.read_text(encoding="utf-8")
            patch = json.dumps({"top_layer": {"work_style": ["先调研后动手"]}}, ensure_ascii=False)
            result = self.run_python(
                "upsert-user-memory",
                "--patch-json",
                patch,
                "--dry-run",
                "--json",
                env=env,
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["status"] == "dry_run"
            assert user_json.read_text(encoding="utf-8") == before_text

    def test_watch_codex_sessions_auto_audits_and_recall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = self.make_env(tmp)
            codex_home = Path(tmp) / "codex_home"
            workspace = Path(tmp) / "workspace"
            changed_file = workspace / "alpha.txt"
            changed_file.parent.mkdir(parents=True, exist_ok=True)
            changed_file.write_text("alpha\n", encoding="utf-8")

            session_applied = "019cf5b1-d644-7de3-885e-4e1ba50790c6"
            turn_applied = "turn-applied"
            self.write_session_file(
                codex_home,
                session_applied,
                turn_applied,
                user_message="请更新 alpha.txt 并验证",
                final_reply="alpha.txt 已更新并通过测试",
                changed_paths=["alpha.txt"],
                cwd=str(workspace),
            )

            session_skipped = "019cf5b1-d644-7de3-885e-4e1ba50790c7"
            turn_skipped = "turn-skipped"
            self.write_session_file(
                codex_home,
                session_skipped,
                turn_skipped,
                user_message="请回答这个问题，不要改文件",
                final_reply="这是只读回答，没有产生 durable 改动",
                changed_paths=None,
            )

            watch_result = self.run_python(
                "watch-codex-sessions",
                "--codex-home",
                str(codex_home),
                "--once",
                "--json",
                env=env,
            )
            assert watch_result.returncode == 0, watch_result.stderr
            watch_payload = json.loads(watch_result.stdout)
            assert len(watch_payload["processed_turns"]) == 2
            assert {item["writeback_decision"] for item in watch_payload["processed_turns"]} == {"applied", "skipped"}

            applied_audit = self.run_python(
                "show-turn-audit",
                "--session-id",
                session_applied,
                "--turn-id",
                turn_applied,
                "--json",
                env=env,
            )
            assert applied_audit.returncode == 0, applied_audit.stderr
            applied_payload = json.loads(applied_audit.stdout)
            assert applied_payload["turn_start_status"] == "applied"
            assert applied_payload["writeback_decision"] == "applied"
            assert str(changed_file) in applied_payload["changed_paths"]

            skipped_audit = self.run_python(
                "show-turn-audit",
                "--session-id",
                session_skipped,
                "--turn-id",
                turn_skipped,
                "--json",
                env=env,
            )
            assert skipped_audit.returncode == 0, skipped_audit.stderr
            skipped_payload = json.loads(skipped_audit.stdout)
            assert skipped_payload["writeback_decision"] == "skipped"
            assert skipped_payload["turn_start_status"] == "applied"

            applied_task_id = next(item["task_id"] for item in watch_payload["processed_turns"] if item["turn_id"] == turn_applied)
            recall_task = self.run_python("recall-memory", "--task-id", applied_task_id, "--json", env=env)
            assert recall_task.returncode == 0, recall_task.stderr
            recall_task_payload = json.loads(recall_task.stdout)
            assert recall_task_payload["task_memory"]["task_id"] == applied_task_id
            assert recall_task_payload["recent_turn_delta"][-1]["writeback_decision"] == "applied"

            recall_session = self.run_python("recall-memory", "--session-id", session_skipped, "--json", env=env)
            assert recall_session.returncode == 0, recall_session.stderr
            recall_session_payload = json.loads(recall_session.stdout)
            assert recall_session_payload["session_memory"]["session_id"] == session_skipped
            assert recall_session_payload["turn_audits"][-1]["writeback_decision"] == "skipped"

            search_result = self.run_python("search-memory", "--query", "alpha.txt", "--json", env=env)
            assert search_result.returncode == 0, search_result.stderr
            search_payload = json.loads(search_result.stdout)
            assert search_payload["task_hits"]
            assert search_payload["turn_hits"]

            validate_result = self.run_python("validate-store", "--json", env=env)
            assert validate_result.returncode == 0, validate_result.stderr
            validate_payload = json.loads(validate_result.stdout)
            assert session_applied in validate_payload["session_ids"]
            assert validate_payload["turn_audit_count"] == 2
