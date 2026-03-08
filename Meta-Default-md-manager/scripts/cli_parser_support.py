from __future__ import annotations

import argparse


def build_parser(
    cmd_registry,
    cmd_scan,
    cmd_collect,
    cmd_push,
    cmd_contract,
    cmd_directive,
    cmd_render_audit_docs,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    registry = subparsers.add_parser("registry")
    registry.add_argument("--skill-root")
    registry.add_argument("--json", action="store_true")
    registry.set_defaults(func=cmd_registry)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--skill-root")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--skill-root")
    directive.add_argument("--stage", choices=["scan", "collect", "push"], required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    render_audit_docs = subparsers.add_parser("render-audit-docs")
    render_audit_docs.add_argument("--skill-root")
    render_audit_docs.add_argument("--json", action="store_true")
    render_audit_docs.set_defaults(func=cmd_render_audit_docs)

    scan = subparsers.add_parser("scan")
    scan.add_argument("--skill-root")
    scan.add_argument("--source-root")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=cmd_scan)

    collect = subparsers.add_parser("collect")
    collect.add_argument("--skill-root")
    collect.add_argument("--source-root")
    collect.add_argument("--json", action="store_true")
    collect.set_defaults(func=cmd_collect)

    push = subparsers.add_parser("push")
    push.add_argument("--skill-root")
    push.add_argument("--target-source-path", action="append", default=[])
    push.add_argument("--all", action="store_true")
    push.add_argument("--json", action="store_true")
    push.set_defaults(func=cmd_push)
    return parser
