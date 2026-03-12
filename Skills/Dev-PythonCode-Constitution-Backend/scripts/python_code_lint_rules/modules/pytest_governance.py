from __future__ import annotations

import re
from pathlib import Path

from python_code_lint_rules.shared import is_ignored_path, load_ini_sections, load_toml, make_gate, make_violation, read_text, rel

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/pytest_governance.py"
TEST_FILE_RE = re.compile(r"(^test_.*\.py$|.*_test\.py$)")
PYTEST_MARK_RE = re.compile(r"pytest\.mark\.([A-Za-z_][A-Za-z0-9_]*)")
DEFAULT_MARKS = {"parametrize", "skip", "skipif", "xfail", "usefixtures", "filterwarnings", "asyncio", "anyio"}


def _iter_test_files(root: Path) -> list[Path]:
    files = [
        path
        for path in root.rglob("*.py")
        if path.is_file() and not is_ignored_path(path, root) and TEST_FILE_RE.match(path.name)
    ]
    deduped: dict[Path, None] = {}
    for path in files:
        deduped[path] = None
    return list(deduped.keys())


def _pytest_settings(root: Path) -> tuple[dict[str, object], str]:
    pytest_ini = root / "pytest.ini"
    if pytest_ini.exists():
        parser = load_ini_sections(pytest_ini)
        if parser is not None and parser.has_section("pytest"):
            section = {key: value for key, value in parser.items("pytest")}
            return section, rel(pytest_ini, root)

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = load_toml(pyproject) or {}
        tool = data.get("tool", {}) if isinstance(data, dict) else {}
        pytest_data = tool.get("pytest", {}) if isinstance(tool, dict) else {}
        ini_options = pytest_data.get("ini_options", {}) if isinstance(pytest_data, dict) else {}
        if isinstance(ini_options, dict):
            return ini_options, rel(pyproject, root)

    return {}, ""


def _uses_importlib_mode(settings: dict[str, object]) -> bool:
    import_mode = settings.get("import_mode")
    if isinstance(import_mode, str) and import_mode.strip() == "importlib":
        return True
    addopts = settings.get("addopts", "")
    if isinstance(addopts, list):
        addopts = " ".join(str(item) for item in addopts)
    return isinstance(addopts, str) and "--import-mode=importlib" in addopts


def _uses_strict_markers(settings: dict[str, object]) -> bool:
    for key in ("strict_markers", "strict"):
        value = settings.get(key)
        if isinstance(value, bool) and value:
            return True
        if isinstance(value, str) and value.strip().lower() == "true":
            return True
    addopts = settings.get("addopts", "")
    if isinstance(addopts, list):
        addopts = " ".join(str(item) for item in addopts)
    return isinstance(addopts, str) and "--strict-markers" in addopts


def lint(root: Path) -> dict[str, object]:
    violations = []
    test_files = [path for path in _iter_test_files(root) if TEST_FILE_RE.match(path.name)]
    settings, config_path = _pytest_settings(root)
    checked = len(test_files) + (1 if config_path else 0)
    if not test_files:
        return make_gate("pytest_governance_gate", violations, checked, rule_file=RULE_FILE)

    if config_path and not _uses_importlib_mode(settings):
        violations.append(
            make_violation(
                config_path,
                "pytest_importlib_mode_required",
                category="pytest_import_mode",
                why_flagged="pytest test suites should opt into importlib mode to avoid path-precedence and duplicate-module surprises",
                suggested_fix="set import_mode = importlib or add --import-mode=importlib in the pytest configuration",
            )
        )

    custom_marks: set[str] = set()
    for path in test_files:
        for mark in PYTEST_MARK_RE.findall(read_text(path)):
            if mark not in DEFAULT_MARKS:
                custom_marks.add(mark)

    if custom_marks and config_path and not _uses_strict_markers(settings):
        violations.append(
            make_violation(
                config_path,
                f"pytest_strict_markers_required:{','.join(sorted(custom_marks))}",
                category="pytest_strict_markers",
                why_flagged="custom pytest markers should run with strict marker validation to avoid silent typos",
                suggested_fix="enable strict_markers = true or --strict-markers in the pytest configuration",
            )
        )

    return make_gate("pytest_governance_gate", violations, checked, rule_file=RULE_FILE)
