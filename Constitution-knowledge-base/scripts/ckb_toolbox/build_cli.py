from __future__ import annotations

import json
from pathlib import Path

from ckb_toolbox.machine_keywords import mechanical_payload
from ckb_toolbox.registry_io import parse_domain_keywords, parse_registry


def main() -> int:
    skill_root = Path(__file__).resolve().parents[2]
    registry = parse_registry(skill_root / "references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml")
    graph_keywords = parse_domain_keywords(skill_root / "references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md")
    out_path = skill_root / "references/anchor_docs_machine/anchor_docs_machine_v1.jsonl"
    rows = []
    for section in ["common_core", "common_conditional", "constraints"]:
        for item in registry[section]:
            doc_path = skill_root / item["doc"]
            payload = mechanical_payload(section, item["anchor_id"], item["graph_node"], item["doc"], doc_path.read_text(encoding="utf-8"), graph_keywords.get(item["graph_node"], []))
            rows.append(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"generated={out_path}")
    print(f"records={len(rows)}")
    return 0
