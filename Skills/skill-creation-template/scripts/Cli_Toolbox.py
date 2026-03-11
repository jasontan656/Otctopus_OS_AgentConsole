#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent


def emit(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for key, value in payload.items():
        print(f"{key}: {value}")
    return 0


def text_payload(path: Path, asset_name: str) -> dict[str, object]:
    return {
        "status": "ok",
        "asset": asset_name,
        "path": str(path),
        "content": path.read_text(encoding="utf-8"),
    }


def cmd_create_skill_from_template(args) -> int:
    cmd = [
        "python3",
        str(SCRIPT_DIR / "create_skill_from_template.py"),
        "--skill-name",
        args.skill_name,
        "--target-root",
        args.target_root,
        "--resources",
        args.resources,
        "--description",
        args.description,
        "--profile",
        args.profile,
    ]
    if args.overwrite:
        cmd.append("--overwrite")
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "create_skill_from_template failed")
    print(completed.stdout.strip())
    return 0


def cmd_skill_template(args) -> int:
    return emit(text_payload(SKILL_ROOT / "assets" / "skill_template" / "SKILL_TEMPLATE.md", "skill_template"), args.json)


def cmd_staged_skill_template(args) -> int:
    return emit(
        text_payload(SKILL_ROOT / "assets" / "skill_template" / "SKILL_TEMPLATE_STAGED.md", "staged_skill_template"),
        args.json,
    )


def cmd_openai_template(args) -> int:
    return emit(text_payload(SKILL_ROOT / "assets" / "skill_template" / "openai_template.yaml", "openai_template"), args.json)


def cmd_contract_reference(args) -> int:
    return emit(text_payload(SKILL_ROOT / "references" / "skill_template_contract_v1.md", "contract_reference"), args.json)


def cmd_staged_skill_reference(args) -> int:
    return emit(
        text_payload(
            SKILL_ROOT / "references" / "staged_cli_first_profile_reference.md",
            "staged_skill_reference",
        ),
        args.json,
    )


def cmd_runtime_contract_template(args) -> int:
    return emit(
        text_payload(
            SKILL_ROOT / "assets" / "skill_template" / "runtime" / "SKILL_RUNTIME_CONTRACT_TEMPLATE.json",
            "runtime_contract_template",
        ),
        args.json,
    )


def cmd_architecture_playbook(args) -> int:
    return emit(text_payload(SKILL_ROOT / "references" / "skill_architecture_playbook.md", "architecture_playbook"), args.json)


def cmd_runtime_contract(args) -> int:
    payload = json.loads((SKILL_ROOT / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.json").read_text(encoding="utf-8"))
    return emit(payload, args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skill-Creation-Template unified toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_skill = subparsers.add_parser("create-skill-from-template")
    create_skill.add_argument("--skill-name", required=True)
    create_skill.add_argument("--target-root", required=True)
    create_skill.add_argument("--resources", default="scripts,references,assets,tests")
    create_skill.add_argument("--description", default="")
    create_skill.add_argument("--profile", default="basic", choices=("basic", "staged_cli_first"))
    create_skill.add_argument("--overwrite", action="store_true")
    create_skill.set_defaults(func=cmd_create_skill_from_template)

    for name, func in (
        ("skill-template", cmd_skill_template),
        ("staged-skill-template", cmd_staged_skill_template),
        ("openai-template", cmd_openai_template),
        ("contract-reference", cmd_contract_reference),
        ("staged-skill-reference", cmd_staged_skill_reference),
        ("runtime-contract-template", cmd_runtime_contract_template),
        ("architecture-playbook", cmd_architecture_playbook),
        ("runtime-contract", cmd_runtime_contract),
    ):
        sub = subparsers.add_parser(name)
        sub.add_argument("--json", action="store_true")
        sub.set_defaults(func=func)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
