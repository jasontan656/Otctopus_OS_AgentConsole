from __future__ import annotations

import json


TOP_LEVEL_RULES = [
    "rules/FULLSTACK_SKILL_HARD_RULES.md",
    "references/runtime/SKILL_RUNTIME_CONTRACT.md",
]

STAGE_DEFINITIONS: dict[str, dict[str, object]] = {
    "mother_doc": {
        "command": "mother-doc-stage",
        "scope": "strengthen user intent, navigate Mother_Doc recursively by agents.md, and write back current-state authored docs",
        "must_load": TOP_LEVEL_RULES,
        "requires": [],
        "prompt_entry": {
            "skill": "Meta-prompt-write",
            "action": "strengthen the current user prompt with full repo context before selecting Mother_Doc scope",
        },
        "navigation_entry": {
            "root_readme": "/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/README.md",
            "root_agents": "/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/agents.md",
            "rule": "read README.md and agents.md at the current scope, choose the next path, and recurse until the full impact surface is covered",
        },
        "produces": [
            "Mother_Doc container tree",
            "recursive agents.md indexes",
            "container-level docs",
            "implementation inputs",
        ],
        "writeback_rule": "overwrite in place and keep only the current state; project-internal document versions are not maintained",
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
