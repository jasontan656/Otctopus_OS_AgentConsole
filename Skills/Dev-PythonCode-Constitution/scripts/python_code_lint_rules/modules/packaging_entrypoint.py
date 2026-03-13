from __future__ import annotations

from pathlib import Path

from python_code_lint_rules.shared import has_package_ancestor, iter_files, load_toml, make_gate, make_violation, rel

RULE_FILE = "Dev-PythonCode-Constitution/scripts/python_code_lint_rules/modules/packaging_entrypoint.py"


def _has_cli_candidate(root: Path) -> bool:
    for path in iter_files(root, {".py"}):
        if not has_package_ancestor(path, root):
            continue
        name = path.name.lower()
        stem = path.stem.lower()
        if name == "__main__.py" or stem == "cli" or stem.endswith("_cli"):
            return True
    return False


def lint(root: Path) -> dict[str, object]:
    violations = []
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return make_gate("packaging_entrypoint_gate", violations, 0, rule_file=RULE_FILE)

    checked = 1
    data = load_toml(pyproject)
    path_text = rel(pyproject, root)
    if data is None:
        violations.append(
            make_violation(
                path_text,
                "invalid_pyproject_toml",
                category="pyproject_integrity",
                why_flagged="packaging metadata must stay machine-readable for Python tooling to consume it",
                suggested_fix="fix pyproject.toml syntax before relying on packaging or pytest tooling",
            )
        )
        return make_gate("packaging_entrypoint_gate", violations, checked, rule_file=RULE_FILE)

    build_system = data.get("build-system")
    project = data.get("project")
    if isinstance(project, dict):
        if not isinstance(build_system, dict):
            violations.append(
                make_violation(
                    path_text,
                    "pyproject_missing_build_system",
                    category="pyproject_build_system",
                    why_flagged="PyPA packaging metadata should declare an explicit build-system table",
                    suggested_fix="add [build-system] with at least requires = [...] and a chosen build backend",
                )
            )
        elif "requires" not in build_system:
            violations.append(
                make_violation(
                    path_text,
                    "pyproject_build_system_requires_missing",
                    category="pyproject_build_system",
                    why_flagged="build-system requires tells Python tooling which backend dependencies are needed to build the project",
                    suggested_fix="add requires = [...] under [build-system]",
                )
            )

        requires_python = project.get("requires-python")
        if not isinstance(requires_python, str) or not requires_python.strip():
            violations.append(
                make_violation(
                    path_text,
                    "pyproject_requires_python_missing",
                    category="pyproject_requires_python",
                    why_flagged="project metadata should declare the supported Python version range explicitly",
                    suggested_fix="set requires-python = \">=3.x\" under [project]",
                )
            )

        scripts = project.get("scripts")
        gui_scripts = project.get("gui-scripts")
        if _has_cli_candidate(root) and not isinstance(scripts, dict) and not isinstance(gui_scripts, dict):
            violations.append(
                make_violation(
                    path_text,
                    "pyproject_project_scripts_missing",
                    category="pyproject_entrypoint",
                    why_flagged="package-style Python CLI entrypoints should be declared in project.scripts or project.gui-scripts",
                    suggested_fix="add [project.scripts] (or [project.gui-scripts]) and point each CLI name to module:function",
                )
            )

    return make_gate("packaging_entrypoint_gate", violations, checked, rule_file=RULE_FILE)
