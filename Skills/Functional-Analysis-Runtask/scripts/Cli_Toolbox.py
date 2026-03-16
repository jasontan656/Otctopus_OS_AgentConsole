#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtask_workflow_runtime import (
    STAGES,
    compile_reading_chain,
    runtime_contract_payload,
    scaffold_workspace,
    stage_checklist_payload,
    stage_lint_payload,
    task_gate_check_payload,
    task_runtime_scaffold,
)


def emit(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0 if payload.get("status", "ok") not in {"fail", "error"} else 1


def cmd_runtime_contract(args: argparse.Namespace) -> int:
    return emit(runtime_contract_payload(), args.json)


def cmd_read_context(args: argparse.Namespace) -> int:
    selection = [item.strip() for item in args.selection.split(",") if item.strip()]
    return emit(compile_reading_chain(args.entry, selection), args.json)


def cmd_stage_checklist(args: argparse.Namespace) -> int:
    return emit(stage_checklist_payload(args.stage), args.json)


def cmd_workspace_scaffold(args: argparse.Namespace) -> int:
    return emit(scaffold_workspace(Path(args.workspace_root), force=args.force), args.json)


def cmd_stage_lint(args: argparse.Namespace) -> int:
    return emit(stage_lint_payload(Path(args.workspace_root), args.stage), args.json)


def cmd_task_gate_check(args: argparse.Namespace) -> int:
    return emit(task_gate_check_payload(), args.json)


def cmd_task_runtime_scaffold(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace_root) if args.workspace_root else None
    return emit(task_runtime_scaffold(args.task_name, workspace_root=workspace_root, force=args.force), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI toolbox for Functional-Analysis-Runtask.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    runtime_contract = subparsers.add_parser("runtime-contract")
    runtime_contract.add_argument("--json", action="store_true")
    runtime_contract.set_defaults(func=cmd_runtime_contract)

    for name in ("read-contract-context", "read-path-context"):
        read_context = subparsers.add_parser(name)
        read_context.add_argument("--entry", required=True)
        read_context.add_argument("--selection", default="")
        read_context.add_argument("--json", action="store_true")
        read_context.set_defaults(func=cmd_read_context)

    stage_checklist = subparsers.add_parser("stage-checklist")
    stage_checklist.add_argument("--stage", choices=sorted(STAGES), required=True)
    stage_checklist.add_argument("--json", action="store_true")
    stage_checklist.set_defaults(func=cmd_stage_checklist)

    workspace_scaffold = subparsers.add_parser("workspace-scaffold")
    workspace_scaffold.add_argument("--workspace-root", required=True)
    workspace_scaffold.add_argument("--force", action="store_true")
    workspace_scaffold.add_argument("--json", action="store_true")
    workspace_scaffold.set_defaults(func=cmd_workspace_scaffold)

    task_gate = subparsers.add_parser("task-gate-check")
    task_gate.add_argument("--json", action="store_true")
    task_gate.set_defaults(func=cmd_task_gate_check)

    task_runtime = subparsers.add_parser("task-runtime-scaffold")
    task_runtime.add_argument("--task-name", required=True)
    task_runtime.add_argument("--workspace-root")
    task_runtime.add_argument("--force", action="store_true")
    task_runtime.add_argument("--json", action="store_true")
    task_runtime.set_defaults(func=cmd_task_runtime_scaffold)

    stage_lint = subparsers.add_parser("stage-lint")
    stage_lint.add_argument("--workspace-root", required=True)
    stage_lint.add_argument("--stage", choices=sorted(set(STAGES) | {"all"}), required=True)
    stage_lint.add_argument("--json", action="store_true")
    stage_lint.set_defaults(func=cmd_stage_lint)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
