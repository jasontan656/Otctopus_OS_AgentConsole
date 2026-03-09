from __future__ import annotations

import argparse
from pathlib import Path

from mother_doc_agents_manager import (
    acquire_cli_lock as acquire_agents_lock,
    collect_from_scan as collect_agents_from_scan,
    load_registry as load_agents_registry,
    load_runtime_contract as load_agents_runtime_contract,
    load_stage_directive as load_agents_stage_directive,
    push_agents_tree,
    resolve_skill_root as resolve_agents_skill_root,
    scan_agents_tree,
)
from agents_target_runtime import load_target_contract as load_agents_target_contract
from toolbox_ops import emit_contract


def mother_doc_agents_contract(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    return emit_contract(load_agents_runtime_contract(skill_root), as_json=args.json)


def mother_doc_agents_directive(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    return emit_contract(load_agents_stage_directive(skill_root, args.stage), as_json=args.json)


def mother_doc_agents_registry(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    payload = load_agents_registry(skill_root)
    payload["skill_root"] = str(skill_root)
    return emit_contract(payload, as_json=args.json)


def mother_doc_agents_target_contract(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    payload = load_agents_target_contract(skill_root, args.relative_path, args.file_kind)
    return emit_contract(payload, as_json=args.json)


def mother_doc_agents_scan(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    document_root = Path(args.document_root).resolve()
    with acquire_agents_lock(skill_root, "scan"):
        payload = scan_agents_tree(skill_root, document_root)
    return emit_contract(payload, as_json=args.json)


def mother_doc_agents_collect(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    with acquire_agents_lock(skill_root, "collect"):
        payload = collect_agents_from_scan(skill_root)
    return emit_contract(payload, as_json=args.json)


def mother_doc_agents_push(args: argparse.Namespace) -> int:
    skill_root = resolve_agents_skill_root(getattr(args, "skill_root", None))
    document_root = Path(args.document_root).resolve()
    with acquire_agents_lock(skill_root, "push"):
        payload = push_agents_tree(skill_root, document_root, dry_run=args.dry_run)
    return emit_contract(payload, as_json=args.json)
