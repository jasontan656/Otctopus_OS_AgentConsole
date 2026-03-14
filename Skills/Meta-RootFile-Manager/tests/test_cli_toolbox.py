from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_external_agents(part_a_body: str, owner: str | None = None) -> str:
    content = (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n"
    )
    if owner is None:
        return content
    return f"---\nowner: {json.dumps(owner, ensure_ascii=False)}\n---\n{content}"


def render_internal_human(part_a_body: str, payload: dict) -> str:
    return (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n\n"
        "<part_B>\n\n"
        "```json\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
        "```\n"
        "</part_B>\n"
    )


def workspace_part_a() -> str:
    return (
        "1. 根入口命令\n"
        "- 在处理 workspace root 路径规则之前，必须先运行：\n"
        "- `placeholder_root_command`\n"
        "- 当前环境为 `WSL`；若需要调用系统 Python，使用 `python3`。\n\n"
        "2. 技能类任务附加入口\n"
        "- 任何时候只要任务涉及技能、技能镜像、技能安装、技能同步、技能注册、技能治理或技能运行时，必须阅读：\n"
        "- `placeholder_repo_contract`\n\n"
        "3. 语言规范\n"
        "- 对话输出必须使用中文为主。\n"
        "- 起草与写回文档时默认使用中文为主，英文为辅。\n"
        "- 英文只用于技术栈、路径、命令、环境变量、API 名、函数名、类名与其他工程向标识符。\n\n"
        "4. 当前受管 repo 边界\n"
        "- `$meta-github-operation` 当前仅管理以下 repo：\n"
        "- `Octopus_OS`\n"
        "- `Otctopus_OS_AgentConsole`\n"
        "- `Otctopus_OS_AgentConsole` 仍承担与 `~/.codex/skills` 的受控映射关系\n\n"
        "5. Multi-AGENT 工作模式\n"
        "- Multi-AGENT work mode 下，同一文件夹在工作过程中可能出现未预期的并行改动。\n"
        "- 当出现与当前任务无关的并行变更时，应忽略这些无关变更，只关注与当前任务直接相关的文件。\n\n"
        "6. 治理链约束\n"
        "- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.\n"
    )


def payload() -> dict:
    return {
        "owner": "placeholder_owner",
        "entry_role": "repo_runtime_entry",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
        },
        "default_meta_skill_order": [
            "placeholder_skill_1",
            "placeholder_skill_2",
            "placeholder_skill_3",
            "placeholder_skill_4",
            "placeholder_skill_5",
            "placeholder_skill_6",
            "placeholder_skill_7",
        ],
        "turn_start_actions": [
            "placeholder_turn_start_1",
            "placeholder_turn_start_2",
            "placeholder_turn_start_3",
            "placeholder_turn_start_4",
        ],
        "runtime_constraints": [
            "placeholder_constraint_1",
            "placeholder_constraint_2",
            "placeholder_constraint_3",
            "placeholder_constraint_4",
        ],
        "execution_modes": {
            "READ_EXEC": {
                "goal": "placeholder_read_goal",
                "default_actions": [
                    "placeholder_read_action_1",
                    "placeholder_read_action_2",
                ],
            },
            "WRITE_EXEC": {
                "goal": "default to full-coverage edits for the intended change",
                "default_actions": [
                    "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
                ],
            },
        },
        "repo_local_contract_handoff": [
            "placeholder_handoff_1",
            "placeholder_handoff_2",
            "placeholder_handoff_3",
        ],
        "forbidden_primary_runtime_pattern": [],
        "turn_end_actions": [
            "placeholder_turn_end_1",
            "placeholder_turn_end_2",
            "placeholder_turn_end_3",
            "placeholder_turn_end_4",
            "placeholder_turn_end_5",
            "placeholder_turn_end_6",
            "placeholder_turn_end_7",
            "placeholder_turn_end_8",
        ],
    }


def resolve_replace_me(value: object, resolved: str = "resolved_value") -> object:
    if isinstance(value, dict):
        return {key: resolve_replace_me(item, resolved) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_replace_me(item, resolved) for item in value]
    if isinstance(value, str):
        return value.replace("replace_me", resolved)
    return value


