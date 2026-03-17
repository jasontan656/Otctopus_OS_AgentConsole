#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from governance_controller import govern
from runtime_support import build_config
from runtime_support import discover_skills
from runtime_support import render_prompt
from runtime_support import status_payload
from runtime_types import ControllerFinalPayload
from runtime_types import DiscoveryPayload
from runtime_types import JSONDict
from runtime_types import PromptRenderPayload
from runtime_types import RuntimeConfig
from runtime_types import StatusPayload


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
CONTRACT_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = CONTRACT_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = CONTRACT_ROOT / "DIRECTIVE_INDEX.json"


ToolboxPayload = JSONDict | DiscoveryPayload | PromptRenderPayload | StatusPayload | ControllerFinalPayload


def _emit(payload: ToolboxPayload, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("status", "ok"))
    return 0


def _read_json(path: Path) -> JSONDict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_runtime_config(args: argparse.Namespace) -> tuple[RuntimeConfig, list[str] | None]:
    skill_names = getattr(args, "skill_name", None)
    if isinstance(skill_names, str):
        skill_names = [skill_names]
    return build_config(
        repo_root=Path(args.repo_root).resolve() if getattr(args, "repo_root", None) else None,
        skills_root=Path(args.skills_root).resolve() if getattr(args, "skills_root", None) else None,
        runtime_root=Path(args.runtime_root).resolve() if getattr(args, "runtime_root", None) else None,
        include_self=getattr(args, "include_self", False),
        max_parallel=getattr(args, "max_parallel", 4),
        poll_seconds=getattr(args, "poll_seconds", 10),
    ), skill_names


def cmd_contract(args: argparse.Namespace) -> int:
    return _emit(_read_json(CONTRACT_PATH), args.json)


def cmd_directive(args: argparse.Namespace) -> int:
    index = _read_json(DIRECTIVE_INDEX_PATH)
    topics = index.get("topics", {})
    if not isinstance(topics, dict) or args.topic not in topics:
        raise SystemExit(f"unknown topic: {args.topic}")
    entry = topics[args.topic]
    if not isinstance(entry, dict):
        raise SystemExit(f"invalid directive index for: {args.topic}")
    json_path = entry.get("json_path")
    if not isinstance(json_path, str):
        raise SystemExit(f"invalid directive json_path for: {args.topic}")
    return _emit(_read_json(CONTRACT_ROOT / json_path), args.json)


def cmd_list_targets(args: argparse.Namespace) -> int:
    config, skill_names = _build_runtime_config(args)
    return _emit(discover_skills(config, skill_names=skill_names), args.json)


def cmd_status(args: argparse.Namespace) -> int:
    config, skill_names = _build_runtime_config(args)
    return _emit(status_payload(config, skill_names=skill_names), args.json)


def cmd_render_prompt(args: argparse.Namespace) -> int:
    config, _ = _build_runtime_config(args)
    return _emit(render_prompt(config, args.skill_name), args.json)


def cmd_govern(args: argparse.Namespace) -> int:
    config, skill_names = _build_runtime_config(args)
    return _emit(govern(config, skill_names=skill_names), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Python-SubAgentGov toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    list_targets = subparsers.add_parser("list-targets")
    list_targets.add_argument("--repo-root")
    list_targets.add_argument("--skills-root")
    list_targets.add_argument("--runtime-root")
    list_targets.add_argument("--include-self", action="store_true")
    list_targets.add_argument("--skill-name", action="append")
    list_targets.add_argument("--json", action="store_true")
    list_targets.set_defaults(func=cmd_list_targets)

    status = subparsers.add_parser("status")
    status.add_argument("--repo-root")
    status.add_argument("--skills-root")
    status.add_argument("--runtime-root")
    status.add_argument("--include-self", action="store_true")
    status.add_argument("--skill-name", action="append")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)

    render = subparsers.add_parser("render-prompt")
    render.add_argument("--repo-root")
    render.add_argument("--skills-root")
    render.add_argument("--runtime-root")
    render.add_argument("--skill-name", required=True)
    render.add_argument("--json", action="store_true")
    render.set_defaults(func=cmd_render_prompt)

    govern_cmd = subparsers.add_parser("govern")
    govern_cmd.add_argument("--repo-root")
    govern_cmd.add_argument("--skills-root")
    govern_cmd.add_argument("--runtime-root")
    govern_cmd.add_argument("--include-self", action="store_true")
    govern_cmd.add_argument("--skill-name", action="append")
    govern_cmd.add_argument("--max-parallel", type=int, default=4)
    govern_cmd.add_argument("--poll-seconds", type=int, default=10)
    govern_cmd.add_argument("--json", action="store_true")
    govern_cmd.set_defaults(func=cmd_govern)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
