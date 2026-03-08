#!/usr/bin/env python3
"""Run full L0-L13 governance gate for one instance.
Adapted from Octupos-OS l0_l13_full_gate_lint.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_SEQUENCE = [
    "mstg_l0_l13_linear_lint.py",
    "mstg_l0_l13_layer_schema_lint.py",
    "tooling_governance_lint.py",
    "mstg_target_governance_outcome_lint.py",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run all L0-L13 gate lints for governance instance")
    p.add_argument("--instance-root", required=True)
    p.add_argument("--pretty", action="store_true")
    return p.parse_args()


def try_parse_json(text: str) -> dict[str, Any]:
    s = (text or "").strip()
    if not s:
        return {}
    try:
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else {"raw_stdout": s}
    except Exception:
        return {"raw_stdout": s}


def run_script(scripts_dir: Path, script_name: str, instance_root: Path) -> dict[str, Any]:
    script_path = scripts_dir / script_name
    cmd = [sys.executable, str(script_path), "--instance-root", str(instance_root)]
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    payload = try_parse_json(proc.stdout)
    status = str(payload.get("status", "")).upper()
    passed = proc.returncode == 0 and status == "PASS"
    return {
        "script": script_name,
        "cmd": cmd,
        "exit_code": proc.returncode,
        "pass": passed,
        "status": payload.get("status", "UNKNOWN"),
        "scope": payload.get("scope", ""),
        "checks": payload.get("checks", {}),
        "error_count": len(payload.get("errors", [])) if isinstance(payload.get("errors"), list) else None,
        "stderr_tail": (proc.stderr or "")[-800:],
        "payload": payload,
    }


def lint(instance_root: Path) -> dict[str, Any]:
    scripts_dir = Path(__file__).resolve().parent
    rows: list[dict[str, Any]] = []
    failing_scripts: list[str] = []

    for script_name in SCRIPT_SEQUENCE:
        row = run_script(scripts_dir, script_name, instance_root)
        rows.append(row)
        if not row["pass"]:
            failing_scripts.append(script_name)

    status = "PASS" if not failing_scripts else "FAIL"
    return {
        "status": status,
        "scope": "mstg_l0_l13_full_gate",
        "checks": {
            "total_scripts": len(SCRIPT_SEQUENCE),
            "passed_scripts": len(SCRIPT_SEQUENCE) - len(failing_scripts),
            "failed_scripts": len(failing_scripts),
        },
        "failing_scripts": failing_scripts,
        "results": rows,
    }


def main() -> int:
    args = parse_args()
    payload = lint(Path(args.instance_root).expanduser().resolve())
    if args.pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0 if payload["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
