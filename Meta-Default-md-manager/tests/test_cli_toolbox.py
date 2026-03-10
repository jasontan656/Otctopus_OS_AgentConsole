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


class CliToolboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.workspace = self.root / "AI_Projects"
        self.runtime = self.workspace / "Codex_Skill_Runtime" / "Meta-Default-md-manager"
        self.mirror = self.workspace / "Codex_Skills_Mirror" / "Meta-Default-md-manager"
        self.installed = self.root / ".codex" / "skills" / "Meta-Default-md-manager"

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
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_machine.json",
            json.dumps({"mode": "repo"}, indent=2),
        )
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "AGENTS_machine.json",
            json.dumps({"mode": "root"}, indent=2),
        )
        write(
            self.workspace / "AGENTS.md",
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n`HOOK_LOAD`: Apply this AGENTS contract.\n\n[PART A]\n\nroot\n",
        )
        write(
            self.workspace / "Codex_Skills_Mirror" / "AGENTS.md",
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n`HOOK_LOAD`: Apply this AGENTS contract.\n\n[PART A]\n\nrepo\n",
        )
        write(
            self.workspace / "Octopus_OS" / "AGENTS.md",
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n`HOOK_LOAD`: Apply this AGENTS contract.\n\n[PART A]\n\nexcluded\n",
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

    def test_push_exports_only_part_a(self) -> None:
        human = self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_human.md"
        write(
            human,
            "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]\n\n`HOOK_LOAD`: Apply this AGENTS contract.\n\n<part_A>\nrepo updated\n</part_A>\n\n<part_B>\n```json\n{\n  \"mode\": \"repo\"\n}\n```\n</part_B>\n",
        )
        write(
            self.mirror / "assets" / "managed_targets" / "AI_Projects" / "Codex_Skills_Mirror" / "AGENTS_machine.json",
            json.dumps({"mode": "repo"}, indent=2),
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
        self.assertEqual(payload["payload"]["mode"], "repo")

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


if __name__ == "__main__":
    unittest.main()
