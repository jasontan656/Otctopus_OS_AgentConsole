#!/usr/bin/env python3
"""Composite artifact writers for MSTG L0-L13 docs."""

from __future__ import annotations

from pathlib import Path
import re
import shutil

import mstg_yaml as yaml


def chain_objective(chain_id: str, chain_objectives: dict[str, str]) -> str:
    return chain_objectives.get(chain_id, "该链用于目标技能工具文档回填与闭环维护，需在 L2 定义子里程碑并在 L13 验收。")


def chain_slug(chain_id: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_-]+", "_", chain_id).strip("_").lower()
    return token or "chain"


def chain_focus(chain_id: str) -> str:
    focus_map = {
        "chain_tool_inventory_baseline": "工具盘点与分类基线（tool_id/entrypoint/domain/owner）",
        "chain_usage_contract_backfill": "工具使用文档回填（命令、输入、输出、usage锚点）",
        "chain_modification_development_backfill": "工具修改与开发文档回填（workflow、required_docs、development记录）",
        "chain_sync_traceability_closure": "工具文档同步闭环（registry/docs/anchors/ledger/gate）",
        "chain_batch_governance_rollout": "多技能批量工具文档治理与审计同步",
    }
    return focus_map.get(chain_id, "目标技能工具文档维护链")


def _render_chain_map_doc(
    chain_packets: dict[str, list[str]],
    chain_objectives: dict[str, str],
    tool_catalog: dict[str, str],
) -> str:
    tool_ids = sorted(tool_catalog.keys())
    lines = [
        "# Milestone Chain Map",
        "",
        "## Purpose",
        "Provide a chain-oriented surface for target-skill tool documentation backfill and maintenance.",
        "",
        "## Tool Coverage Baseline",
        f"- managed_tool_count: `{len(tool_ids)}`",
        "- source: `runtime/TOOL_REGISTRY.yaml`",
    ]
    if tool_ids:
        lines.append("- managed_tool_ids:")
        for tool_id in tool_ids:
            lines.append(f"  - `{tool_id}`")
    lines.extend(
        [
            "",
            "## Chains",
        ]
    )
    for chain_id, packets in chain_packets.items():
        lines.append(f"- chain_id: `{chain_id}`")
        lines.append(f"- chain_slug: `{chain_slug(chain_id)}`")
        lines.append(f"- tool_doc_focus: {chain_focus(chain_id)}")
        lines.append(f"- l1_doc: `docs/L1/chains/{chain_slug(chain_id)}.md`")
        lines.append(f"- l2_doc: `docs/L2/chains/{chain_slug(chain_id)}/README.md`")
        lines.append(f"- objective: {chain_objective(chain_id, chain_objectives)}")
        lines.append("- packets:")
        for packet in packets:
            lines.append(f"  - `{packet}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_l1_chain_doc(
    chain_id: str,
    chain_objectives: dict[str, str],
    packets: list[str],
    tool_catalog: dict[str, str],
) -> str:
    tool_ids = sorted(tool_catalog.keys())
    lines = [
        f"# L1 Tool-Doc Chain: {chain_id}",
        "",
        "## Objective",
        chain_objective(chain_id, chain_objectives),
        "",
        "## Chain Focus",
        f"- {chain_focus(chain_id)}",
        "",
        "## Ownership",
        f"- chain_id: `{chain_id}`",
        f"- chain_slug: `{chain_slug(chain_id)}`",
        f"- l2_chain_doc: `docs/L2/chains/{chain_slug(chain_id)}/README.md`",
        f"- managed_tool_count: `{len(tool_ids)}`",
        "",
        "## Required Tool Doc Surfaces",
        "- `usage`",
        "- `modification`",
        "- `development`",
        "",
        "## Sub-Milestone Preview",
    ]
    for packet in packets:
        lines.append(f"- `{packet}`")
    lines.append("")
    return "\n".join(lines)


