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
        "<part_B>\n\n"
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
            "$meta-github-operation ( applicable on every write_exec turn. Automatically push everything done to github for tracability )",
            "$skill-mirror-to-codex (all skill edit must happen first in octopus-os-agent-console or its legacy alias Codex_Skills_Mirror, then use the skill to push/install to the codex installation folder )",
            "$skill-creation-template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
            "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
            "$Constitution-knowledge-base (for skill CLI tool lints )",
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
            "$meta-github-operation (after any write to octopus-os-agent-console, commit-and-push the repo for Git traceability; Git push is not a substitute for syncing the codex installation directory)",
            "$skill-mirror-to-codex (edit skills only in the product repo mirror paths, never directly in the codex installation directory; after editing, use Push for already-installed skills and Install for newly created skills)",
            "$skill-creation-template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
            "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
            "$Constitution-knowledge-base (for skill CLI tool lints )",
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
        "turn_start_actions": [
            "use the returned target contract JSON as the runtime rule source",
            "classify the turn as READ_EXEC or WRITE_EXEC",
            "if the turn will write octopus-os-agent-console, plan same-turn Constitution lint and Git traceability from the start",
            "if the turn touches language surfaces, enforce outward English docs and inward Chinese development boundaries before editing",
            "if the turn will edit a skill, treat the mirror copy in the product repo as the only editable source and determine whether downstream sync must be Push or Install",
        ],
        "runtime_constraints": [
            "treat CLI JSON as the primary runtime rule source",
            "stay within the concrete repo-local boundary defined by this payload",
            "public-facing product README and docs must remain English-only",
            "end-user wizard and installation TUI surfaces must support both English and Chinese",
            "skill core docs, governance contracts, and internal iteration artifacts may remain Chinese-first",
            "GitHub-facing product iteration logs and commit subjects should prefer English wording",
            "product-facing docs and product tools must not be pushed into the codex installation directory; only syncable skill roots and .system may flow downstream",
        ],
        "execution_modes": {
            "READ_EXEC": {
                "goal": "answer without changing files",
                "default_actions": [
                    "prefer direct CLI contract output over opening markdown rule files",
                    "treat README.md as the public English summary instead of inferring product positioning from internal skill docs",
                ],
            },
            "WRITE_EXEC": {
                "goal": "edit files or trigger manager-owned write flows",
                "default_actions": [
                    "apply the default meta sequence before editing",
                    "state the intended write scope before editing",
                    "for public product surfaces, keep English-only wording and avoid leaking internal Chinese governance content",
                    "for skill edits, write only the mirror copy under the product repo and do not directly edit the codex installed copy",
                    "after skill edits, run skill-mirror-to-codex Push for existing installed skills or Install for newly created skills",
                    "run Constitution lint on octopus-os-agent-console before closing the turn",
                    "complete same-turn commit-and-push when octopus-os-agent-console files are written",
                ],
            },
        },
        "forbidden_primary_runtime_pattern": [
            "Do not treat audit markdown paths as the main runtime instructions.",
        ],
        "turn_end_actions": [
            "run Constitution lint on the concrete octopus-os-agent-console target root",
            "if the turn edited a skill, complete skill-mirror-to-codex Push or Install before closing the turn",
        ],
        "repo_name": "octopus-os-agent-console",
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
        self.repo_root = self.workspace / "octopus-os-agent-console"
        self.mirror = self.repo_root / "Meta-Default-md-manager"
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
                        "octopus-os-agent-console/AGENTS.md",
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
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_machine.json",
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
            self.repo_root / "AGENTS.md",
            render_external_agents("repo"),
        )
        os.symlink(self.repo_root, self.workspace / "Codex_Skills_Mirror", target_is_directory=True)
        write(self.repo_root / "README.md", "# Public Product Summary\n")
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
        self.assertIn("octopus-os-agent-console/AGENTS.md", paths)
        self.assertNotIn("Octopus_OS/AGENTS.md", paths)
        self.assertEqual(sorted(paths), ["AGENTS.md", "octopus-os-agent-console/AGENTS.md"])
        self.assertTrue((self.runtime / "scan" / "latest.json").exists())

    def test_collect_creates_internal_human_and_syncs_installed(self) -> None:
        result = self.run_cli("collect", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        mirror_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
        installed_human = self.installed / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
        self.assertTrue(mirror_human.exists())
        self.assertEqual(mirror_human.read_text(encoding="utf-8"), installed_human.read_text(encoding="utf-8"))
        human_text = mirror_human.read_text(encoding="utf-8")
        self.assertIn("<part_A>", human_text)
        self.assertIn("<part_B>", human_text)
        self.assertIn("```json", human_text)
        payload = json.loads(result.stdout)
        self.assertNotIn("legacy_part_a_marker_detected", payload["operations"][0])

    def test_push_exports_only_part_a(self) -> None:
        human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
        write(human, render_internal_human("repo updated", repo_payload()))
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_machine.json",
            json.dumps(repo_payload(), ensure_ascii=False, indent=2),
        )
        result = self.run_cli("push", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        external = (self.repo_root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("repo updated", external)
        self.assertIn("<part_A>", external)
        self.assertNotIn("<part_B>", external)

    def test_target_contract_reads_machine_payload(self) -> None:
        result = self.run_cli(
            "target-contract",
            "--source-path",
            str(self.repo_root / "AGENTS.md"),
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["payload"]["repo_name"], "octopus-os-agent-console")
        self.assertEqual(payload["payload"]["language_policy"]["public_product_readme_and_docs"], "English-only")

    def test_scan_can_filter_exact_source_path(self) -> None:
        result = self.run_cli(
            "scan",
            "--json",
            "--source-path",
            str(self.repo_root / "AGENTS.md"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([item["relative_path"] for item in payload["entries"]], ["octopus-os-agent-console/AGENTS.md"])

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
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
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
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
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
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
        root_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_human.md"
        write(repo_human, render_internal_human("repo", repo_payload()))
        write(root_human, render_internal_human("root", root_payload()))
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_machine.json",
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
        repo_human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "octopus-os-agent-console" / "AGENTS_human.md"
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

    def test_target_contract_accepts_legacy_repo_alias_source_path(self) -> None:
        result = self.run_cli(
            "target-contract",
            "--source-path",
            str(self.workspace / "Codex_Skills_Mirror" / "AGENTS.md"),
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(
            payload["managed_machine_path"].endswith(
                "assets/managed_targets/AI_Projects/octopus-os-agent-console/AGENTS_machine.json"
            )
        )


if __name__ == "__main__":
    unittest.main()
