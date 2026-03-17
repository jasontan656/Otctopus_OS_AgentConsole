from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast

from cli_support import (
    BACKEND_PYTHON,
    JsonObject,
    META_ENHANCE_CLI,
    META_ENHANCE_FILTER,
    RESULT_ROOT,
    SKILL_ROOT,
    now_iso,
    run_command,
    summarize_completed_process,
    write_text,
)
from factory_support import build_intent_draft


class EnhancedIntentPayload(TypedDict):
    status: str
    contract_call: JsonObject
    directive_call: JsonObject
    filter_call: JsonObject
    draft_path: str
    intent_output_path: str
    final_intent_output: str
    enhanced_at: str
    runtime_logs: JsonObject


def enhance_factory_payload(factory_payload: JsonObject) -> EnhancedIntentPayload:
    intent_root = RESULT_ROOT / "intent_enhancement"
    intent_root.mkdir(parents=True, exist_ok=True)
    source_digest = str(factory_payload["source_digest"])
    draft_path = intent_root / f"{source_digest}_draft.txt"
    intent_path = intent_root / f"{source_digest}_intent.txt"
    write_text(draft_path, build_intent_draft(factory_payload) + "\n")

    contract = run_command(
        [str(BACKEND_PYTHON), str(META_ENHANCE_CLI), "contract", "--json"],
        cwd=SKILL_ROOT,
    )
    directive = run_command(
        [str(BACKEND_PYTHON), str(META_ENHANCE_CLI), "directive", "--topic", "intent-clarify", "--json"],
        cwd=SKILL_ROOT,
    )
    filtered = run_command(
        [
            "python3",
            str(META_ENHANCE_FILTER),
            "--mode",
            "intent_clarify",
            "--input-file",
            str(draft_path),
            "--output-path",
            str(intent_path),
            "--json",
        ],
        cwd=SKILL_ROOT,
    )
    payload = cast(JsonObject, json.loads(filtered.stdout))
    final_intent_output = str(payload.get("final_intent_output", "")).strip()
    if not final_intent_output.startswith("INTENT:"):
        raise RuntimeError("Meta-Enhance-Prompt did not return a valid INTENT block")
    runtime_logs = payload.get("runtime_logs", {})
    return {
        "status": "pass",
        "contract_call": summarize_completed_process(contract),
        "directive_call": summarize_completed_process(directive),
        "filter_call": summarize_completed_process(filtered),
        "draft_path": str(draft_path),
        "intent_output_path": str(intent_path),
        "final_intent_output": final_intent_output,
        "enhanced_at": now_iso(),
        "runtime_logs": runtime_logs if isinstance(runtime_logs, dict) else {},
    }
