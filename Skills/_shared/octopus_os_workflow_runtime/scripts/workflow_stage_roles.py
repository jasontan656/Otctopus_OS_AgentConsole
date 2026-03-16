from __future__ import annotations


GRAPH_STAGE_ROLES = {
    "mother_doc": {
        "read_policy": "align the live requirement source first, then read graph context only to reconcile current code reality and structural boundaries",
        "update_policy": "do_not_update_graph_in_this_stage",
    },
    "construction_plan": {
        "read_policy": "read graph context in this stage to decompose execution atom packs against real module boundaries and dependencies",
        "update_policy": "do_not_update_graph_in_this_stage",
    },
    "implementation": {
        "read_policy": "do_not_read_graph_as_a_stage_artifact; implementation must read concrete code directly",
        "update_policy": "do_not_update_graph_in_this_stage",
    },
    "acceptance": {
        "read_policy": "do_not_read_graph_as_acceptance_evidence",
        "update_policy": "after acceptance evidence is complete, run graph-postflight to refresh downstream maintenance context",
    },
}
