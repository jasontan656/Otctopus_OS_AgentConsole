from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
FILTER_SCRIPT = SKILL_ROOT / "scripts" / "filter_active_invoke_output.py"
TOOLBOX_SCRIPT = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


class TestMetaEnhancePromptRuntime:
    def run_filter(self, *args: str, workspace_root: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["META_ENHANCE_PROMPT_WORKSPACE_ROOT"] = str(workspace_root)
        return subprocess.run(
            ["python3", str(FILTER_SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
            env=env,
        )

    def run_toolbox(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(TOOLBOX_SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def write_sample_session(self, codex_home: Path, *, session_id: str = "019c-example") -> Path:
        session_file = codex_home / "sessions" / "2026" / "03" / "16" / f"rollout-2026-03-16T08-00-00-{session_id}.jsonl"
        session_file.parent.mkdir(parents=True, exist_ok=True)
        rows = [
            {
                "timestamp": "2026-03-16T08:00:00.000Z",
                "type": "session_meta",
                "payload": {
                    "id": session_id,
                    "timestamp": "2026-03-16T08:00:00.000Z",
                    "cwd": "/tmp/demo",
                    "originator": "codex_cli_rs",
                    "cli_version": "0.106.0",
                    "source": "cli",
                    "model_provider": "openai",
                },
            },
            {
                "timestamp": "2026-03-16T08:00:01.000Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "请先帮我看第一段上下文。"}],
                },
            },
            {
                "timestamp": "2026-03-16T08:00:02.000Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "这是第一轮 assistant reply。"}],
                },
            },
            {
                "timestamp": "2026-03-16T08:00:03.000Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "请读取 tool context 后继续总结。"}],
                },
            },
            {
                "timestamp": "2026-03-16T08:00:04.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call_output",
                    "output": "tool context: lint warnings=3",
                },
            },
            {
                "timestamp": "2026-03-16T08:00:05.000Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "这是最后一轮 assistant reply。"}],
                },
            },
        ]
        session_file.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
        return session_file

    def test_intent_clarify_requires_usable_intent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "intent_clarify",
                "--input-text",
                "GOAL:",
                "--json",
                workspace_root=Path(tmp),
                check=False,
            )

            assert completed.returncode == 11
            payload = json.loads(completed.stdout)
            assert payload["mode_decision"] == "intent_clarify_mode"
            assert payload["filter_exit_message"] == "invalid_output: missing_required_sections=INTENT"

    def test_active_invoke_alias_writes_governed_intent_output_and_logs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "active_invoke",
                "--input-text",
                "\n".join(
                    [
                        "INTENT: 把用户原话压缩成可执行的真实需求意图。",
                        "INPUTS:",
                        "- 原始用户描述",
                        "VALIDATION:",
                        "- 不要输出六段合同",
                    ]
                ),
                "--json",
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            output_path = Path(payload["output_path"])
            machine_log = Path(payload["runtime_logs"]["machine_log_path"])
            human_log = Path(payload["runtime_logs"]["human_log_path"])

            assert payload["mode_decision"] == "intent_clarify_mode"
            assert output_path.exists()
            assert machine_log.exists()
            assert human_log.exists()
            assert payload["final_intent_output"].startswith("INTENT:\n")
            assert "INPUTS:" not in payload["final_intent_output"]
            assert output_path.read_text(encoding="utf-8") == payload["final_intent_output"]
            assert "Codex_Skills_Result/Meta-Enhance-Prompt/intent_clarify" in str(output_path)
            assert payload["chat_publish_policy"].startswith("If the final intent output is published in chat")

    def test_intent_clarify_wraps_plain_text_into_intent_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "intent_clarify",
                "--input-text",
                "把用户模糊原话压缩成逻辑闭环的需求意图，不再扩写成六段模板。",
                "--json",
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            assert payload["mode_decision"] == "intent_clarify_mode"
            assert payload["extracted_intent"] == "把用户模糊原话压缩成逻辑闭环的需求意图，不再扩写成六段模板。"
            assert payload["final_intent_output"].startswith("INTENT:\n")

    def test_intent_clarify_treats_codex_id_wrapper_as_context_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "intent_clarify",
                "--input-text",
                '先阅读 codex id : 019c-example 的最后一轮助理回复，理解上下文后，帮我强化如下prompt:("把当前对话整理成可直接执行的意图。")',
                "--json",
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            assert payload["context_request_detected"] is True
            assert payload["target_prompt_detected"] is True
            assert payload["target_prompt_source"] == "embedded_prompt_wrapper"
            assert payload["context_session_refs"] == [{"kind": "codex", "id": "019c-example"}]
            assert payload["extracted_intent"] == "把当前对话整理成可直接执行的意图。"
            assert "codex id" not in payload["final_intent_output"].lower()
            assert "先阅读" not in payload["final_intent_output"]

    def test_skill_directive_error_keeps_skill_directive_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "skill_directive",
                "--input-text",
                "$NonExistSkill do something",
                "--json",
                workspace_root=Path(tmp),
                check=False,
            )

            assert completed.returncode == 13
            payload = json.loads(completed.stdout)
            assert payload["mode_decision"] == "skill_directive_mode"

    def test_skill_directive_returns_cli_first_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "skill_directive",
                "--input-text",
                "$Meta-Enhance-Prompt strengthen prompt",
                "--json",
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            resolved = payload["resolved_skills"][0]
            assert "Cli_Toolbox.py contract --json" in resolved["contract_command"]
            assert "directive --topic intent-clarify --json" in resolved["intent_clarify_command"]
            assert "directive --topic active-invoke --json" in resolved["active_invoke_command"]
            assert "session" in resolved["session_context_policy"]
            assert payload["chat_publish_policy"].startswith("When publishing a final intent output in chat")

    def test_skill_directive_marks_session_context_as_pre_read_parameter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "skill_directive",
                "--input-text",
                "$Meta-Enhance-Prompt 先阅读 codex id : 019c-example 的最后一轮助理回复，再帮我强化 prompt:(\"输出最终 INTENT\")",
                "--json",
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            assert payload["session_context_detected"] is True
            assert "pre-read context" in payload["final_skill_read_directive"]
            assert "read-session-context --lookup-key codex_id --lookup-id 019c-example --json" in payload["final_skill_read_directive"]

    def test_json_stdout_and_output_file_are_split(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "intent_output.txt"
            completed = self.run_filter(
                "--mode",
                "intent_clarify",
                "--input-text",
                "INTENT: 输出澄清后的用户真实需求。",
                "--json",
                "--output-path",
                str(output_path),
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            assert completed.stdout.lstrip().startswith("{")
            assert payload["output_path"] == str(output_path.resolve())
            assert output_path.read_text(encoding="utf-8") == payload["final_intent_output"]
            assert not output_path.read_text(encoding="utf-8").lstrip().startswith("{")

    def test_skill_directive_json_output_path_writes_plain_text_directive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "directive.txt"
            completed = self.run_filter(
                "--mode",
                "skill_directive",
                "--input-text",
                "$Meta-Enhance-Prompt strengthen prompt",
                "--json",
                "--output-path",
                str(output_path),
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            assert output_path.read_text(encoding="utf-8") == payload["final_skill_read_directive"]
            assert not output_path.read_text(encoding="utf-8").lstrip().startswith("{")

    def test_toolbox_contract_and_directive_read_runtime_assets(self) -> None:
        contract = self.run_toolbox("contract", "--json")
        directive = self.run_toolbox("directive", "--topic", "intent-clarify", "--json")
        legacy_alias = self.run_toolbox("directive", "--topic", "active-invoke", "--json")
        session_context = self.run_toolbox("directive", "--topic", "session-context-read", "--json")

        contract_payload = json.loads(contract.stdout)
        directive_payload = json.loads(directive.stdout)
        legacy_alias_payload = json.loads(legacy_alias.stdout)
        session_context_payload = json.loads(session_context.stdout)

        assert contract_payload["contract_name"] == "meta_enhance_prompt_runtime_contract"
        assert directive_payload["topic"] == "intent-clarify"
        assert legacy_alias_payload["topic"] == "intent-clarify"
        assert session_context_payload["topic"] == "session-context-read"

    def test_toolbox_read_session_context_defaults_to_last_assistant_plus_user_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / ".codex"
            self.write_sample_session(codex_home)

            completed = self.run_toolbox(
                "read-session-context",
                "--lookup-key",
                "codex_id",
                "--lookup-id",
                "019c-example",
                "--codex-home",
                str(codex_home),
                "--json",
            )

            payload = json.loads(completed.stdout)
            assert payload["status"] == "ok"
            assert payload["matched_session"]["session_id"] == "019c-example"
            assert payload["focused_chat"]["user_prompt"]["text"] == "请读取 tool context 后继续总结。"
            assert payload["focused_chat"]["assistant_reply"]["text"] == "这是最后一轮 assistant reply。"
            assert [item["role"] for item in payload["context_items"]] == ["user", "assistant"]

    def test_toolbox_read_session_context_can_fetch_other_context_from_same_session(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / ".codex"
            self.write_sample_session(codex_home)

            completed = self.run_toolbox(
                "read-session-context",
                "--session-id",
                "019c-example",
                "--codex-home",
                str(codex_home),
                "--message-role",
                "tool_output",
                "--message-key",
                "text",
                "--message-query",
                "lint warnings",
                "--message-match-mode",
                "contains",
                "--context-mode",
                "window",
                "--window-before",
                "1",
                "--window-after",
                "1",
                "--include-role",
                "user",
                "--include-role",
                "assistant",
                "--include-role",
                "tool_output",
                "--json",
            )

            payload = json.loads(completed.stdout)
            assert payload["status"] == "ok"
            assert payload["focused_chat"]["anchor_message"]["role"] == "tool_output"
            assert "lint warnings=3" in payload["focused_chat"]["anchor_message"]["text"]
            assert [item["role"] for item in payload["context_items"]] == ["user", "tool_output", "assistant"]
