#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from artifact_support import lint_managed_artifacts, sync_client_mirror, write_managed_artifacts
from cli_support import (
    CONTRACT_PATH,
    DIRECTIVE_INDEX_PATH,
    compile_reading_chain,
    emit,
    load_request_text,
    read_json,
    resolve_runtime,
    run_command,
)
from factory_support import build_intent_draft, factoryize_request, register_run_snapshot
from intent_support import enhance_factory_payload
from subagent_support import (
    keyword_first_decision_summary,
    launch_and_wait_subagent,
    latest_subagent_status,
    runtask_validation_summary,
    scaffold_runtask,
    validation_closeout_summary,
)


def cmd_contract(args: argparse.Namespace) -> int:
    return emit(read_json(CONTRACT_PATH), args.json)


def cmd_directive(args: argparse.Namespace) -> int:
    index = read_json(DIRECTIVE_INDEX_PATH)
    topics = index.get("topics", {})
    if not isinstance(topics, dict) or args.topic not in topics:
        raise SystemExit(f"unknown topic: {args.topic}")
    entry = topics[args.topic]
    if not isinstance(entry, dict):
        raise SystemExit(f"invalid directive index for: {args.topic}")
    json_path = entry.get("json_path")
    if not isinstance(json_path, str):
        raise SystemExit(f"invalid directive json_path for: {args.topic}")
    return emit(read_json(DIRECTIVE_INDEX_PATH.parent / json_path), args.json)


def cmd_read_contract_context(args: argparse.Namespace) -> int:
    return emit(compile_reading_chain(args.entry), args.json)


def cmd_target_runtime_contract(args: argparse.Namespace) -> int:
    return emit(resolve_runtime(args.target_root, args.mirror_root), args.json)


def cmd_factory_intake(args: argparse.Namespace) -> int:
    request_text = load_request_text(args.request_text, args.request_file)
    return emit(factoryize_request(request_text), args.json)


def cmd_intent_enhance(args: argparse.Namespace) -> int:
    request_text = load_request_text(args.request_text, args.request_file)
    payload = factoryize_request(request_text)
    enhanced = enhance_factory_payload(payload)
    return emit(
        {
            "status": "pass",
            "factory_payload": payload,
            "intent_draft": build_intent_draft(payload),
            "enhanced_intent": enhanced,
        },
        args.json,
    )


def cmd_runtask_scaffold(args: argparse.Namespace) -> int:
    request_text = load_request_text(args.request_text, args.request_file)
    factory_payload = factoryize_request(request_text)
    runtask = scaffold_runtask(factory_payload, workspace_root=args.workspace_root)
    return emit(runtask, args.json)


def cmd_artifact_refresh(args: argparse.Namespace) -> int:
    runtime = resolve_runtime(args.target_root, args.mirror_root)
    if runtime["status"] != "pass":
        return emit({"status": "fail", "runtime": runtime}, args.json)
    snapshot = None
    if args.snapshot_file:
        snapshot = read_json(Path(args.snapshot_file))
    write_result = write_managed_artifacts(runtime["mother_doc_root"], snapshot=snapshot)
    mirror_result = {"status": "skipped", "reason": "skip_mirror_sync"}
    if not args.skip_mirror_sync:
        mirror_result = sync_client_mirror(runtime["mother_doc_root"], runtime["client_mirror_root"])
    audit = lint_managed_artifacts(
        runtime["mother_doc_root"],
        None if args.skip_mirror_sync else runtime["client_mirror_root"],
    )
    return emit(
        {
            "status": "pass" if audit["status"] == "pass" else "fail",
            "runtime": runtime,
            "artifact_write": write_result,
            "mirror_sync": mirror_result,
            "lint_audit": audit,
        },
        args.json,
    )


def _run_subagent_chain(args: argparse.Namespace) -> dict[str, object]:
    runtime = resolve_runtime(args.target_root, args.mirror_root)
    request_text = load_request_text(args.request_text, args.request_file)
    factory_payload = factoryize_request(request_text)
    enhanced_intent = enhance_factory_payload(factory_payload)
    runtask = scaffold_runtask(factory_payload, workspace_root=args.workspace_root)
    subagent_run = launch_and_wait_subagent(
        factory_payload,
        enhanced_intent,
        runtask,
        poll_interval_seconds=args.poll_interval_seconds,
        idle_timeout_seconds=args.idle_timeout_seconds,
        extra_add_dirs=[runtime["repo_root"], runtime["mother_doc_root"], runtime["client_mirror_root"], runtask["workspace_root"]],
    )
    return {
        "runtime": runtime,
        "factory_payload": factory_payload,
        "enhanced_intent": enhanced_intent,
        "runtask": runtask,
        "subagent_run": subagent_run,
    }


