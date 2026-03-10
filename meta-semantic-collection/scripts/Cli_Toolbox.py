#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PAYLOAD_PATH = SKILL_ROOT / "assets" / "runtime" / "semantic_pool_payload.json"


def load_payload(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_payload(payload)
    return payload


def validate_payload(payload: object) -> None:
    if not isinstance(payload, list):
        raise ValueError("payload must be a list")
    seen_terms: dict[str, str] = {}
    for index, entry in enumerate(payload):
        if not isinstance(entry, dict):
            raise ValueError(f"entry[{index}] must be an object")
        keys = set(entry.keys())
        if keys != {"collection", "action_semantic_description"}:
            raise ValueError(f"entry[{index}] must contain exactly collection and action_semantic_description")
        collection = entry["collection"]
        description = entry["action_semantic_description"]
        if not isinstance(collection, list) or not collection:
            raise ValueError(f"entry[{index}].collection must be a non-empty list")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"entry[{index}].action_semantic_description must be a non-empty string")
        for term in collection:
            if not isinstance(term, str) or not term.strip():
                raise ValueError(f"entry[{index}].collection contains an invalid term")
            normalized = term.strip()
            previous = seen_terms.get(normalized)
            if previous and previous != description.strip():
                raise ValueError(f"term '{normalized}' maps to multiple descriptions")
            seen_terms[normalized] = description.strip()