class TestCliToolbox:
    def setup_method(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.workspace = self.root / "AI_Projects"
        self.repo_root = self.workspace / "Otctopus_OS_AgentConsole"
        self.skill_root = self.repo_root / "Skills" / "Meta-RootFile-Manager"
        self.installed = self.root / ".codex" / "skills" / "Meta-RootFile-Manager"
        self.runtime = self.workspace / "Codex_Skill_Runtime" / "Meta-RootFile-Manager"

        self._copy_skill_tree()
        self._seed_workspace()
        self._seed_managed_agents()

    def teardown_method(self) -> None:
        self.tempdir.cleanup()

    def _copy_skill_tree(self) -> None:
        src = SCRIPT.parents[1]
        for path in src.rglob("*"):
            if "__pycache__" in path.parts:
                continue
            relative = path.relative_to(src)
            target = self.skill_root / relative
            if path.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                write(target, path.read_text(encoding="utf-8"))

    def _seed_workspace(self) -> None:
        write(self.workspace / "AGENTS.md", render_external_agents("workspace root"))
        write(self.repo_root / "AGENTS.md", render_external_agents("repo root"))
        write(self.repo_root / "README.md", "# Console\n")
        write(self.workspace / "Octopus_OS" / "README.md", "# Octopus\n")
        write(self.repo_root / "CHANGELOG.md", "## 0.1.0\n")
        write(self.repo_root / "CONTRIBUTING.md", "贡献说明\n")
        write(self.repo_root / "SECURITY.md", "security\n")
        write(self.repo_root / "CODE_OF_CONDUCT.md", "be nice\n")
        write(self.repo_root / "LICENSE", "MIT\n")
        write(self.repo_root / ".gitignore", ".venv/\n")
        write(self.workspace / "Octopus_OS" / ".gitignore", ".cache/\n")
        write(self.repo_root / "pytest.ini", "[pytest]\n")
        write(self.repo_root / "requirements-backend_skills.lock.txt", "pytest==8.0.0\n")

    def _seed_managed_agents(self) -> None:
        root_assets = self.skill_root / "assets" / "managed_targets" / "AI_Projects"
        write(root_assets / "AGENTS_human.md", render_internal_human(workspace_part_a(), payload()))
        write(root_assets / "AGENTS_machine.json", json.dumps(payload(), ensure_ascii=False, indent=2) + "\n")
        write(
            root_assets / "Otctopus_OS_AgentConsole" / "AGENTS_human.md",
            render_internal_human("repo root", payload()),
        )
        write(
            root_assets / "Otctopus_OS_AgentConsole" / "AGENTS_machine.json",
            json.dumps(payload(), ensure_ascii=False, indent=2) + "\n",
        )

    def _seed_legacy_alias_dir(self) -> None:
        (self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror").mkdir(
            parents=True, exist_ok=True
        )
        (self.installed / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror").mkdir(
            parents=True, exist_ok=True
        )

    def run_cli(self, *args: str, workspace_root: Path | None = None, expect_ok: bool = True) -> dict:
        env = os.environ.copy()
        env["MDM_WORKSPACE_ROOT"] = str(workspace_root or self.workspace)
        env["MDM_MIRROR_SKILL_ROOT"] = str(self.skill_root)
        env["MDM_INSTALLED_SKILL_ROOT"] = str(self.installed)
        env["MDM_RUNTIME_ROOT"] = str(self.runtime)
        result = subprocess.run(
            ["python3", str(self.skill_root / "scripts" / "Cli_Toolbox.py"), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        if expect_ok and result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        if not expect_ok and result.returncode == 0:
            raise AssertionError("expected failure")
        return json.loads(result.stdout)

    def test_scan_returns_multiple_channels(self) -> None:
        result = self.run_cli("scan", "--json", "--write-runtime-report")
        channels = {entry["channel_id"] for entry in result["entries"]}
        assert "AGENTS_MD" in channels
        assert "README_MD" in channels
        assert "GITIGNORE" in channels
        assert (self.runtime / "scan" / "latest.json").exists()

    def test_collect_syncs_plain_mapping_and_installed_copy(self) -> None:
        result = self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        assert result["operation_count"] == 1
        owner = result["operations"][0]["owner"]
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        installed = (
            self.installed
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        assert managed.read_text(encoding="utf-8").startswith("---\nowner: ")
        assert managed.read_text(encoding="utf-8").endswith("# Console\n")
        assert installed.read_text(encoding="utf-8").startswith("---\nowner: ")
        assert installed.read_text(encoding="utf-8").endswith("# Console\n")
        assert owner in managed.read_text(encoding="utf-8")

    def test_push_writes_plain_mapping_back_to_external(self) -> None:
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        write(managed, "# Updated\n")
        result = self.run_cli("push", "--json", "--source-path", str(self.repo_root / "README.md"))
        assert result["operation_count"] == 1
        assert (self.repo_root / "README.md").read_text(encoding="utf-8") == "# Updated\n"

    def test_target_contract_returns_channel_metadata_for_plain_file(self) -> None:
        self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        result = self.run_cli("target-contract", "--source-path", str(self.repo_root / "README.md"), "--json")
        assert result["channel_id"] == "README_MD"
        assert result["mapping_mode"] == "plain_copy"
        assert "owner" in result
        assert result["managed_files"]["mapped"].endswith("README_MD__governed_external.md")
        assert "owner_meta" not in result["managed_files"]

    def test_scaffold_can_open_non_agents_channel(self) -> None:
        target_dir = self.workspace / "NewRepo"
        result = self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "package.json",
        )
        assert result["operation_count"] == 1
        assert (target_dir / "package.json").exists()
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "NewRepo"
            / "PACKAGE_JSON__governed_external.json"
        )
        assert managed.exists()

    def test_scaffold_creates_agents_template_with_complete_payload(self) -> None:
        target_dir = self.workspace / "NewRepo"
        result = self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        assert result["operation_count"] == 1

        external_path = target_dir / "AGENTS.md"
        external_text = external_path.read_text(encoding="utf-8")
        assert "2. 技能类任务附加入口" in external_text
        assert "6. 治理链约束" in external_text
        assert external_text.count("- replace_me") == 6

        managed_dir = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "NewRepo"
        )
        managed_machine = managed_dir / "AGENTS_machine.json"
        payload = json.loads(managed_machine.read_text(encoding="utf-8"))
        root_template = json.loads(
            (
                self.skill_root
                / "assets"
                / "managed_targets"
                / "AI_Projects"
                / "AGENTS_machine.json"
            ).read_text(encoding="utf-8")
        )
        assert list(payload.keys()) == list(root_template.keys())
        assert payload["entry_role"] == "replace_me"
        assert payload["runtime_source_policy"]["runtime_rule_source"] == "CLI_JSON"
        assert payload["runtime_source_policy"]["audit_fields_are_not_primary_runtime_instructions"] is True
        assert payload["runtime_source_policy"]["path_metadata_is_not_action_guidance"] is True
        assert payload["default_meta_skill_order"] == ["replace_me"]
        assert payload["turn_start_actions"] == ["replace_me"]
        assert payload["runtime_constraints"] == ["replace_me"]
        assert payload["execution_modes"]["READ_EXEC"]["goal"] == "replace_me"
        assert payload["execution_modes"]["READ_EXEC"]["default_actions"] == ["replace_me"]
        assert payload["execution_modes"]["WRITE_EXEC"]["goal"] == (
            "default to full-coverage edits for the intended change"
        )
        assert payload["execution_modes"]["WRITE_EXEC"]["default_actions"] == [
            "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
        ]
        assert payload["repo_local_contract_handoff"] == ["replace_me"]
        assert payload["forbidden_primary_runtime_pattern"] == []
        assert payload["turn_end_actions"] == ["replace_me"]

    def test_lint_fails_after_scaffold_for_new_agents_target_until_writeback(self) -> None:
        target_dir = self.workspace / "NewRepo"
        self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(target_dir / "AGENTS.md"),
            expect_ok=False,
        )
        assert result["failed_count"] == 1
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "external_replace_me_remaining" in error_text
        assert "payload_replace_me_remaining" in error_text

    def test_lint_detects_plain_mapping_drift(self) -> None:
        self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        managed = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "README_MD__governed_external.md"
        )
        write(managed, "# Drift\n")
        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(self.repo_root / "README.md"),
            expect_ok=False,
        )
        assert result["failed_count"] == 1
        assert "managed_mapping_content_drift" in result["failures"][0]["errors"]

    def test_target_contract_keeps_agents_payload(self) -> None:
        result = self.run_cli("target-contract", "--source-path", str(self.repo_root / "AGENTS.md"), "--json")
        assert result["channel_id"] == "AGENTS_MD"
        assert "owner" in result
        assert "payload" in result

    def test_contract_exposes_agents_payload_entry(self) -> None:
        result = self.run_cli("contract", "--json")
        assert result["skill_name"] == "Meta-RootFile-Manager"
        assert "agents_payload_contract" in result["tool_entry"]["commands"]
        assert "agents-payload-contract" in result["tool_entry"]["commands"]["agents_payload_contract"]
        assert "new_writeback" in result["tool_entry"]["commands"]
        assert "new-writeback" in result["tool_entry"]["commands"]["new_writeback"]

    def test_agents_payload_contract_returns_targeted_workflow(self) -> None:
        result = self.run_cli(
            "agents-payload-contract",
            "--source-path",
            str(self.repo_root / "AGENTS.md"),
            "--json",
        )
        assert result["channel_id"] == "AGENTS_MD"
        assert result["managed_files"]["machine"].endswith("AGENTS_machine.json")
        assert "Meta-Enhance-Prompt" in result["tool_entry"]["meta_enhance_prompt"]["contract"]
        assert any("smallest precise payload semantics" in item for item in result["workflow"])
        assert any("Do not add anything beyond the user request by default." == item for item in result["rules"])

    def test_agents_payload_contract_rejects_non_agents_source(self) -> None:
        result = self.run_cli(
            "agents-payload-contract",
            "--source-path",
            str(self.repo_root / "README.md"),
            "--json",
            expect_ok=False,
        )
        assert result["error"] == "agents_payload_contract_requires_agents_target"

    def test_new_writeback_rejects_replace_me_leftover(self) -> None:
        target_dir = self.workspace / "NewRepo"
        self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        result = self.run_cli(
            "new-writeback",
            "--json",
            "--source-path",
            str(target_dir / "AGENTS.md"),
            expect_ok=False,
        )
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "external_replace_me_remaining" in error_text
        assert "payload_replace_me_remaining" in error_text

    def test_new_writeback_finalizes_agents_after_fill(self) -> None:
        target_dir = self.workspace / "NewRepo"
        self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        external_path = target_dir / "AGENTS.md"
        managed_machine = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "NewRepo"
            / "AGENTS_machine.json"
        )
        managed_human = managed_machine.with_name("AGENTS_human.md")

        write(
            external_path,
            external_path.read_text(encoding="utf-8").replace("replace_me", "resolved_value"),
        )
        payload = json.loads(managed_machine.read_text(encoding="utf-8"))
        resolved_payload = resolve_replace_me(payload)
        write(managed_machine, json.dumps(resolved_payload, ensure_ascii=False, indent=2) + "\n")

        result = self.run_cli(
            "new-writeback",
            "--json",
            "--source-path",
            str(external_path),
        )
        assert result["operation_count"] == 1
        assert "replace_me" not in managed_human.read_text(encoding="utf-8")

    def test_lint_rejects_non_cli_root_entry_for_codex_skills_target(self) -> None:
        source_path = self.root / ".codex" / "skills" / "AGENTS.md"
        owner = self.run_cli(
            "target-contract",
            "--source-path",
            str(source_path),
            "--json",
            workspace_root=self.root,
        )["owner"]
        write(
            source_path,
            render_external_agents(
                (
                    "1. 根入口命令\n"
                    "- 这里不能写说明句子\n\n"
                    "2. 技能类任务附加入口\n"
                    "- N/A\n\n"
                    "3. 语言规范\n"
                    "- N/A\n\n"
                    "4. 当前受管 repo 边界\n"
                    "- 禁止直接在 `/tmp/.codex/skills` 安装目录修改技能。\n\n"
                    "5. Multi-AGENT 工作模式\n"
                    "- N/A\n\n"
                    "6. 治理链约束\n"
                    "- N/A\n"
                ),
                owner=owner,
            ),
        )
        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(source_path),
            workspace_root=self.root,
            expect_ok=False,
        )
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "codex_skills_root_entry_command_invalid" in error_text

    def test_lint_rejects_skill_name_repeated_outside_default_meta_skill_order(self) -> None:
        governed_owner = (
            "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 "
            "runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
        )
        invalid_payload = {
            "owner": governed_owner,
            "entry_role": "repo_runtime_entry",
            "runtime_source_policy": {
                "runtime_rule_source": "CLI_JSON",
                "audit_fields_are_not_primary_runtime_instructions": True,
                "path_metadata_is_not_action_guidance": True,
            },
            "default_meta_skill_order": [
                "$meta-github-operation (Git traceability for repo writes)",
            ],
            "peer_summary_policy": {
                "available": True,
                "relation": "same_level_summary",
                "read_policy": "available_for_public_product_summary",
                "guidance": "same-level README.md is available and should be treated as the public English product summary for this repo",
            },
            "language_policy": {
                "conversation_and_internal_coordination": "Chinese-first",
                "public_product_readme_and_docs": "English-only",
                "wizard_user_interface": "Bilingual English/Chinese required",
                "internal_skill_core_and_governance_docs": "Chinese allowed for internal iteration",
                "git_iteration_logs_for_github": "English-preferred",
            },
            "skills_required_techstacks": {
                "python_backend": [],
                "vue3_typescript_frontend": [],
            },
            "turn_start_actions": [
                "plan same-turn Git traceability through $meta-github-operation",
            ],
            "runtime_constraints": [
                "treat CLI JSON as the primary runtime rule source",
            ],
            "execution_modes": {
                "READ_EXEC": {
                    "goal": "inspect without changing files",
                    "default_actions": [],
                },
                "WRITE_EXEC": {
                    "goal": "edit files",
                    "default_actions": [],
                },
            },
            "forbidden_primary_runtime_pattern": [],
            "turn_end_actions": [],
            "repo_name": "Otctopus_OS_AgentConsole",
        }
        managed_human = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Otctopus_OS_AgentConsole"
            / "AGENTS_human.md"
        )
        managed_machine = managed_human.with_name("AGENTS_machine.json")
        write(managed_human, render_internal_human("repo root", invalid_payload))
        write(managed_machine, json.dumps(invalid_payload, ensure_ascii=False, indent=2) + "\n")

        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(self.repo_root / "AGENTS.md"),
            expect_ok=False,
        )

        error_text = "\n".join(result["failures"][0]["errors"])
        assert "payload_skill_repeated_outside_default_meta_skill_order:$meta-github-operation" in error_text

    def test_lint_rejects_parent_agents_duplicate_phrase(self) -> None:
        parent_external = self.workspace / "Octopus_OS" / "AGENTS.md"
        child_external = self.workspace / "Octopus_OS" / "Client_Applications" / "AGENTS.md"
        parent_phrase = "Parent duplicate phrase should not be repeated downstream"
        payload_phrase = "child payload must not repeat parent payload phrase exactly"

        write(self.workspace / "Octopus_OS" / "README.md", "# Octopus\n")
        write(parent_external, render_external_agents(parent_phrase))
        write(child_external, render_external_agents(parent_phrase))

        parent_managed_dir = (
            self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "Octopus_OS"
        )
        child_managed_dir = (
            parent_managed_dir / "Client_Applications"
        )
        parent_payload = json.loads((parent_managed_dir / "AGENTS_machine.json").read_text(encoding="utf-8"))
        child_payload = json.loads((child_managed_dir / "AGENTS_machine.json").read_text(encoding="utf-8"))
        parent_payload["runtime_constraints"] = [payload_phrase]
        child_payload["runtime_constraints"] = [payload_phrase]
        write(parent_managed_dir / "AGENTS_human.md", render_internal_human(parent_phrase, parent_payload))
        write(parent_managed_dir / "AGENTS_machine.json", json.dumps(parent_payload, ensure_ascii=False, indent=2) + "\n")
        write(child_managed_dir / "AGENTS_human.md", render_internal_human(parent_phrase, child_payload))
        write(child_managed_dir / "AGENTS_machine.json", json.dumps(child_payload, ensure_ascii=False, indent=2) + "\n")

        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(child_external),
            expect_ok=False,
        )

        error_text = "\n".join(result["failures"][0]["errors"])
        assert "parent_agents_duplicate_phrase:Octopus_OS/AGENTS.md:part_a" in error_text
        assert "parent_agents_duplicate_phrase:Octopus_OS/AGENTS.md:$.runtime_constraints[0]" in error_text

    def test_lint_rejects_nonstandard_write_exec_block(self) -> None:
        managed_machine = (
            self.skill_root
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "AGENTS_machine.json"
        )
        managed_human = managed_machine.with_name("AGENTS_human.md")
        invalid_payload = {
            "owner": self.run_cli(
                "target-contract",
                "--source-path",
                str(self.workspace / "AGENTS.md"),
                "--json",
            )["owner"],
            "entry_role": "workspace_root_runtime_entry",
            "runtime_source_policy": {
                "runtime_rule_source": "CLI_JSON",
                "audit_fields_are_not_primary_runtime_instructions": True,
                "path_metadata_is_not_action_guidance": True,
            },
            "default_meta_skill_order": [],
            "turn_start_actions": [],
            "runtime_constraints": [],
            "execution_modes": {
                "READ_EXEC": {
                    "goal": "answer, inspect, classify, or route without changing files",
                    "default_actions": [],
                },
                "WRITE_EXEC": {
            "goal": "edit files or trigger manager-owned write flows",
            "default_actions": [
                "edit the minimal correct scope that matches the user intent",
            ],
                },
            },
            "repo_local_contract_handoff": [],
            "forbidden_primary_runtime_pattern": [],
            "turn_end_actions": [],
        }
        write(managed_machine, json.dumps(invalid_payload, ensure_ascii=False, indent=2) + "\n")
        write(managed_human, render_internal_human("workspace root", invalid_payload))

        result = self.run_cli(
            "lint",
            "--json",
            "--source-path",
            str(self.workspace / "AGENTS.md"),
            expect_ok=False,
        )

        error_text = "\n".join(result["failures"][0]["errors"])
        assert "write_exec_goal_must_match_standard" in error_text
        assert "write_exec_default_actions_must_match_standard" in error_text

    def test_collect_prunes_legacy_alias_dir(self) -> None:
        self._seed_legacy_alias_dir()
        result = self.run_cli("collect", "--json", "--source-path", str(self.repo_root / "README.md"))
        assert any(item.endswith("Codex_Skills_Mirror") for item in result["removed_legacy_dirs"])
        assert not (
            self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror"
        ).exists()
        assert not (
            self.installed / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror"
        ).exists()

    def test_runtime_local_scaffold_uses_runtime_managed_assets_without_registry_writeback(self) -> None:
        target_dir = self.runtime / "sandbox" / "sample_repo" / "Development_Docs"
        result = self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        assert result["operation_count"] == 1
        external_path = target_dir / "AGENTS.md"
        assert external_path.exists()
        target_contract = self.run_cli("target-contract", "--source-path", str(external_path), "--json")
        assert target_contract["channel_id"] == "AGENTS_MD"
        assert target_contract["managed_dir"].startswith(str(self.runtime / "managed_targets"))
        assert not target_contract["managed_dir"].startswith(str(self.skill_root / "assets" / "managed_targets"))

        rules = json.loads((self.skill_root / "rules" / "scan_rules.json").read_text(encoding="utf-8"))
        governed = rules["channels"]["AGENTS_MD"]["governed_source_paths"]
        assert "Codex_Skill_Runtime/Meta-RootFile-Manager/sandbox/sample_repo/Development_Docs/AGENTS.md" not in governed
        assert not (
            self.installed
            / "assets"
            / "managed_targets"
            / "AI_Projects"
            / "Codex_Skill_Runtime"
            / "Meta-RootFile-Manager"
            / "sandbox"
            / "sample_repo"
            / "Development_Docs"
            / "AGENTS_human.md"
        ).exists()
        runtime_payload = json.loads(
            (
                self.runtime
                / "managed_targets"
                / "sandbox"
                / "sample_repo"
                / "Development_Docs"
                / "AGENTS_machine.json"
            ).read_text(encoding="utf-8")
        )
        assert runtime_payload["entry_role"] == "replace_me"
        assert runtime_payload["default_meta_skill_order"][0] == "replace_me"
        assert runtime_payload["execution_modes"]["WRITE_EXEC"]["default_actions"] == [
            "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
        ]

    def test_collect_runtime_local_agents_updates_runtime_managed_pair(self) -> None:
        target_dir = self.runtime / "sandbox" / "sample_repo" / "Development_Docs"
        self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        external_path = target_dir / "AGENTS.md"
        write(
            external_path,
            render_external_agents(
                "1. 根入口命令\n- 在处理当前目录路径规则之前，必须先运行：\n- `placeholder`\n",
                owner=self.run_cli("target-contract", "--source-path", str(external_path), "--json")["owner"],
            ),
        )
        result = self.run_cli("collect", "--json", "--source-path", str(external_path))
        assert result["operation_count"] == 1
        managed_human = (
            self.runtime
            / "managed_targets"
            / "sandbox"
            / "sample_repo"
            / "Development_Docs"
            / "AGENTS_human.md"
        )
        machine_payload = (
            self.runtime
            / "managed_targets"
            / "sandbox"
            / "sample_repo"
            / "Development_Docs"
            / "AGENTS_machine.json"
        )
        assert managed_human.exists()
        assert "placeholder" in managed_human.read_text(encoding="utf-8")
        assert json.loads(machine_payload.read_text(encoding="utf-8"))["owner"] == result["operations"][0]["owner"]
