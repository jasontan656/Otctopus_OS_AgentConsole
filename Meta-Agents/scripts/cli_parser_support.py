from __future__ import annotations

import argparse


def build_parser(cmd_registry, cmd_scan_collect, cmd_sync_out) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    registry = subparsers.add_parser("registry")
    registry.add_argument("--skill-root")
    registry.add_argument("--json", action="store_true")
    registry.set_defaults(func=cmd_registry)

    scan_collect = subparsers.add_parser("scan-collect")
    scan_collect.add_argument("--skill-root")
    scan_collect.add_argument("--source-root")
    scan_collect.add_argument("--json", action="store_true")
    scan_collect.set_defaults(func=cmd_scan_collect)

    sync_out = subparsers.add_parser("sync-out")
    sync_out.add_argument("--skill-root")
    sync_out.add_argument("--target-source-path", action="append", default=[])
    sync_out.add_argument("--all", action="store_true")
    sync_out.add_argument("--json", action="store_true")
    sync_out.set_defaults(func=cmd_sync_out)
    return parser