def _render_l2_chain_doc(
    chain_id: str,
    chain_objectives: dict[str, str],
    packets: list[str],
    tool_catalog: dict[str, str],
) -> str:
    tool_ids = sorted(tool_catalog.keys())
    lines = [
        f"# L2 Tool-Doc Packet: {chain_id}",
        "",
        "## Source",
        f"- from_l1: `docs/L1/chains/{chain_slug(chain_id)}.md`",
        f"- chain_id: `{chain_id}`",
        "",
        "## Objective",
        chain_objective(chain_id, chain_objectives),
        "",
        "## Tool Coverage",
        f"- managed_tool_count: `{len(tool_ids)}`",
        "- tool_source: `runtime/TOOL_REGISTRY.yaml`",
        "",
        "## Required Tool Doc Sections",
        "- usage: command_examples / inputs / outputs / script_anchor_refs / doc_anchor_refs",
        "- modification: update_workflow / required_docs / sync_contract",
        "- development: owner / self_evolution_requirements / records",
        "",
        "## Packets",
    ]
    for idx, packet in enumerate(packets, start=1):
        lines.append(f"- m{idx}: `{packet}`")
    lines.extend(
        [
            "",
            "## Closure Contract",
            "- final_layer: `L13`",
            "- required_evidence_ref: `docs/L13/README.md#验收证据与闭环归档`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_tool_doc_sync_contract(managed_skill: str) -> str:
    lines = [
        "# Tool Doc Sync Contract",
        "",
        "## Scope",
        f"- managed_skill: `{managed_skill}`",
        "- applies_to: all tools in runtime registry and toolbox scripts",
        "",
        "## Mandatory Rules",
        "- Any self-evolution change must keep script, runtime registry, and structured docs synchronized.",
        "- `runtime/TOOL_DOCS_STRUCTURED.yaml` and `runtime/TOOL_REGISTRY.yaml` must stay tool_id-aligned.",
        "- Machine-map anchors must be updated when script paths, docs paths, or evidence paths change.",
        "- Every material tool evolution must append one traceable entry to `runtime/TOOL_CHANGE_LEDGER.jsonl`.",
        "",
        "## Required Verification",
        "- Run `mstg_l0_l13_full_gate_lint.py` and require PASS.",
        "- Run `mstg_target_governance_outcome_lint.py` and require PASS.",
        "- Confirm outcome lint has zero high-severity violations before release.",
        "",
    ]
    return "\n".join(lines)


def _render_self_evolution_traceability(managed_skill: str) -> str:
    lines = [
        "# Self Evolution Traceability",
        "",
        "## Scope",
        f"- managed_skill: `{managed_skill}`",
        "- objective: ensure every governance evolution is auditable and reproducible.",
        "",
        "## Trace Workflow",
        "- Step 1: update affected docs first (`L0-L13` and composite docs).",
        "- Step 2: update scripts and keep anchors resolvable.",
        "- Step 3: append `runtime/TOOL_CHANGE_LEDGER.jsonl` record with required keys.",
        "- Step 4: run full gate and target outcome lint until PASS.",
        "- Step 5: finalize governance audit timeline with run-id linked closure.",
        "",
        "## Minimum Ledger Fields",
        "- `event_id`",
        "- `timestamp_utc`",
        "- `tool_id`",
        "- `change_type`",
        "- `summary`",
        "",
    ]
    return "\n".join(lines)


def write_composite_governance_artifacts(
    *,
    instance_root: Path,
    managed_skill: str,
    chain_packets: dict[str, list[str]],
    chain_objectives: dict[str, str],
    tool_catalog: dict[str, str],
) -> dict[str, list[str]]:
    docs_root = instance_root / "docs"
    assets_root = instance_root / "assets"
    chains_doc_dir = docs_root / "chains"
    l1_chain_doc_dir = docs_root / "L1" / "chains"
    l2_chain_doc_dir = docs_root / "L2" / "chains"
    tooling_doc_dir = docs_root / "tooling"
    evolution_doc_dir = docs_root / "evolution"
    chains_asset_dir = assets_root / "chains"

    for d in (
        chains_doc_dir,
        l1_chain_doc_dir,
        l2_chain_doc_dir,
        tooling_doc_dir,
        evolution_doc_dir,
        chains_asset_dir,
    ):
        d.mkdir(parents=True, exist_ok=True)

    expected_slugs = {chain_slug(chain_id) for chain_id in chain_packets.keys()}
    for old_doc in l1_chain_doc_dir.glob("*.md"):
        if old_doc.name == "AGENTS.md":
            continue
        if old_doc.stem not in expected_slugs:
            old_doc.unlink()
    for entry in l2_chain_doc_dir.iterdir():
        if entry.name == "AGENTS.md":
            continue
        if entry.is_dir() and entry.name not in expected_slugs:
            shutil.rmtree(entry)
        if entry.is_file() and entry.suffix.lower() == ".md":
            entry.unlink()

    chain_map_path = chains_doc_dir / "MILESTONE_CHAIN_MAP.md"
    chain_map_path.write_text(_render_chain_map_doc(chain_packets, chain_objectives, tool_catalog), encoding="utf-8")

    tooling_sync_path = tooling_doc_dir / "TOOL_DOC_SYNC_CONTRACT.md"
    tooling_sync_path.write_text(_render_tool_doc_sync_contract(managed_skill), encoding="utf-8")

    traceability_path = evolution_doc_dir / "SELF_EVOLUTION_TRACEABILITY.md"
    traceability_path.write_text(_render_self_evolution_traceability(managed_skill), encoding="utf-8")

    chain_asset_path = chains_asset_dir / "milestone_chain_packets.yaml"
    chain_asset_payload = {
        "schema_version": "mstg_milestone_chain_packets_v1",
        "managed_skill": managed_skill,
        "chain_count": len(chain_packets),
        "chains": [
            {
                "chain_id": chain_id,
                "objective": chain_objective(chain_id, chain_objectives),
                "packets": list(packets),
            }
            for chain_id, packets in chain_packets.items()
        ],
    }
    chain_asset_path.write_text(yaml.safe_dump(chain_asset_payload, allow_unicode=True, sort_keys=False), encoding="utf-8")

    l1_chain_docs: list[str] = []
    l2_chain_docs: list[str] = []
    for chain_id, packets in chain_packets.items():
        slug = chain_slug(chain_id)
        l1_doc = l1_chain_doc_dir / f"{slug}.md"
        l1_doc.write_text(_render_l1_chain_doc(chain_id, chain_objectives, packets, tool_catalog), encoding="utf-8")
        l1_chain_docs.append(str(l1_doc))

        l2_doc = l2_chain_doc_dir / slug / "README.md"
        l2_doc.parent.mkdir(parents=True, exist_ok=True)
        l2_doc.write_text(_render_l2_chain_doc(chain_id, chain_objectives, packets, tool_catalog), encoding="utf-8")
        l2_chain_docs.append(str(l2_doc))

    return {
        "docs": [
            str(chain_map_path),
            str(tooling_sync_path),
            str(traceability_path),
            *l1_chain_docs,
            *l2_chain_docs,
        ],
        "assets": [str(chain_asset_path)],
    }
