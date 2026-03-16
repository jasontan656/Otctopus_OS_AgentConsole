from __future__ import annotations

import argparse

from mdm_cli_contract_commands import (
    cmd_agents_domain_contract,
    cmd_agents_payload_contract,
    cmd_contract,
    cmd_target_contract,
)
from mdm_cli_stage_commands import (
    cmd_collect,
    cmd_lint,
    cmd_push,
    cmd_scan,
)
from mdm_cli_write_commands import cmd_agents_maintain, cmd_new_writeback, cmd_scaffold
from toolbox_support import add_common_report_args


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Cli_Toolbox.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    contract.set_defaults(func=cmd_contract)

    scan = subparsers.add_parser("scan")
    add_common_report_args(scan)
    scan.set_defaults(func=cmd_scan)

    lint = subparsers.add_parser("lint")
    add_common_report_args(lint)
    lint.set_defaults(func=cmd_lint)

    collect = subparsers.add_parser("collect")
    add_common_report_args(collect)
    collect.add_argument("--allow-invalid-external", action="store_true")
    collect.set_defaults(func=cmd_collect)

    push = subparsers.add_parser("push")
    add_common_report_args(push)
    push.add_argument("--allow-invalid-internal", action="store_true")
    push.set_defaults(func=cmd_push)

    scaffold = subparsers.add_parser("scaffold")
    add_common_report_args(scaffold)
    scaffold.add_argument(
        "--target-dir",
        action="append",
        required=True,
        help="External directory to place governed file skeletons into. Repeatable.",
    )
    scaffold.add_argument("--file-kind", action="append", default=[], help="Governed filename to scaffold. Repeatable.")
    scaffold.add_argument("--all-governed", action="store_true", help="Scaffold all currently governed file kinds.")
    scaffold.add_argument("--allow-existing", action="store_true", help="Allow overwriting existing scaffold targets.")
    scaffold.set_defaults(func=cmd_scaffold)

    agents_maintain = subparsers.add_parser("agents-maintain")
    add_common_report_args(agents_maintain)
    agents_maintain.add_argument("--intent", required=True, help="Natural-language AGENTS maintenance request.")
    agents_maintain.set_defaults(func=cmd_agents_maintain)

    new_writeback = subparsers.add_parser("new-writeback")
    new_writeback.add_argument("--dry-run", action="store_true")
    new_writeback.add_argument("--json", action="store_true", help="Print machine-readable JSON to stdout.")
    new_writeback.add_argument(
        "--write-runtime-report",
        action="store_true",
        help="Write latest result JSON into Codex_Skill_Runtime/<skill>/artifacts/<stage>/latest.json and append a timestamped runtime log under logs/<stage>/.",
    )
    new_writeback.add_argument("--report-path", help="Optional custom JSON report path. When set, also writes the report there.")
    new_writeback.add_argument("--source-path", action="append", required=True, help="Exact external AGENTS path to finalize. Repeatable.")
    new_writeback.set_defaults(func=cmd_new_writeback)

    target_contract = subparsers.add_parser("target-contract")
    target_contract.add_argument("--source-path", required=True)
    target_contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    target_contract.set_defaults(func=cmd_target_contract)

    agents_payload_contract = subparsers.add_parser("agents-payload-contract")
    agents_payload_contract.add_argument("--source-path", required=True)
    agents_payload_contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    agents_payload_contract.set_defaults(func=cmd_agents_payload_contract)

    agents_domain_contract = subparsers.add_parser("agents-domain-contract")
    agents_domain_contract.add_argument("--source-path", required=True)
    agents_domain_contract.add_argument("--domain", required=True)
    agents_domain_contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    agents_domain_contract.set_defaults(func=cmd_agents_domain_contract)

    return parser
