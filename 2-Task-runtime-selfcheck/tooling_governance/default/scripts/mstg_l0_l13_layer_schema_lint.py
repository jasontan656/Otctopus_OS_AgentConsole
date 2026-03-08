#!/usr/bin/env python3
"""Lint L0-L13 layer schema completeness for governance instance.
Adapted from Octupos-OS l0_l13_layer_schema_lint.py.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import mstg_yaml as yaml

DOC_FILES = {
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

BASE_REQUIRED_MAP_KEYS = [
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

LAYER_REQUIRED_SECTIONS: dict[int, list[str]] = {
    4: ["## 决策与控制点"],
    5: ["## 执行规格"],
    6: ["## 接口与数据契约"],
    7: ["## 文件与资产映射"],
    8: ["## 实施切片与写入计划"],
    9: ["## 测试与 Hazard 覆盖"],
    10: ["## 部署与回滚门禁"],
    11: ["## 运行与审计 Runbook"],
    12: ["## 运营策略与例外处理"],
    13: ["## 验收证据与闭环归档", "## 代码落地映射"],
}

LAYER_REQUIRED_MAP_KEYS: dict[int, list[str]] = {
    4: ["decision_gates"],
    5: ["execution_contracts"],
    6: ["interface_contracts"],
    7: ["asset_mappings"],
    8: ["write_slices"],
    9: ["test_hazard_matrix"],
    10: ["release_rollback_gates"],
    11: ["runbook_controls"],
    12: ["operation_exceptions"],
    13: ["acceptance_evidence_pack"],
}


def extract_machine_map(markdown_text: str) -> dict[str, Any] | None:
    m = re.search(r"## Machine Map\s*```yaml\s*(.*?)\s*```", markdown_text, flags=re.S)
    if not m:
        return None
    try:
        obj = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def chain_slug(chain_id: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_-]+", "_", chain_id).strip("_").lower()
    return token or "chain"


def normalize_str_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        token = str(item).strip()
        if token:
            out.append(token)
    return out


def parse_tool_registry_ids(path: Path) -> list[str]:
    if not path.is_file():
        return []
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(payload, dict):
        return []
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return []
    out: list[str] = []
    for row in tools:
        if not isinstance(row, dict):
            continue
        tool_id = str(row.get("tool_id", "")).strip()
        if tool_id:
            out.append(tool_id)
    return sorted(set(out))


def infer_target_skill_dir(instance_root: Path) -> Path:
    if len(instance_root.parents) < 2:
        return instance_root
    parent_name = instance_root.parent.name
    if parent_name in {"tooling_governance", "governance_instance"}:
        return instance_root.parents[1]
    return instance_root.parents[1]


def anchor_path_resolvable(instance_root: Path, target_skill_dir: Path, anchor_ref: str) -> bool:
    ref = str(anchor_ref or "").strip()
    if not ref:
        return False
    clean = ref.split("#", 1)[0].strip()
    if not clean:
        return False
    p = Path(clean)
    if p.is_absolute():
        return p.exists()
    if (instance_root / clean).exists():
        return True
    if (target_skill_dir / clean).exists():
        return True
    return False


def lint(instance_root: Path) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    target_skill_dir = infer_target_skill_dir(instance_root)
    tool_registry_path = instance_root / "runtime" / "TOOL_REGISTRY.yaml"
    tool_registry_ids = parse_tool_registry_ids(tool_registry_path)
    checks: dict[str, Any] = {
        "layer_total": 14,
        "doc_found": 0,
        "schema_ok_layers": 0,
        "tool_registry_path": str(tool_registry_path),
        "tool_registry_tool_count": len(tool_registry_ids),
        "anchor_path_checks": 0,
        "anchor_path_resolve_failures": 0,
    }

    if not tool_registry_path.is_file():
        errors.append(
            {
                "code": "TOOL_REGISTRY_MISSING",
                "message": "runtime/TOOL_REGISTRY.yaml missing; cannot verify tool_anchor_refs",
                "path": str(tool_registry_path),
            }
        )

    for i in range(14):
        doc_path = instance_root / "docs" / DOC_FILES[i]
        if not doc_path.is_file():
            errors.append({"code": "LAYER_DOC_MISSING", "message": f"L{i} doc missing", "path": str(doc_path)})
            continue

        checks["doc_found"] += 1
        text = doc_path.read_text(encoding="utf-8")
        mm = extract_machine_map(text)
        if mm is None:
            errors.append({"code": "MACHINE_MAP_PARSE_FAIL", "message": f"L{i} machine map parse failed", "path": str(doc_path)})
            continue

        missing_base = [k for k in BASE_REQUIRED_MAP_KEYS if k not in mm]
        if missing_base:
            errors.append(
                {
                    "code": "MACHINE_MAP_BASE_KEYS_MISSING",
                    "message": f"L{i} missing base keys: {missing_base}",
                    "path": str(doc_path),
                }
            )
            continue

        if mm.get("layer_id") != f"L{i}":
            errors.append({"code": "MACHINE_MAP_LAYER_ID_INVALID", "message": f"L{i} layer_id must be L{i}", "path": str(doc_path)})

        if i == 1:
            chains = normalize_str_list(mm.get("milestone_chains"))
            l1_docs = mm.get("l1_chain_docs")
            if not isinstance(l1_docs, dict):
                errors.append({"code": "L1_CHAIN_DOC_MAP_MISSING", "message": "L1 must include l1_chain_docs mapping", "path": str(doc_path)})
            else:
                for chain_id in chains:
                    expected_rel = f"docs/L1/chains/{chain_slug(chain_id)}.md"
                    actual_rel = str(l1_docs.get(chain_id, "")).strip()
                    if actual_rel != expected_rel:
                        errors.append(
                            {
                                "code": "L1_CHAIN_DOC_MAP_MISMATCH",
                                "message": f"L1 chain doc mapping mismatch for {chain_id}",
                                "path": str(doc_path),
                            }
                        )
                    checks["anchor_path_checks"] += 1
                    if not anchor_path_resolvable(instance_root, target_skill_dir, expected_rel):
                        checks["anchor_path_resolve_failures"] += 1
                        errors.append(
                            {
                                "code": "L1_CHAIN_DOC_PATH_UNRESOLVABLE",
                                "message": f"L1 chain doc path cannot be resolved for {chain_id}",
                                "path": str(doc_path),
                                "anchor_ref": expected_rel,
                            }
                        )

        if i == 2:
            packets = mm.get("l2_sub_milestone_packets")
            chains = list(packets.keys()) if isinstance(packets, dict) else []
            l2_docs = mm.get("l2_chain_docs")
            if not isinstance(l2_docs, dict):
                errors.append({"code": "L2_CHAIN_DOC_MAP_MISSING", "message": "L2 must include l2_chain_docs mapping", "path": str(doc_path)})
            else:
                for chain_id in chains:
                    expected_rel = f"docs/L2/chains/{chain_slug(chain_id)}/README.md"
                    actual_rel = str(l2_docs.get(chain_id, "")).strip()
                    if actual_rel != expected_rel:
                        errors.append(
                            {
                                "code": "L2_CHAIN_DOC_MAP_MISMATCH",
                                "message": f"L2 chain doc mapping mismatch for {chain_id}",
                                "path": str(doc_path),
                            }
                        )
                    checks["anchor_path_checks"] += 1
                    if not anchor_path_resolvable(instance_root, target_skill_dir, expected_rel):
                        checks["anchor_path_resolve_failures"] += 1
                        errors.append(
                            {
                                "code": "L2_CHAIN_DOC_PATH_UNRESOLVABLE",
                                "message": f"L2 chain doc path cannot be resolved for {chain_id}",
                                "path": str(doc_path),
                                "anchor_ref": expected_rel,
                            }
                        )

        for sec in LAYER_REQUIRED_SECTIONS.get(i, []):
            if sec not in text:
                errors.append({"code": "LAYER_SECTION_MISSING", "message": f"L{i} missing section: {sec}", "path": str(doc_path)})

        for key in LAYER_REQUIRED_MAP_KEYS.get(i, []):
            if key not in mm:
                errors.append({"code": "LAYER_MAP_KEY_MISSING", "message": f"L{i} missing map key: {key}", "path": str(doc_path)})
                continue
            if not isinstance(mm.get(key), list) or not mm.get(key):
                errors.append({"code": "LAYER_MAP_KEY_INVALID", "message": f"L{i} map key must be non-empty list: {key}", "path": str(doc_path)})

        for key in ANCHOR_LIST_FIELDS:
            values = normalize_str_list(mm.get(key))
            if not values:
                errors.append(
                    {
                        "code": "ANCHOR_FIELD_INVALID",
                        "message": f"L{i} {key} must be non-empty list of strings",
                        "path": str(doc_path),
                    }
                )
                continue

            if key == "tool_anchor_refs" and tool_registry_ids:
                unknown = [row for row in values if row not in tool_registry_ids]
                if unknown:
                    errors.append(
                        {
                            "code": "TOOL_ANCHOR_UNKNOWN",
                            "message": f"L{i} has unknown tool anchors not present in TOOL_REGISTRY",
                            "path": str(doc_path),
                            "unknown_tool_anchors": unknown,
                        }
                    )

            if key in {"script_anchor_refs", "asset_anchor_refs", "evidence_anchor_refs"}:
                for ref in values:
                    checks["anchor_path_checks"] += 1
                    if not anchor_path_resolvable(instance_root, target_skill_dir, ref):
                        checks["anchor_path_resolve_failures"] += 1
                        errors.append(
                            {
                                "code": "ANCHOR_PATH_UNRESOLVABLE",
                                "message": f"L{i} anchor path cannot be resolved",
                                "path": str(doc_path),
                                "anchor_field": key,
                                "anchor_ref": ref,
                                "instance_root": str(instance_root),
                                "target_skill_dir": str(target_skill_dir),
                            }
                        )

        if not isinstance(mm.get("code_mapping_refs"), list) or not mm.get("code_mapping_refs"):
            errors.append({"code": "CODE_MAPPING_REFS_INVALID", "message": f"L{i} code_mapping_refs must be non-empty list", "path": str(doc_path)})

        checks["schema_ok_layers"] += 1

    status = "PASS" if not errors else "FAIL"
    return {"status": status, "scope": "mstg_l0_l13_layer_schema", "checks": checks, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint L0-L13 layer schema completeness")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    payload = lint(Path(args.instance_root).expanduser().resolve())
    if args.pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0 if payload["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
