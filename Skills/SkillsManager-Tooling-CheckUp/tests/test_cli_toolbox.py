from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"
RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "references" / "runtime_contracts"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def extract_part_b_payload(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    marker_open = "```json\n"
    marker_close = "\n```"
    start = text.index(marker_open) + len(marker_open)
    end = text.index(marker_close, start)
    return json.loads(text[start:end])


class CliToolboxTests(unittest.TestCase):
    def test_contract_returns_json_payload(self) -> None:
        completed = run_cli("contract", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["contract_name"], "skills_tooling_checkup_runtime_contract")
        self.assertEqual(payload["tool_entry"]["commands"]["contract"], "./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json")

    def test_directive_returns_known_topic(self) -> None:
        completed = run_cli("directive", "--topic", "read-audit", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["topic"], "read-audit")
        self.assertEqual(payload["doc_kind"], "instruction")

    def test_directive_rejects_unknown_topic(self) -> None:
        completed = run_cli("directive", "--topic", "missing-topic", "--json")
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["error"], "unknown_directive_topic")

    def test_govern_target_reports_non_compliant_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "Example-Skill"
            (target_root / "agents").mkdir(parents=True)
            (target_root / "scripts").mkdir(parents=True)
            (target_root / "references" / "runtime_contracts").mkdir(parents=True)
            (target_root / "references" / "governance").mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: Example Skill\ndescription: example\n---\n\n# Example Skill\n",
                encoding="utf-8",
            )
            (target_root / "agents" / "openai.yaml").write_text("interface:\n  default_prompt: \"read markdown\"\n", encoding="utf-8")
            (target_root / "scripts" / "Cli_Toolbox.py").write_text("print('tooling')\n", encoding="utf-8")
            (target_root / "references" / "runtime_contracts" / "EXAMPLE_CONTRACT_human.md").write_text(
                "<part_A>\ntext\n</part_A>\n\n<part_B>\n\n```json\n{}\n```\n</part_B>\n",
                encoding="utf-8",
            )
            (target_root / "references" / "governance" / "LEGACY_CONTRACT.md").write_text("# legacy\n", encoding="utf-8")

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["compliant"])
            self.assertIn("references/runtime_contracts/EXAMPLE_CONTRACT_human.md", payload["audit"]["missing_json_payloads"])
            self.assertIn("references/governance/LEGACY_CONTRACT.md", payload["audit"]["legacy_markdown_only_assets"])
            self.assertFalse(payload["audit"]["agent_prompt_cli_first"])
            self.assertTrue(payload["audit"]["tooling_surface_detected"])
            self.assertEqual(payload["action"], "govern_target_skill_tooling")

    def test_govern_target_reports_no_tooling_surface_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "No-Tooling-Skill"
            target_root.mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: No Tooling\ndescription: example\n---\n\n# No Tooling\n",
                encoding="utf-8",
            )

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertTrue(payload["compliant"])
            self.assertEqual(payload["audit"]["audit_mode"], "no_tooling_surface_detected")
            self.assertFalse(payload["audit"]["tooling_surface_detected"])

    def test_govern_target_requires_runtime_surface_when_tooling_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir) / "Tooling-Skill"
            (target_root / "scripts").mkdir(parents=True)
            (target_root / "SKILL.md").write_text(
                "---\nname: Tooling Skill\ndescription: example\n---\n\n# Tooling Skill\n",
                encoding="utf-8",
            )
            (target_root / "scripts" / "Cli_Toolbox.py").write_text("print('tooling')\n", encoding="utf-8")

            completed = run_cli("govern-target", "--target-skill-root", str(target_root), "--json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["compliant"])
            self.assertEqual(payload["audit"]["audit_mode"], "tooling_surface_audit")
            self.assertTrue(payload["audit"]["tooling_surface_detected"])

    def test_human_and_json_payloads_match(self) -> None:
        for json_path in sorted(RUNTIME_ROOT.glob("*.json")):
            if json_path.name == "DIRECTIVE_INDEX.json":
                continue
            human_path = json_path.with_name(f"{json_path.stem}_human.md")
            self.assertTrue(human_path.exists(), human_path)
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8")), extract_part_b_payload(human_path))


if __name__ == "__main__":
    unittest.main()
