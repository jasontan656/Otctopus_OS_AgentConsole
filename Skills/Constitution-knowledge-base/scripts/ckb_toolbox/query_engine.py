from __future__ import annotations

import json
from typing import Dict, List, Tuple

REQUIRED_COMMON_ANCHORS: list[str] = []
REQUIRED_CONSTRAINT_ANCHORS: list[str] = []
REQUIRED_GATES: list[str] = []
MINIMUM_KEYWORD_CONTRACT = {
    "bilingual_required": True,
    "min_keywords": {"zh": 1, "en": 1},
    "enforcement": "block_on_missing",
}


def emit_jsonl(obj: Dict[str, object]) -> None:
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def match_domains(
    zh_terms: List[str],
    en_terms: List[str],
    domain_keywords: Dict[str, List[str]],
) -> List[str]:
    all_terms = [*zh_terms, *en_terms]
    matched: List[str] = []
    for domain, keywords in domain_keywords.items():
        if any(term.lower() in keyword.lower() or keyword.lower() in term.lower() for keyword in keywords for term in all_terms):
            matched.append(domain)
    return matched


def score_record(
    rec: Dict[str, object],
    zh_terms: List[str],
    en_terms: List[str],
    matched_domains: List[str],
) -> Tuple[int, List[str]]:
    bag_en = " ".join(
        [
            str(rec.get("id", "")),
            str(rec.get("domain", "")),
            str(rec.get("title_en", "")),
            " ".join(str(x) for x in rec.get("keywords_en", [])),
            " ".join(str(x) for x in rec.get("must", [])),
            " ".join(str(x) for x in rec.get("forbid", [])),
            " ".join(str(x) for x in rec.get("gate", [])),
        ]
    ).lower()
    bag_zh = " ".join(str(x) for x in rec.get("keywords_zh", []))
    score = 0
    matched_terms: List[str] = []
    for term in en_terms:
        if term.lower() and term.lower() in bag_en:
            score += 2
            matched_terms.append(term)
    for term in zh_terms:
        if term and term in bag_zh:
            score += 2
            matched_terms.append(term)
    if str(rec.get("domain", "")) in matched_domains:
        score += 3
    record_id = str(rec.get("id", "")).lower()
    for term in en_terms:
        if term.lower() and term.lower() in record_id:
            score += 1
    stable: List[str] = []
    seen = set()
    for term in matched_terms:
        lowered = term.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        stable.append(term)
    return score, stable
