from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


def split_keywords(raw: str) -> List[str]:
    parts = re.split(r"[,\s;|，；、]+", raw.strip())
    uniq: List[str] = []
    seen = set()
    for part in parts:
        token = part.strip()
        if not token:
            continue
        lowered = token.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        uniq.append(token)
    return uniq


def parse_registry(registry_path: Path) -> Dict[str, List[Dict[str, str]]]:
    sections: Dict[str, List[Dict[str, str]]] = {
        "common_core": [],
        "common_conditional": [],
        "constraints": [],
    }
    current_section = ""
    current_item: Dict[str, str] | None = None
    for line in registry_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith(":") and stripped[:-1] in sections:
            current_section = stripped[:-1]
            current_item = None
            continue
        if not current_section:
            continue
        if stripped.startswith("- anchor_id:"):
            current_item = {"anchor_id": stripped.split(":", 1)[1].strip(), "graph_node": "", "doc": ""}
            sections[current_section].append(current_item)
            continue
        if current_item is None:
            continue
        if stripped.startswith("graph_node:"):
            current_item["graph_node"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("doc:"):
            current_item["doc"] = stripped.split(":", 1)[1].strip()
    return sections


def parse_domain_keywords(graph_path: Path) -> Dict[str, List[str]]:
    domains: Dict[str, List[str]] = {}
    current_domain = ""
    in_keywords = False
    for line in graph_path.read_text(encoding="utf-8").splitlines():
        domain_match = re.match(r"^\s{2}([a-z0-9_]+(?:_domain|_always_on)):\s*$", line)
        if domain_match:
            current_domain = domain_match.group(1)
            domains.setdefault(current_domain, [])
            in_keywords = False
            continue
        if current_domain and re.match(r"^\s{4}keywords:\s*$", line):
            in_keywords = True
            continue
        if not in_keywords:
            continue
        keyword_match = re.match(r"^\s{6}-\s+(.+?)\s*$", line)
        if keyword_match:
            domains[current_domain].append(keyword_match.group(1).strip().strip('"').strip("'"))
            continue
        if line and not line.startswith(" " * 6):
            in_keywords = False
    return domains


def load_machine_records(path: Path) -> Dict[str, Dict[str, object]]:
    records: Dict[str, Dict[str, object]] = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        if not row.strip():
            continue
        obj = json.loads(row)
        record_id = str(obj.get("id", ""))
        if record_id:
            records[record_id] = obj
    return records
