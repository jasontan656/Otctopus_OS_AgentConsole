#!/usr/bin/env python3
"""Three-mode governance workflow entrypoint for Meta-skills-tooling-governance.

Mode1: audit target skill and report gaps + remediation surface.
Mode2: create governance plans based on mode1 output.
Mode3: execute writeback modifications and update plan execution status.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def scripts_root() -> Path:
    return Path(__file__).resolve().parent


def run_json_cmd(cmd: list[str], *, cwd: Path) -> tuple[int, dict[str, Any], str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    out = (proc.stdout or "").strip()
    payload: dict[str, Any]
    try:
        payload = json.loads(out) if out else {}
        if not isinstance(payload, dict):
            payload = {"raw_stdout": out}
    except Exception:
        payload = {"raw_stdout": out}
    return proc.returncode, payload, (proc.stderr or "")[-2000:]


def normalize_plan_dirs(plan_dirs: list[str], plan_set_dir: str) -> list[Path]:
    rows: list[Path] = []
    for raw in plan_dirs:
        p = Path(raw).expanduser().resolve()
        if p.is_dir():
            rows.append(p)

    if plan_set_dir.strip():
        root = Path(plan_set_dir).expanduser().resolve()
        if root.is_dir():
            for child in sorted(root.iterdir()):
                if child.is_dir() and re.match(r"^P\d{2}_", child.name):
                    rows.append(child.resolve())

    uniq: list[Path] = []
    seen: set[str] = set()
    for row in rows:
        key = str(row)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(row)
    return uniq


def resolve_instance_root(target_skill_dir: Path, instance_name: str) -> Path:
    candidates = [
        target_skill_dir / "tooling_governance" / instance_name,
        target_skill_dir / "governance_instance" / instance_name,
        target_skill_dir / "governance_instance" / "self",
    ]
    for p in candidates:
        if p.is_dir() and (p / "docs").is_dir() and (p / "runtime").is_dir():
            return p.resolve()
    return candidates[0].resolve()


def mode1_audit(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    target_skill_dir = Path(args.target_skill_dir).expanduser().resolve()
    if not target_skill_dir.is_dir():
        return 1, {
            "status": "FAIL",
            "mode": "mode1_audit",
            "error": "TARGET_SKILL_DIR_NOT_FOUND",
            "target_skill_dir": str(target_skill_dir),
        }

    cmd = [
        "python3",
        str(scripts_root() / "mstg_target_skill_audit.py"),
        "--target-skill-dir",
        str(target_skill_dir),
        "--format",
        args.report_format,
    ]
    if args.instance_name.strip():
        cmd.extend(["--instance-name", args.instance_name.strip()])
    if args.skip_gates:
        cmd.append("--skip-gates")
    if args.pretty:
        cmd.append("--pretty")

    code, payload, stderr = run_json_cmd(cmd, cwd=target_skill_dir)
    out = {
        "status": "PASS" if code == 0 else "FAIL",
        "mode": "mode1_audit",
        "target_skill_dir": str(target_skill_dir),
        "command": cmd,
        "result": payload,
        "stderr_tail": stderr,
        "next_mode": "mode2_plan",
        "next_gate": "进入 mode2 前需要用户显式给出 continue",
    }
    return code, out


def mode2_plan(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    target_skill_dir = Path(args.target_skill_dir).expanduser().resolve()
    if not target_skill_dir.is_dir():
        return 1, {
            "status": "FAIL",
            "mode": "mode2_plan",
            "error": "TARGET_SKILL_DIR_NOT_FOUND",
            "target_skill_dir": str(target_skill_dir),
        }

    if not args.confirm_continue:
        return 2, {
            "status": "BLOCKED",
            "mode": "mode2_plan",
            "error": "USER_CONTINUE_REQUIRED",
            "message": "mode2 需要显式 continue 门禁；请携带 --confirm-continue 重新执行",
        }

    audit_report = Path(args.audit_report).expanduser().resolve() if args.audit_report.strip() else None
    if audit_report is not None and not audit_report.exists():
        return 1, {
            "status": "FAIL",
            "mode": "mode2_plan",
            "error": "AUDIT_REPORT_NOT_FOUND",
            "audit_report": str(audit_report),
        }

    cmd = [
        "python3",
        str(scripts_root() / "mstg_governance_plan_manager.py"),
        "create",
        "--target-skill-dir",
        str(target_skill_dir),
        "--title-words",
        *args.title_words,
        "--status",
        args.status,
        "--plan-shape",
        args.plan_shape,
        "--analysis-profile",
        args.analysis_profile,
        "--max-tasks",
        str(args.max_tasks),
        "--max-touch-files",
        str(args.max_touch_files),
        "--max-dependency-edges",
        str(args.max_dependency_edges),
        "--confirm-continue",
    ]
    if args.total_tasks is not None:
        cmd.extend(["--total-tasks", str(args.total_tasks)])
    if args.total_touch_files is not None:
        cmd.extend(["--total-touch-files", str(args.total_touch_files)])
    if args.dependency_edges is not None:
        cmd.extend(["--dependency-edges", str(args.dependency_edges)])
    if args.plan_count is not None:
        cmd.extend(["--plan-count", str(args.plan_count)])
    if audit_report is not None:
        cmd.extend(["--audit-report", str(audit_report)])

    code, payload, stderr = run_json_cmd(cmd, cwd=target_skill_dir)
    out = {
        "status": "PASS" if code == 0 else "FAIL",
        "mode": "mode2_plan",
        "target_skill_dir": str(target_skill_dir),
        "audit_report": str(audit_report) if audit_report is not None else "",
        "command": cmd,
        "result": payload,
        "stderr_tail": stderr,
        "next_mode": "mode3_execute",
    }
    return code, out


def mode3_execute(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    target_skill_dir = Path(args.target_skill_dir).expanduser().resolve()
    if not target_skill_dir.is_dir():
        return 1, {
            "status": "FAIL",
            "mode": "mode3_execute",
            "error": "TARGET_SKILL_DIR_NOT_FOUND",
            "target_skill_dir": str(target_skill_dir),
        }

    plan_dirs = normalize_plan_dirs(args.plan_dir, args.plan_set_dir)
    if not plan_dirs:
        return 2, {
            "status": "BLOCKED",
            "mode": "mode3_execute",
            "error": "PLAN_DIR_REQUIRED",
            "message": "mode3 需要 --plan-set-dir 或至少一个来自 mode2 输出的 --plan-dir",
        }

    plan_updates: list[dict[str, Any]] = []
    for plan_dir in plan_dirs:
        step_cmd = [
            "python3",
            str(scripts_root() / "mstg_governance_plan_manager.py"),
            "record-step",
            "--plan-dir",
            str(plan_dir),
            "--step-id",
            "M3_EXECUTE_START",
            "--status",
            "in_progress",
            "--summary",
            "mode3 execution started",
            "--task-id",
            "T1",
        ]
        code, payload, stderr = run_json_cmd(step_cmd, cwd=target_skill_dir)
        plan_updates.append(
            {
                "plan_dir": str(plan_dir),
                "phase": "start",
                "exit_code": code,
                "result": payload,
                "stderr_tail": stderr,
            }
        )

    init_cmd = [
        "python3",
        str(scripts_root() / "init_tooling_governance_instance.py"),
        "--target-skill-dir",
        str(target_skill_dir),
        "--instance-name",
        args.instance_name,
    ]
    if args.force:
        init_cmd.append("--force")
    if args.skip_backfill:
        init_cmd.append("--skip-backfill")
    if args.no_auto_whitelist:
        init_cmd.append("--no-auto-whitelist")

    init_code, init_payload, init_stderr = run_json_cmd(init_cmd, cwd=target_skill_dir)
    instance_root = resolve_instance_root(target_skill_dir, args.instance_name)

    full_gate_cmd = [
        "python3",
        str(scripts_root() / "mstg_l0_l13_full_gate_lint.py"),
        "--instance-root",
        str(instance_root),
    ]
    gate_code, gate_payload, gate_stderr = run_json_cmd(full_gate_cmd, cwd=target_skill_dir)

    outcome_cmd = [
        "python3",
        str(scripts_root() / "mstg_target_governance_outcome_lint.py"),
        "--instance-root",
        str(instance_root),
    ]
    outcome_code, outcome_payload, outcome_stderr = run_json_cmd(outcome_cmd, cwd=target_skill_dir)

    final_ok = init_code == 0 and gate_code == 0 and outcome_code == 0
    finish_result = "PASS" if final_ok else "FAIL"
    finish_summary = args.execution_summary.strip() or f"mode3 execution {finish_result.lower()}"

    for plan_dir in plan_dirs:
        step_cmd = [
            "python3",
            str(scripts_root() / "mstg_governance_plan_manager.py"),
            "record-step",
            "--plan-dir",
            str(plan_dir),
            "--step-id",
            "M3_EXECUTE_FINISH",
            "--status",
            "done" if final_ok else "failed",
            "--summary",
            finish_summary,
            "--task-id",
            "T1",
        ]
        code, payload, stderr = run_json_cmd(step_cmd, cwd=target_skill_dir)
        plan_updates.append(
            {
                "plan_dir": str(plan_dir),
                "phase": "finish_step",
                "exit_code": code,
                "result": payload,
                "stderr_tail": stderr,
            }
        )

        finish_cmd = [
            "python3",
            str(scripts_root() / "mstg_governance_plan_manager.py"),
            "finish-plan",
            "--plan-dir",
            str(plan_dir),
            "--result",
            finish_result,
            "--summary",
            finish_summary,
        ]
        code, payload, stderr = run_json_cmd(finish_cmd, cwd=target_skill_dir)
        plan_updates.append(
            {
                "plan_dir": str(plan_dir),
                "phase": "finish_plan",
                "exit_code": code,
                "result": payload,
                "stderr_tail": stderr,
            }
        )

    out = {
        "status": "PASS" if final_ok else "FAIL",
        "mode": "mode3_execute",
        "target_skill_dir": str(target_skill_dir),
        "instance_root": str(instance_root),
        "plan_dir_count": len(plan_dirs),
        "plan_dirs": [str(p) for p in plan_dirs],
        "execution": {
            "init": {
                "command": init_cmd,
                "exit_code": init_code,
                "result": init_payload,
                "stderr_tail": init_stderr,
            },
            "full_gate": {
                "command": full_gate_cmd,
                "exit_code": gate_code,
                "result": gate_payload,
                "stderr_tail": gate_stderr,
            },
            "target_outcome_lint": {
                "command": outcome_cmd,
                "exit_code": outcome_code,
                "result": outcome_payload,
                "stderr_tail": outcome_stderr,
            },
        },
        "plan_updates": plan_updates,
    }
    return 0 if final_ok else 1, out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MSTG three-mode governance workflow")
    sub = parser.add_subparsers(dest="mode", required=True)

    p1 = sub.add_parser("mode1_audit", help="Mode1: audit target and report gaps")
    p1.add_argument("--target-skill-dir", required=True)
    p1.add_argument("--instance-name", default="")
    p1.add_argument("--report-format", default="json", choices=["json", "markdown"])
    p1.add_argument("--skip-gates", action="store_true")
    p1.add_argument("--pretty", action="store_true")

    p2 = sub.add_parser("mode2_plan", help="Mode2: create plans from mode1 outputs")
    p2.add_argument("--target-skill-dir", required=True)
    p2.add_argument("--title-words", nargs="+", required=True)
    p2.add_argument("--audit-report", required=True)
    p2.add_argument("--confirm-continue", action="store_true")
    p2.add_argument("--status", default="READY", choices=["READY", "NOTES", "ready", "notes"])
    p2.add_argument("--plan-shape", default="auto", choices=["auto", "composite", "single"])
    p2.add_argument("--analysis-profile", default="normal", choices=["simple", "normal", "complex"])
    p2.add_argument("--total-tasks", type=int)
    p2.add_argument("--total-touch-files", type=int)
    p2.add_argument("--dependency-edges", type=int)
    p2.add_argument("--max-tasks", type=int, default=6)
    p2.add_argument("--max-touch-files", type=int, default=10)
    p2.add_argument("--max-dependency-edges", type=int, default=12)
    p2.add_argument("--plan-count", type=int)
    p2.add_argument("--pretty", action="store_true")

    p3 = sub.add_parser("mode3_execute", help="Mode3: execute writeback modifications")
    p3.add_argument("--target-skill-dir", required=True)
    p3.add_argument("--instance-name", default="default")
    p3.add_argument("--plan-set-dir", default="")
    p3.add_argument("--plan-dir", action="append", default=[])
    p3.add_argument("--execution-summary", default="")
    p3.add_argument("--force", action="store_true")
    p3.add_argument("--skip-backfill", action="store_true")
    p3.add_argument("--no-auto-whitelist", action="store_true")
    p3.add_argument("--pretty", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "mode1_audit":
        code, payload = mode1_audit(args)
    elif args.mode == "mode2_plan":
        code, payload = mode2_plan(args)
    else:
        code, payload = mode3_execute(args)

    if getattr(args, "pretty", False):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
