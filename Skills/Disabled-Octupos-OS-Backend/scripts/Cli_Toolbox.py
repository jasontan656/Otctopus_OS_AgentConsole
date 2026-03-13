#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cli_support import ACCEPTANCE_MATRIX_PATH, ACCEPTANCE_REPORT_PATH, CODEBASE_ROOT, CONSTRUCTION_PLAN_ROOT, MOTHER_DOC_PATH, MOTHER_DOC_ROOT, RUNTIME_ROOT
from cli_support import STAGES, TEMPLATES
from cli_support import acceptance_lint_result, graph_postflight_summary, graph_preflight_summary
from cli_support import construction_plan_init_result, construction_plan_lint_summary, mother_doc_archive_result
from cli_support import mother_doc_init_result, mother_doc_lint_summary, workflow_contract_document
from stage_contract_support import stage_command_contract_spec, stage_doc_contract_spec, stage_graph_contract_spec
def print_document(document: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(document, indent=2))
    else:
        for key, value in document.items():
            print(f"{key}: {value}")
    return 0
def cmd_workflow_contract(args: argparse.Namespace) -> int:
    return print_document(workflow_contract_document(), args.json)
def cmd_stage_checklist(args: argparse.Namespace) -> int:
    document = {"stage": args.stage, **STAGES[args.stage]}
    return print_document(document, args.json)
def _cmd_stage_contract(args: argparse.Namespace, kind: str) -> int:
    factories = {
        "doc": lambda: stage_doc_contract_spec(args.stage, MOTHER_DOC_ROOT),
        "command": lambda: stage_command_contract_spec(args.stage, MOTHER_DOC_ROOT, CONSTRUCTION_PLAN_ROOT, CODEBASE_ROOT),
        "graph": lambda: stage_graph_contract_spec(args.stage, CODEBASE_ROOT),
    }
    return print_document(factories[kind](), args.json)
def cmd_graph_preflight(args: argparse.Namespace) -> int:
    repo = args.repo or args.codebase_root or str(CODEBASE_ROOT)
    document = graph_preflight_summary(Path(repo).resolve(), args.allow_missing_index)
    return print_document(document, args.json)
def cmd_graph_postflight(args: argparse.Namespace) -> int:
    repo = args.repo or args.codebase_root or str(CODEBASE_ROOT)
    document = graph_postflight_summary(Path(repo).resolve())
    return print_document(document, args.json)
def cmd_template_index(args: argparse.Namespace) -> int:
    document = {name: str(path) for name, path in TEMPLATES.items()}
    return print_document(document, args.json)
def cmd_mother_doc_init(args: argparse.Namespace) -> int:
    target = Path(args.target or MOTHER_DOC_ROOT).resolve()
    document, status_code = mother_doc_init_result(target, args.force)
    print_document(document, args.json)
    return status_code
def cmd_mother_doc_archive(args: argparse.Namespace) -> int:
    target = Path(args.target or MOTHER_DOC_ROOT).resolve()
    document, status_code = mother_doc_archive_result(target, args.force, args.archive_slug)
    print_document(document, args.json)
    return status_code
def cmd_construction_plan_init(args: argparse.Namespace) -> int:
    target = Path(args.target or CONSTRUCTION_PLAN_ROOT).resolve()
    design_plan_path = Path(args.design_plan or MOTHER_DOC_ROOT / "08_dev_execution_plan.md").resolve()
    document, status_code = construction_plan_init_result(target, design_plan_path, args.force)
    print_document(document, args.json)
    return status_code
