from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "create_skill_from_template.py"


def run_generator(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


class TestCreateSkillFromTemplateRegressionTest:
    def test_guide_only_mode_generates_minimal_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "guide-only-sandbox",
                "--target-root",
                temp_dir,
                "--skill-mode",
                "guide_only",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

            assert payload["skill_mode"] == "guide_only"
            assert payload["resources_created"] == ["agents"]
            assert "skill_mode: guide_only" in skill_md
            assert "## 1. 模型立刻需要知道的事情" in skill_md
            assert "## 2. 技能正文" in skill_md
            assert "## 3. 目录结构图" in skill_md
            assert (skill_dir / "agents" / "openai.yaml").exists()
            assert not (skill_dir / "path").exists()
            assert not (skill_dir / "scripts").exists()
            assert not (skill_dir / "references").exists()
            assert not (skill_dir / "assets").exists()
            assert not (skill_dir / "tests").exists()

    def test_guide_with_tool_mode_generates_root_with_path_agents_and_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "guide-with-tool-sandbox",
                "--target-root",
                temp_dir,
                "--skill-mode",
                "guide_with_tool",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            toolbox_output = subprocess.run(
                ["python3", str(skill_dir / "scripts" / "Cli_Toolbox.py"), "runtime-contract", "--json"],
                text=True,
                capture_output=True,
                check=True,
            )
            runtime_contract = json.loads(toolbox_output.stdout)
            compiled_output = subprocess.run(
                ["python3", str(skill_dir / "scripts" / "Cli_Toolbox.py"), "read-path-context", "--entry", "primary_flow", "--json"],
                text=True,
                capture_output=True,
                check=True,
            )
            compiled_payload = json.loads(compiled_output.stdout)

            assert payload["skill_mode"] == "guide_with_tool"
            assert payload["resources_created"] == ["path", "agents", "scripts"]
            assert "skill_mode: guide_with_tool" in skill_md
            assert "reading_chain:" in skill_md
            assert "## 1. 模型立刻需要知道的事情" in skill_md
            assert "## 2. 功能入口" in skill_md
            assert "## 3. 目录结构图" in skill_md
            assert "[primary_flow]" in skill_md
            assert runtime_contract["skill_mode"] == "guide_with_tool"
            assert runtime_contract["entry_doc"] == "path/primary_flow/00_PRIMARY_FLOW_ENTRY.md"
            assert "read-path-context" in runtime_contract["commands"]
            assert compiled_payload["status"] == "ok"
            assert "Primary Flow Entry" in compiled_payload["compiled_markdown"]
            assert (skill_dir / "path" / "primary_flow" / "00_PRIMARY_FLOW_ENTRY.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "10_CONTRACT.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "15_TOOLS.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "20_EXECUTION.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "30_VALIDATION.md").exists()
            assert (skill_dir / "agents" / "openai.yaml").exists()
            assert (skill_dir / "scripts" / "Cli_Toolbox.py").exists()
            assert (skill_dir / "scripts" / "test_skill_layout.py").exists()
            assert not (skill_dir / "references").exists()
            assert not (skill_dir / "assets").exists()
            assert not (skill_dir / "tests").exists()

    def test_executable_workflow_mode_generates_compound_workflow_subpath(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = run_generator(
                "--skill-name",
                "workflow-sandbox",
                "--target-root",
                temp_dir,
                "--skill-mode",
                "executable_workflow_skill",
                "--overwrite",
            )
            skill_dir = Path(payload["skill_dir"])
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            toolbox_output = subprocess.run(
                ["python3", str(skill_dir / "scripts" / "Cli_Toolbox.py"), "runtime-contract", "--json"],
                text=True,
                capture_output=True,
                check=True,
            )
            runtime_contract = json.loads(toolbox_output.stdout)
            compiled_output = subprocess.run(
                [
                    "python3",
                    str(skill_dir / "scripts" / "Cli_Toolbox.py"),
                    "read-path-context",
                    "--entry",
                    "primary_flow",
                    "--selection",
                    "step_01",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            compiled_payload = json.loads(compiled_output.stdout)

            assert payload["skill_mode"] == "executable_workflow_skill"
            assert "reading_chain:" in skill_md
            assert "## 1. 模型立刻需要知道的事情" in skill_md
            assert "## 2. 功能入口" in skill_md
            assert "## 3. 目录结构图" in skill_md
            assert "[primary_flow]" in skill_md
            assert runtime_contract["skill_mode"] == "executable_workflow_skill"
            assert "read-path-context" in runtime_contract["commands"]
            assert compiled_payload["status"] == "ok"
            assert any(item.endswith("steps/step_01/00_STEP_ENTRY.md") for item in compiled_payload["resolved_chain"])
            assert (skill_dir / "path" / "primary_flow" / "00_PRIMARY_FLOW_ENTRY.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "15_TOOLS.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "20_WORKFLOW_INDEX.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "steps" / "step_01" / "00_STEP_ENTRY.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "steps" / "step_02" / "30_VALIDATION.md").exists()
            assert (skill_dir / "path" / "primary_flow" / "steps" / "step_03" / "30_VALIDATION.md").exists()
            assert (skill_dir / "scripts" / "Cli_Toolbox.py").exists()
            assert not (skill_dir / "references").exists()
            assert not (skill_dir / "assets").exists()
            assert not (skill_dir / "tests").exists()
