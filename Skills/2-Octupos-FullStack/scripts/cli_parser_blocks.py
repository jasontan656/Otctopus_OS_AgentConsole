from __future__ import annotations

import argparse

from skill_runtime_entry import load_skill_facade_contract, load_skill_runtime_contract, resolve_skill_root
from stage_contract_support import (
    get_stage_checklist,
    get_stage_command_contract,
    get_stage_doc_contract,
    get_stage_graph_contract,
)
from stage_runtime import emit_stage_payload
from toolbox_ops import append_development_log, emit_contract

STAGES = ("mother_doc", "implementation", "evidence")


def register_skill_runtime_parsers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    definitions = (
        (
            "skill-runtime-contract",
            "print the skill-level runtime contract; models must prefer this CLI JSON over markdown",
            load_skill_runtime_contract,
        ),
        (
            "skill-facade-contract",
            "print the runtime routing map for stage entry and specialized sub-branches",
            load_skill_facade_contract,
        ),
    )
    for command, help_text, loader in definitions:
        parser = subparsers.add_parser(command, help=help_text)
        parser.add_argument("--skill-root", default=None, help="override skill root")
        parser.add_argument("--json", action="store_true")
        parser.set_defaults(
            func=lambda args, contract_loader=loader: emit_contract(
                contract_loader(resolve_skill_root(args.skill_root)),
                as_json=args.json,
            )
        )


def register_stage_contract_parsers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    definitions = (
        ("stage-checklist", "print the checklist for a specific stage", get_stage_checklist),
        ("stage-doc-contract", "print the document-loading contract for a specific stage", get_stage_doc_contract),
        ("stage-command-contract", "print the command contract for a specific stage", get_stage_command_contract),
        ("stage-graph-contract", "print the graph contract for a specific stage", get_stage_graph_contract),
    )
    for command, help_text, loader in definitions:
        parser = subparsers.add_parser(command, help=help_text)
        parser.add_argument("--stage", choices=STAGES, required=True)
        parser.add_argument("--json", action="store_true")
        parser.set_defaults(func=lambda args, contract_loader=loader: emit_contract(contract_loader(args.stage), as_json=args.json))


def register_stage_summary_parsers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    definitions = (
        ("mother-doc-stage", "print scope and carry-forward requirements for the mother_doc stage", "mother_doc"),
        ("implementation-stage", "print scope and carry-forward requirements for the implementation stage", "implementation"),
        ("evidence-stage", "print scope and carry-forward requirements for the evidence stage", "evidence"),
    )
    for command, help_text, stage in definitions:
        parser = subparsers.add_parser(command, help=help_text)
        parser.add_argument("--json", action="store_true")
        parser.set_defaults(func=lambda args, stage_name=stage: emit_stage_payload(stage_name, as_json=args.json))


def register_development_log_parsers(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    default_document_root: str,
) -> None:
    definitions = (
        (
            "append-implementation-log",
            "append an evidence-stage implementation batch log entry under Mother_Doc/common/development_logs",
            "implementation",
        ),
        (
            "append-deployment-log",
            "append an evidence-stage deployment checkpoint log entry under Mother_Doc/common/development_logs",
            "deployment",
        ),
    )
    for command, help_text, kind in definitions:
        parser = subparsers.add_parser(command, help=help_text)
        parser.add_argument("--document-root", default=default_document_root, help="Mother_Doc root")
        parser.add_argument("--summary", required=True)
        parser.add_argument("--doc-path", action="append", default=[])
        parser.add_argument("--code-path", action="append", default=[])
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--json", action="store_true")
        parser.set_defaults(
            func=lambda args, log_kind=kind: append_development_log(
                argparse.Namespace(**vars(args), kind=log_kind)
            )
        )
