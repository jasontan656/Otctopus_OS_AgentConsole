from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List

STOP_EN = {"the", "and", "or", "for", "to", "of", "in", "on", "with", "from", "by", "as", "is", "are", "be", "must", "do", "dont", "rule", "rules", "common", "tech", "stack", "constraint", "constraints"}
STOP_ZH = {"必须", "不要", "以及", "通过", "进行", "使用", "输出", "项目", "规则", "约束", "执行", "要求", "全覆盖"}


def anchor_to_title(anchor_id: str) -> str:
    parts = anchor_id.split("_")
    if parts and parts[0] in {"common", "tech", "constraint", "constraints"}:
        parts = parts[1:]
    return " ".join(parts) or anchor_id


def extract_keywords_en(anchor_id: str, graph_node: str, text: str, graph_kws: List[str]) -> List[str]:
    out: List[str] = []
    seen = set()
    def add(token: str) -> None:
        lowered = token.strip().lower()
        if not lowered or len(lowered) < 2 or lowered in STOP_EN or lowered in seen:
            return
        seen.add(lowered)
        out.append(lowered)
    for raw in [anchor_id, graph_node, *graph_kws]:
        for part in re.split(r"[_\-\s/]+", raw):
            add(part)
    for code in re.findall(r"`([A-Za-z0-9_./:-]+)`", text):
        for part in re.split(r"[_\-./:]+", code):
            add(part)
    for word in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{1,40}", text[:6000]):
        for part in re.split(r"[_\-]+", word):
            add(part)
    return out[:24]


def extract_keywords_zh(text: str) -> List[str]:
    counter = Counter()
    for token in re.findall(r"[\u4e00-\u9fff]{2,4}", text[:5000]):
        if token in STOP_ZH:
            continue
        counter[token] += 1
    return [token for token, _ in counter.most_common(12)]


def mechanical_payload(cat: str, anchor_id: str, domain: str, src: str, text: str, graph_kws: List[str]) -> Dict[str, object]:
    is_common_core = cat == "common_core"
    priority = "always_on" if is_common_core else "query_hit"
    cohit = [] if is_common_core else ["common_core_always_on"]
    must = [f"apply_{anchor_id}", "emit_id_cat_domain_src", "emit_keywords_and_gate"]
    must.insert(1, "always_attach_on_query" if is_common_core else "attach_when_keyword_or_domain_hits" if cat == "common_conditional" else "enforce_block_when_condition_met")
    gate = ["bilingual_keywords_required", "always_on" if is_common_core else "score_gt_0"]
    return {
        "v": "machine_v1",
        "id": anchor_id,
        "cat": cat,
        "domain": domain,
        "priority": priority,
        "cohit": cohit,
        "title_en": anchor_to_title(anchor_id),
        "keywords_en": extract_keywords_en(anchor_id, domain, text, graph_kws),
        "keywords_zh": extract_keywords_zh(text),
        "must": must,
        "forbid": ["no_disk_write", "no_markdown_body_output", "no_non_jsonl_output"],
        "gate": gate,
        "evidence": ["id", "cat", "domain", "src", "score", "matched_terms"],
        "src": src,
    }
