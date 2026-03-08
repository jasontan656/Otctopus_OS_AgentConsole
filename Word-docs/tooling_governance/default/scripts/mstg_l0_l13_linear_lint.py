#!/usr/bin/env python3
"""Lint L0-L13 docs for tooling governance instance.
Supports composite directory layout with strict backbone chain.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import mstg_yaml as yaml

DOC_FILES = [
    "L0/README.md",
    "L1/README.md",
    "L2/README.md",
    "L3/README.md",
    "L4/README.md",
    "L5/README.md",
    "L6/README.md",
    "L7/README.md",
    "L8/README.md",
    "L9/README.md",
    "L10/README.md",
    "L11/README.md",
    "L12/README.md",
    "L13/README.md",
]

MAP_REQUIRED_FIELDS = [
    "layer_id",
    "anchor",
    "dependency",
    "input",
    "output",
    "acceptance",
    "upstream",
    "downstream",
    "decision_control_ref",
    "execution_spec_ref",
    "acceptance_evidence_ref",
    "tool_anchor_refs",
    "script_anchor_refs",
    "asset_anchor_refs",
    "evidence_anchor_refs",
    "code_mapping_refs",
    "path",
]
ANCHOR_LIST_FIELDS = ["tool_anchor_refs", "script_anchor_refs", "asset_anchor_refs", "evidence_anchor_refs"]


def chain_slug(chain_id: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_-]+", "_", chain_id).strip("_").lower()
    return token or "chain"


def extract_machine_map(markdown_text: str) -> dict[str, Any] | None:
    m = re.search(r"## Machine Map\s*```yaml\s*(.*?)\s*```", markdown_text, flags=re.S)
    if not m:
        return None
    try:
        obj = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def expected_upstream(idx: int) -> str:
    return f"L{idx-1}" if idx > 0 else "none"


def expected_downstream(idx: int) -> str:
    return f"L{idx+1}" if idx < 13 else "none"


def normalized_chain_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for row in value:
        token = str(row).strip()
        if token:
            out.append(token)
    return out


def normalized_chain_packets(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    out: dict[str, list[str]] = {}
    for key, packets in value.items():
        chain_id = str(key).strip()
        if not chain_id:
            continue
        if isinstance(packets, list):
            rows = [str(p).strip() for p in packets if str(p).strip()]
        else:
            rows = []
        out[chain_id] = rows
    return out


def normalized_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for row in value:
        token = str(row).strip()
        if token:
            out.append(token)
    return out


def validate_milestone_chain_contract(mm_by_layer: dict[int, dict[str, Any]], errors: list[dict[str, Any]], docs_dir: Path) -> dict[str, Any]:
    l1_path = str(docs_dir / "L1/README.md")
    l2_path = str(docs_dir / "L2/README.md")
    l13_path = str(docs_dir / "L13/README.md")

    l1 = mm_by_layer.get(1)
    l2 = mm_by_layer.get(2)
    l13 = mm_by_layer.get(13)
    if not isinstance(l1, dict) or not isinstance(l2, dict) or not isinstance(l13, dict):
        errors.append(
            {
                "code": "CHAIN_CONTRACT_LAYER_MISSING",
                "path": str(docs_dir),
                "message": "L1/L2/L13 machine maps are required for milestone chain closure lint",
            }
        )
        return {
            "milestone_chain_count": 0,
            "closure_chain_count": 0,
            "chain_contract_valid": False,
        }

    l1_chains = normalized_chain_list(l1.get("milestone_chains"))
    l1_count = l1.get("milestone_chain_count")
    if not isinstance(l1_count, int):
        errors.append(
            {
                "code": "L1_CHAIN_COUNT_INVALID",
                "path": l1_path,
                "message": "milestone_chain_count must be integer",
            }
        )
    if len(l1_chains) == 0:
        errors.append(
            {
                "code": "L1_CHAIN_LIST_EMPTY",
                "path": l1_path,
                "message": "milestone_chains must contain at least one chain",
            }
        )
    if isinstance(l1_count, int) and l1_count != len(l1_chains):
        errors.append(
            {
                "code": "L1_CHAIN_COUNT_MISMATCH",
                "path": l1_path,
                "message": "milestone_chain_count must equal len(milestone_chains)",
                "expected": len(l1_chains),
                "actual": l1_count,
            }
        )

    if len(set(l1_chains)) != len(l1_chains):
        errors.append(
            {
                "code": "L1_CHAIN_DUPLICATE",
                "path": l1_path,
                "message": "milestone_chains contains duplicate chain ids",
                "chains": l1_chains,
            }
        )

    l2_packets = normalized_chain_packets(l2.get("l2_sub_milestone_packets"))
    if not l2_packets:
        errors.append(
            {
                "code": "L2_CHAIN_PACKET_MISSING",
                "path": l2_path,
                "message": "l2_sub_milestone_packets must be a non-empty mapping",
            }
        )

    l2_chain_ids = list(l2_packets.keys())
    missing_in_l2 = [c for c in l1_chains if c not in l2_packets]
    extra_in_l2 = [c for c in l2_chain_ids if c not in l1_chains]
    if missing_in_l2 or extra_in_l2:
        errors.append(
            {
                "code": "L1_L2_CHAIN_SET_MISMATCH",
                "path": l2_path,
                "message": "L2 chain packet keys must match L1 milestone chains",
                "missing_in_l2": missing_in_l2,
                "extra_in_l2": extra_in_l2,
            }
        )

    for chain_id in l1_chains:
        packets = l2_packets.get(chain_id, [])
        if not packets:
            errors.append(
                {
                    "code": "L2_CHAIN_PACKET_EMPTY",
                    "path": l2_path,
                    "message": "each L1 chain must have non-empty L2 packets",
                    "chain_id": chain_id,
                }
            )
        expected_l1_chain_doc = docs_dir / "L1" / "chains" / f"{chain_slug(chain_id)}.md"
        if not expected_l1_chain_doc.is_file():
            errors.append(
                {
                    "code": "L1_CHAIN_DOC_MISSING",
                    "path": str(expected_l1_chain_doc),
                    "message": "each L1 chain must have a dedicated chain doc",
                    "chain_id": chain_id,
                }
            )
        expected_l2_chain_doc = docs_dir / "L2" / "chains" / chain_slug(chain_id) / "README.md"
        if not expected_l2_chain_doc.is_file():
            errors.append(
                {
                    "code": "L2_CHAIN_DOC_MISSING",
                    "path": str(expected_l2_chain_doc),
                    "message": "each L1 chain must have a dedicated L2 chain packet doc",
                    "chain_id": chain_id,
                }
            )

    l1_chain_docs = l1.get("l1_chain_docs")
    if not isinstance(l1_chain_docs, dict):
        errors.append(
            {
                "code": "L1_CHAIN_DOC_MAP_MISSING",
                "path": l1_path,
                "message": "L1 machine map must include l1_chain_docs mapping",
            }
        )
    else:
        for chain_id in l1_chains:
            expected_rel = f"docs/L1/chains/{chain_slug(chain_id)}.md"
            actual_rel = str(l1_chain_docs.get(chain_id, "")).strip()
            if actual_rel != expected_rel:
                errors.append(
                    {
                        "code": "L1_CHAIN_DOC_MAP_MISMATCH",
                        "path": l1_path,
                        "message": "L1 chain doc mapping mismatch",
                        "chain_id": chain_id,
                        "expected": expected_rel,
                        "actual": actual_rel,
                    }
                )

    l2_chain_docs = l2.get("l2_chain_docs")
    if not isinstance(l2_chain_docs, dict):
        errors.append(
            {
                "code": "L2_CHAIN_DOC_MAP_MISSING",
                "path": l2_path,
                "message": "L2 machine map must include l2_chain_docs mapping",
            }
        )
    else:
        for chain_id in l1_chains:
            expected_rel = f"docs/L2/chains/{chain_slug(chain_id)}/README.md"
            actual_rel = str(l2_chain_docs.get(chain_id, "")).strip()
            if actual_rel != expected_rel:
                errors.append(
                    {
                        "code": "L2_CHAIN_DOC_MAP_MISMATCH",
                        "path": l2_path,
                        "message": "L2 chain doc mapping mismatch",
                        "chain_id": chain_id,
                        "expected": expected_rel,
                        "actual": actual_rel,
                    }
                )

    closure = l13.get("milestone_chain_closure")
    if not isinstance(closure, dict):
        errors.append(
            {
                "code": "L13_CHAIN_CLOSURE_MISSING",
                "path": l13_path,
                "message": "milestone_chain_closure is required in L13 machine map",
            }
        )
        return {
            "milestone_chain_count": len(l1_chains),
            "closure_chain_count": 0,
            "chain_contract_valid": False,
        }

    if closure.get("required_final_layer") != "L13":
        errors.append(
            {
                "code": "L13_CHAIN_CLOSURE_TARGET_INVALID",
                "path": l13_path,
                "message": "milestone_chain_closure.required_final_layer must be L13",
                "actual": closure.get("required_final_layer"),
            }
        )

    closure_rows = closure.get("chains")
    if not isinstance(closure_rows, list):
        errors.append(
            {
                "code": "L13_CHAIN_CLOSURE_ROWS_INVALID",
                "path": l13_path,
                "message": "milestone_chain_closure.chains must be a list",
            }
        )
        closure_rows = []

    closure_chain_ids: list[str] = []
    for idx, row in enumerate(closure_rows):
        if not isinstance(row, dict):
            errors.append(
                {
                    "code": "L13_CHAIN_CLOSURE_ROW_INVALID",
                    "path": l13_path,
                    "message": "closure row must be object",
                    "index": idx,
                }
            )
            continue

        chain_id = str(row.get("chain_id", "")).strip()
        if not chain_id:
            errors.append(
                {
                    "code": "L13_CHAIN_ID_MISSING",
                    "path": l13_path,
                    "message": "closure row missing chain_id",
                    "index": idx,
                }
            )
            continue

        closure_chain_ids.append(chain_id)
        if row.get("from_layer") != "L2":
            errors.append(
                {
                    "code": "L13_CHAIN_FROM_LAYER_INVALID",
                    "path": l13_path,
                    "message": "closure from_layer must be L2",
                    "chain_id": chain_id,
                    "actual": row.get("from_layer"),
                }
            )
        if row.get("to_layer") != "L13":
            errors.append(
                {
                    "code": "L13_CHAIN_TO_LAYER_INVALID",
                    "path": l13_path,
                    "message": "closure to_layer must be L13",
                    "chain_id": chain_id,
                    "actual": row.get("to_layer"),
                }
            )

    missing_in_l13 = [c for c in l1_chains if c not in closure_chain_ids]
    extra_in_l13 = [c for c in closure_chain_ids if c not in l1_chains]
    if missing_in_l13 or extra_in_l13:
        errors.append(
            {
                "code": "L1_L13_CHAIN_SET_MISMATCH",
                "path": l13_path,
                "message": "L13 closure chains must match L1 milestone chains",
                "missing_in_l13": missing_in_l13,
                "extra_in_l13": extra_in_l13,
            }
        )

    chain_contract_valid = len([e for e in errors if str(e.get("code", "")).startswith(("L1_", "L2_", "L13_", "CHAIN_"))]) == 0
    return {
        "milestone_chain_count": len(l1_chains),
        "closure_chain_count": len(closure_chain_ids),
        "chain_contract_valid": chain_contract_valid,
    }


def lint(instance_root: Path) -> tuple[bool, dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    index_path = instance_root / "runtime" / "L0_L13_LINEAR_INDEX.yaml"
    if not index_path.is_file():
        errors.append({"code": "MISSING_INDEX", "path": str(index_path), "message": "missing runtime/L0_L13_LINEAR_INDEX.yaml"})
        return False, {"status": "FAIL", "scope": "mstg_linear_l0_l13", "errors": errors}

    try:
        index_obj = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append({"code": "INDEX_PARSE_FAIL", "path": str(index_path), "message": str(exc)})
        return False, {"status": "FAIL", "scope": "mstg_linear_l0_l13", "errors": errors}

    linearity = str(index_obj.get("linearity", "")).strip()
    if linearity not in {"strict", "backbone_strict_composite_docs"}:
        errors.append(
            {
                "code": "INDEX_NOT_STRICT",
                "path": str(index_path),
                "message": "linearity must be strict or backbone_strict_composite_docs",
                "actual": linearity,
            }
        )

    layers = index_obj.get("layers")
    if not isinstance(layers, list) or len(layers) != 14:
        errors.append({"code": "INDEX_LAYERS_INVALID", "path": str(index_path), "message": "layers must contain 14 items"})
        layers = []

    mm_by_layer: dict[int, dict[str, Any]] = {}
    docs_dir = instance_root / "docs"

    for i, name in enumerate(DOC_FILES):
        path = docs_dir / name
        if not path.is_file():
            errors.append({"code": "MISSING_LAYER_DOC", "path": str(path), "message": f"missing docs/{name}"})
            continue

        text = path.read_text(encoding="utf-8")
        if "## Machine Map" not in text:
            errors.append({"code": "MISSING_MACHINE_MAP", "path": str(path), "message": "missing machine map section"})
            continue
        mm = extract_machine_map(text)
        if mm is None:
            errors.append({"code": "MACHINE_MAP_PARSE_FAIL", "path": str(path), "message": "cannot parse machine map yaml"})
            continue

        mm_by_layer[i] = mm
        missing_fields = [k for k in MAP_REQUIRED_FIELDS if k not in mm]
        if missing_fields:
            errors.append({"code": "MACHINE_MAP_MISSING_FIELDS", "path": str(path), "message": "missing required fields", "fields": missing_fields})
            continue

        expected_layer = f"L{i}"
        if mm.get("layer_id") != expected_layer:
            errors.append({"code": "LAYER_ID_MISMATCH", "path": str(path), "message": f"layer_id must be {expected_layer}"})
        if mm.get("upstream") != expected_upstream(i):
            errors.append({"code": "UPSTREAM_MISMATCH", "path": str(path), "message": f"upstream must be {expected_upstream(i)}"})
        if mm.get("downstream") != expected_downstream(i):
            errors.append({"code": "DOWNSTREAM_MISMATCH", "path": str(path), "message": f"downstream must be {expected_downstream(i)}"})
        if mm.get("anchor") != f"l{i}::composite_layer":
            errors.append({"code": "ANCHOR_MISMATCH", "path": str(path), "message": f"anchor must be l{i}::composite_layer"})
        if mm.get("path") != f"docs/{name}":
            errors.append({"code": "PATH_MISMATCH", "path": str(path), "message": f"path must be docs/{name}"})
        for anchor_key in ANCHOR_LIST_FIELDS:
            rows = normalized_str_list(mm.get(anchor_key))
            if not rows:
                errors.append(
                    {
                        "code": "ANCHOR_FIELD_INVALID",
                        "path": str(path),
                        "message": f"{anchor_key} must be non-empty list of strings",
                    }
                )

    if isinstance(layers, list) and len(layers) == 14:
        for i, row in enumerate(layers):
            if not isinstance(row, dict):
                errors.append({"code": "INDEX_ROW_INVALID", "path": str(index_path), "message": f"layers[{i}] must be object"})
                continue
            expected_name = DOC_FILES[i]
            if row.get("layer_id") != f"L{i}":
                errors.append({"code": "INDEX_LAYER_ID_MISMATCH", "path": str(index_path), "message": f"layers[{i}].layer_id mismatch"})
            if row.get("path") != f"docs/{expected_name}":
                errors.append({"code": "INDEX_PATH_MISMATCH", "path": str(index_path), "message": f"layers[{i}].path mismatch"})

    chain_checks = validate_milestone_chain_contract(mm_by_layer, errors, docs_dir)

    ok = len(errors) == 0
    payload = {
        "status": "PASS" if ok else "FAIL",
        "scope": "mstg_linear_l0_l13",
        "errors": errors,
        "checks": {
            "layer_count": 14,
            "index_present": True,
            "error_count": len(errors),
            **chain_checks,
        },
    }
    return ok, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint L0-L13 linear governance docs")
    parser.add_argument("--instance-root", required=True)
    args = parser.parse_args()

    ok, payload = lint(Path(args.instance_root).expanduser().resolve())
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