def cmd_construction_plan_lint(args: argparse.Namespace) -> int:
    target = args.path or str(CONSTRUCTION_PLAN_ROOT)
    document = construction_plan_lint_summary(Path(target).resolve())
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1
def cmd_mother_doc_lint(args: argparse.Namespace) -> int:
    target = args.path or args.mother_doc or str(MOTHER_DOC_ROOT)
    document = mother_doc_lint_summary(Path(target).resolve())
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1
def cmd_acceptance_lint(args: argparse.Namespace) -> int:
    document = acceptance_lint_result(
        Path(args.matrix_path).resolve(),
        Path(args.report_path).resolve(),
        CODEBASE_ROOT,
        RUNTIME_ROOT,
    )
    print_document(document, args.json)
    return 0 if document["status"] == "pass" else 1
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    workflow = subparsers.add_parser("workflow-contract")
    workflow.add_argument("--json", action="store_true")
    workflow.set_defaults(func=cmd_workflow_contract)

    checklist = subparsers.add_parser("stage-checklist")
    checklist.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    checklist.add_argument("--json", action="store_true")
    checklist.set_defaults(func=cmd_stage_checklist)

    stage_doc = subparsers.add_parser("stage-doc-contract")
    stage_doc.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    stage_doc.add_argument("--json", action="store_true")
    stage_doc.set_defaults(func=lambda args: _cmd_stage_contract(args, "doc"))

    stage_command = subparsers.add_parser("stage-command-contract")
    stage_command.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    stage_command.add_argument("--json", action="store_true")
    stage_command.set_defaults(func=lambda args: _cmd_stage_contract(args, "command"))

    stage_graph = subparsers.add_parser("stage-graph-contract")
    stage_graph.add_argument("--stage", required=True, choices=list(STAGES.keys()))
    stage_graph.add_argument("--json", action="store_true")
    stage_graph.set_defaults(func=lambda args: _cmd_stage_contract(args, "graph"))

    preflight = subparsers.add_parser("graph-preflight")
    preflight.add_argument("--repo", default=None)
    preflight.add_argument("--codebase-root", dest="codebase_root", default=None)
    preflight.add_argument("--runtime-root", dest="runtime_root", default=str(RUNTIME_ROOT))
    preflight.add_argument("--allow-missing-index", action="store_true")
    preflight.add_argument("--json", action="store_true")
    preflight.set_defaults(func=cmd_graph_preflight)

    postflight = subparsers.add_parser("graph-postflight")
    postflight.add_argument("--repo", default=None)
    postflight.add_argument("--codebase-root", dest="codebase_root", default=None)
    postflight.add_argument("--json", action="store_true")
    postflight.set_defaults(func=cmd_graph_postflight)

    templates = subparsers.add_parser("template-index")
    templates.add_argument("--json", action="store_true")
    templates.set_defaults(func=cmd_template_index)

    mother_doc_init = subparsers.add_parser("mother-doc-init")
    mother_doc_init.add_argument("--target", default=str(MOTHER_DOC_ROOT))
    mother_doc_init.add_argument("--force", action="store_true")
    mother_doc_init.add_argument("--json", action="store_true")
    mother_doc_init.set_defaults(func=cmd_mother_doc_init)

    mother_doc_archive = subparsers.add_parser("mother-doc-archive")
    mother_doc_archive.add_argument("--target", default=str(MOTHER_DOC_ROOT))
    mother_doc_archive.add_argument("--archive-slug", default=None)
    mother_doc_archive.add_argument("--force", action="store_true")
    mother_doc_archive.add_argument("--json", action="store_true")
    mother_doc_archive.set_defaults(func=cmd_mother_doc_archive)

    construction_plan_init = subparsers.add_parser("construction-plan-init")
    construction_plan_init.add_argument("--target", default=str(CONSTRUCTION_PLAN_ROOT))
    construction_plan_init.add_argument("--design-plan", default=str(MOTHER_DOC_ROOT / "08_dev_execution_plan.md"))
    construction_plan_init.add_argument("--force", action="store_true")
    construction_plan_init.add_argument("--json", action="store_true")
    construction_plan_init.set_defaults(func=cmd_construction_plan_init)

    construction_plan_lint = subparsers.add_parser("construction-plan-lint")
    construction_plan_lint.add_argument("--path", default=None)
    construction_plan_lint.add_argument("--json", action="store_true")
    construction_plan_lint.set_defaults(func=cmd_construction_plan_lint)

    mother_doc_lint = subparsers.add_parser("mother-doc-lint")
    mother_doc_lint.add_argument("--path", default=None)
    mother_doc_lint.add_argument("--mother-doc", dest="mother_doc", default=None)
    mother_doc_lint.add_argument("--json", action="store_true")
    mother_doc_lint.set_defaults(func=cmd_mother_doc_lint)

    acceptance_lint = subparsers.add_parser("acceptance-lint")
    acceptance_lint.add_argument("--matrix-path", default=str(ACCEPTANCE_MATRIX_PATH))
    acceptance_lint.add_argument("--report-path", default=str(ACCEPTANCE_REPORT_PATH))
    acceptance_lint.add_argument("--json", action="store_true")
    acceptance_lint.set_defaults(func=cmd_acceptance_lint)
    return parser
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))
if __name__ == "__main__":
    raise SystemExit(main())