def cmd_runtask_subagent_run(args: argparse.Namespace) -> int:
    payload = _run_subagent_chain(args)
    overall_status = "pass" if payload["subagent_run"]["status"] == "pass" else "fail"
    payload["status"] = overall_status
    return emit(payload, args.json)


def cmd_subagent_status(args: argparse.Namespace) -> int:
    return emit(latest_subagent_status(args.run_id), args.json)


def cmd_self_governance_run(args: argparse.Namespace) -> int:
    subagent_payload = _run_subagent_chain(args)
    runtime = subagent_payload["runtime"]
    factory_payload = subagent_payload["factory_payload"]
    enhanced_intent = subagent_payload["enhanced_intent"]
    runtask = subagent_payload["runtask"]
    subagent_run = subagent_payload["subagent_run"]
    runtask_validation = runtask_validation_summary(runtask)
    keyword_first_summary = keyword_first_decision_summary(str(runtask["workspace_root"]))
    artifact_write = write_managed_artifacts(
        runtime["mother_doc_root"],
        snapshot={
            "factory_payload": factory_payload,
            "enhanced_intent": enhanced_intent,
            "subagent_run": subagent_run,
            "runtask_validation": runtask_validation,
            "keyword_first_decision_summary": keyword_first_summary,
        },
    )
    mirror_result = {"status": "skipped", "reason": "skip_mirror_sync"}
    if not args.skip_mirror_sync:
        mirror_result = sync_client_mirror(runtime["mother_doc_root"], runtime["client_mirror_root"])
    lint_audit = lint_managed_artifacts(
        runtime["mother_doc_root"],
        None if args.skip_mirror_sync else runtime["client_mirror_root"],
    )
    git_traceability = _git_traceability_summary(runtime)
    validation_closeout = validation_closeout_summary(
        run_id=str(subagent_run["run_id"]),
        subagent_run=subagent_run,
        runtask_payload=runtask,
        runtask_validation=runtask_validation,
        artifact_refresh=artifact_write,
        lint_audit=lint_audit,
        git_traceability_summary=git_traceability,
    )
    run_snapshot = {
        "run_id": subagent_run["run_id"],
        "runtime": runtime,
        "factory_payload": factory_payload,
        "enhanced_intent": enhanced_intent,
        "runtask": runtask,
        "subagent_run": subagent_run,
        "runtask_validation": runtask_validation,
        "keyword_first_decision_summary": keyword_first_summary,
        "artifact_refresh": artifact_write,
        "mirror_sync": mirror_result,
        "lint_audit": lint_audit,
        "git_traceability_summary": git_traceability,
        "validation_closeout": validation_closeout,
    }
    evolution = register_run_snapshot(run_snapshot)
    overall_status = "pass"
    if (
        runtime["status"] != "pass"
        or subagent_run["status"] != "pass"
        or runtask_validation["status"] != "pass"
        or lint_audit["status"] != "pass"
        or validation_closeout["status"] != "pass"
    ):
        overall_status = "fail"
    return emit(
        {
            "status": overall_status,
            "runtime": runtime,
            "factory_payload": factory_payload,
            "enhanced_intent": enhanced_intent,
            "runtask": runtask,
            "subagent_run": subagent_run,
            "runtask_validation": runtask_validation,
            "keyword_first_decision_summary": keyword_first_summary,
            "artifact_refresh": artifact_write,
            "mirror_sync": mirror_result,
            "lint_audit": lint_audit,
            "git_traceability_summary": git_traceability,
            "validation_closeout": validation_closeout,
            "skill_evolution": evolution,
        },
        args.json,
    )


def cmd_artifact_lint_audit(args: argparse.Namespace) -> int:
    runtime = resolve_runtime(args.target_root, args.mirror_root)
    audit = lint_managed_artifacts(runtime["mother_doc_root"], runtime["client_mirror_root"])
    return emit({"status": audit["status"], "runtime": runtime, "audit": audit}, args.json)


