from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConstitutionToolingTests(unittest.TestCase):
    def test_frontend_governance_artifacts_are_removed(self) -> None:
        registry = (ROOT / "references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml").read_text(encoding="utf-8")
        graph = (ROOT / "references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md").read_text(encoding="utf-8")
        machine = (ROOT / "references/anchor_docs_machine/anchor_docs_machine_v1.jsonl").read_text(encoding="utf-8")

        self.assertNotIn("constraint_frontend_expansion_rule", registry)
        self.assertNotIn("constraint_frontend_expansion_rule", machine)
        self.assertNotIn("frontend_domain", graph)

    def test_query_contract_has_new_gates(self) -> None:
        output = subprocess.check_output(
            [
                "python3",
                str(ROOT / "scripts/constitution_keyword_query.py"),
                "--keywords-zh",
                "会话,权限",
                "--keywords-en",
                "session,permission",
            ],
            text=True,
        ).splitlines()
        rows = [json.loads(line) for line in output]
        contract = next(row for row in rows if row["record"] == "constitution_enforcement_contract")
        self.assertIn("typed_contract_gate", contract["required_gates"])
        self.assertIn("payload_normalize_gate", contract["required_gates"])
        self.assertIn("permission_boundary_gate", contract["required_gates"])
        self.assertTrue(all("common_observability" not in json.dumps(row, ensure_ascii=False) for row in rows))

    def test_static_lints_detect_and_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            bad = root / "bad"
            bad.mkdir()
            (bad / "user_domain.py").write_text(
                "import requests\nrequests.get(\"https://example.com\")\n",
                encoding="utf-8",
            )
            bad_result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(bad)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(bad_result.returncode, 1)
            bad_report = json.loads(bad_result.stdout)
            self.assertTrue(any(g["gate"] == "modularity_gate" and g["status"] == "fail" for g in bad_report["gates"]))

            good = root / "good"
            (good / "rules").mkdir(parents=True)
            (good / "modules").mkdir(parents=True)
            (good / "contracts.schema.json").write_text(
                '{"contract_name":"x","contract_version":"1.0.0","required_fields":[],"optional_fields":[],"validation_mode":"strict"}',
                encoding="utf-8",
            )
            (good / "auth_policy.yaml").write_text(
                'actor_id: u\nrole: admin\nscope: all\naction: run\npolicy_version: 1\nauthz_result: allow\ndeny_code: none\napproval_ref: apr-1\nhigh_risk: true\n',
                encoding="utf-8",
            )
            (good / "payload_normalizer.py").write_text(
                'trace_id="t"\nsession_id="s"\nactor_id="a"\nchannel="telegram"\npayload_version="1"\nschema_name="x"\nraw_ref="r"\ntelegram_update={}\n',
                encoding="utf-8",
            )
            good_result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(good)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(good_result.returncode, 0, good_result.stdout + good_result.stderr)

    def test_file_structure_repo_token_does_not_misfire_on_report(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            good = root / "good"
            good.mkdir()
            (good / "acceptance_report.md").write_text("# ok\n", encoding="utf-8")
            good_result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(good)],
                text=True,
                capture_output=True,
                check=False,
            )
            good_report = json.loads(good_result.stdout)
            file_structure_gate = next(g for g in good_report["gates"] if g["gate"] == "file_structure_gate")
            self.assertFalse(
                any(v["reason"] == "repo_name_must_end_with__repo.py" for v in file_structure_gate["violations"]),
                good_result.stdout + good_result.stderr,
            )

            bad = root / "bad"
            bad.mkdir()
            (bad / "user_repository.py").write_text("VALUE = 1\n", encoding="utf-8")
            bad_result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(bad)],
                text=True,
                capture_output=True,
                check=False,
            )
            bad_report = json.loads(bad_result.stdout)
            file_structure_gate = next(g for g in bad_report["gates"] if g["gate"] == "file_structure_gate")
            self.assertTrue(
                any(v["reason"] == "repo_name_must_end_with__repo.py" for v in file_structure_gate["violations"]),
                bad_result.stdout + bad_result.stderr,
            )

    def test_fat_file_distinguishes_contract_support_from_real_cli(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            scripts = root / "scripts"
            scripts.mkdir(parents=True)

            contract_support = scripts / "workflow_stage_contract.py"
            contract_support.write_text("VALUE = 1\n" * 230, encoding="utf-8")

            cli_script = scripts / "run_cli.py"
            cli_script.write_text(
                "import argparse\n"
                "parser = argparse.ArgumentParser()\n"
                "parser.add_argument('--x')\n"
                + ("print('x')\n" * 221),
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            fat_gate = next(g for g in report["gates"] if g["gate"] == "fat_file_gate")
            violations = {v["path"]: v["reason"] for v in fat_gate["violations"]}
            self.assertNotIn("scripts/workflow_stage_contract.py", violations, result.stdout + result.stderr)
            self.assertEqual(violations.get("scripts/run_cli.py"), "cli_or_task_script>220", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
