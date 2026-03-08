#!/usr/bin/env python3
"""Map changed files to impacted L-layer governance docs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

import mstg_yaml as yaml

LAYER_TO_DOC = {
    0: "L0/README.md",
    1: "L1/README.md",
    2: "L2/README.md",
    3: "L3/README.md",
    4: "L4/README.md",
    5: "L5/README.md",
    6: "L6/README.md",
    7: "L7/README.md",
    8: "L8/README.md",
    9: "L9/README.md",
    10: "L10/README.md",
    11: "L11/README.md",
    12: "L12/README.md",
    13: "L13/README.md",
}
ANCHOR_PATH_FIELDS = ["script_anchor_refs", "asset_anchor_refs", "evidence_anchor_refs", "code_mapping_refs"]

RULES: list[tuple[re.Pattern[str], list[int], str]] = [
    (re.compile(r"^docs/L1/chains/.*\.md$"), [1, 2, 13], "l1_chain_doc"),
    (re.compile(r"^docs/L2/chains/.*/README\.md$"), [2, 13], "l2_chain_doc"),
    (re.compile(r"^scripts/.*lint.*\.py$"), [9, 12, 13], "lint_or_gate_script"),
    (re.compile(r"^scripts/.*writeback.*\.py$"), [6, 8, 10, 11, 13], "writeback_script"),
    (re.compile(r"^scripts/.*apply.*change.*\.py$"), [6, 10, 11, 12, 13], "governed_apply_change_script"),
    (re.compile(r"^scripts/.*context.*backfill.*\.py$"), [1, 2, 3, 6, 10, 11, 13], "context_backfill_script"),
    (re.compile(r"^scripts/.*registry.*\.py$"), [1, 3, 11, 12], "registry_script"),
    (re.compile(r"^scripts/.*audit.*\.py$"), [8, 10, 11, 12], "audit_observability_script"),
    (re.compile(r"^scripts/.*docs.*\.py$"), [0, 1, 5, 10], "docs_structured_script"),
    (re.compile(r"^scripts/.*shared.*runtime.*\.py$"), [3, 4, 11], "shared_runtime_script"),
    (re.compile(r"^runtime/TOOL_REGISTRY\.yaml$"), [1, 2, 6], "tool_registry"),
    (re.compile(r"^runtime/TOOL_DOCS_STRUCTURED\.yaml$"), [0, 1, 5, 10], "structured_docs"),
    (re.compile(r"^runtime/TOOL_CHANGE_LEDGER\.jsonl$"), [10, 11, 13], "change_ledger"),
    (re.compile(r"^assets/schemas/.*"), [2, 6, 12], "schema_assets"),
    (re.compile(r"^references/shared_tooling_runtime_contract\.yaml$"), [3, 4], "shared_runtime_contract"),
]


def read_paths(path_file: Path | None, inline_paths: list[str]) -> list[str]:
    rows = [p.strip().replace("\\", "/") for p in inline_paths if p.strip()]
    if path_file is not None and path_file.is_file():
        rows.extend([line.strip().replace("\\", "/") for line in path_file.read_text(encoding="utf-8").splitlines() if line.strip()])
    return rows


def infer_target_skill_dir(instance_root: Path) -> Path:
    if len(instance_root.parents) < 2:
        return instance_root
    parent_name = instance_root.parent.name
    if parent_name in {"tooling_governance", "governance_instance"}:
        return instance_root.parents[1]
    return instance_root.parents[1]


def normalize_path_token(path_value: str) -> str:
    token = str(path_value or "").strip().replace("\\", "/")
    token = token.split("#", 1)[0].strip()
    while token.startswith("./"):
        token = token[2:]
    return token


def normalize_changed_path(raw: str, *, instance_root: Path | None, target_skill_dir: Path | None) -> str:
    token = normalize_path_token(raw)
    if not token:
        return ""

    p = Path(token)
    if p.is_absolute():
        if target_skill_dir is not None:
            try:
                token = p.relative_to(target_skill_dir).as_posix()
                return normalize_path_token(token)
            except Exception:
                pass
        if instance_root is not None:
            try:
                token = p.relative_to(instance_root).as_posix()
                return normalize_path_token(token)
            except Exception:
                pass
        return p.as_posix()
    return token


def extract_machine_map(markdown_text: str) -> dict[str, object] | None:
    m = re.search(r"## Machine Map\s*```yaml\s*(.*?)\s*```", markdown_text, flags=re.S)
    if not m:
        return None
    try:
        payload = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def load_anchor_index(instance_root: Path) -> dict[int, dict[str, set[str]]]:
    docs_dir = instance_root / "docs"
    out: dict[int, dict[str, set[str]]] = {}
    for layer, name in LAYER_TO_DOC.items():
        doc_path = docs_dir / name
        if not doc_path.is_file():
            continue
        mm = extract_machine_map(doc_path.read_text(encoding="utf-8"))
        if not isinstance(mm, dict):
            continue

        field_rows: dict[str, set[str]] = {}
        for field in ANCHOR_PATH_FIELDS:
            raw = mm.get(field)
            if not isinstance(raw, list):
                continue
            values = {normalize_path_token(str(row)) for row in raw if normalize_path_token(str(row))}
            if values:
                field_rows[field] = values
        if field_rows:
            out[layer] = field_rows
    return out


def match_layers(rel_path: str, *, anchor_index: dict[int, dict[str, set[str]]]) -> tuple[list[int], list[str]]:
    layers: set[int] = set()
    reasons: list[str] = []

    for layer, field_rows in anchor_index.items():
        for field, refs in field_rows.items():
            if rel_path in refs:
                layers.add(layer)
                reasons.append(f"machine_map_anchor:{field}")
    if layers:
        return sorted(layers), sorted(set(reasons))

    for pattern, layer_ids, reason in RULES:
        if pattern.search(rel_path):
            layers.update(layer_ids)
            reasons.append(reason)
    if not layers:
        layers.update([0, 13])
        reasons.append("default_boundary_review")
    return sorted(layers), reasons


def aggregate(
    paths: Iterable[str],
    *,
    instance_root: Path | None,
    target_skill_dir: Path | None,
    anchor_index: dict[int, dict[str, set[str]]],
) -> dict[str, object]:
    by_file = []
    all_layers: set[int] = set()
    all_reasons: set[str] = set()

    for raw in paths:
        rel = normalize_changed_path(raw, instance_root=instance_root, target_skill_dir=target_skill_dir)
        if not rel:
            continue
        layers, reasons = match_layers(rel, anchor_index=anchor_index)
        all_layers.update(layers)
        all_reasons.update(reasons)
        by_file.append(
            {
                "path": raw,
                "normalized_path": rel,
                "impact_layers": [f"L{x}" for x in layers],
                "impact_docs": [f"docs/{LAYER_TO_DOC[x]}" for x in layers],
                "reasons": reasons,
            }
        )

    result = {
        "status": "PASS",
        "changed_file_count": len(by_file),
        "impacted_layers": [f"L{x}" for x in sorted(all_layers)],
        "impacted_docs": [f"docs/{LAYER_TO_DOC[x]}" for x in sorted(all_layers)],
        "reasons": sorted(all_reasons),
        "by_file": by_file,
        "mapping_strategy": {
            "machine_map_anchor_first": True,
            "fallback_rules_enabled": True,
            "anchor_layer_count": len(anchor_index),
        },
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Map changed files to impacted L docs")
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--paths-file")
    parser.add_argument("--instance-root", default="")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    path_file = Path(args.paths_file).expanduser().resolve() if args.paths_file else None
    paths = read_paths(path_file, args.path)
    instance_root = Path(args.instance_root).expanduser().resolve() if args.instance_root.strip() else None
    target_skill_dir = infer_target_skill_dir(instance_root) if instance_root is not None else None
    anchor_index = load_anchor_index(instance_root) if instance_root is not None else {}

    result = aggregate(
        paths,
        instance_root=instance_root,
        target_skill_dir=target_skill_dir,
        anchor_index=anchor_index,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