def _git_traceability_summary(runtime: dict[str, object]) -> dict[str, object]:
    skill_repo_root = CONTRACT_PATH.parents[2]
    artifact_repo_root = Path(str(runtime["repo_root"]))
    skill_status = run_command(["git", "status", "--short"], cwd=skill_repo_root, check=False)
    artifact_status = run_command(["git", "status", "--short"], cwd=artifact_repo_root, check=False)
    skill_lines = [line for line in skill_status.stdout.splitlines() if "Skills/Workflow-SiteMap-Creation" in line]
    artifact_lines = [
        line
        for line in artifact_status.stdout.splitlines()
        if "Development_Docs/mother_doc" in line or "Client_Applications/mother_doc" in line
    ]
    return {
        "status": "pass",
        "skill_repo_root": str(skill_repo_root),
        "artifact_repo_root": str(artifact_repo_root),
        "skill_repo_changes": skill_lines,
        "artifact_repo_changes": artifact_lines,
        "skill_repo_dirty": bool(skill_lines),
        "artifact_repo_dirty": bool(artifact_lines),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Workflow-SiteMap-Creation toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    read_context = subparsers.add_parser("read-contract-context")
    read_context.add_argument("--entry", required=True, choices=["self_governance", "artifact_lint_audit"])
    read_context.add_argument("--json", action="store_true")
    read_context.set_defaults(func=cmd_read_contract_context)

    runtime = subparsers.add_parser("target-runtime-contract")
    runtime.add_argument("--target-root", default=None)
    runtime.add_argument("--mirror-root", default=None)
    runtime.add_argument("--json", action="store_true")
    runtime.set_defaults(func=cmd_target_runtime_contract)

    factory = subparsers.add_parser("factory-intake")
    factory.add_argument("--request-text", default=None)
    factory.add_argument("--request-file", default=None)
    factory.add_argument("--json", action="store_true")
    factory.set_defaults(func=cmd_factory_intake)

    intent = subparsers.add_parser("intent-enhance")
    intent.add_argument("--request-text", default=None)
    intent.add_argument("--request-file", default=None)
    intent.add_argument("--json", action="store_true")
    intent.set_defaults(func=cmd_intent_enhance)

    runtask = subparsers.add_parser("runtask-scaffold")
    runtask.add_argument("--request-text", default=None)
    runtask.add_argument("--request-file", default=None)
    runtask.add_argument("--workspace-root", default=None)
    runtask.add_argument("--json", action="store_true")
    runtask.set_defaults(func=cmd_runtask_scaffold)

    runtask_subagent = subparsers.add_parser("runtask-subagent-run")
    runtask_subagent.add_argument("--target-root", default=None)
    runtask_subagent.add_argument("--mirror-root", default=None)
    runtask_subagent.add_argument("--request-text", default=None)
    runtask_subagent.add_argument("--request-file", default=None)
    runtask_subagent.add_argument("--workspace-root", default=None)
    runtask_subagent.add_argument("--poll-interval-seconds", type=int, default=5)
    runtask_subagent.add_argument("--idle-timeout-seconds", type=int, default=600)
    runtask_subagent.add_argument("--json", action="store_true")
    runtask_subagent.set_defaults(func=cmd_runtask_subagent_run)

    subagent_status = subparsers.add_parser("subagent-status")
    subagent_status.add_argument("--run-id", default=None)
    subagent_status.add_argument("--json", action="store_true")
    subagent_status.set_defaults(func=cmd_subagent_status)

    artifact_refresh = subparsers.add_parser("artifact-refresh")
    artifact_refresh.add_argument("--target-root", default=None)
    artifact_refresh.add_argument("--mirror-root", default=None)
    artifact_refresh.add_argument("--snapshot-file", default=None)
    artifact_refresh.add_argument("--skip-mirror-sync", action="store_true")
    artifact_refresh.add_argument("--json", action="store_true")
    artifact_refresh.set_defaults(func=cmd_artifact_refresh)

    self_governance = subparsers.add_parser("self-governance-run")
    self_governance.add_argument("--target-root", default=None)
    self_governance.add_argument("--mirror-root", default=None)
    self_governance.add_argument("--request-text", default=None)
    self_governance.add_argument("--request-file", default=None)
    self_governance.add_argument("--workspace-root", default=None)
    self_governance.add_argument("--skip-mirror-sync", action="store_true")
    self_governance.add_argument("--poll-interval-seconds", type=int, default=5)
    self_governance.add_argument("--idle-timeout-seconds", type=int, default=600)
    self_governance.add_argument("--json", action="store_true")
    self_governance.set_defaults(func=cmd_self_governance_run)

    lint_audit = subparsers.add_parser("artifact-lint-audit")
    lint_audit.add_argument("--target-root", default=None)
    lint_audit.add_argument("--mirror-root", default=None)
    lint_audit.add_argument("--json", action="store_true")
    lint_audit.set_defaults(func=cmd_artifact_lint_audit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
