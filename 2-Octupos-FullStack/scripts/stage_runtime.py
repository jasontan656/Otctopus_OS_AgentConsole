from __future__ import annotations

import json


TOP_LEVEL_RULES = [
    "rules/FULLSTACK_SKILL_HARD_RULES.md",
    "references/runtime/SKILL_RUNTIME_CONTRACT.md",
]

STAGE_DEFINITIONS: dict[str, dict[str, object]] = {
    "mother_doc": {
        "command": "mother-doc-stage",
        "scope": "maintain Mother_Doc structure, container expansion, naming, and authored document contracts",
        "must_load": TOP_LEVEL_RULES,
        "requires": [],
        "produces": [
            "Mother_Doc container tree",
            "container-level docs",
            "implementation inputs",
        ],
    },
    "implementation": {
        "command": "implementation-stage",
        "scope": "implement code and runtime changes strictly from Mother_Doc outputs",
        "must_load": TOP_LEVEL_RULES,
        "requires": [
            "mother_doc stage outputs",
        ],
        "produces": [
            "code changes",
            "runtime changes",
            "evidence inputs",
        ],
    },
    "evidence": {
        "command": "evidence-stage",
        "scope": "capture delivery evidence from implementation outputs and bind it back to Mother_Doc",
        "must_load": TOP_LEVEL_RULES,
        "requires": [
            "mother_doc stage outputs",
            "implementation stage outputs",
        ],
        "produces": [
            "execution evidence",
            "acceptance witnesses",
            "writeback records",
        ],
    },
}


def emit_stage_payload(stage_name: str, *, as_json: bool) -> int:
    payload = {
        "stage": stage_name,
        **STAGE_DEFINITIONS[stage_name],
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0
