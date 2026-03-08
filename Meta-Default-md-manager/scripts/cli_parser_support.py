from __future__ import annotations

import argparse


def build_parser(cmd_registry, cmd_scan, cmd_collect, cmd_push) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    registry = subparsers.add_parser("registry")
    registry.add_argument("--skill-root")
    registry.add_argument("--json", action="store_true")
    registry.set_defaults(func=cmd_registry)

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
