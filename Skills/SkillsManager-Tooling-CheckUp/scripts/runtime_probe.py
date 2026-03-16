from __future__ import annotations

from pathlib import Path

from audit_models import SurfaceProbe


def detect_surface(target_root: Path) -> SurfaceProbe:
    scripts_root = target_root / "scripts"
    references_root = target_root / "references"
    cli_path = scripts_root / "Cli_Toolbox.py"
    runtime_contract_json = references_root / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT.json"
    tooling_docs_root = references_root / "tooling"
    tests_root = target_root / "tests"
    return {
        "scripts_present": scripts_root.is_dir(),
        "cli_path": str(cli_path) if cli_path.is_file() else None,
        "runtime_contract_json": str(runtime_contract_json) if runtime_contract_json.is_file() else None,
        "tooling_docs_present": tooling_docs_root.is_dir() and any(tooling_docs_root.rglob("*.md")),
        "tests_present": tests_root.is_dir() and any(tests_root.rglob("test_*.py")),
    }
