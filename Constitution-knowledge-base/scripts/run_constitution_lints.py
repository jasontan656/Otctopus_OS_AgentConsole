#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from constitution_lint_rules.modules import code_governance, fat_file, file_structure, folder_structure, modularity, payload_normalize, permission_boundary, typed_contract

MODULES = [
    code_governance,
    fat_file,
    file_structure,
    folder_structure,
    modularity,
    typed_contract,
    payload_normalize,
    permission_boundary,
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run constitution static lint gates.")
    parser.add_argument("--target", required=True, help="Target repository root.")
    args = parser.parse_args()
    root = Path(args.target).resolve()
    if not root.exists() or not root.is_dir():
        parser.error("--target 必须是存在的目录。")
    gates = [module.lint(root) for module in MODULES]
    failed = [gate for gate in gates if gate["status"] != "pass"]
    report = {
        "target": str(root),
        "gates": gates,
        "summary": {"total": len(gates), "failed": len(failed), "passed": len(gates) - len(failed)},
    }
    print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
