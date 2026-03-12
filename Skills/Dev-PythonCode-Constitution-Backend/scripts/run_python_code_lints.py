#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from python_code_lint_rules.modules import (
    absolute_path,
    code_governance,
    fat_file,
    file_structure,
    hardcoded_asset,
    logging_boundary,
    modularity,
    payload_normalize,
    permission_boundary,
    subprocess_safety,
    typed_contract,
    typing_governance,
)
from python_code_lint_rules.reporting import build_report

MODULES = [
    code_governance,
    fat_file,
    file_structure,
    modularity,
    typing_governance,
    subprocess_safety,
    logging_boundary,
    typed_contract,
    payload_normalize,
    permission_boundary,
    hardcoded_asset,
    absolute_path,
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Python code governance static lint gates.")
    parser.add_argument("--target", required=True, help="Target repository root.")
    args = parser.parse_args()
    root = Path(args.target).resolve()
    if not root.exists() or not root.is_dir():
        parser.error("--target 必须是存在的目录。")
    gates = [module.lint(root) for module in MODULES]
    rule_files = {
        f"{module.__name__.rsplit('.', 1)[-1]}_gate": str(Path(module.__file__).resolve().relative_to(WORKSPACE_ROOT))
        for module in MODULES
    }
    report = build_report(root, gates, rule_files)
    failed = [gate for gate in report["gates"] if gate["status"] != "pass"]
    print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
