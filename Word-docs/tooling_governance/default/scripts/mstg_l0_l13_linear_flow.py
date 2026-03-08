#!/usr/bin/env python3
"""Chain inference and anchor mapping helpers for MSTG L0-L13 writeback."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import mstg_yaml as yaml

from mstg_l0_l13_linear_layers import chain_slug
from mstg_l0_l13_linear_profile import (
    anchor_path_resolvable,
    extract_machine_map,
    normalize_anchor_token,
    resolve_tool_id,
)
from mstg_l0_l13_writeback_contracts import (
    ANCHOR_ASSET_FALLBACKS,
    ANCHOR_TOOL_FALLBACKS,
    ASSET_TO_LAYERS,
    BASELINE_CHAIN_PACKETS,
    BATCH_ROLLOUT_SIGNAL_FILES,
    DEFAULT_TOOL_TO_SCRIPT,
    EVIDENCE_TO_LAYERS,
    SCRIPT_EXTRA_TO_LAYERS,
    TOOL_TO_LAYERS,
)


def _normalize_packets(raw: Any) -> dict[str, list[str]]:
    if not isinstance(raw, dict):
        return {}
    out: dict[str, list[str]] = {}
    for key, val in raw.items():
        chain_id = str(key).strip()
        if not chain_id:
            continue
        packets: list[str] = []
        if isinstance(val, list):
            for item in val:
                token = str(item).strip()
                if token:
                    packets.append(token)
        if not packets:
            fallback = BASELINE_CHAIN_PACKETS.get(chain_id, [])
            packets = list(fallback) if fallback else ["m1_replace_me"]
        out[chain_id] = packets
    return out


def parse_chain_spec_file(path: Path) -> dict[str, list[str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        if isinstance(data.get("l2_sub_milestone_packets"), dict):
            return _normalize_packets(data.get("l2_sub_milestone_packets"))

        rows = data.get("milestone_chains")
        if isinstance(rows, list):
            packets: dict[str, list[str]] = {}
            for row in rows:
                if not isinstance(row, dict):
                    continue
                chain_id = str(row.get("chain_id", "")).strip()
                if not chain_id:
                    continue
                items = row.get("packets")
                if isinstance(items, list):
                    values = [str(x).strip() for x in items if str(x).strip()]
                else:
                    values = []
                packets[chain_id] = values or list(BASELINE_CHAIN_PACKETS.get(chain_id, ["m1_replace_me"]))
            if packets:
                return packets

        if all(isinstance(v, list) for v in data.values()):
            return _normalize_packets(data)

    return {}


def load_existing_chain_packets(instance_root: Path) -> dict[str, list[str]]:
    l1 = instance_root / "docs" / "L1/README.md"
    l2 = instance_root / "docs" / "L2/README.md"
    if not l1.is_file() or not l2.is_file():
        return {}

    l1_mm = extract_machine_map(l1.read_text(encoding="utf-8"))
    l2_mm = extract_machine_map(l2.read_text(encoding="utf-8"))
    if not isinstance(l1_mm, dict) or not isinstance(l2_mm, dict):
        return {}

    chains = l1_mm.get("milestone_chains")
    packets_obj = l2_mm.get("l2_sub_milestone_packets")
    if not isinstance(chains, list) or not isinstance(packets_obj, dict):
        return {}

    normalized_packets = _normalize_packets(packets_obj)
    ordered: dict[str, list[str]] = {}
    for row in chains:
        chain_id = str(row).strip()
        if not chain_id:
            continue
        packets = normalized_packets.get(chain_id)
        if packets:
            ordered[chain_id] = packets

    if ordered:
        return ordered

    return {}


def is_legacy_governance_chain_packets(packets: dict[str, list[str]]) -> bool:
    if not packets:
        return False
    legacy_signals = {
        "chain_target_skill_governance_delivery",
        "chain_init_governance_instance",
        "chain_incremental_change",
        "chain_self_governance_audit",
    }
    return bool(set(packets.keys()) & legacy_signals)


def has_batch_rollout_signals(target_skill_dir: Path | None, managed_skill: str) -> bool:
    if target_skill_dir is None:
        return managed_skill == "Meta-skills-tooling-governance"
    return managed_skill == "Meta-skills-tooling-governance" or any(
        (target_skill_dir / rel).is_file() for rel in BATCH_ROLLOUT_SIGNAL_FILES
    )


def infer_chain_packets(
    instance_root: Path,
    target_skill_dir: Path | None,
    managed_skill: str,
    chain_spec_file: Path | None,
    chain_infer_mode: str,
) -> tuple[dict[str, list[str]], str]:
    if chain_spec_file is not None:
        spec_packets = parse_chain_spec_file(chain_spec_file)
        if spec_packets:
            return spec_packets, "chain_spec_file"

    if chain_infer_mode in {"auto", "existing-first"}:
        existing = load_existing_chain_packets(instance_root)
        if existing:
            if chain_infer_mode == "auto" and is_legacy_governance_chain_packets(existing):
                pass
            else:
                return existing, "existing_instance_docs"

    packets: dict[str, list[str]] = {
        "chain_tool_inventory_baseline": list(BASELINE_CHAIN_PACKETS["chain_tool_inventory_baseline"]),
        "chain_usage_contract_backfill": list(BASELINE_CHAIN_PACKETS["chain_usage_contract_backfill"]),
        "chain_modification_development_backfill": list(BASELINE_CHAIN_PACKETS["chain_modification_development_backfill"]),
        "chain_sync_traceability_closure": list(BASELINE_CHAIN_PACKETS["chain_sync_traceability_closure"]),
    }
    if has_batch_rollout_signals(target_skill_dir, managed_skill):
        packets["chain_batch_governance_rollout"] = list(BASELINE_CHAIN_PACKETS["chain_batch_governance_rollout"])

    return packets, "capability_inference"


def _select_by_layer(mapping: dict[str, list[int]], layer_num: int) -> list[str]:
    return sorted([key for key, layers in mapping.items() if layer_num in layers])


def tool_anchor_refs(layer_num: int, registry_tool_ids: set[str]) -> list[str]:
    base_rows = _select_by_layer(TOOL_TO_LAYERS, layer_num)
    if not base_rows:
        base_rows = sorted(TOOL_TO_LAYERS.keys())

    if not registry_tool_ids:
        return base_rows

    resolved: list[str] = []
    for base_tool_id in base_rows:
        tool_id = resolve_tool_id(base_tool_id, registry_tool_ids)
        if tool_id:
            resolved.append(tool_id)

    if not resolved:
        for fallback in ANCHOR_TOOL_FALLBACKS:
            if fallback in registry_tool_ids:
                resolved.append(fallback)
                break

    if not resolved and registry_tool_ids:
        resolved.append(sorted(registry_tool_ids)[0])

    return sorted(set(resolved))


def script_anchor_refs(
    layer_num: int,
    tool_ids: list[str],
    tool_catalog: dict[str, str],
    instance_root: Path,
    target_skill_dir: Path | None,
) -> list[str]:
    rows: list[str] = []
    for tool_id in tool_ids:
        script_path = tool_catalog.get(tool_id)
        if script_path:
            rows.append(normalize_anchor_token(script_path))
            continue

        alias = tool_id[3:] if tool_id.startswith("tg_") else tool_id
        default_script = DEFAULT_TOOL_TO_SCRIPT.get(alias)
        if default_script:
            rows.append(normalize_anchor_token(default_script))

    rows.extend(
        normalize_anchor_token(path)
        for path, layers in SCRIPT_EXTRA_TO_LAYERS.items()
        if layer_num in layers
    )

    if not rows:
        rows.extend(normalize_anchor_token(path) for path in tool_catalog.values())
    if not rows:
        rows.extend(normalize_anchor_token(path) for path in DEFAULT_TOOL_TO_SCRIPT.values())

    unique_rows = sorted(set(row for row in rows if row))
    resolved = [row for row in unique_rows if anchor_path_resolvable(row, instance_root, target_skill_dir)]
    return resolved if resolved else unique_rows[:1]


def asset_anchor_refs(layer_num: int, instance_root: Path, target_skill_dir: Path | None) -> list[str]:
    rows = _select_by_layer(ASSET_TO_LAYERS, layer_num)
    if not rows:
        rows = sorted(ASSET_TO_LAYERS.keys())
    rows = [normalize_anchor_token(row) for row in rows if row]
    resolved = [row for row in rows if anchor_path_resolvable(row, instance_root, target_skill_dir)]
    if resolved:
        return sorted(set(resolved))

    fallbacks = [row for row in ANCHOR_ASSET_FALLBACKS if anchor_path_resolvable(row, instance_root, target_skill_dir)]
    return fallbacks if fallbacks else sorted(set(rows))[:1]


def evidence_anchor_refs(
    layer_num: int,
    instance_root: Path,
    target_skill_dir: Path | None,
    doc_files: dict[int, str],
) -> list[str]:
    rows = _select_by_layer(EVIDENCE_TO_LAYERS, layer_num)
    if not rows:
        rows = ["docs/L13/README.md"]
    current_doc = f"docs/{doc_files[layer_num]}"
    if current_doc not in rows:
        rows.append(current_doc)

    rows = [normalize_anchor_token(row) for row in rows if row]
    resolved = [row for row in rows if anchor_path_resolvable(row, instance_root, target_skill_dir)]
    if resolved:
        return sorted(set(resolved))
    return sorted(set(rows))[:1]


def chain_doc_evidence_refs(layer_num: int, chain_packets: dict[str, list[str]]) -> list[str]:
    template_by_layer = {
        1: "docs/L1/chains/{slug}.md",
        2: "docs/L2/chains/{slug}/README.md",
    }
    template = template_by_layer.get(layer_num, "")
    refs = {template.format(slug=chain_slug(chain_id)) for chain_id in chain_packets.keys()} if template else set()
    return sorted(refs)


def code_mapping_refs(script_refs: list[str], asset_refs: list[str]) -> list[str]:
    rows = sorted(set(normalize_anchor_token(x) for x in (script_refs + asset_refs) if x))
    return rows if rows else ["runtime/L0_L13_LINEAR_INDEX.yaml"]
