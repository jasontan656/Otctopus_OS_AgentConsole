from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestPythonCodeLintTests:
    def _run_lint(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(ROOT / "scripts/run_python_code_lints.py"), "--target", str(target)],
            text=True,
            capture_output=True,
            check=False,
        )

    def _assert_enhanced_report_shape(self, report: dict[str, object]) -> None:
        assert "summary_enhanced" in report
        assert "gate_diagnostics" in report
        assert "violation_details" in report
        assert "clusters" in report

    def test_static_lints_detect_and_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            bad = root / "bad"
            bad.mkdir()
            (bad / "user_domain.py").write_text(
                "import requests\nrequests.get('https://example.com')\n",
                encoding="utf-8",
            )
            bad_result = self._run_lint(bad)
            assert bad_result.returncode == 1, bad_result.stdout + bad_result.stderr
            bad_report = json.loads(bad_result.stdout)
            self._assert_enhanced_report_shape(bad_report)
            assert any(g["gate"] == "modularity_gate" and g["status"] == "fail" for g in bad_report["gates"])

            good = root / "good"
            good.mkdir()
            (good / "user_orchestrator.py").write_text("def run() -> None:\n    pass\n", encoding="utf-8")
            good_result = self._run_lint(good)
            assert good_result.returncode == 0, good_result.stdout + good_result.stderr

    def test_hardcoded_asset_gate_detects_inline_prompt_and_allows_external_asset(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            bad = root / "bad_prompt.py"
            bad.write_text(
                'PROMPT = """\n'
                "You are an audit assistant.\n"
                "## 1. Goal\n"
                "- 必须读取规则\n"
                "- 禁止跳过验证\n"
                "- 输出契约固定\n"
                "- workflow 需要完整\n"
                "- name: inline\n"
                "- description: inline\n"
                "- 必须遵守 assets/rules\n"
                '"""\n',
                encoding="utf-8",
            )
            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "hardcoded_asset_gate")
            assert any(v["path"] == "bad_prompt.py" for v in gate["violations"])

            assets = root / "assets"
            assets.mkdir(exist_ok=True)
            (assets / "prompt.txt").write_text("You are an audit assistant.\n", encoding="utf-8")
            (root / "loader.py").write_text(
                "from pathlib import Path\n"
                "PROMPT = (Path(__file__).parent / 'assets' / 'prompt.txt').read_text(encoding='utf-8')\n",
                encoding="utf-8",
            )
            result = self._run_lint(root)
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "hardcoded_asset_gate")
            assert not (any(v["path"] == "loader.py" for v in gate["violations"]))

    def test_absolute_path_gate_respects_repo_boundaries(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            octopus_root = Path(tmp) / "Octopus_OS"
            octopus_root.mkdir()
            (octopus_root / "deploy.py").write_text(
                'CONFIG = "/home/jasontan656/AI_Projects/Octopus_OS/config/settings.yaml"\n'
                'ESCAPE = "../../shared/runtime.json"\n',
                encoding="utf-8",
            )
            result = self._run_lint(octopus_root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            reasons = {v["reason"] for v in next(g for g in report["gates"] if g["gate"] == "absolute_path_gate")["violations"]}
            assert "octopus_os_forbids_unix_absolute_paths" in reasons
            assert "octopus_os_forbids_repo_escape_relative_paths" in reasons

    def test_fat_file_distinguishes_contract_support_from_real_cli(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            scripts = root / "scripts"
            scripts.mkdir(parents=True)

            (scripts / "workflow_stage_contract.py").write_text("VALUE = 1\n" * 230, encoding="utf-8")
            (scripts / "run_cli.py").write_text(
                "import argparse\n"
                "parser = argparse.ArgumentParser()\n"
                "parser.add_argument('--x')\n"
                + ("print('x')\n" * 421),
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            fat_gate = next(g for g in report["gates"] if g["gate"] == "fat_file_gate")
            violations = {v["path"]: v["reason"] for v in fat_gate["violations"]}
            assert "scripts/workflow_stage_contract.py" not in violations
            assert violations.get("scripts/run_cli.py") == "cli_or_task_script>420"

    def test_lint_ignores_virtualenv_and_temp_like_directories(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)

            venv_pkg = root / ".venv_backend_skills" / "lib" / "python3.12" / "site-packages"
            venv_pkg.mkdir(parents=True)
            (venv_pkg / "bad_domain.py").write_text(
                "import requests\nrequests.get('https://example.com')\n",
                encoding="utf-8",
            )

            temp_runtime = root / ".tmp_runtime"
            temp_runtime.mkdir()
            (temp_runtime / "bad_prompt.py").write_text(
                'PROMPT = """\n'
                "You are an audit assistant.\n"
                "## 1. Goal\n"
                "- 必须读取规则\n"
                "- 禁止跳过验证\n"
                "- 输出契约固定\n"
                "- workflow 需要完整\n"
                "- name: inline\n"
                "- description: inline\n"
                "- 必须遵守 assets/rules\n"
                '"""\n',
                encoding="utf-8",
            )

            build_dir = root / "build" / "generated"
            build_dir.mkdir(parents=True)
            (build_dir / "bad_controller.py").write_text(
                "from some_repo import UserRepository\n"
                "def run() -> None:\n"
                "    Repository('x')\n",
                encoding="utf-8",
            )

            src = root / "src"
            src.mkdir()
            (src / "user_orchestrator.py").write_text("def run() -> None:\n    pass\n", encoding="utf-8")

            result = self._run_lint(root)
            assert result.returncode == 0, result.stdout + result.stderr
            report = json.loads(result.stdout)
            assert all(g["status"] == "pass" for g in report["gates"])

    def test_non_python_contract_and_rules_assets_stay_out_of_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "main.py").write_text("def run() -> None:\n    pass\n", encoding="utf-8")

            docs = root / "docs"
            docs.mkdir()
            (docs / "workflow_rules.md").write_text("# Workflow Rules\n- keep this generic\n", encoding="utf-8")

            contracts = root / "contracts"
            contracts.mkdir()
            (contracts / "app_contract.yaml").write_text("name: generic-contract\n", encoding="utf-8")

            result = self._run_lint(root)
            assert result.returncode == 0, result.stdout + result.stderr
            report = json.loads(result.stdout)

            typed_gate = next(g for g in report["gates"] if g["gate"] == "typed_contract_gate")
            file_gate = next(g for g in report["gates"] if g["gate"] == "file_structure_gate")

            assert not typed_gate["violations"]
            assert not file_gate["violations"]
            assert all(g["gate"] != "folder_structure_gate" for g in report["gates"])

    def test_python_related_contract_and_rule_assets_remain_governed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            contracts = root / "assets" / "contracts"
            contracts.mkdir(parents=True)
            docs = root / "docs"
            docs.mkdir()

            (root / "loader.py").write_text(
                "from pathlib import Path\n"
                "CONFIG = (Path(__file__).parent / 'assets' / 'contracts' / 'runtime_contract.yaml').read_text(encoding='utf-8')\n"
                "RULES = (Path(__file__).parent / 'docs' / 'python_rule.md').read_text(encoding='utf-8')\n",
                encoding="utf-8",
            )
            (contracts / "runtime_contract.yaml").write_text("name: runtime-contract\n", encoding="utf-8")
            (docs / "python_rule.md").write_text("# Python Rule\n- keep runtime aligned\n", encoding="utf-8")

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)

            typed_gate = next(g for g in report["gates"] if g["gate"] == "typed_contract_gate")
            file_gate = next(g for g in report["gates"] if g["gate"] == "file_structure_gate")

            typed_paths = {v["path"] for v in typed_gate["violations"]}
            file_paths = {v["path"] for v in file_gate["violations"]}

            assert "assets/contracts/runtime_contract.yaml" in typed_paths
            assert "docs/python_rule.md" in file_paths

    def test_typing_governance_requires_public_annotations(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_service.py").write_text(
                "def process(payload):\n"
                "    return payload\n",
                encoding="utf-8",
            )
            (root / "good_service.py").write_text(
                "def process(payload: dict[str, str]) -> dict[str, str]:\n"
                "    return payload\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "typing_governance_gate")
            violations = {v["path"]: v["reason"] for v in gate["violations"]}
            assert violations.get("bad_service.py", "").startswith("public_function_missing_type_hints:")
            assert "good_service.py" not in violations

    def test_subprocess_safety_flags_popen_and_shell_true(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_task.py").write_text(
                "import subprocess\n"
                "def run_task() -> None:\n"
                "    subprocess.Popen(['echo', 'x'])\n"
                "    subprocess.run('echo x', shell=True)\n",
                encoding="utf-8",
            )
            (root / "good_task.py").write_text(
                "import subprocess\n"
                "def run_task() -> None:\n"
                "    subprocess.run(['echo', 'x'], check=False)\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "subprocess_safety_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_task.py", "prefer_subprocess_run_over_popen") in reasons
            assert ("bad_task.py", "subprocess_shell_true_forbidden") in reasons
            assert not any(path == "good_task.py" for path, _reason in reasons)

    def test_logging_boundary_prefers_named_loggers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_service.py").write_text(
                "import logging\n"
                "logger = logging.getLogger()\n"
                "logging.basicConfig(level=logging.INFO)\n"
                "def run() -> None:\n"
                "    logging.info('hello')\n",
                encoding="utf-8",
            )
            (root / "good_service.py").write_text(
                "import logging\n"
                "logger = logging.getLogger(__name__)\n"
                "def run() -> None:\n"
                "    logger.info('hello')\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "logging_boundary_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_service.py", "logging_getlogger_requires_explicit_name") in reasons
            assert ("bad_service.py", "logging_basicconfig_forbidden_in_library_code") in reasons
            assert ("bad_service.py", "root_logger_call_forbidden") in reasons
            assert not any(path == "good_service.py" for path, _reason in reasons)

    def test_pytest_governance_requires_importlib_mode_and_strict_markers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            tests = root / "tests"
            tests.mkdir()
            (tests / "test_api.py").write_text(
                "import pytest\n"
                "@pytest.mark.slow\n"
                "def test_api() -> None:\n"
                "    assert True\n",
                encoding="utf-8",
            )
            (root / "pytest.ini").write_text(
                "[pytest]\n"
                "addopts = -q\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "pytest_governance_gate")
            reasons = {v["reason"] for v in gate["violations"]}
            assert "pytest_importlib_mode_required" in reasons
            assert "pytest_strict_markers_required:slow" in reasons

    def test_resource_loading_prefers_importlib_resources(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            pkg = root / "src" / "demo_pkg"
            pkg.mkdir(parents=True)
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            (pkg / "reader.py").write_text(
                "from pathlib import Path\n"
                "def load_prompt() -> str:\n"
                "    return Path(__file__).with_name('prompt.txt').read_text(encoding='utf-8')\n",
                encoding="utf-8",
            )
            (pkg / "good_reader.py").write_text(
                "from importlib import resources\n"
                "def load_prompt() -> str:\n"
                "    return resources.files(__package__).joinpath('prompt.txt').read_text(encoding='utf-8')\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "resource_loading_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("src/demo_pkg/reader.py", "package_resource_should_use_importlib_resources") in reasons
            assert not any(path == "src/demo_pkg/good_reader.py" for path, _reason in reasons)

    def test_packaging_entrypoint_requires_pyproject_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            pkg = root / "src" / "demo_pkg"
            pkg.mkdir(parents=True)
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            (pkg / "__main__.py").write_text("def main() -> None:\n    pass\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                "[project]\n"
                "name = 'demo-pkg'\n"
                "version = '0.1.0'\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "packaging_entrypoint_gate")
            reasons = {v["reason"] for v in gate["violations"]}
            assert "pyproject_missing_build_system" in reasons
            assert "pyproject_requires_python_missing" in reasons
            assert "pyproject_project_scripts_missing" in reasons

    def test_exception_governance_blocks_bare_and_swallowed_broad_handlers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_handler.py").write_text(
                "def run() -> None:\n"
                "    try:\n"
                "        work()\n"
                "    except:\n"
                "        return\n"
                "\n"
                "def other() -> None:\n"
                "    try:\n"
                "        work()\n"
                "    except Exception:\n"
                "        return\n"
                "\n"
                "def base() -> None:\n"
                "    try:\n"
                "        work()\n"
                "    except BaseException:\n"
                "        raise\n",
                encoding="utf-8",
            )
            (root / "good_handler.py").write_text(
                "def run() -> None:\n"
                "    try:\n"
                "        work()\n"
                "    except ValueError:\n"
                "        raise\n"
                "\n"
                "def other() -> None:\n"
                "    try:\n"
                "        work()\n"
                "    except Exception as exc:\n"
                "        raise RuntimeError('failed') from exc\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "exception_governance_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_handler.py", "bare_except_forbidden") in reasons
            assert ("bad_handler.py", "broad_exception_without_reraise") in reasons
            assert ("bad_handler.py", "baseexception_handler_forbidden") in reasons
            assert not any(path == "good_handler.py" for path, _reason in reasons)

    def test_http_timeout_gate_requires_requests_timeout_and_preserves_httpx_defaults(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_http.py").write_text(
                "import requests\n"
                "import httpx\n"
                "\n"
                "def fetch() -> None:\n"
                "    requests.get('https://example.com')\n"
                "    requests.post('https://example.com', timeout=None)\n"
                "    session = requests.Session()\n"
                "    session.get('https://example.com')\n"
                "    httpx.get('https://example.com', timeout=None)\n"
                "    client = httpx.Client(timeout=None)\n"
                "    client.get('https://example.com')\n",
                encoding="utf-8",
            )
            (root / "good_http.py").write_text(
                "import requests\n"
                "import httpx\n"
                "\n"
                "def fetch() -> None:\n"
                "    requests.get('https://example.com', timeout=(3.05, 10))\n"
                "    client = httpx.Client()\n"
                "    client.get('https://example.com')\n"
                "    httpx.get('https://example.com')\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "http_timeout_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_http.py", "requests_timeout_required") in reasons
            assert ("bad_http.py", "requests_timeout_none_forbidden") in reasons
            assert ("bad_http.py", "httpx_timeout_none_forbidden") in reasons
            assert ("bad_http.py", "httpx_client_timeout_none_forbidden") in reasons
            assert not any(path == "good_http.py" for path, _reason in reasons)

    def test_data_boundary_prefers_explicit_payload_contracts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_payload.py").write_text(
                "def handle_event(payload: dict[str, str]) -> None:\n"
                "    pass\n"
                "\n"
                "def build_payload() -> dict[str, str]:\n"
                "    return {'kind': 'demo'}\n",
                encoding="utf-8",
            )
            (root / "good_payload.py").write_text(
                "from typing import TypedDict\n"
                "\n"
                "class EventPayload(TypedDict):\n"
                "    kind: str\n"
                "\n"
                "def handle_event(payload: EventPayload) -> None:\n"
                "    pass\n"
                "\n"
                "def build_payload() -> EventPayload:\n"
                "    return {'kind': 'demo'}\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "data_boundary_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_payload.py", "payload_like_argument_uses_mapping_contract:payload") in reasons
            assert ("bad_payload.py", "payload_like_return_uses_mapping_contract") in reasons
            assert not any(path == "good_payload.py" for path, _reason in reasons)

    def test_concurrency_boundary_requires_task_ownership_and_managed_executors(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_concurrency.py").write_text(
                "from asyncio import create_task as spawn_task\n"
                "import concurrent.futures as futures\n"
                "\n"
                "async def run() -> None:\n"
                "    spawn_task(work())\n"
                "    executor = futures.ThreadPoolExecutor(max_workers=2)\n"
                "    executor.submit(blocking_work)\n",
                encoding="utf-8",
            )
            (root / "good_concurrency.py").write_text(
                "import asyncio\n"
                "import concurrent.futures as futures\n"
                "\n"
                "async def run() -> None:\n"
                "    task = asyncio.create_task(work())\n"
                "    await task\n"
                "    with futures.ThreadPoolExecutor(max_workers=2) as executor:\n"
                "        executor.submit(blocking_work)\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "concurrency_boundary_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_concurrency.py", "asyncio_create_task_requires_explicit_task_owner") in reasons
            assert ("bad_concurrency.py", "executor_constructor_requires_context_manager") in reasons
            assert not any(path == "good_concurrency.py" for path, _reason in reasons)

    def test_import_side_effect_gate_blocks_runtime_work_at_import_time(self) -> None:
        with tempfile.TemporaryDirectory(prefix="py_lint_", dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            (root / "bad_imports.py").write_text(
                "from datetime import datetime\n"
                "import asyncio\n"
                "import httpx\n"
                "from pathlib import Path\n"
                "\n"
                "CLIENT = httpx.Client()\n"
                "CONFIG = Path('settings.json').read_text(encoding='utf-8')\n"
                "STARTED_AT = datetime.now()\n"
                "TASK = asyncio.create_task(run())\n",
                encoding="utf-8",
            )
            (root / "good_imports.py").write_text(
                "from datetime import datetime\n"
                "import httpx\n"
                "from pathlib import Path\n"
                "\n"
                "def build_runtime() -> tuple[httpx.Client, str, datetime]:\n"
                "    return httpx.Client(), Path('settings.json').read_text(encoding='utf-8'), datetime.now()\n"
                "\n"
                "if __name__ == '__main__':\n"
                "    build_runtime()\n",
                encoding="utf-8",
            )

            result = self._run_lint(root)
            assert result.returncode == 1, result.stdout + result.stderr
            report = json.loads(result.stdout)
            gate = next(g for g in report["gates"] if g["gate"] == "import_side_effect_gate")
            reasons = {(v["path"], v["reason"]) for v in gate["violations"]}
            assert ("bad_imports.py", "import_side_effect:module_import_constructs_runtime_client") in reasons
            assert ("bad_imports.py", "import_side_effect:module_import_performs_file_io") in reasons
            assert ("bad_imports.py", "import_side_effect:module_import_reads_current_time") in reasons
            assert ("bad_imports.py", "import_side_effect:module_import_starts_background_task") in reasons
            assert not any(path == "good_imports.py" for path, _reason in reasons)
