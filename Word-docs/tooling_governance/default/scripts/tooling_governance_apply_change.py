#!/usr/bin/env python3
"""Unified governance change entrypoint: docs first, script change second, ops + gates last."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path
from typing import Any

from governance_audit_log import append_step, finish_run, start_run


def run_cmd(cmd: list[str], *, cwd: Path) -> tuple[int, dict[str, Any], str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    out = (proc.stdout or "").strip()
    payload: dict[str, Any]
    try:
        payload = json.loads(out) if out else {}
        if not isinstance(payload, dict):
            payload = {"raw_stdout": out}
    except Exception:
        payload = {"raw_stdout": out}
    return proc.returncode, payload, (proc.stderr or "")[-1200:]


def run_shell(command: str, *, cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(["bash", "-lc", command], cwd=cwd, text=True, capture_output=True, check=False)
    return proc.returncode, (proc.stdout or "")[-3000:], (proc.stderr or "")[-3000:]


def audit_step_safe(run_id: str, *, step: str, status: str, message: str = "", details: dict[str, Any] | None = None) -> None:
    if not run_id:
        return
    try:
        append_step(
            run_id=run_id,
            step=step,
            status=status,
            message=message,
            details=details or {},
            source_script=Path(__file__).name,
        )
    except Exception:
        return


def audit_finish_safe(run_id: str, *, status: str, summary: str, details: dict[str, Any] | None = None) -> None:
    if not run_id:
        return
    try:
        finish_run(
            run_id=run_id,
            status=status,
            summary=summary,
            details=details or {},
            source_script=Path(__file__).name,
        )
    except Exception:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply governed change with deterministic sequence")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--tool-id", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--script-cmd", default="", help="Command executed after pre-doc update")
    parser.add_argument("--author", default="ai_maintained")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    instance_root = Path(args.instance_root).expanduser().resolve()
    scripts_dir = Path(__file__).resolve().parent
    target_skill_dir = instance_root.parents[1] if len(instance_root.parents) >= 2 else instance_root
    managed_skill = target_skill_dir.name

    run_id = ""
    try:
        run = start_run(
            source_script=Path(__file__).name,
            governance_target_skill=managed_skill,
            governance_target_path=str(target_skill_dir),
            governance_objective="Apply change with enforced sequence: docs -> script -> ops -> ledger -> full_gate(including target outcome lint)",
            batch_mode=False,
            metadata={
                "tool_id": args.tool_id,
                "summary": args.summary,
                "changed_paths": args.changed_path,
                "script_cmd": args.script_cmd,
                "dry_run": args.dry_run,
            },
        )
        run_id = str(run.get("run_id", "")).strip()
    except Exception:
        run_id = ""

    steps: list[dict[str, Any]] = []

    # Step 1: docs pre-update
    pre_summary = f"pre-change docs update: {args.summary}"
    docs_cmd = [
        "python3",
        str(scripts_dir / "tooling_docs_record.py"),
        "--instance-root",
        str(instance_root),
        "--tool-id",
        args.tool_id,
        "--record-type",
        "modification",
        "--summary",
        pre_summary,
        "--author",
        args.author,
    ]
    for p in args.changed_path:
        docs_cmd.extend(["--evidence", p])
    code, payload, stderr = run_cmd(docs_cmd, cwd=target_skill_dir)
    steps.append({"step": "docs_pre_update", "exit_code": code, "payload": payload, "stderr_tail": stderr})
    audit_step_safe(run_id, step="docs_pre_update", status="PASS" if code == 0 else "FAIL", details={"exit_code": code})
    if code != 0:
        out = {"status": "FAIL", "error": "DOCS_PRE_UPDATE_FAILED", "steps": steps, "governance_audit_run_id": run_id}
        audit_finish_safe(run_id, status="FAIL", summary="apply_change failed at docs_pre_update", details=out)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    # Step 2: impact map
    impact_cmd = [
        "python3",
        str(scripts_dir / "tooling_change_impact_mapper.py"),
        "--instance-root",
        str(instance_root),
    ]
    for p in args.changed_path:
        impact_cmd.extend(["--path", p])
    impact_cmd.append("--pretty")
    code, payload, stderr = run_cmd(impact_cmd, cwd=target_skill_dir)
    steps.append({"step": "impact_map", "exit_code": code, "payload": payload, "stderr_tail": stderr})
    audit_step_safe(run_id, step="impact_map", status="PASS" if code == 0 else "FAIL", details={"exit_code": code})
    if code != 0:
        out = {"status": "FAIL", "error": "IMPACT_MAP_FAILED", "steps": steps, "governance_audit_run_id": run_id}
        audit_finish_safe(run_id, status="FAIL", summary="apply_change failed at impact_map", details=out)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1
    impacted_docs = payload.get("impacted_docs", []) if isinstance(payload.get("impacted_docs"), list) else []

    # Step 3: script update
    if args.script_cmd.strip():
        if args.dry_run:
            steps.append({"step": "script_update", "status": "SKIP", "reason": "dry_run=true", "command": args.script_cmd})
            audit_step_safe(run_id, step="script_update", status="SKIP", message="dry_run=true")
        else:
            code, stdout_tail, stderr_tail = run_shell(args.script_cmd, cwd=target_skill_dir)
            steps.append(
                {
                    "step": "script_update",
                    "exit_code": code,
                    "command": args.script_cmd,
                    "stdout_tail": stdout_tail,
                    "stderr_tail": stderr_tail,
                }
            )
            audit_step_safe(run_id, step="script_update", status="PASS" if code == 0 else "FAIL", details={"exit_code": code})
            if code != 0:
                out = {"status": "FAIL", "error": "SCRIPT_UPDATE_FAILED", "steps": steps, "governance_audit_run_id": run_id}
                audit_finish_safe(run_id, status="FAIL", summary="apply_change failed at script_update", details=out)
                print(json.dumps(out, ensure_ascii=False, indent=2))
                return 1
    else:
        steps.append({"step": "script_update", "status": "SKIP", "reason": "script_cmd not provided"})
        audit_step_safe(run_id, step="script_update", status="SKIP", message="script_cmd not provided")

    # Step 4: ops docs post-update
    post_summary = f"post-change ops/docs update: {args.summary}"
    post_cmd = [
        "python3",
        str(scripts_dir / "tooling_docs_record.py"),
        "--instance-root",
        str(instance_root),
        "--tool-id",
        args.tool_id,
        "--record-type",
        "modification",
        "--summary",
        post_summary,
        "--author",
        args.author,
    ]
    for d in impacted_docs:
        post_cmd.extend(["--evidence", d])
    code, payload, stderr = run_cmd(post_cmd, cwd=target_skill_dir)
    steps.append({"step": "ops_post_docs_update", "exit_code": code, "payload": payload, "stderr_tail": stderr})
    audit_step_safe(run_id, step="ops_post_docs_update", status="PASS" if code == 0 else "FAIL", details={"exit_code": code})
    if code != 0:
        out = {"status": "FAIL", "error": "OPS_DOCS_UPDATE_FAILED", "steps": steps, "governance_audit_run_id": run_id}
        audit_finish_safe(run_id, status="FAIL", summary="apply_change failed at ops_post_docs_update", details=out)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    # Step 5: ledger append
    ledger_cmd = [
        "python3",
        str(scripts_dir / "tooling_change_ledger.py"),
        "--instance-root",
        str(instance_root),
        "--tool-id",
        args.tool_id,
        "--change-type",
        "governed_update",
        "--summary",
        args.summary,
    ]
    for p in args.changed_path:
        ledger_cmd.extend(["--changed-path", p])
    for d in impacted_docs:
        ledger_cmd.extend(["--docs-updated", d])
    ledger_cmd.extend(["--artifacts-updated", "runtime/TOOL_CHANGE_LEDGER.jsonl"])
    code, payload, stderr = run_cmd(ledger_cmd, cwd=target_skill_dir)
    steps.append({"step": "ledger_append", "exit_code": code, "payload": payload, "stderr_tail": stderr})
    audit_step_safe(run_id, step="ledger_append", status="PASS" if code == 0 else "FAIL", details={"exit_code": code})
    if code != 0:
        out = {"status": "FAIL", "error": "LEDGER_APPEND_FAILED", "steps": steps, "governance_audit_run_id": run_id}
        audit_finish_safe(run_id, status="FAIL", summary="apply_change failed at ledger_append", details=out)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    # Step 6: full gate
    gate_cmd = [
        "python3",
        str(scripts_dir / "mstg_l0_l13_full_gate_lint.py"),
        "--instance-root",
        str(instance_root),
    ]
    code, payload, stderr = run_cmd(gate_cmd, cwd=target_skill_dir)
    steps.append({"step": "full_gate", "exit_code": code, "payload": payload, "stderr_tail": stderr})
    audit_step_safe(run_id, step="full_gate", status="PASS" if code == 0 else "FAIL", details={"exit_code": code})
    if code != 0:
        out = {"status": "FAIL", "error": "FULL_GATE_FAILED", "steps": steps, "governance_audit_run_id": run_id}
        audit_finish_safe(run_id, status="FAIL", summary="apply_change failed at full_gate", details=out)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    out = {
        "status": "PASS",
        "instance_root": str(instance_root),
        "target_skill_dir": str(target_skill_dir),
        "tool_id": args.tool_id,
        "summary": args.summary,
        "changed_paths": args.changed_path,
        "script_cmd": args.script_cmd,
        "steps": steps,
        "governance_audit_run_id": run_id,
    }
    audit_finish_safe(run_id, status="PASS", summary="apply_change completed", details={"tool_id": args.tool_id})
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
