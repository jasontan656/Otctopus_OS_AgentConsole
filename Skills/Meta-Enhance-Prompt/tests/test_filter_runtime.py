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

    def test_active_invoke_requires_all_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "active_invoke",
                "--input-text",
                "just do it",
                "--json",
                workspace_root=Path(tmp),
                check=False,
            )

            assert completed.returncode == 11
            payload = json.loads(completed.stdout)
            assert payload["mode_decision"] == "active_invoke_mode"
            assert "missing_required_sections" in payload["filter_exit_message"]

    def test_active_invoke_writes_governed_output_and_logs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = self.run_filter(
                "--mode",
                "active_invoke",
                "--input-text",
                "\n".join(
                    [
                        "GOAL: Repair contract",
                        "REPO_CONTEXT_AND_IMPACT:",
                        "- Survey repo",
                        "INPUTS:",
                        "- User request",
                        "OUTPUTS:",
                        "- Final prompt",
                        "BOUNDARIES:",
                        "- No extra scope",
                        "VALIDATION:",
                        "- Six sections remain",
                    ]
                ),
                "--json",
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            output_path = Path(payload["output_path"])
            machine_log = Path(payload["runtime_logs"]["machine_log_path"])
            human_log = Path(payload["runtime_logs"]["human_log_path"])

            assert payload["mode_decision"] == "active_invoke_mode"
            assert output_path.exists()
            assert machine_log.exists()
            assert human_log.exists()
            assert "GOAL:" in payload["final_prompt_copy_paste"]
            assert output_path.read_text(encoding="utf-8") == payload["final_prompt_copy_paste"]
            assert "Codex_Skills_Result/Meta-Enhance-Prompt/active_invoke" in str(output_path)
            assert payload["chat_publish_policy"].startswith("If the final prompt is pasted in chat")

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
            assert "directive --topic active-invoke --json" in resolved["active_invoke_command"]
            assert payload["chat_publish_policy"].startswith("When publishing an active_invoke contract in chat")

    def test_json_stdout_and_output_file_are_split(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "active_prompt.txt"
            completed = self.run_filter(
                "--mode",
                "active_invoke",
                "--input-text",
                "\n".join(
                    [
                        "GOAL: Repair contract",
                        "REPO_CONTEXT_AND_IMPACT:",
                        "- Survey repo",
                        "INPUTS:",
                        "- User request",
                        "OUTPUTS:",
                        "- Final prompt",
                        "BOUNDARIES:",
                        "- No extra scope",
                        "VALIDATION:",
                        "- Six sections remain",
                    ]
                ),
                "--json",
                "--output-path",
                str(output_path),
                workspace_root=Path(tmp),
            )

            payload = json.loads(completed.stdout)
            assert completed.stdout.lstrip().startswith("{")
            assert payload["output_path"] == str(output_path.resolve())
            assert output_path.read_text(encoding="utf-8") == payload["final_prompt_copy_paste"]
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
        directive = self.run_toolbox("directive", "--topic", "active-invoke", "--json")

        contract_payload = json.loads(contract.stdout)
        directive_payload = json.loads(directive.stdout)

        assert contract_payload["contract_name"] == "meta_enhance_prompt_runtime_contract"
        assert directive_payload["topic"] == "active-invoke"
