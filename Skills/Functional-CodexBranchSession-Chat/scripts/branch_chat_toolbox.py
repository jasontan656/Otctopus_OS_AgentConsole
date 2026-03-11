#!/usr/bin/env python3
"""
@scenario: tooling
@dept: codex_skill
@purpose: cli_entry
"""

from __future__ import annotations

import argparse

from command_support import cmd_answer_question, cmd_extract_final_reply, cmd_locate_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cli_Toolbox for Functional-CodexBranchSession-Chat")
    subparsers = parser.add_subparsers(dest="command", required=True)

    locate = subparsers.add_parser("locate-session", help="Locate session files by session/resume id")
    locate.add_argument("--session-id", default="")
    locate.add_argument("--resume-id", default="")
    locate.add_argument("--codex-home", default=None)
    locate.set_defaults(func=cmd_locate_session)

    extract = subparsers.add_parser("extract-final-reply", help="Extract assistant final reply by keyword")
    extract.add_argument("--session-id", default="")
    extract.add_argument("--resume-id", default="")
    extract.add_argument("--keyword", default="")
    extract.add_argument("--codex-home", default=None)
    extract.add_argument("--case-sensitive", action="store_true")
    extract.set_defaults(func=cmd_extract_final_reply)

    answer = subparsers.add_parser("answer-question", help="Locate reply and prepare a direct answer payload")
    answer.add_argument("--session-id", default="")
    answer.add_argument("--resume-id", default="")
    answer.add_argument("--keyword", default="")
    answer.add_argument("--question", required=True)
    answer.add_argument("--evidence-limit", type=int, default=8)
    answer.add_argument("--codex-home", default=None)
    answer.add_argument("--case-sensitive", action="store_true")
    answer.set_defaults(func=cmd_answer_question)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
