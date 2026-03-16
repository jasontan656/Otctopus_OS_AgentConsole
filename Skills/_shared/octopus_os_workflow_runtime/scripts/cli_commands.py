#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cli_support import STAGES
from cli_support import acceptance_lint_result, construction_plan_init_result, construction_plan_lint_summary
from cli_support import graph_postflight_summary, graph_preflight_summary
from cli_support import mother_doc_audit_summary
from cli_support import mother_doc_archive_result, mother_doc_init_result, mother_doc_lint_summary
from cli_support import mother_doc_mark_modified_result, mother_doc_state_sync_result
from cli_support import target_scaffold_result, workflow_contract_document
from mother_doc_root_index_support import refresh_root_index_result
from mother_doc_sync_support import mother_doc_sync_result
from skill_runtime_context import active_stage
from stage_contract_support import (
    stage_command_contract_payload,
    stage_doc_contract_payload,
    stage_graph_contract_payload,
)
from target_runtime_support import TargetRuntimeRecord, resolve_target_runtime, target_runtime_contract_payload
from workflow_skill_runtime import compile_reading_chain, runtime_contract_payload


def print_document(document: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(document, indent=2))
    else:
        for key, value in document.items():
            print(f"{key}: {value}")
    return 0


def cmd_runtime_contract(args: argparse.Namespace) -> int:
    return print_document(runtime_contract_payload(), args.json)


def cmd_read_context(args: argparse.Namespace) -> int:
    selection = [item.strip() for item in args.selection.split(",") if item.strip()]
    return print_document(compile_reading_chain(args.entry, selection), args.json)


def cmd_workflow_contract(args: argparse.Namespace) -> int:
    return print_document(
        workflow_contract_document(
            target_root=args.target_root,
            development_docs_root=args.development_docs_root,
            docs_root=args.docs_root,
            module_dir=args.module_dir,
            codebase_root=args.codebase_root,
            graph_runtime_root=args.graph_runtime_root,
            project_agents=args.project_agents,
        ),
        args.json,
    )


def cmd_target_runtime_contract(args: argparse.Namespace) -> int:
    document = target_runtime_contract_payload(
        target_root=args.target_root,
        development_docs_root=args.development_docs_root,
        docs_root=args.docs_root,
        module_dir=args.module_dir,
        codebase_root=args.codebase_root,
        graph_runtime_root=args.graph_runtime_root,
        project_agents=args.project_agents,
    )
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1


def _resolve_runtime(args: argparse.Namespace) -> TargetRuntimeRecord:
    return resolve_target_runtime(
        target_root=args.target_root,
        development_docs_root=args.development_docs_root,
        docs_root=args.docs_root,
        module_dir=args.module_dir,
        codebase_root=args.codebase_root,
        graph_runtime_root=args.graph_runtime_root,
        project_agents=args.project_agents,
    )


def _emit_runtime_not_ready(runtime: TargetRuntimeRecord, as_json: bool) -> int:
    document = {
        "status": "fail",
        "reason": "target_runtime_not_ready",
        "missing_prerequisites": runtime["missing_prerequisites"],
        "target_root": str(runtime["target_root"]),
        "development_docs_root": str(runtime["development_docs_root"]),
        "module_dir": runtime["module_dir"],
        "docs_root": str(runtime["docs_root"]),
    }
    print_document(document, as_json)
    return 1


def cmd_stage_checklist(args: argparse.Namespace) -> int:
    if args.stage != active_stage():
        return print_document(
            {
                "status": "fail",
                "reason": "stage_mismatch",
                "expected_stage": active_stage(),
                "received_stage": args.stage,
            },
            args.json,
        )
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"]:
        return _emit_runtime_not_ready(runtime, args.json)
    document = {
        "stage": args.stage,
        **STAGES[args.stage],
        "target_runtime_precheck_required": True,
        "target_runtime_contract": target_runtime_contract_payload(
            target_root=args.target_root,
            development_docs_root=args.development_docs_root,
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
            "client_mother_doc_root": str(runtime["client_mother_doc_root"]),
            "construction_plan_root": str(runtime["construction_plan_root"]),
            "codebase_root": str(runtime["codebase_root"]),
            "graph_runtime_root": str(runtime["graph_runtime_root"]),
        },
    }
    return print_document(document, args.json)


def _cmd_stage_contract(args: argparse.Namespace, kind: str) -> int:
    if args.stage != active_stage():
        return print_document(
            {
                "status": "fail",
                "reason": "stage_mismatch",
                "expected_stage": active_stage(),
                "received_stage": args.stage,
                "contract_kind": kind,
            },
            args.json,
        )
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
    return print_document(factories[kind](), args.json)


