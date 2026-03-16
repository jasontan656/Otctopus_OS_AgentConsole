from __future__ import annotations

import argparse

from cli_commands import (
    cmd_acceptance_lint,
    cmd_construction_plan_init,
    cmd_construction_plan_lint,
    cmd_graph_postflight,
    cmd_graph_preflight,
    cmd_mother_doc_archive,
    cmd_mother_doc_audit,
    cmd_mother_doc_init,
    cmd_mother_doc_lint,
    cmd_mother_doc_mark_modified,
    cmd_mother_doc_refresh_root_index,
    cmd_mother_doc_state_sync,
    cmd_mother_doc_sync_client_copy,
    cmd_read_context,
    cmd_runtime_contract,
    cmd_stage_checklist,
    cmd_target_runtime_contract,
    cmd_target_scaffold,
    cmd_template_index,
    cmd_workflow_contract,
    _cmd_stage_contract,
)
from skill_runtime_context import allowed_commands, stage_choices


EXPOSED_COMMANDS = allowed_commands()


def _enabled(name: str) -> bool:
    return name in EXPOSED_COMMANDS


def add_runtime_scope_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target-root", default=None)
    parser.add_argument("--development-docs-root", default=None)
    parser.add_argument("--docs-root", default=None)
    parser.add_argument("--module-dir", default=None)
    parser.add_argument("--codebase-root", default=None)
    parser.add_argument("--graph-runtime-root", default=None)
    parser.add_argument("--project-agents", default=None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("runtime-contract", "contract"):
        if _enabled(name):
            runtime_contract = subparsers.add_parser(name)
            runtime_contract.add_argument("--json", action="store_true")
            runtime_contract.set_defaults(func=cmd_runtime_contract)

    for name in ("read-path-context", "read-contract-context"):
        if _enabled(name):
            read_context = subparsers.add_parser(name)
            read_context.add_argument("--entry", required=True)
            read_context.add_argument("--selection", default="")
            read_context.add_argument("--json", action="store_true")
            read_context.set_defaults(func=cmd_read_context)

    if _enabled("target-runtime-contract"):
        target_runtime = subparsers.add_parser("target-runtime-contract")
        add_runtime_scope_args(target_runtime)
        target_runtime.add_argument("--json", action="store_true")
        target_runtime.set_defaults(func=cmd_target_runtime_contract)

    if _enabled("workflow-contract"):
        workflow = subparsers.add_parser("workflow-contract")
        add_runtime_scope_args(workflow)
        workflow.add_argument("--json", action="store_true")
        workflow.set_defaults(func=cmd_workflow_contract)

    if _enabled("stage-checklist"):
        checklist = subparsers.add_parser("stage-checklist")
        add_runtime_scope_args(checklist)
        checklist.add_argument("--stage", required=True, choices=stage_choices())
        checklist.add_argument("--json", action="store_true")
        checklist.set_defaults(func=cmd_stage_checklist)

    if _enabled("stage-doc-contract"):
        stage_doc = subparsers.add_parser("stage-doc-contract")
        add_runtime_scope_args(stage_doc)
        stage_doc.add_argument("--stage", required=True, choices=stage_choices())
        stage_doc.add_argument("--json", action="store_true")
        stage_doc.set_defaults(func=lambda args: _cmd_stage_contract(args, "doc"))

    if _enabled("stage-command-contract"):
        stage_command = subparsers.add_parser("stage-command-contract")
        add_runtime_scope_args(stage_command)
        stage_command.add_argument("--stage", required=True, choices=stage_choices())
        stage_command.add_argument("--json", action="store_true")
        stage_command.set_defaults(func=lambda args: _cmd_stage_contract(args, "command"))

    if _enabled("stage-graph-contract"):
        stage_graph = subparsers.add_parser("stage-graph-contract")
        add_runtime_scope_args(stage_graph)
        stage_graph.add_argument("--stage", required=True, choices=stage_choices())
        stage_graph.add_argument("--json", action="store_true")
        stage_graph.set_defaults(func=lambda args: _cmd_stage_contract(args, "graph"))

    if _enabled("graph-preflight"):
        preflight = subparsers.add_parser("graph-preflight")
        add_runtime_scope_args(preflight)
        preflight.add_argument("--repo", default=None)
        preflight.add_argument("--allow-missing-index", action="store_true")
        preflight.add_argument("--json", action="store_true")
        preflight.set_defaults(func=cmd_graph_preflight)

    if _enabled("graph-postflight"):
        postflight = subparsers.add_parser("graph-postflight")
        add_runtime_scope_args(postflight)
        postflight.add_argument("--repo", default=None)
        postflight.add_argument("--json", action="store_true")
        postflight.set_defaults(func=cmd_graph_postflight)

    if _enabled("target-scaffold"):
        target_scaffold = subparsers.add_parser("target-scaffold")
        add_runtime_scope_args(target_scaffold)
        target_scaffold.add_argument("--force", action="store_true")
        target_scaffold.add_argument("--json", action="store_true")
        target_scaffold.set_defaults(func=cmd_target_scaffold)

    if _enabled("template-index"):
        templates = subparsers.add_parser("template-index")
        templates.add_argument("--json", action="store_true")
        templates.set_defaults(func=cmd_template_index)

    if _enabled("mother-doc-init"):
        mother_doc_init = subparsers.add_parser("mother-doc-init")
        add_runtime_scope_args(mother_doc_init)
        mother_doc_init.add_argument("--target", default=None)
        mother_doc_init.add_argument("--force", action="store_true")
        mother_doc_init.add_argument("--json", action="store_true")
        mother_doc_init.set_defaults(func=cmd_mother_doc_init)

    if _enabled("mother-doc-archive"):
        mother_doc_archive = subparsers.add_parser("mother-doc-archive")
        add_runtime_scope_args(mother_doc_archive)
        mother_doc_archive.add_argument("--target", default=None)
        mother_doc_archive.add_argument("--archive-slug", default=None)
        mother_doc_archive.add_argument("--force", action="store_true")
        mother_doc_archive.add_argument("--json", action="store_true")
        mother_doc_archive.set_defaults(func=cmd_mother_doc_archive)

    if _enabled("construction-plan-init"):
        construction_plan_init = subparsers.add_parser("construction-plan-init")
        add_runtime_scope_args(construction_plan_init)
        construction_plan_init.add_argument("--target", default=None)
        construction_plan_init.add_argument("--design-plan", default=None)
        construction_plan_init.add_argument(
            "--plan-kind",
            default="official_plan",
            choices=["official_plan", "preview_skeleton"],
        )
        construction_plan_init.add_argument("--force", action="store_true")
        construction_plan_init.add_argument("--json", action="store_true")
        construction_plan_init.set_defaults(func=cmd_construction_plan_init)

    if _enabled("construction-plan-lint"):
        construction_plan_lint = subparsers.add_parser("construction-plan-lint")
        add_runtime_scope_args(construction_plan_lint)
        construction_plan_lint.add_argument("--path", default=None)
        construction_plan_lint.add_argument("--require-execution-eligible", action="store_true")
        construction_plan_lint.add_argument("--json", action="store_true")
        construction_plan_lint.set_defaults(func=cmd_construction_plan_lint)

    if _enabled("mother-doc-lint"):
        mother_doc_lint = subparsers.add_parser("mother-doc-lint")
        add_runtime_scope_args(mother_doc_lint)
        mother_doc_lint.add_argument("--path", default=None)
        mother_doc_lint.add_argument("--mother-doc", dest="mother_doc", default=None)
        mother_doc_lint.add_argument("--json", action="store_true")
        mother_doc_lint.set_defaults(func=cmd_mother_doc_lint)

    if _enabled("mother-doc-audit"):
        mother_doc_audit = subparsers.add_parser("mother-doc-audit")
        add_runtime_scope_args(mother_doc_audit)
        mother_doc_audit.add_argument("--path", default=None)
        mother_doc_audit.add_argument("--mother-doc", dest="mother_doc", default=None)
        mother_doc_audit.add_argument(
            "--soft-fail-exit",
            action="store_true",
            help="Emit the audit payload but exit 0 even when audit_gate_allowed=false.",
        )
        mother_doc_audit.add_argument("--json", action="store_true")
        mother_doc_audit.set_defaults(func=cmd_mother_doc_audit)

    if _enabled("mother-doc-refresh-root-index"):
        mother_doc_refresh_root_index = subparsers.add_parser("mother-doc-refresh-root-index")
        add_runtime_scope_args(mother_doc_refresh_root_index)
        mother_doc_refresh_root_index.add_argument("--path", default=None)
        mother_doc_refresh_root_index.add_argument("--json", action="store_true")
        mother_doc_refresh_root_index.set_defaults(func=cmd_mother_doc_refresh_root_index)

    if _enabled("mother-doc-state-sync"):
        mother_doc_state_sync = subparsers.add_parser("mother-doc-state-sync")
        add_runtime_scope_args(mother_doc_state_sync)
        mother_doc_state_sync.add_argument("--path", default=None)
        mother_doc_state_sync.add_argument("--doc-ref", action="append", required=True)
        mother_doc_state_sync.add_argument("--from-state", required=True)
        mother_doc_state_sync.add_argument("--to-state", required=True)
        mother_doc_state_sync.add_argument("--pack-ref", default=None)
        mother_doc_state_sync.add_argument("--json", action="store_true")
        mother_doc_state_sync.set_defaults(func=cmd_mother_doc_state_sync)

    if _enabled("mother-doc-mark-modified"):
        mother_doc_mark_modified = subparsers.add_parser("mother-doc-mark-modified")
        add_runtime_scope_args(mother_doc_mark_modified)
        mother_doc_mark_modified.add_argument("--path", default=None)
        mother_doc_mark_modified.add_argument("--doc-ref", action="append")
        mother_doc_mark_modified.add_argument("--repo-root", default=None)
        mother_doc_mark_modified.add_argument("--auto-from-git", action="store_true")
        mother_doc_mark_modified.add_argument("--json", action="store_true")
        mother_doc_mark_modified.set_defaults(func=cmd_mother_doc_mark_modified)

    if _enabled("mother-doc-sync-client-copy"):
        mother_doc_sync = subparsers.add_parser("mother-doc-sync-client-copy")
        add_runtime_scope_args(mother_doc_sync)
        mother_doc_sync.add_argument("--source", default=None)
        mother_doc_sync.add_argument("--mirror", default=None)
        mother_doc_sync.add_argument("--json", action="store_true")
        mother_doc_sync.set_defaults(func=cmd_mother_doc_sync_client_copy)

    if _enabled("acceptance-lint"):
        acceptance_lint = subparsers.add_parser("acceptance-lint")
        add_runtime_scope_args(acceptance_lint)
        acceptance_lint.add_argument("--matrix-path", default=None)
        acceptance_lint.add_argument("--report-path", default=None)
        acceptance_lint.add_argument("--json", action="store_true")
        acceptance_lint.set_defaults(func=cmd_acceptance_lint)

    return parser
