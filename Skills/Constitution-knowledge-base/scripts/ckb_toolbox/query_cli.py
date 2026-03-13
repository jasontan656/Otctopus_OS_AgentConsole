from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

from ckb_toolbox.query_engine import (
    MINIMUM_KEYWORD_CONTRACT,
    REQUIRED_COMMON_ANCHORS,
    REQUIRED_CONSTRAINT_ANCHORS,
    REQUIRED_GATES,
    emit_jsonl,
    match_domains,
    score_record,
)
from ckb_toolbox.registry_io import (
    load_machine_records,
    parse_domain_keywords,
    parse_registry,
    split_keywords,
)

FORBIDDEN_OUTPUT_ARG_PATTERN = re.compile(
    r"^--(out|output|file|save|export|write|dump|path)(?:$|[-_=])",
    re.IGNORECASE,
)

QuerySectionItem = Dict[str, str]
MachineRecord = Dict[str, object]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query constitution machine rules by bilingual keywords.")
    parser.add_argument("--keywords-zh", required=True, help="Chinese keywords, comma/space separated.")
    parser.add_argument("--keywords-en", required=True, help="English keywords, comma/space separated.")
    return parser


def emit_hits(
    section: str,
    items: List[QuerySectionItem],
    machine: Dict[str, MachineRecord],
    zh_terms: List[str],
    en_terms: List[str],
    matched_domains: List[str],
    skill_root: Path,
) -> list[str]:
    if not items:
        return []
    hits = []
    for item in items:
        rec = machine.get(item["anchor_id"])
        if not rec:
            continue
        score, matched_terms = score_record(rec, zh_terms, en_terms, matched_domains)
        if score > 0:
            hits.append((score, matched_terms, rec))
    if not hits:
        emit_jsonl({"record": "no_hit", "section": section, "reason": "score<=0"})
        return []
    for score, matched_terms, rec0 in sorted(hits, key=lambda x: (-x[0], str(x[2].get("id", "")))):
        rec = dict(rec0)
        rec.update({
            "record": "constitution_rule",
            "section": section,
            "score": score,
            "matched_terms": matched_terms,
            "src": str((skill_root / str(rec.get("src", ""))).resolve()),
        })
        emit_jsonl(rec)
    return sorted({str(hit[2].get("id", "")) for hit in hits if hit[2].get("id")})


def main() -> int:
    parser = build_parser()
    args, unknown = parser.parse_known_args()
    if unknown:
        forbidden = [item for item in unknown if FORBIDDEN_OUTPUT_ARG_PATTERN.match(item)]
        if forbidden:
            parser.error("禁止落盘参数：不允许使用 --out/--output/--file/--save/--export/--write/--dump/--path。")
        parser.error(f"未知参数：{' '.join(unknown)}")
    zh_terms = split_keywords(args.keywords_zh)
    en_terms = split_keywords(args.keywords_en)
    if not zh_terms or not en_terms:
        parser.error("必须双语输入：--keywords-zh 与 --keywords-en 都必须提供至少 1 个关键词。")
    skill_root = Path(__file__).resolve().parents[2]
    sections = parse_registry(skill_root / "references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml")
    domains = parse_domain_keywords(skill_root / "references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md")
    machine = load_machine_records(skill_root / "references/anchor_docs_machine/anchor_docs_machine_v1.jsonl")
    matched_domains = match_domains(zh_terms, en_terms, domains)
    emit_jsonl({
        "record": "query_meta",
        "tool": "Cli_Toolbox.constitution_keyword_query",
        "mode": "machine_jsonl_v1",
        "keywords": {"zh": zh_terms, "en": en_terms},
        "matched_domains": matched_domains,
        "common_policy": "constraints_on_hit_only",
        "minimum_keyword_contract_record": "minimum_keyword_contract",
        "enforcement_contract_record": "constitution_enforcement_contract",
        "output_contract": "console_only_no_disk_no_markdown",
    })
    emit_jsonl({"record": "minimum_keyword_contract", **MINIMUM_KEYWORD_CONTRACT, "provided_keywords": {"zh": zh_terms, "en": en_terms}})
    if sections["common_core"]:
        for item in sorted(sections["common_core"], key=lambda x: x["anchor_id"]):
            rec = dict(machine.get(item["anchor_id"], {}))
            if not rec:
                continue
            rec.update({"record": "constitution_rule", "section": "common_core", "src": str((skill_root / str(rec.get("src", ""))).resolve())})
            emit_jsonl(rec)
    emit_hits("common_conditional", sections["common_conditional"], machine, zh_terms, en_terms, matched_domains, skill_root)
    matched_constraints = emit_hits("constraints", sections["constraints"], machine, zh_terms, en_terms, matched_domains, skill_root)
    emit_jsonl({
        "record": "constitution_enforcement_contract",
        "required_common_anchors": REQUIRED_COMMON_ANCHORS,
        "required_constraint_anchors": REQUIRED_CONSTRAINT_ANCHORS,
        "matched_constraint_anchors": matched_constraints,
        "required_gates": REQUIRED_GATES,
        "minimum_keyword_contract": MINIMUM_KEYWORD_CONTRACT,
        "static_enforcement_scope": {
            "lintable_categories": [],
            "hard_gate_focus": [],
            "non_goal": [
                "dependency_selection",
                "framework_selection",
                "runtime_dependency_binding",
                "runtime_evidence",
                "python_code_lint_execution",
            ],
        },
        "enforcement_decision": "pass",
        "execution_owner_hint": "specialized skill or repo-local contract",
    })
    return 0
