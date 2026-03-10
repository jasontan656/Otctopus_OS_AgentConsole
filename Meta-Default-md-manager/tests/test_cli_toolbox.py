from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_external_agents(part_a_body: str) -> str:
    return (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n"
    )


def render_internal_human(part_a_body: str, payload: dict) -> str:
    return (
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        "<part_A>\n"
        f"{part_a_body}\n"
        "</part_A>\n\n"
        "<part_B>\n"
        "```json\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
        "```\n"
        "</part_B>\n"
    )


def root_payload() -> dict:
    return {
        "entry_role": "workspace_root_runtime_entry",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
        },
        "default_meta_skill_order": [
            "meta_prompt",
            "meta_mindchain",
            "meta_reasoningchain",
        ],
        "turn_start_actions": [
            "validate root AGENTS exists",
            "classify the turn as READ_EXEC or WRITE_EXEC",
        ],
        "runtime_constraints": [
            "treat CLI JSON as the primary runtime rule source",
            "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
        ],
        "execution_modes": {
            "READ_EXEC": {
                "goal": "answer without changing files",
                "default_actions": [
                    "prefer direct CLI contract output over opening markdown rule files",
                ],
            },
            "WRITE_EXEC": {
                "goal": "edit files or trigger manager-owned write flows",
                "default_actions": [
                    "apply the default meta sequence before editing",
                    "state the intended write scope before editing",
                ],
            },
        },
        "repo_local_contract_handoff": [
            "load repo-local target contract before repo-specific write, lint, or Git actions",
        ],
        "forbidden_primary_runtime_pattern": [
            "Do not treat audit markdown paths as the main runtime instructions.",
        ],
        "turn_end_actions": [
            "defer repo-specific lint or Git duties to the concrete repo-local contract when applicable",
        ],
    }


def repo_payload() -> dict:
    return {
        "entry_role": "repo_runtime_entry",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
        },
        "default_meta_skill_order": [
            "meta_prompt",
            "meta_mindchain",
            "meta_reasoningchain",
        ],
        "peer_summary_policy": {
            "available": False,
            "relation": "same_level_summary",
            "read_policy": "not_available",
            "guidance": "same-level README.md is not available for this target",
        },
        "turn_start_actions": [
            "use the returned target contract JSON as the runtime rule source",
            "classify the turn as READ_EXEC or WRITE_EXEC",
        ],
        "runtime_constraints": [
            "treat CLI JSON as the primary runtime rule source",
            "stay within the concrete repo-local boundary defined by this payload",
        ],
        "execution_modes": {
            "READ_EXEC": {
                "goal": "answer without changing files",
                "default_actions": [
                    "prefer direct CLI contract output over opening markdown rule files",
                ],
            },
            "WRITE_EXEC": {
                "goal": "edit files or trigger manager-owned write flows",
                "default_actions": [
                    "state the intended write scope before editing",
                    "complete same-turn commit-and-push when Codex_Skills_Mirror files are written",
                ],
            },
        },
        "forbidden_primary_runtime_pattern": [
            "Do not treat audit markdown paths as the main runtime instructions.",
        ],
        "turn_end_actions": [
            "run Constitution lint on the concrete Codex_Skills_Mirror target root",
        ],
        "repo_name": "Codex_Skills_Mirror",
    }


def legacy_repo_payload() -> dict:
    return {
        "entry_role": "repo_runtime_entry",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
        },
        "document_semantic_standard": [
            "single document, single semantic theme",
        ],
        "peer_summary_policy": {
            "available": False,
            "relation": "same_level_summary",
            "read_policy": "not_available",
            "guidance": "same-level README.md is not available for this target",
        },
        "turn_start_actions": [
            "use the returned target contract JSON as the runtime rule source",
            "classify the turn as READ_EXEC or WRITE_EXEC",
        ],
        "runtime_constraints": [
            "treat CLI JSON as the primary runtime rule source",
            "stay within the concrete Codex_Skills_Mirror repo boundary defined by this payload",
        ],
        "execution_modes": {
            "READ_EXEC": {
                "goal": "answer without changing files",
                "default_actions": [
                    "prefer direct CLI contract output over opening markdown rule files",
                ],
            },
            "WRITE_EXEC": {
                "goal": "edit files or trigger manager-owned write flows",
                "default_must_use": [
                    "meta_github_operation",
                ],
                "default_actions": [
                    "state the intended write scope before editing",
                ],
            },
        },
        "forbidden_primary_runtime_pattern": [
            "Do not treat audit markdown paths as the main runtime instructions.",
        ],
        "turn_end_actions": [
            "run Constitution lint on the concrete Codex_Skills_Mirror target root",
        ],
        "repo_name": "Codex_Skills_Mirror",
    }


class CliToolboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.workspace = self.root / "AI_Projects"
        self.runtime = self.workspace / "Codex_Skill_Runtime" / "Meta-Default-md-manager"
        self.mirror = self.workspace / "Codex_Skills_Mirror" / "Meta-Default-md-manager"
        self.installed = self.root / ".codex" / "skills" / "Meta-Default-md-manager"

        real_skill_root = Path(__file__).resolve().parents[1]
        payload_contract = (
            real_skill_root / "references" / "runtime_contracts" / "AGENTS_payload_structure.json"
        ).read_text(encoding="utf-8")

        write(
            self.mirror / "rules" / "scan_rules.json",
            json.dumps(
                {
                    "version": 1,
                    "governed_source_paths": [
                        "AGENTS.md",
                        "Codex_Skills_Mirror/AGENTS.md",
                    ],
                    "exact_filename_rules": ["AGENTS.md"],
                    "keyword_rules": [],
                    "disallowed_path_keywords": ["Octopus_OS"],
                    "structure_template_map": {
                        "AGENTS.md": "references/runtime_contracts/AGENTS_content_structure.md"
                    },
                }
            ),
        )
        write(
            self.mirror / "references" / "runtime_contracts" / "AGENTS_payload_structure.json",
            payload_contract,
        )
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_machine.json",
            json.dumps(repo_payload(), ensure_ascii=False, indent=2),
        )
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_machine.json",
            json.dumps(root_payload(), ensure_ascii=False, indent=2),
        )
        write(
            self.workspace / "AGENTS.md",
            render_external_agents("root"),
        )
        write(
            self.workspace / "Codex_Skills_Mirror" / "AGENTS.md",
            render_external_agents("repo"),
        )
        write(
            self.workspace / "Octopus_OS" / "AGENTS.md",
            render_external_agents("excluded"),
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["MDM_WORKSPACE_ROOT"] = str(self.workspace)
        env["MDM_MIRROR_SKILL_ROOT"] = str(self.mirror)
        env["MDM_INSTALLED_SKILL_ROOT"] = str(self.installed)
        env["MDM_RUNTIME_ROOT"] = str(self.runtime)
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_scan_finds_governed_agents_and_excludes_octopus_os(self) -> None:
        result = self.run_cli("scan", "--json", "--write-runtime-report")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        paths = [item["relative_path"] for item in payload["entries"]]
        self.assertIn("AGENTS.md", paths)
        self.assertIn("Codex_Skills_Mirror/AGENTS.md", paths)
        self.assertNotIn("Octopus_OS/AGENTS.md", paths)
        self.assertEqual(sorted(paths), ["AGENTS.md", "Codex_Skills_Mirror/AGENTS.md"])
        self.assertTrue((self.runtime / "scan" / "latest.json").exists())

    def test_collect_creates_internal_human_and_syncs_installed(self) -> None:
        result = self.run_cli("collect", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        mirror_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        installed_human = self.installed / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        self.assertTrue(mirror_human.exists())
        self.assertEqual(mirror_human.read_text(encoding="utf-8"), installed_human.read_text(encoding="utf-8"))
        human_text = mirror_human.read_text(encoding="utf-8")
        self.assertIn("<part_A>", human_text)
        self.assertIn("<part_B>", human_text)
        self.assertIn("```json", human_text)
        payload = json.loads(result.stdout)
        self.assertNotIn("legacy_part_a_marker_detected", payload["operations"][0])

    def test_push_exports_only_part_a(self) -> None:
        human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        write(human, render_internal_human("repo updated", repo_payload()))
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_machine.json",
            json.dumps(repo_payload(), ensure_ascii=False, indent=2),
        )
        result = self.run_cli("push", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        external = (self.workspace / "Codex_Skills_Mirror" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("repo updated", external)
        self.assertIn("<part_A>", external)
        self.assertNotIn("<part_B>", external)

    def test_target_contract_reads_machine_payload(self) -> None:
        result = self.run_cli(
            "target-contract",
            "--source-path",
            str(self.workspace / "Codex_Skills_Mirror" / "AGENTS.md"),
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["payload"]["repo_name"], "Codex_Skills_Mirror")

    def test_scan_can_filter_exact_source_path(self) -> None:
        result = self.run_cli(
            "scan",
            "--json",
            "--source-path",
            str(self.workspace / "Codex_Skills_Mirror" / "AGENTS.md"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([item["relative_path"] for item in payload["entries"]], ["Codex_Skills_Mirror/AGENTS.md"])

    def test_scaffold_creates_external_and_internal_agents_skeletons(self) -> None:
        target_dir = self.workspace / "New_Module"
        result = self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--all-governed",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        external = target_dir / "AGENTS.md"
        human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "New_Module" / "AGENTS_human.md"
        machine = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "New_Module" / "AGENTS_machine.json"
        self.assertTrue(external.exists())
        self.assertTrue(human.exists())
        self.assertTrue(machine.exists())
        self.assertIn("<part_A>", external.read_text(encoding="utf-8"))
        self.assertNotIn("<part_B>", external.read_text(encoding="utf-8"))
        self.assertIn("<part_B>", human.read_text(encoding="utf-8"))
        self.assertEqual(json.loads(machine.read_text(encoding="utf-8")), {})
        updated_rules = json.loads((self.mirror / "rules" / "scan_rules.json").read_text(encoding="utf-8"))
        self.assertIn("New_Module/AGENTS.md", updated_rules["governed_source_paths"])

    def test_lint_accepts_current_locked_structure(self) -> None:
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        root_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        write(repo_human, render_internal_human("repo", repo_payload()))
        write(root_human, render_internal_human("root", root_payload()))
        result = self.run_cli("lint", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_lint_rejects_legacy_external_shape(self) -> None:
        write(
            self.workspace / "AGENTS.md",
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n`HOOK_LOAD`: Apply this AGENTS contract.\n\n[PART A]\nroot\n",
        )
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        root_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        write(repo_human, render_internal_human("repo", repo_payload()))
        write(root_human, render_internal_human("root", root_payload()))
        result = self.run_cli("lint", "--json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertTrue(
            any(
                "legacy_part_a_marker_forbidden" in error
                for failure in payload["failures"]
                for error in failure["errors"]
            )
        )

    def test_lint_rejects_repo_machine_payload_structure_drift(self) -> None:
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        root_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        write(repo_human, render_internal_human("repo", repo_payload()))
        write(root_human, render_internal_human("root", root_payload()))
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_machine.json",
            json.dumps(legacy_repo_payload(), ensure_ascii=False, indent=2),
        )
        result = self.run_cli("lint", "--json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertTrue(
            any(
                "payload_extra_key:$.document_semantic_standard" in error
                or "payload_missing_key:$.default_meta_skill_order" in error
                for failure in payload["failures"]
                for error in failure["errors"]
            )
        )

    def test_lint_rejects_repo_human_payload_structure_drift(self) -> None:
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        root_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        write(repo_human, render_internal_human("repo", legacy_repo_payload()))
        write(root_human, render_internal_human("root", root_payload()))
        result = self.run_cli("lint", "--json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertTrue(
            any(
                "payload_extra_key:$.document_semantic_standard" in error
                or "payload_missing_key:$.default_meta_skill_order" in error
                for failure in payload["failures"]
                for error in failure["errors"]
            )
        )


if __name__ == "__main__":
    unittest.main()