def cmd_graph_preflight(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.repo is None:
        return _emit_runtime_not_ready(runtime, args.json)
    repo = args.repo or str(runtime["codebase_root"])
    graph_runtime_root = Path(args.graph_runtime_root or runtime["graph_runtime_root"]).resolve()
    document = graph_preflight_summary(Path(repo).resolve(), args.allow_missing_index, graph_runtime_root)
    return print_document(document, args.json)


def cmd_graph_postflight(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.repo is None:
        return _emit_runtime_not_ready(runtime, args.json)
    repo = args.repo or str(runtime["codebase_root"])
    graph_runtime_root = Path(args.graph_runtime_root or runtime["graph_runtime_root"]).resolve()
    document = graph_postflight_summary(Path(repo).resolve(), graph_runtime_root)
    return print_document(document, args.json)


def cmd_target_scaffold(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    document, status_code = target_scaffold_result(runtime, args.force)
    print_document(document, args.json)
    return status_code


def cmd_template_index(args: argparse.Namespace) -> int:
    from cli_support import TEMPLATES

    document = {name: str(path) for name, path in TEMPLATES.items()}
    return print_document(document, args.json)


def cmd_mother_doc_init(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.target is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.target or runtime["mother_doc_root"]).resolve()
    document, status_code = mother_doc_init_result(target, args.force)
    print_document(document, args.json)
    return status_code


def cmd_mother_doc_archive(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.target is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.target or runtime["mother_doc_root"]).resolve()
    document, status_code = mother_doc_archive_result(target, args.force, args.archive_slug)
    print_document(document, args.json)
    return status_code


def cmd_construction_plan_init(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.target is None and args.design_plan is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.target or runtime["construction_plan_root"]).resolve()
    design_plan_path = Path(args.design_plan).resolve() if args.design_plan else None
    document, status_code = construction_plan_init_result(
        target,
        design_plan_path,
        args.force,
        args.plan_kind,
    )
    print_document(document, args.json)
    return status_code


def cmd_construction_plan_lint(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = args.path or str(runtime["construction_plan_root"])
    document = construction_plan_lint_summary(
        Path(target).resolve(),
        require_execution_eligible=args.require_execution_eligible,
    )
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1


def cmd_mother_doc_lint(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None and args.mother_doc is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = args.path or args.mother_doc or str(runtime["mother_doc_root"])
    document = mother_doc_lint_summary(Path(target).resolve())
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1


def cmd_mother_doc_audit(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None and args.mother_doc is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = args.path or args.mother_doc or str(runtime["mother_doc_root"])
    document = mother_doc_audit_summary(Path(target).resolve())
    print_document(document, args.json)
    if args.soft_fail_exit:
        return 0
    return 0 if document["status"] == "pass" else 1


def cmd_mother_doc_refresh_root_index(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.path or runtime["mother_doc_root"]).resolve()
    document, status_code = refresh_root_index_result(target)
    print_document(document, args.json)
    return status_code


def cmd_mother_doc_state_sync(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.path or runtime["mother_doc_root"]).resolve()
    document = mother_doc_state_sync_result(
        target,
        args.doc_ref,
        args.from_state,
        args.to_state,
        args.pack_ref,
    )
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1


def cmd_mother_doc_mark_modified(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    target = Path(args.path or runtime["mother_doc_root"]).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else None
    document = mother_doc_mark_modified_result(
        target,
        args.doc_ref or [],
        repo_root,
        args.auto_from_git,
    )
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1


def cmd_mother_doc_sync_client_copy(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.source is None:
        return _emit_runtime_not_ready(runtime, args.json)
    source_root = Path(args.source or runtime["mother_doc_root"]).resolve()
    mirror_root = Path(args.mirror or runtime["client_mother_doc_root"]).resolve()
    document, status_code = mother_doc_sync_result(source_root, mirror_root)
    print_document(document, args.json)
    return status_code


def cmd_acceptance_lint(args: argparse.Namespace) -> int:
    runtime = _resolve_runtime(args)
    if not runtime["ready_for_service"] and args.matrix_path is None and args.report_path is None:
        return _emit_runtime_not_ready(runtime, args.json)
    document = acceptance_lint_result(
        Path(args.matrix_path or runtime["acceptance_matrix_path"]).resolve(),
        Path(args.report_path or runtime["acceptance_report_path"]).resolve(),
        Path(runtime["codebase_root"]),
        Path(runtime["target_root"]),
    )
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1
