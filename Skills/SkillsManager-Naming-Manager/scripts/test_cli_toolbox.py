from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "Cli_Toolbox.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


class CliToolboxTests(unittest.TestCase):
    def test_runtime_contract_returns_new_shape_payload(self) -> None:
        completed = run_cli("runtime-contract", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["skill_name"], "SkillsManager-Naming-Manager")
        self.assertEqual(payload["root_shape"], ["SKILL.md", "path", "agents", "scripts"])
        self.assertIn("read-contract-context", payload["commands"])

    def test_read_contract_context_compiles_naming_policy(self) -> None:
        completed = run_cli("read-contract-context", "--entry", "naming_policy", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["entry"], "naming_policy")
        self.assertIn("path/naming_policy/10_CONTRACT.md", payload["resolved_chain"])

    def test_read_contract_context_compiles_registry_chain(self) -> None:
        completed = run_cli("read-contract-context", "--entry", "registry_governance", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("path/registry_governance/25_SKILL_REGISTRY.md", payload["resolved_chain"])


if __name__ == "__main__":
    unittest.main()
