#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os

from runtime_pain_batch_engine import run_with_args
from runtime_pain_batch_support import DEFAULT_HISTORY, DEFAULT_MEMORY_RUNTIME, FORCED_SCOPE_MODE


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Turn-end runtime selfcheck: inspect current-turn or recent-run pain points from an external provider, skip noisy output when the run is smooth, and support same-turn verified repair writeback for bounded issues."
    )
    ap.add_argument(
        "mode_token",
        nargs="*",
        help="Use `>` (or omit mode) for turn-end selfcheck. Use `修复` only when a bounded fix is already applied and verification-backed writeback is intended.",
    )
    ap.add_argument("--mode", default="auto", choices=["auto", "diagnose", "repair"])
    ap.add_argument(
        "--memory-runtime",
        default=DEFAULT_MEMORY_RUNTIME,
        help="Path to an external runtime pain provider implementing optimization-list and optional optimization-resolve.",
    )
    ap.add_argument("--history-path", default=str(DEFAULT_HISTORY))
    ap.add_argument("--session-id", default="")
    ap.add_argument("--thread-id", default=os.environ.get("CODEX_THREAD_ID", ""))
    ap.add_argument(
        "--session-scope-mode",
        default=FORCED_SCOPE_MODE,
        choices=["auto", "thread_scoped", "all_threads"],
        help="Accepted for compatibility, but runtime extraction is always enforced as all_threads.",
    )
    ap.add_argument("--max-results", type=int, default=200)
    ap.add_argument("--include-resolved", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--group-key", action="append", default=[])
    ap.add_argument("--resolved-by", default="Meta-Runtime-Selfcheck")
    ap.add_argument("--turn-id", default="runtime-pain-batch")
    ap.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=False)
    ap.add_argument(
        "--repair-cmd",
        action="append",
        default=[],
        help="Deprecated: ignored. Code changes must be applied manually via apply_patch.",
    )
    ap.add_argument("--verify-cmd", action="append", default=[])
    ap.add_argument("--repair-timeout-sec", type=int, default=180)
    ap.add_argument("--repair-workdir", default="")
    ap.add_argument(
        "--auto-repair-cmd",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Deprecated: ignored. Runtime selfcheck no longer auto-executes repair commands.",
    )
    ap.add_argument("--manual-repair-applied", action=argparse.BooleanOptionalAction, default=False)
    ap.add_argument("--manual-repair-path", action="append", default=[])
    return ap


def main() -> int:
    return run_with_args(build_parser().parse_args())


__all__ = ["build_parser", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