def dump_payload(payload: list[dict[str, object]]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def emit(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for key, value in payload.items():
        if isinstance(value, (dict, list)):
            print(f"{key}:")
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            print(f"{key}: {value}")
    return 0


def build_runtime_contract(payload_path: Path) -> dict[str, object]:
    semantic_pool = load_payload(payload_path)
    return {
        "contract_name": "META_SEMANTIC_COLLECTION_RUNTIME_CONTRACT",
        "contract_version": "v1",
        "skill_name": "meta-semantic-collection",
        "enforcement_mode": "required",
        "turn_start": {
            "required": True,
            "action": "load_semantic_pool_runtime_contract",
            "cli_command": "python3 scripts/Cli_Toolbox.py runtime-contract --json",
        },
        "turn_end": {
            "required": False,
            "action": "upsert_semantic_pool_on_valid_clarification",
            "condition": "only when a new valid semantic clarification appears in this turn",
        },
        "translation_contract": {
            "payload_file": str(payload_path),
            "entry_schema": {
                "collection": "list[str]",
                "action_semantic_description": "str",
            },
            "hard_rules": [
                "semantic_pool_payload must only be read through this runtime contract in normal execution",
                "multiple terms may map to one action_semantic_description",
                "one term must not map to multiple action_semantic_description values",
                "when prompt terms hit the pool, pool semantics override model default interpretation",
            ],
        },
        "semantic_pool_payload": semantic_pool,
    }


def normalize_terms(raw_terms: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for raw in raw_terms:
        term = raw.strip()
        if not term or term in seen:
            continue
        seen.add(term)
        ordered.append(term)
    if not ordered:
        raise ValueError("at least one non-empty term is required")
    return ordered


def make_diff(before: str, after: str, path: Path) -> str:
    lines = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
        lineterm="",
    )
    return "\n".join(lines)


def upsert_payload(payload: list[dict[str, object]], terms: list[str], description: str) -> tuple[list[dict[str, object]], dict[str, object]]:
    normalized_terms = normalize_terms(terms)
    normalized_description = description.strip()
    if not normalized_description:
        raise ValueError("description must be non-empty")

    updated = json.loads(json.dumps(payload, ensure_ascii=False))
    exact_desc_indexes = [
        idx for idx, entry in enumerate(updated) if entry["action_semantic_description"].strip() == normalized_description
    ]
    overlapping_indexes = [
        idx for idx, entry in enumerate(updated) if any(term in entry["collection"] for term in normalized_terms)
    ]

    target_index: int | None = None
    if exact_desc_indexes:
        target_index = exact_desc_indexes[0]
        for idx in reversed(exact_desc_indexes[1:]):
            updated[target_index]["collection"].extend(updated[idx]["collection"])
            del updated[idx]
            overlapping_indexes = [i - 1 if i > idx else i for i in overlapping_indexes if i != idx]
    elif overlapping_indexes:
        if len(set(overlapping_indexes)) > 1:
            raise ValueError("provided terms overlap multiple existing descriptions; split the update or clarify the target description")
        target_index = overlapping_indexes[0]
        updated[target_index]["action_semantic_description"] = normalized_description

    if target_index is None:
        updated.append(
            {
                "collection": normalized_terms,
                "action_semantic_description": normalized_description,
            }
        )
        action = "created_entry"
        target_index = len(updated) - 1
    else:
        action = "updated_entry"

    for idx, entry in enumerate(updated):
        if idx == target_index:
            continue
        entry["collection"] = [term for term in entry["collection"] if term not in normalized_terms]

    updated[target_index]["collection"] = normalize_terms(updated[target_index]["collection"] + normalized_terms)
    updated = [entry for entry in updated if entry["collection"]]
    validate_payload(updated)

    summary = {
        "action": action,
        "target_index": target_index,
        "terms": normalized_terms,
        "description": normalized_description,
    }
    return updated, summary


def cmd_runtime_contract(args) -> int:
    payload = build_runtime_contract(Path(args.payload_path))
    return emit(payload, args.json)


def cmd_upsert_payload(args) -> int:
    payload_path = Path(args.payload_path)
    payload = load_payload(payload_path)
    before_text = dump_payload(payload)
    updated_payload, summary = upsert_payload(payload, list(args.term or []), args.description)
    after_text = dump_payload(updated_payload)
    diff_text = make_diff(before_text, after_text, payload_path)

    result = {
        "status": "dry_run" if args.dry_run else "written",
        "payload_path": str(payload_path),
        "summary": summary,
        "diff": diff_text,
        "resulting_contract_preview": build_runtime_contract_from_payload(payload_path, updated_payload),
    }
    if not args.dry_run:
        payload_path.write_text(after_text, encoding="utf-8")
    return emit(result, args.json)


def build_runtime_contract_from_payload(payload_path: Path, semantic_pool: list[dict[str, object]]) -> dict[str, object]:
    validate_payload(semantic_pool)
    return {
        "contract_name": "META_SEMANTIC_COLLECTION_RUNTIME_CONTRACT",
        "contract_version": "v1",
        "skill_name": "meta-semantic-collection",
        "enforcement_mode": "required",
        "turn_start": {
            "required": True,
            "action": "load_semantic_pool_runtime_contract",
            "cli_command": "python3 scripts/Cli_Toolbox.py runtime-contract --json",
        },
        "turn_end": {
            "required": False,
            "action": "upsert_semantic_pool_on_valid_clarification",
            "condition": "only when a new valid semantic clarification appears in this turn",
        },
        "translation_contract": {
            "payload_file": str(payload_path),
            "entry_schema": {
                "collection": "list[str]",
                "action_semantic_description": "str",
            },
            "hard_rules": [
                "semantic_pool_payload must only be read through this runtime contract in normal execution",
                "multiple terms may map to one action_semantic_description",
                "one term must not map to multiple action_semantic_description values",
                "when prompt terms hit the pool, pool semantics override model default interpretation",
            ],
        },
        "semantic_pool_payload": semantic_pool,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="meta-semantic-collection toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    runtime_contract = subparsers.add_parser("runtime-contract")
    runtime_contract.add_argument("--payload-path", default=str(PAYLOAD_PATH))
    runtime_contract.add_argument("--json", action="store_true")
    runtime_contract.set_defaults(func=cmd_runtime_contract)

    upsert = subparsers.add_parser("upsert-payload")
    upsert.add_argument("--payload-path", default=str(PAYLOAD_PATH))
    upsert.add_argument("--term", action="append", required=True)
    upsert.add_argument("--description", required=True)
    upsert.add_argument("--dry-run", action="store_true")
    upsert.add_argument("--json", action="store_true")
    upsert.set_defaults(func=cmd_upsert_payload)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
