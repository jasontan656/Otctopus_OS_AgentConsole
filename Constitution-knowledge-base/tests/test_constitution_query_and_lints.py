from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConstitutionToolingTests(unittest.TestCase):
    def _assert_enhanced_report_shape(self, report: dict[str, object]) -> None:
        self.assertIn("summary_enhanced", report)
        self.assertIn("gate_diagnostics", report)
        self.assertIn("violation_details", report)
        self.assertIn("clusters", report)
        summary = report["summary_enhanced"]
        self.assertIn("failed_gate_count", summary)
        self.assertIn("total_violation_count", summary)
        self.assertIn("deduped_issue_count", summary)
        self.assertIn("likely_rule_scope_issues", summary)
        self.assertIn("likely_real_code_issues", summary)

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
        self.assertIn("hardcoded_asset_gate", contract["required_gates"])
        self.assertIn("absolute_path_gate", contract["required_gates"])
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
            self._assert_enhanced_report_shape(bad_report)
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
            self._assert_enhanced_report_shape(json.loads(good_result.stdout))

    def test_hardcoded_asset_gate_detects_inline_prompt_and_allows_external_asset(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp) / "skill_repo"
            root.mkdir()
            bad = root / "bad_prompt.py"
            bad.write_text(
                'PROMPT = """\n'
                "You are an audit assistant.\n"
                "## 1. Goal\n"
                "- 你是审计助手\n"
                "- 必须读取规则\n"
                "- 禁止跳过验证\n"
                "- 输出契约固定\n"
                "- workflow 需要完整\n"
                "- name: inline\n"
                "- description: inline\n"
                '"""\n',
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
            self._assert_enhanced_report_shape(report)
            gate = next(g for g in report["gates"] if g["gate"] == "hardcoded_asset_gate")
            self.assertTrue(any(v["path"] == "bad_prompt.py" for v in gate["violations"]), result.stdout + result.stderr)
            detail = next(v for v in report["violation_details"] if v["gate"] == "hardcoded_asset_gate" and v["path"] == "bad_prompt.py")
            self.assertEqual(detail["category"], "embedded_markdown_template")
            self.assertTrue(detail["line_hits"], result.stdout + result.stderr)
            self.assertIn("workflow", detail["matched_text_preview"], result.stdout + result.stderr)
            self.assertTrue(detail["cluster_key"].startswith("hardcoded_asset:"), result.stdout + result.stderr)
            self.assertTrue(detail["suggested_fix"], result.stdout + result.stderr)
            self.assertTrue(any(cluster["cluster_key"] == detail["cluster_key"] for cluster in report["clusters"]), result.stdout + result.stderr)

            good = root / "loader.py"
            (root / "assets").mkdir(exist_ok=True)
            (root / "assets" / "prompt.txt").write_text("You are an audit assistant.\n", encoding="utf-8")
            good.write_text(
                "from pathlib import Path\n"
                "PROMPT_PATH = Path(__file__).parent / 'assets' / 'prompt.txt'\n"
                "PROMPT = PROMPT_PATH.read_text(encoding='utf-8')\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "hardcoded_asset_gate")
            self.assertFalse(any(v["path"] == "loader.py" for v in gate["violations"]), result.stdout + result.stderr)

    def test_absolute_path_gate_respects_octopus_boundary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            octopus_root = Path(tmp) / "Octopus_OS"
            octopus_root.mkdir()
            (octopus_root / "deploy.py").write_text(
                'CONFIG = "/home/jasontan656/AI_Projects/Octopus_OS/config/settings.yaml"\n'
                'ESCAPE = "../../shared/runtime.json"\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(octopus_root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self._assert_enhanced_report_shape(report)
            gate = next(g for g in report["gates"] if g["gate"] == "absolute_path_gate")
            reasons = {v["reason"] for v in gate["violations"]}
            self.assertIn("octopus_os_forbids_unix_absolute_paths", reasons, result.stdout + result.stderr)
            self.assertIn("octopus_os_forbids_ai_projects_prefix", reasons, result.stdout + result.stderr)
            self.assertIn("octopus_os_forbids_repo_escape_relative_paths", reasons, result.stdout + result.stderr)
            detail = next(
                v
                for v in report["violation_details"]
                if v["gate"] == "absolute_path_gate" and v["reason"] == "octopus_os_forbids_unix_absolute_paths"
            )
            self.assertEqual(detail["category"], "user_absolute_path_literal")
            self.assertTrue(detail["line_hits"], result.stdout + result.stderr)
            self.assertIn("/home/jasontan656/AI_Projects/Octopus_OS", detail["matched_text_preview"], result.stdout + result.stderr)
            self.assertTrue(detail["suggested_fix"], result.stdout + result.stderr)

    def test_absolute_path_gate_allows_ai_projects_prefix_for_workspace_manager_repo(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            manager_root = Path(tmp) / "Codex_Skills_Mirror"
            manager_root.mkdir()
            (manager_root / "sync.py").write_text(
                'MIRROR = "AI_Projects/Codex_Skills_Mirror/Meta-Skill-Mirror"\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(manager_root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            (manager_root / "bad_home.py").write_text(
                'SECRET = "/home/jasontan656/.ssh/id_rsa"\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                ["python3", str(ROOT / "scripts/run_constitution_lints.py"), "--target", str(manager_root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "absolute_path_gate")
            self.assertTrue(
                any(v["reason"] == "non_octopus_repo_forbids_user_absolute_paths" for v in gate["violations"]),
                result.stdout + result.stderr,
            )
            detail = next(
                v
                for v in report["violation_details"]
                if v["gate"] == "absolute_path_gate" and v["path"] == "bad_home.py"
            )
            self.assertEqual(detail["issue_kind"], "real_content_issue")
            gate_diag = next(g for g in report["gate_diagnostics"] if g["gate"] == "absolute_path_gate")
            self.assertIn("rule_file", gate_diag)
            self.assertIn("recommended_first_action", gate_diag)

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
                + ("print('x')\n" * 421),
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
            self.assertEqual(violations.get("scripts/run_cli.py"), "cli_or_task_script>420", result.stdout + result.stderr)

    def test_nested_assets_and_tests_are_skipped_but_real_files_still_lint(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ctest_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp) / "Codex_Skills_Mirror"
            vendored = root / "Meta-code-graph-base" / "assets" / "gitnexus_core" / "test" / "unit"
            agents = root / "3-Octupos-OS-Backend" / "agents"
            nested_tests = root / "Meta-Default-md-manager" / "tests"
            vendored.mkdir(parents=True)
            agents.mkdir(parents=True)
            nested_tests.mkdir(parents=True)

            (vendored / "repo-manager.test.ts").write_text(
                'const HOME = "/home/jasontan656/tmp/repo";\n',
                encoding="utf-8",
            )
            (nested_tests / "test_case.py").write_text(
                'SECRET = "/home/jasontan656/.ssh/id_rsa"\n',
                encoding="utf-8",
            )
            (agents / "openai.yaml").write_text(
                'default_prompt: "/home/jasontan656/.cache/codex/runtime.txt"\n',
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

            summary = report["summary_enhanced"]
            self.assertGreaterEqual(summary["deduped_issue_count"], 1, result.stdout + result.stderr)
            self.assertEqual(summary["likely_rule_scope_issues"], 0, result.stdout + result.stderr)
            self.assertEqual(summary["likely_duplicated_vendor_issues"], 0, result.stdout + result.stderr)
            self.assertGreaterEqual(summary["likely_real_code_issues"], 1, result.stdout + result.stderr)

            self.assertFalse(
                any("gitnexus_core" in v["path"] for v in report["violation_details"]),
                result.stdout + result.stderr,
            )
            self.assertFalse(
                any(v["path"] == "Meta-Default-md-manager/tests/test_case.py" for v in report["violation_details"]),
                result.stdout + result.stderr,
            )

            real_detail = next(v for v in report["violation_details"] if v["path"] == "3-Octupos-OS-Backend/agents/openai.yaml")
            self.assertEqual(real_detail["issue_kind"], "real_content_issue")

            absolute_diag = next(g for g in report["gate_diagnostics"] if g["gate"] == "absolute_path_gate")
            self.assertEqual(absolute_diag["deduped_cluster_count"], 1, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
