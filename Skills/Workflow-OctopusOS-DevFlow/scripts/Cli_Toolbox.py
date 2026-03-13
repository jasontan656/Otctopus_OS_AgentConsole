#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cli_support import ACCEPTANCE_MATRIX_PATH, ACCEPTANCE_REPORT_PATH, CODEBASE_ROOT, CONSTRUCTION_PLAN_ROOT, MOTHER_DOC_PATH, MOTHER_DOC_ROOT, RUNTIME_ROOT
from cli_support import STAGES, TEMPLATES
from cli_support import acceptance_lint_payload, graph_postflight_payload, graph_preflight_payload
from cli_support import construction_plan_init_payload, construction_plan_lint_payload, mother_doc_archive_payload
from cli_support import mother_doc_init_payload, mother_doc_lint_payload, mother_doc_state_sync_payload, target_scaffold_payload, workflow_contract_payload
from stage_contract_support import stage_command_contract_payload, stage_doc_contract_payload, stage_graph_contract_payload
from target_runtime_support import resolve_target_runtime, target_runtime_contract_payload
def print_payload(payload: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0
def cmd_workflow_contract(args: argparse.Namespace) -> int:
    return print_payload(
        workflow_contract_payload(
            target_root=args.target_root,
            docs_root=args.docs_root,
            module_dir=args.module_dir,
            codebase_root=args.codebase_root,
            graph_runtime_root=args.graph_runtime_root,
            project_agents=args.project_agents,
        ),
        args.json,
    )


def cmd_target_runtime_contract(args: argparse.Namespace) -> int:
    payload = target_runtime_contract_payload(
        target_root=args.target_root,
        docs_root=args.docs_root,
        module_dir=args.module_dir,
        codebase_root=args.codebase_root,
        graph_runtime_root=args.graph_runtime_root,
        project_agents=args.project_agents,
    )
    print_payload(payload, args.json)
    return 0 if payload["status"] == "pass" else 1


def _resolve_runtime(args: argparse.Namespace) -> dict[str, object]:
    return resolve_target_runtime(
        target_root=args.target_root,
        docs_root=args.docs_root,
        module_dir=args.module_dir,
        codebase_root=args.codebase_root,
        graph_runtime_root=args.graph_runtime_root,
        project_agents=args.project_agents,
    )


def _emit_runtime_not_ready(runtime: dict[str, object], as_json: bool) -> int:
    payload = {
        "status": "fail",
        "reason": "target_runtime_not_ready",
        "missing_prerequisites": runtime["missing_prerequisites"],
        "target_root": str(runtime["target_root"]),
        "development_docs_root": str(runtime["development_docs_root"]),
        "module_dir": runtime["module_dir"],
        "docs_root": str(runtime["docs_root"]),
    }
    print_payload(payload, as_json)
    return 1


def cmd_stage_checklist(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"]:
        return _emit_runtime_not_ready(runtime, args.json)
    payload = {
        "stage": args.stage,
        **STAGES[args.stage],
        "target_runtime_precheck_required": True,
        "target_runtime_contract": target_runtime_contract_payload(
            target_root=args.target_root,
            docs_root=args.docs_root,
            module_dir=args.module_dir,
            codebase_root=args.codebase_root,
            graph_runtime_root=args.graph_runtime_root,
            project_agents=args.project_agents,
        ),
        "resolved_paths": {
            "target_root": str(runtime["target_root"]),
            "docs_root": str(runtime["docs_root"]),
            "mother_doc_root": str(runtime["mother_doc_root"]),
            "construction_plan_root": str(runtime["construction_plan_root"]),
            "codebase_root": str(runtime["codebase_root"]),
            "graph_runtime_root": str(runtime["graph_runtime_root"]),
        },
    }
    return print_payload(payload, args.json)
def _cmd_stage_contract(args: argparse.Namespace, kind: str) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"]:
        return _emit_runtime_not_ready(runtime, args.json)
    factories = {
        "doc": lambda: stage_doc_contract_payload(
            args.stage,
            Path(runtime["mother_doc_root"]),
            runtime,
        ),
        "command": lambda: stage_command_contract_payload(
            args.stage,
            Path(runtime["mother_doc_root"]),
            Path(runtime["construction_plan_root"]),
            Path(runtime["codebase_root"]),
            runtime,
        ),
        "graph": lambda: stage_graph_contract_payload(
            args.stage,
            Path(runtime["codebase_root"]),
            Path(runtime["graph_runtime_root"]),
        ),
    }
    return print_payload(factories[kind](), args.json)
def cmd_graph_preflight(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.repo is None:
        return _emit_runtime_not_ready(runtime, args.json)
    repo = args.repo or str(runtime["codebase_root"])
    graph_runtime_root = Path(args.graph_runtime_root or runtime["graph_runtime_root"]).resolve()
    payload = graph_preflight_payload(Path(repo).resolve(), args.allow_missing_index, graph_runtime_root)
    return print_payload(payload, args.json)
def cmd_graph_postflight(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.repo is None:
        return _emit_runtime_not_ready(runtime, args.json)
    repo = args.repo or str(runtime["codebase_root"])
    graph_runtime_root = Path(args.graph_runtime_root or runtime["graph_runtime_root"]).resolve()
    payload = graph_postflight_payload(Path(repo).resolve(), graph_runtime_root)
    return print_payload(payload, args.json)
def cmd_target_scaffold(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    payload, status_code = target_scaffold_payload(runtime, args.force)
    print_payload(payload, args.json)
    return status_code


def cmd_template_index(args: argparse.Namespace) -> int:
    payload = {name: str(path) for name, path in TEMPLATES.items()}
    return print_payload(payload, args.json)
def cmd_mother_doc_init(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.target is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.target or runtime["mother_doc_root"]).resolve()
    payload, status_code = mother_doc_init_payload(target, args.force)
    print_payload(payload, args.json)
    return status_code
def cmd_mother_doc_archive(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.target is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.target or runtime["mother_doc_root"]).resolve()
    payload, status_code = mother_doc_archive_payload(target, args.force, args.archive_slug)
    print_payload(payload, args.json)
    return status_code
def cmd_construction_plan_init(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.target is None and args.design_plan is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.target or runtime["construction_plan_root"]).resolve()
    design_plan_path = Path(args.design_plan or Path(runtime["mother_doc_root"]) / "08_dev_execution_plan.md").resolve()
    payload, status_code = construction_plan_init_payload(target, design_plan_path, args.force)
    print_payload(payload, args.json)
    return status_code
def cmd_construction_plan_lint(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = args.path or str(runtime["construction_plan_root"])
    payload = construction_plan_lint_payload(Path(target).resolve())
    print_payload(payload, args.json)
    return 0 if payload["status"] == "pass" else 1
def cmd_mother_doc_lint(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None and args.mother_doc is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = args.path or args.mother_doc or str(runtime["mother_doc_root"])
    payload = mother_doc_lint_payload(Path(target).resolve())
    print_payload(payload, args.json)
    return 0 if payload["status"] == "pass" else 1
def cmd_mother_doc_state_sync(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.path or runtime["mother_doc_root"]).resolve()
    payload = mother_doc_state_sync_payload(
        target,
        args.doc_ref,
        args.from_state,
        args.to_state,
        args.pack_ref,
    )
    print_payload(payload, args.json)
    return 0 if payload["status"] == "pass" else 1
def cmd_acceptance_lint(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.matrix_path is None and args.report_path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    payload = acceptance_lint_payload(
        Path(args.matrix_path or runtime["acceptance_matrix_path"]).resolve(),
        Path(args.report_path or runtime["acceptance_report_path"]).resolve(),
        Path(runtime["codebase_root"]),
        Path(runtime["target_root"]),
    )
    print_payload(payload, args.json)
    return 0 if payload["status"] == "pass" else 1
def add_runtime_scope_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target-root", default=None)
    parser.add_argument("--docs-root", default=None)
    parser.add_argument("--module-dir", default=None)
    parser.add_argument("--codebase-root", default=None)
    parser.add_argument("--graph-runtime-root", default=None)
    parser.add_argument("--project-agents", default=None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    target_runtime = subparsers.add_parser("target-runtime-contract")
    add_runtime_scope_args(target_runtime)
    target_runtime.add_argument("--json", action="store_true")
    target_runtime.set_defaults(func=cmd_target_runtime_contract)

    workflow = subparsers.add_parser("workflow-contract")
    add_runtime_scope_args(workflow)
    workflow.add_argument("--json", action="store_true")
    workflow.set_defaults(func=cmd_workflow_contract)

    checklist = subparsers.add_parser("stage-checklist")
    add_runtime_scope_args(checklist)
    checklist.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    checklist.add_argument("--json", action="store_true")
    checklist.set_defaults(func=cmd_stage_checklist)

    stage_doc = subparsers.add_parser("stage-doc-contract")
    add_runtime_scope_args(stage_doc)
    stage_doc.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    stage_doc.add_argument("--json", action="store_true")
    stage_doc.set_defaults(func=lambda args: _cmd_stage_contract(args, "doc"))

    stage_command = subparsers.add_parser("stage-command-contract")
    add_runtime_scope_args(stage_command)
    stage_command.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    stage_command.add_argument("--json", action="store_true")
    stage_command.set_defaults(func=lambda args: _cmd_stage_contract(args, "command"))

    stage_graph = subparsers.add_parser("stage-graph-contract")
    add_runtime_scope_args(stage_graph)
    stage_graph.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    stage_graph.add_argument("--json", action="store_true")
    stage_graph.set_defaults(func=lambda args: _cmd_stage_contract(args, "graph"))

    preflight = subparsers.add_parser("graph-preflight")
    add_runtime_scope_args(preflight)
    preflight.add_argument("--repo", default=None)
    preflight.add_argument("--allow-missing-index", action="store_true")
    preflight.add_argument("--json", action="store_true")
    preflight.set_defaults(func=cmd_graph_preflight)

    postflight = subparsers.add_parser("graph-postflight")
    add_runtime_scope_args(postflight)
    postflight.add_argument("--repo", default=None)
    postflight.add_argument("--json", action="store_true")
    postflight.set_defaults(func=cmd_graph_postflight)

    target_scaffold = subparsers.add_parser("target-scaffold")
    add_runtime_scope_args(target_scaffold)
    target_scaffold.add_argument("--force", action="store_true")
    target_scaffold.add_argument("--json", action="store_true")
    target_scaffold.set_defaults(func=cmd_target_scaffold)

    templates = subparsers.add_parser("template-index")
    templates.add_argument("--json", action="store_true")
    templates.set_defaults(func=cmd_template_index)

    mother_doc_init = subparsers.add_parser("mother-doc-init")
    add_runtime_scope_args(mother_doc_init)
    mother_doc_init.add_argument("--target", default=None)
    mother_doc_init.add_argument("--force", action="store_true")
    mother_doc_init.add_argument("--json", action="store_true")
    mother_doc_init.set_defaults(func=cmd_mother_doc_init)

    mother_doc_archive = subparsers.add_parser("mother-doc-archive")
    add_runtime_scope_args(mother_doc_archive)
    mother_doc_archive.add_argument("--target", default=None)
    mother_doc_archive.add_argument("--archive-slug", default=None)
    mother_doc_archive.add_argument("--force", action="store_true")
    mother_doc_archive.add_argument("--json", action="store_true")
    mother_doc_archive.set_defaults(func=cmd_mother_doc_archive)

    construction_plan_init = subparsers.add_parser("construction-plan-init")
    add_runtime_scope_args(construction_plan_init)
    construction_plan_init.add_argument("--target", default=None)
    construction_plan_init.add_argument("--design-plan", default=None)
    construction_plan_init.add_argument("--force", action="store_true")
    construction_plan_init.add_argument("--json", action="store_true")
    construction_plan_init.set_defaults(func=cmd_construction_plan_init)

    construction_plan_lint = subparsers.add_parser("construction-plan-lint")
    add_runtime_scope_args(construction_plan_lint)
    construction_plan_lint.add_argument("--path", default=None)
    construction_plan_lint.add_argument("--json", action="store_true")
    construction_plan_lint.set_defaults(func=cmd_construction_plan_lint)

    mother_doc_lint = subparsers.add_parser("mother-doc-lint")
    add_runtime_scope_args(mother_doc_lint)
    mother_doc_lint.add_argument("--path", default=None)
    mother_doc_lint.add_argument("--mother-doc", dest="mother_doc", default=None)
    mother_doc_lint.add_argument("--json", action="store_true")
    mother_doc_lint.set_defaults(func=cmd_mother_doc_lint)

    mother_doc_state_sync = subparsers.add_parser("mother-doc-state-sync")
    add_runtime_scope_args(mother_doc_state_sync)
    mother_doc_state_sync.add_argument("--path", default=None)
    mother_doc_state_sync.add_argument("--doc-ref", action="append", required=True)
    mother_doc_state_sync.add_argument("--from-state", required=True)
    mother_doc_state_sync.add_argument("--to-state", required=True)
    mother_doc_state_sync.add_argument("--pack-ref", default=None)
    mother_doc_state_sync.add_argument("--json", action="store_true")
    mother_doc_state_sync.set_defaults(func=cmd_mother_doc_state_sync)

    acceptance_lint = subparsers.add_parser("acceptance-lint")
    add_runtime_scope_args(acceptance_lint)
    acceptance_lint.add_argument("--matrix-path", default=None)
    acceptance_lint.add_argument("--report-path", default=None)
    acceptance_lint.add_argument("--json", action="store_true")
    acceptance_lint.set_defaults(func=cmd_acceptance_lint)
    return parser
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))
if __name__ == "__main__":
    raise SystemExit(main())
