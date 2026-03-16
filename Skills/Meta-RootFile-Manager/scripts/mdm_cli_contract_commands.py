from __future__ import annotations

import argparse
import json
from pathlib import Path

from rootfile_runtime import detect_paths, resolve_agents_domain_contract, resolve_target_contract
from toolbox_contracts import build_agents_payload_contract, load_skill_runtime_contract


def _emit_error(payload: dict[str, object]) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1


def cmd_target_contract(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    source_path = Path(args.source_path).resolve()
    try:
        result = resolve_target_contract(paths, source_path)
    except FileNotFoundError as exc:
        return _emit_error({"error": str(exc), "source_path": str(source_path)})
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_contract(args: argparse.Namespace) -> int:
    del args
    payload = load_skill_runtime_contract()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_agents_payload_contract(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    source_path = Path(args.source_path).resolve()
    try:
        payload = build_agents_payload_contract(paths, source_path)
    except FileNotFoundError as exc:
        return _emit_error({"error": str(exc), "source_path": str(source_path)})
    except ValueError as exc:
        return _emit_error(
            {
                "status": "error",
                "error": str(exc),
                "source_path": str(source_path),
            }
        )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_agents_domain_contract(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    source_path = Path(args.source_path).resolve()
    try:
        payload = resolve_agents_domain_contract(paths, source_path, args.domain)
    except FileNotFoundError as exc:
        return _emit_error({"error": str(exc), "source_path": str(source_path), "domain": args.domain})
    except ValueError as exc:
        return _emit_error(
            {
                "status": "error",
                "error": str(exc),
                "source_path": str(source_path),
                "domain": args.domain,
            }
        )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0
