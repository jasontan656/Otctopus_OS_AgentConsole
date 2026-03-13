from __future__ import annotations

import json

from stage_contract_support import (
    TOP_LEVEL_RESIDENT_DOCS,
    get_stage_command_contract,
    get_stage_doc_contract,
    get_stage_graph_contract,
    get_stage_summary,
)


def emit_stage_payload(stage_name: str, *, as_json: bool) -> int:
    payload = {
        **get_stage_summary(stage_name),
        "top_level_resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_doc_contract": get_stage_doc_contract(stage_name),
        "stage_command_contract": get_stage_command_contract(stage_name),
        "stage_graph_contract": get_stage_graph_contract(stage_name),
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0
