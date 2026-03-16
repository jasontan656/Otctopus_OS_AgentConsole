from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"

ROOT_OWNER = "由 `$Meta-RootFile-Manager` 作为 `AI_Projects` workspace root 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
REPO_OWNER = "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"

DOMAIN_ORDER = (
    "hook_identity",
    "turn_start",
    "runtime_constraints",
    "execution_modes",
    "repo_handoff",
    "turn_end",
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_part_a(contract_body: str, reminder_body: str) -> str:
    return (
        "<contract>\n"
        f"{contract_body.strip()}\n"
        "</contract>\n\n"
        "<reminder>\n"
        f"{reminder_body.strip()}\n"
        "</reminder>"
    )


def render_external_agents(part_a_body: str) -> str:
    return (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        f"{part_a_body}\n"
    )


def render_internal_human(part_a_body: str, payload: dict, owner: str | None = None) -> str:
    blocks: list[str] = []
    for domain_id in DOMAIN_ORDER:
        block = payload[domain_id]
        serialized = {"domain_id": domain_id}
        serialized.update(block)
        blocks.append(f"```json\n{json.dumps(serialized, ensure_ascii=False, indent=2)}\n```")
    content = (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n\n"
        "<part_B>\n\n"
        f"{chr(10).join(blocks)}\n"
        "</part_B>\n"
    )
    if owner is None:
        return content
    return f"---\nowner: {json.dumps(owner, ensure_ascii=False)}\n---\n{content}"


def extract_payload_from_internal_human(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    part_b = text.split("<part_B>", 1)[1].split("</part_B>", 1)[0]
    payload: dict[str, dict] = {}
    for match in re.finditer(r"```json\n(.*?)\n```", part_b, flags=re.DOTALL):
        block = json.loads(match.group(1))
        domain_id = block.pop("domain_id")
        payload[domain_id] = block
    return payload


def workspace_part_a() -> str:
    contract = (
        "1. 合同定位\n"
        "- 本文件是测试用 workspace root 合同。\n\n"
        "2. 一级读取入口\n"
        "- `placeholder_root_command`\n\n"
        "3. 二级分域读取\n"
        "- hook_identity:\n"
        "- `placeholder_domain_command`\n\n"
        "4. 执行约束\n"
        "- 先读取相关二级合同再进入执行。"
    )
    reminder = (
        "1. 环境提醒\n"
        "- 当前环境为 `WSL`。\n\n"
        "2. 协作提醒\n"
        "- 对话输出以中文为主。"
    )
    return render_part_a(contract, reminder)


def repo_part_a() -> str:
    contract = (
        "1. 合同定位\n"
        "- 本文件是测试用 repo root 合同。\n\n"
        "2. 一级读取入口\n"
        "- `placeholder_repo_command`\n\n"
        "3. 二级分域读取\n"
        "- hook_identity:\n"
        "- `placeholder_repo_domain_command`\n\n"
        "4. 执行约束\n"
        "- 写入前先回到 repo 真源。"
    )
    reminder = (
        "1. 环境提醒\n"
        "- repo-local Python 位于 `./.venv_backend_skills`。\n\n"
        "2. 协作提醒\n"
        "- mirror/install 只作为同步面。"
    )
    return render_part_a(contract, reminder)


def workspace_payload(source_path: str) -> dict:
    def command(domain_id: str) -> str:
        return (
            f'python3 Cli_Toolbox.py agents-domain-contract --source-path "{source_path}" '
            f'--domain "{domain_id}" --json'
        )

    return {
        "hook_identity": {
            "read_command_preview": command("hook_identity"),
            "contract": {
                "entry_role": "test_runtime_contract",
                "contract_scope": "workspace_root",
                "secondary_contract_source": "CLI_JSON",
            },
        },
        "turn_start": {
            "read_command_preview": command("turn_start"),
            "contract": {
                "required_actions": [
                    f"read_target_contract:{source_path}",
                ]
            },
        },
        "runtime_constraints": {
            "read_command_preview": command("runtime_constraints"),
            "contract": {
                "rules": [
                    "language_primary:zh-CN",
                ]
            },
        },
        "execution_modes": {
            "read_command_preview": command("execution_modes"),
            "contract": {
                "READ_EXEC": {
                    "goal": "inspect_without_file_mutation",
                    "default_actions": ["read_contract_output_before_extra_files"],
                },
                "WRITE_EXEC": {
                    "goal": "default to full-coverage edits for the intended change",
                    "default_actions": [
                        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
                    ],
                },
            },
        },
        "repo_handoff": {
            "read_command_preview": command("repo_handoff"),
            "contract": {
                "rules": [
                    "merge_workspace_root_contract_with_repo_local_contract",
                ]
            },
        },
        "turn_end": {
            "read_command_preview": command("turn_end"),
            "contract": {
                "required_actions": [
                    "print_codex_session_id",
                ]
            },
        },
    }


def repo_payload(source_path: str) -> dict:
    def command(domain_id: str) -> str:
        return (
            f'python3 Cli_Toolbox.py agents-domain-contract --source-path "{source_path}" '
            f'--domain "{domain_id}" --json'
        )

    return {
        "hook_identity": {
            "read_command_preview": command("hook_identity"),
            "contract": {
                "entry_role": "repo_runtime_contract",
                "contract_scope": "repo_root",
                "secondary_contract_source": "CLI_JSON",
            },
        },
        "turn_start": {
            "read_command_preview": command("turn_start"),
            "contract": {
                "required_actions": [
                    f"read_target_contract:{source_path}",
                    "classify_turn_mode:READ_EXEC|WRITE_EXEC",
                ]
            },
        },
        "runtime_constraints": {
            "read_command_preview": command("runtime_constraints"),
            "contract": {
                "rules": [
                    "skills_truth_root:Skills",
                    "codex_installation_root:~/.codex/skills",
                ]
            },
        },
        "execution_modes": {
            "read_command_preview": command("execution_modes"),
            "contract": {
                "READ_EXEC": {
                    "goal": "inspect_repo_without_file_mutation",
                    "default_actions": ["read_repo_local_contract_before_skill_runtime_changes"],
                },
                "WRITE_EXEC": {
                    "goal": "default to full-coverage edits for the intended change",
                    "default_actions": [
                        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
                    ],
                },
            },
        },
        "repo_handoff": {
            "read_command_preview": command("repo_handoff"),
            "contract": {
                "rules": [
                    "use_repo_truth_source_for_skill_edits",
                ]
            },
        },
        "turn_end": {
            "read_command_preview": command("turn_end"),
            "contract": {
                "required_actions": [
                    "run_python_lint_if_python_files_changed",
                ]
            },
        },
    }


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
        write(self.workspace / "AGENTS.md", render_external_agents(workspace_part_a()))
        write(self.repo_root / "AGENTS.md", render_external_agents(repo_part_a()))
        write(self.repo_root / "README.md", "# Console\n")
        write(self.workspace / "Octopus_OS" / "README.md", "# Octopus\n")
        write(self.repo_root / ".gitignore", ".venv/\n")
        write(self.workspace / "Octopus_OS" / ".gitignore", ".cache/\n")
        write(self.repo_root / "pytest.ini", "[pytest]\n")
        write(self.repo_root / "requirements-backend_skills.lock.txt", "pytest==8.0.0\n")

    def _seed_managed_agents(self) -> None:
        root_assets = self.skill_root / "assets" / "managed_targets" / "AI_Projects"
        write(
            root_assets / "AGENTS_human.md",
            render_internal_human(workspace_part_a(), workspace_payload("/workspace/AGENTS.md"), ROOT_OWNER),
        )
        write(
            root_assets / "Otctopus_OS_AgentConsole" / "AGENTS_human.md",
            render_internal_human(
                repo_part_a(),
                repo_payload("/workspace/Otctopus_OS_AgentConsole/AGENTS.md"),
                REPO_OWNER,
            ),
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
        assert (self.runtime / "artifacts" / "scan" / "latest.json").exists()

    def test_collect_syncs_plain_mapping_and_installed_copy(self) -> None:
        result = self.run_cli("collect", "--json")
        operations = [item for item in result["operations"] if item["channel_id"] == "README_MD"]
        assert operations
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
        assert managed.exists()
        assert installed.exists()

    def test_target_contract_returns_contract_blocks_and_secondary_reads(self) -> None:
        result = self.run_cli(
            "target-contract",
            "--source-path",
            str(self.workspace / "AGENTS.md"),
            "--json",
        )
        assert "contract_blocks" in result
        assert "secondary_contract_reads" in result
        assert "payload" not in result
        assert list(result["contract_blocks"].keys()) == list(DOMAIN_ORDER)
        assert len(result["secondary_contract_reads"]) == len(DOMAIN_ORDER)

    def test_agents_domain_contract_returns_requested_block(self) -> None:
        result = self.run_cli(
            "agents-domain-contract",
            "--source-path",
            str(self.workspace / "AGENTS.md"),
            "--domain",
            "execution_modes",
            "--json",
        )
        assert result["domain_id"] == "execution_modes"
        assert "WRITE_EXEC" in result["contract"]

    def test_agents_payload_contract_exposes_domain_workflow(self) -> None:
        result = self.run_cli(
            "agents-payload-contract",
            "--source-path",
            str(self.workspace / "AGENTS.md"),
            "--json",
        )
        assert any("domain-contract semantics" in item for item in result["workflow"])
        assert result["secondary_contract_reads"][0]["domain_id"] == "hook_identity"

    def test_scaffold_creates_split_domain_agents_template(self) -> None:
        target_dir = self.workspace / "tmpabc1234" / "sample_repo"
        result = self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        assert result["operation_count"] == 1
        managed_human = (
            self.runtime
            / "managed_targets"
            / "ephemeral_workspace"
            / "tmpabc1234"
            / "sample_repo"
            / "AGENTS_human.md"
        )
        text = managed_human.read_text(encoding="utf-8")
        assert "<contract>" in text
        assert "<reminder>" in text
        assert text.count("```json") == len(DOMAIN_ORDER)
        assert '"domain_id": "hook_identity"' in text

    def test_agents_maintain_updates_contract_surface_without_breaking_layout(self) -> None:
        result = self.run_cli(
            "agents-maintain",
            "--intent",
            '在 "/home/jasontan656/AI_Projects/AGENTS.md" 的 "4. 执行约束" 新增 "先读取目标分域合同再写入"',
            "--json",
        )
        assert result["write_status"] == "applied"
        assert result["selected_part"] == "part_a"
        external_text = (self.workspace / "AGENTS.md").read_text(encoding="utf-8")
        assert "<contract>" in external_text
        assert "<reminder>" in external_text
        assert "先读取目标分域合同再写入" in external_text

    def test_agents_maintain_updates_domain_block(self) -> None:
        result = self.run_cli(
            "agents-maintain",
            "--intent",
            '在 "/home/jasontan656/AI_Projects/AGENTS.md" 的 runtime_constraints 新增 "github_managed_repos:Octopus_OS"',
            "--json",
        )
        assert result["write_status"] == "applied"
        assert result["selected_part"] == "payload"
        managed_human = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        payload_blocks = extract_payload_from_internal_human(managed_human)
        assert "github_managed_repos:Octopus_OS" in payload_blocks["runtime_constraints"]["contract"]["rules"]

    def test_push_exports_visible_contract_surface_only(self) -> None:
        managed_human = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        updated = render_internal_human(
            render_part_a(
                "1. 合同定位\n- 新合同正文。\n\n2. 一级读取入口\n- `cmd`\n\n3. 二级分域读取\n- hook_identity:\n- `cmd2`\n\n4. 执行约束\n- 先看合同。",
                "1. 环境提醒\n- 只是提醒。\n\n2. 协作提醒\n- 继续中文。",
            ),
            workspace_payload("/workspace/AGENTS.md"),
            ROOT_OWNER,
        )
        write(managed_human, updated)
        result = self.run_cli("push", "--json")
        assert result["failures"] == []
        external_text = (self.workspace / "AGENTS.md").read_text(encoding="utf-8")
        assert "新合同正文" in external_text
        assert "<part_B>" not in external_text
        assert "<part_A>" not in external_text
        assert not external_text.startswith("---\n")

    def test_lint_rejects_external_frontmatter_and_internal_part_a_shell(self) -> None:
        invalid_external = (
            "---\n"
            f"owner: {json.dumps(ROOT_OWNER, ensure_ascii=False)}\n"
            "doc_id: leaked\n"
            "---\n"
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
            "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
            "<part_A>\n"
            f"{workspace_part_a()}\n"
            "</part_A>\n"
        )
        write(self.workspace / "AGENTS.md", invalid_external)
        result = self.run_cli("lint", "--json", expect_ok=False)
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "external_agents_forbids_frontmatter" in error_text
        assert "external_agents_forbids_internal_part_a_wrapper" in error_text

    def test_lint_rejects_hard_contract_marker_inside_reminder(self) -> None:
        managed_human = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        invalid_part_a = render_part_a(
            "1. 合同定位\n- 合同正文。\n\n2. 一级读取入口\n- `cmd`\n\n3. 二级分域读取\n- hook_identity:\n- `cmd2`\n\n4. 执行约束\n- 先看合同。",
            "1. 环境提醒\n- 必须先执行提醒。\n\n2. 协作提醒\n- 中文。",
        )
        write(managed_human, render_internal_human(invalid_part_a, workspace_payload("/workspace/AGENTS.md"), ROOT_OWNER))
        result = self.run_cli("lint", "--json", expect_ok=False)
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "reminder_hard_contract_marker" in error_text

    def test_lint_rejects_duplicate_domain_id_block(self) -> None:
        managed_human = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        text = managed_human.read_text(encoding="utf-8")
        duplicate = (
            "\n```json\n"
            + json.dumps(
                {
                    "domain_id": "hook_identity",
                    "read_command_preview": "python3 Cli_Toolbox.py agents-domain-contract --source-path \"/workspace/AGENTS.md\" --domain \"hook_identity\" --json",
                    "contract": {
                        "entry_role": "dup",
                        "contract_scope": "workspace_root",
                        "secondary_contract_source": "CLI_JSON",
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n```\n"
        )
        text = text.replace("</part_B>", f"{duplicate}</part_B>")
        write(managed_human, text)
        result = self.run_cli("lint", "--json", expect_ok=False)
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "part_b_block_duplicate_domain_id:hook_identity" in error_text

    def test_lint_rejects_soft_marker_in_domain_block(self) -> None:
        managed_human = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        invalid_payload = workspace_payload("/workspace/AGENTS.md")
        invalid_payload["runtime_constraints"]["contract"]["rules"] = ["repo summary"]
        write(managed_human, render_internal_human(workspace_part_a(), invalid_payload, ROOT_OWNER))
        result = self.run_cli("lint", "--json", expect_ok=False)
        error_text = "\n".join(result["failures"][0]["errors"])
        assert "payload_soft_marker_forbidden:$.runtime_constraints.contract.rules[0]:summary" in error_text

    def test_payload_owner_stays_in_frontmatter(self) -> None:
        managed_human = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        payload_blocks = extract_payload_from_internal_human(managed_human)
        assert "owner" not in payload_blocks
