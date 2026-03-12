from __future__ import annotations
# contract_name: 2_octupos_fullstack_stage_contract_graph_data
# contract_version: 1.0.0
# validation_mode: static_minimal
# required_fields: EVIDENCE_GRAPH_DOCS,EVIDENCE_GRAPH_COMMANDS
# optional_fields: none

EVIDENCE_GRAPH_DOCS = [
    "references/evidence/00_EVIDENCE_INDEX.md",
    "references/evidence/graph/00_GRAPH_INDEX.md",
    "references/evidence/graph/GRAPH_RUNTIME_CONTRACT.md",
    "references/evidence/graph/GRAPH_COMMAND_CONTRACT.md",
    "references/evidence/graph/GRAPH_NODE_EDGE_MODEL.md",
    "references/evidence/graph/GRAPH_STORAGE_LAYOUT.md",
    "references/evidence/graph/GRAPH_FRONTEND_CONSUMPTION_CONTRACT.md",
    "references/evidence/graph/GRAPH_WRITEBACK_WORKFLOW.md",
    "references/evidence/graph/GRAPH_CHANGE_DETECTION_WORKFLOW.md",
    "references/evidence/graph/GRAPH_QUERY_WORKFLOW.md",
    "references/evidence/graph/GRAPH_RESOURCE_WORKFLOW.md",
    "references/evidence/graph/GRAPH_MIGRATION_MAP.md",
]

EVIDENCE_GRAPH_COMMANDS = [
    {
        "command": "./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/os_graph_cli.py status",
        "purpose": "verify OS_graph runtime readiness and vendored engine availability before graph writeback",
    },
    {
        "command": "./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/os_graph_cli.py sync-doc-bindings",
        "purpose": "materialize authored-doc nodes, edges, and frontend layer bundles under Mother_Doc/graph/runtime",
    },
    {
        "command": "./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/os_graph_cli.py sync-evidence",
        "purpose": "materialize evidence nodes, lifecycle indexes, and evidence-side frontend bundles under Mother_Doc/graph/runtime",
    },
    {
        "command": "./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/os_graph_cli.py <analyze|query|context|impact|detect-changes|resource|map|wiki|cypher> [args...]",
        "purpose": "run the evidence-owned OS_graph command surface without leaving the Disabled-Octupos-FullStack skill",
    },
]
