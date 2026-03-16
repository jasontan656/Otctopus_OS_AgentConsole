from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from doc_models import DirectiveIndexPayload, DirectivePayload, RuntimeContractPayload

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_ROOT = SKILL_ROOT / "references" / "runtime_contracts"


def _read_runtime_contract(path: Path) -> RuntimeContractPayload:
    return cast(RuntimeContractPayload, json.loads(path.read_text(encoding="utf-8")))


def _read_directive_index(path: Path) -> DirectiveIndexPayload:
    return cast(DirectiveIndexPayload, json.loads(path.read_text(encoding="utf-8")))


def _read_directive(path: Path) -> DirectivePayload:
    return cast(DirectivePayload, json.loads(path.read_text(encoding="utf-8")))


def runtime_contract_payload() -> RuntimeContractPayload:
    return _read_runtime_contract(RUNTIME_ROOT / "SKILL_RUNTIME_CONTRACT.json")


def directive_payload(topic: str) -> DirectivePayload:
    index = _read_directive_index(RUNTIME_ROOT / "DIRECTIVE_INDEX.json")
    topics = index["topics"]
    if topic not in topics:
        available = ", ".join(sorted(topics.keys()))
        raise KeyError(f"unknown topic: {topic}. available topics: {available}")
    entry = topics[topic]
    json_path = entry.get("json_path")
    if not isinstance(json_path, str):
        raise KeyError(topic)
    return _read_directive(RUNTIME_ROOT / json_path)
