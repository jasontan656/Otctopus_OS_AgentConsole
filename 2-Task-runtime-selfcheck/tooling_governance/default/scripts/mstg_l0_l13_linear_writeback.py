#!/usr/bin/env python3
"""Write L0-L13 governance docs in composite directory layout for one instance.
Adapted from Octupos-OS l13_linear_chain_writeback.py with MSTG composite extensions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import mstg_yaml as yaml

from mstg_l0_l13_linear_flow import (
    asset_anchor_refs,
    chain_doc_evidence_refs,
    code_mapping_refs,
    evidence_anchor_refs,
    infer_chain_packets,
    script_anchor_refs,
    tool_anchor_refs,
)
from mstg_l0_l13_linear_layers import (
    layer_specific_map_fields,
    render_dynamic_sections,
    write_composite_governance_artifacts,
)
from mstg_l0_l13_linear_profile import (
    build_toolbox_profile,
    load_registry_tool_catalog,
    load_registry_tool_rows,
)
from mstg_l0_l13_writeback_contracts import (
    ANCHOR_FIELD_KEYS,
    CHAIN_OBJECTIVES,
    STATIC_LAYER_SECTIONS,
)

LAYER_DEFS = [
    (0, "L0 Scope and Identity", "Define target-skill tool-doc backfill scope, ownership, and inventory baseline."),
    (1, "L1 Interface Contract", "Define parent chains for tool-doc maintenance contracts and handoff boundaries."),
    (2, "L2 IO Schema Contract", "Define per-chain tool-doc packets and required usage/modification/development schema."),
    (3, "L3 Dependency Runtime Policy", "Define runtime/dependency policy for tool-doc maintenance scripts."),
    (4, "L4 Secrets and Environment Contract", "Define env/secret contract for tool-doc workflows and scripts."),
    (5, "L5 State and Storage Contract", "Define registry/docs/ledger/state synchronization by tool_id."),
    (6, "L6 Execution and Idempotency Flow", "Define deterministic docs-first update flow for tool evolution."),
    (7, "L7 Failure and Triage Model", "Define tool-doc drift/failure taxonomy and triage ownership."),
    (8, "L8 Observability and Log Policy", "Define observable events and evidence for tool-doc maintenance runs."),
    (9, "L9 Test and Regression Matrix", "Define regression matrix for tool-doc synchronization and gates."),
    (10, "L10 Change Ledger Mapping", "Define ledger obligations for every tool script/doc update."),
    (11, "L11 Operations Runbook", "Define operator runbook for daily tool-doc maintenance and incident handling."),
    (12, "L12 Gates and Lint Controls", "Define mandatory validation gates for tool-doc consistency."),
    (13, "L13 Release and Compatibility", "Define closure evidence proving tool-doc maintenance compatibility."),
]

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

LEGACY_DOC_FILES = [
    "L0_SCOPE_AND_IDENTITY.md",
    "L1_INTERFACE_CONTRACT.md",
    "L2_IO_SCHEMA_CONTRACT.md",
    "L3_DEPENDENCY_RUNTIME_POLICY.md",
    "L4_SECRETS_ENV_CONTRACT.md",
    "L5_STATE_STORAGE_CONTRACT.md",
    "L6_EXECUTION_IDEMPOTENCY_FLOW.md",
    "L7_FAILURE_TRIAGE_MODEL.md",
    "L8_OBSERVABILITY_LOG_POLICY.md",
    "L9_TEST_REGRESSION_MATRIX.md",
    "L10_CHANGE_LEDGER_MAPPING.md",
    "L11_OPERATIONS_RUNBOOK.md",
    "L12_GATES_LINT_CONTROLS.md",
    "L13_RELEASE_COMPATIBILITY.md",
]


def render_layer_doc(
    layer_num: int,
    title: str,
    summary: str,
    managed_skill: str,
    chain_packets: dict[str, list[str]],
    instance_root: Path,
    target_skill_dir: Path | None,
    tool_catalog: dict[str, str],
    toolbox_profile: dict[str, Any],
) -> str:
    prev_layer = f"L{layer_num-1}" if layer_num > 0 else "none"
    next_layer = f"L{layer_num+1}" if layer_num < 13 else "none"
    anchor = f"l{layer_num}::composite_layer"

    registry_tool_ids = set(tool_catalog.keys())
    layer_tool_refs = tool_anchor_refs(layer_num, registry_tool_ids)
    layer_script_refs = script_anchor_refs(layer_num, layer_tool_refs, tool_catalog, instance_root, target_skill_dir)
    layer_asset_refs = asset_anchor_refs(layer_num, instance_root, target_skill_dir)
    layer_evidence_refs = evidence_anchor_refs(layer_num, instance_root, target_skill_dir, DOC_FILES)
    layer_evidence_refs = sorted(set(layer_evidence_refs + chain_doc_evidence_refs(layer_num, chain_packets)))

    map_obj: dict[str, Any] = {
        "layer_id": f"L{layer_num}",
        "anchor": anchor,
        "dependency": [prev_layer] if prev_layer != "none" else [],
        "input": [f"{prev_layer} outputs"] if prev_layer != "none" else ["governance baseline"],
        "output": [f"L{layer_num} tool-doc deliverable", f"handoff package for {next_layer}"],
        "acceptance": [
            "Layer objective can be explained by human and agent",
            "Machine map fields are complete and extractable",
            "Next layer handoff is explicit and deterministic",
        ],
        "upstream": prev_layer,
        "downstream": next_layer,
        "decision_control_ref": "docs/L4/README.md#决策与控制点",
        "execution_spec_ref": "docs/L5/README.md#执行规格",
        "acceptance_evidence_ref": "docs/L13/README.md#验收证据与闭环归档",
        "tool_anchor_refs": layer_tool_refs,
        "script_anchor_refs": layer_script_refs,
        "asset_anchor_refs": layer_asset_refs,
        "evidence_anchor_refs": layer_evidence_refs,
        "code_mapping_refs": code_mapping_refs(layer_script_refs, layer_asset_refs),
        "path": f"docs/{DOC_FILES[layer_num]}",
    }
    map_obj.update(
        layer_specific_map_fields(
            layer_num,
            chain_packets,
            ANCHOR_FIELD_KEYS,
            DOC_FILES,
            tool_catalog,
            toolbox_profile,
        )
    )

    lines = [
        f"# L{layer_num} Tooling Documentation Layer: {title}",
        "",
        "## Layer Intent",
        f"{summary}",
        "",
        "## Managed Skill Context",
        f"- managed_skill: `{managed_skill}`",
        f"- layer_id: `L{layer_num}`",
        f"- layer_anchor: `{anchor}`",
        "",
        "## Detailed Narrative",
        f"L{layer_num} must convert upstream constraints into downstream executable tool documentation statements.",
        "This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.",
        "",
    ]

    lines.extend(
        render_dynamic_sections(
            layer_num,
            chain_packets,
            CHAIN_OBJECTIVES,
            STATIC_LAYER_SECTIONS,
            tool_catalog,
            toolbox_profile,
        )
    )

    lines.extend(
        [
            "## 上下游映射（what comes next and why）",
            f"- 上游来源: `{prev_layer}`",
            f"- 下游去向: `{next_layer}`",
            f"- 下一步是什么: 把 L{layer_num} 的输出交给 `{next_layer}`，保持目录化链路可审计。",
            "",
            "## Machine Map",
            "```yaml",
            yaml.safe_dump(map_obj, allow_unicode=True, sort_keys=False).rstrip("\n"),
            "```",
            "",
        ]
    )

    return "\n".join(lines)


def write_linear_chain(
    instance_root: Path,
    managed_skill: str,
    target_skill_dir: Path | None,
    chain_spec_file: Path | None,
    chain_infer_mode: str,
) -> dict[str, Any]:
    docs_dir = instance_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    runtime_dir = instance_root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    legacy_docs_removed: list[str] = []

    for legacy_name in LEGACY_DOC_FILES:
        legacy_path = docs_dir / legacy_name
        if legacy_path.is_file():
            legacy_path.unlink()
            legacy_docs_removed.append(str(legacy_path))

    chain_packets, chain_source = infer_chain_packets(
        instance_root=instance_root,
        target_skill_dir=target_skill_dir,
        managed_skill=managed_skill,
        chain_spec_file=chain_spec_file,
        chain_infer_mode=chain_infer_mode,
    )
    tool_rows = load_registry_tool_rows(instance_root)
    tool_catalog = {row["tool_id"]: row["entrypoint"] for row in tool_rows}
    if not tool_catalog:
        tool_catalog = load_registry_tool_catalog(instance_root)
    if not tool_rows and tool_catalog:
        tool_rows = [
            {
                "tool_id": tool_id,
                "entrypoint": entrypoint,
                "owner": managed_skill,
                "status": "active",
                "domain": "unknown",
            }
            for tool_id, entrypoint in sorted(tool_catalog.items())
        ]
    toolbox_profile = build_toolbox_profile(instance_root, managed_skill, tool_rows)
    composite = write_composite_governance_artifacts(
        instance_root=instance_root,
        managed_skill=managed_skill,
        chain_packets=chain_packets,
        chain_objectives=CHAIN_OBJECTIVES,
        tool_catalog=tool_catalog,
    )

    written_docs: list[str] = []
    layers: list[dict[str, Any]] = []

    for n, title, summary in LAYER_DEFS:
        path = docs_dir / DOC_FILES[n]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            render_layer_doc(
                n,
                title,
                summary,
                managed_skill,
                chain_packets,
                instance_root,
                target_skill_dir,
                tool_catalog,
                toolbox_profile,
            ),
            encoding="utf-8",
        )
        written_docs.append(str(path))
        layers.append(
            {
                "layer_id": f"L{n}",
                "path": f"docs/{DOC_FILES[n]}",
                "upstream": f"L{n-1}" if n > 0 else "none",
                "downstream": f"L{n+1}" if n < 13 else "none",
                "anchor": f"l{n}::composite_layer",
            }
        )

    index = {
        "schema_version": "mstg_l0_l13_composite_chain_v2",
        "managed_skill": managed_skill,
        "layer_count": 14,
        "linearity": "backbone_strict_composite_docs",
        "docs_layout": "composite_directory",
        "l1_l2_chain_doc_strategy": "split_per_chain",
        "milestone_chain_count": len(chain_packets),
        "milestone_chains": list(chain_packets.keys()),
        "milestone_chain_source": chain_source,
        "milestone_chain_closure_target": "L13",
        "layers": layers,
    }
    index_path = runtime_dir / "L0_L13_LINEAR_INDEX.yaml"
    index_path.write_text(yaml.safe_dump(index, allow_unicode=True, sort_keys=False), encoding="utf-8")

    return {
        "status": "PASS",
        "layer_count": 14,
        "milestone_chain_count": len(chain_packets),
        "milestone_chains": list(chain_packets.keys()),
        "milestone_chain_source": chain_source,
        "tool_count": toolbox_profile.get("tool_count", 0),
        "toolbox_scripts_dir": toolbox_profile.get("toolbox_scripts_dir", ""),
        "docs_written": written_docs,
        "composite_docs_written": composite.get("docs", []),
        "composite_assets_written": composite.get("assets", []),
        "legacy_docs_removed": legacy_docs_removed,
        "index_path": str(index_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Write L0-L13 linear governance docs")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--managed-skill", default="replace_me")
    parser.add_argument("--target-skill-dir", default="", help="Target skill directory for capability inference")
    parser.add_argument("--chain-spec-file", default="", help="Optional chain spec file (yaml/json)")
    parser.add_argument(
        "--chain-infer-mode",
        default="auto",
        choices=["auto", "existing-first", "baseline"],
        help="auto: spec > existing docs > capability baseline; existing-first: prefer existing docs; baseline: ignore existing docs",
    )
    args = parser.parse_args()

    instance_root = Path(args.instance_root).expanduser().resolve()
    target_skill_dir = Path(args.target_skill_dir).expanduser().resolve() if args.target_skill_dir.strip() else None
    chain_spec_file = Path(args.chain_spec_file).expanduser().resolve() if args.chain_spec_file.strip() else None

    result = write_linear_chain(
        instance_root=instance_root,
        managed_skill=args.managed_skill,
        target_skill_dir=target_skill_dir,
        chain_spec_file=chain_spec_file,
        chain_infer_mode=args.chain_infer_mode,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
