#!/usr/bin/env python3
"""Lint governed target skill outcome against MSTG expected end-state contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from mstg_target_outcome_lint_helpers import (
    DEFAULT_CONTRACT,
    add_violation,
    add_violation_if,
    anchor_path_resolvable,
    detect_runtime_root,
    ensure_list,
    extract_machine_map,
    infer_target_skill_dir,
    load_contract,
    load_yaml,
    parse_jsonl,
    parse_tool_ids,
    resolve_instance_root,
    severity_counts,
    tool_docs_by_id,
)


def chain_slug(chain_id: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(chain_id or "")).strip("_").lower()
    return token or "chain"


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint target governed skill outcome against MSTG contract")
    parser.add_argument("--instance-root", default="")
    parser.add_argument("--target-skill-dir", default="")
    parser.add_argument("--instance-name", default="")
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    violations: list[dict[str, Any]] = []

    instance_root: Path | None = None
    target_skill_dir: Path | None = None

    if args.instance_root.strip():
        instance_root = Path(args.instance_root).expanduser().resolve()
        if not instance_root.is_dir():
            out = {
                "status": "FAIL",
                "error": "INSTANCE_ROOT_NOT_FOUND",
                "instance_root": str(instance_root),
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        target_skill_dir = (
            Path(args.target_skill_dir).expanduser().resolve()
            if args.target_skill_dir.strip()
            else infer_target_skill_dir(instance_root)
        )
    else:
        if not args.target_skill_dir.strip():
            out = {
                "status": "FAIL",
                "error": "INSTANCE_ROOT_OR_TARGET_SKILL_DIR_REQUIRED",
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        target_skill_dir = Path(args.target_skill_dir).expanduser().resolve()
        if not target_skill_dir.is_dir():
            out = {
                "status": "FAIL",
                "error": "TARGET_SKILL_DIR_NOT_FOUND",
                "target_skill_dir": str(target_skill_dir),
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        resolved = resolve_instance_root(target_skill_dir, args.instance_name.strip() or "default")
        if resolved is None:
            out = {
                "status": "FAIL",
                "error": "INSTANCE_ROOT_NOT_FOUND_UNDER_TARGET",
                "target_skill_dir": str(target_skill_dir),
                "instance_name": args.instance_name.strip() or "default",
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        instance_root = resolved

    assert instance_root is not None
    assert target_skill_dir is not None

    instance_name = args.instance_name.strip() or instance_root.name
    target_skill = target_skill_dir.name
    self_mode = instance_root.name == "self" and instance_root.parent.name == "governance_instance"
    contract_path = Path(args.contract).expanduser().resolve()
    contract = load_contract(contract_path, instance_name=instance_name, target_skill=target_skill)

    target_surface = contract["required"]["target_skill_surface"]
    required_docs = contract["required"]["instance_required_docs"]
    required_runtime_files = contract["required"]["instance_required_runtime_files"]
    required_scripts = contract["required"]["toolbox_required_scripts"]
    required_machine_map_fields = contract["required"]["machine_map"]["required_fields"]
    required_anchor_fields = contract["required"]["machine_map"]["required_anchor_fields"]
    anchor_path_fields = contract["required"]["machine_map"]["anchor_path_fields"]
    required_sections = contract["required"]["structured_docs"]["required_sections"]
    required_usage_keys = contract["required"]["structured_docs"]["usage_required_keys"]

    min_chars = int(contract["non_empty_rules"]["min_non_ws_chars_per_doc"])
    forbidden_tokens = contract["non_empty_rules"]["forbidden_tokens"]

    trace_rules = contract["traceability_rules"]

    docs_dir = instance_root / "docs"
    runtime_dir = instance_root / "runtime"
    scripts_dir = instance_root / "scripts"

    checks: dict[str, Any] = {
        "target_skill_dir": str(target_skill_dir),
        "instance_root": str(instance_root),
        "instance_name": instance_name,
        "self_mode": self_mode,
        "contract_path": str(contract_path),
        "contract_schema_version": contract.get("schema_version", ""),
        "dir_checks": {
            "docs_dir_exists": docs_dir.is_dir(),
            "runtime_dir_exists": runtime_dir.is_dir(),
            "scripts_dir_exists": scripts_dir.is_dir(),
        },
    }

    add_violation_if(
        violations,
        condition=not docs_dir.is_dir(),
        vid="instance_docs_dir_missing",
        severity="high",
        message="instance docs directory missing",
        evidence=[str(docs_dir)],
    )
    add_violation_if(
        violations,
        condition=not runtime_dir.is_dir(),
        vid="instance_runtime_dir_missing",
        severity="high",
        message="instance runtime directory missing",
        evidence=[str(runtime_dir)],
    )
    add_violation_if(
        violations,
        condition=(not scripts_dir.is_dir() and not self_mode),
        vid="instance_scripts_dir_missing",
        severity="high",
        message="instance scripts directory missing",
        evidence=[str(scripts_dir)],
    )

    skill_md = target_skill_dir / "SKILL.md"
    markers = target_surface["contract_markers"]
    require_skill_md_exists = bool(target_surface["require_skill_md_exists"])
    require_injected_contract_markers = bool(target_surface["require_injected_contract_markers"])
    require_meta_mode_keywords = bool(target_surface["require_meta_mode_keywords_in_target_skill"])
    require_self_maintenance_entry = bool(target_surface.get("require_self_maintenance_entry", False))
    self_maintenance_entry_heading = str(target_surface.get("self_maintenance_entry_heading", "")).strip()
    self_maintenance_entry_required_tokens = ensure_list(target_surface.get("self_maintenance_entry_required_tokens"))
    required_keywords = target_surface["contract_keywords"]

    contract_check: dict[str, Any] = {
        "skill_md": str(skill_md),
        "target_surface_policy": {
            "require_skill_md_exists": require_skill_md_exists,
            "require_injected_contract_markers": require_injected_contract_markers,
            "require_meta_mode_keywords_in_target_skill": require_meta_mode_keywords,
            "require_self_maintenance_entry": require_self_maintenance_entry,
        },
        "markers": {"begin": markers["begin"], "end": markers["end"]},
        "missing_keywords": [],
    }

    if not skill_md.is_file():
        if require_skill_md_exists:
            add_violation(
                violations,
                vid="target_skill_md_missing",
                severity="high",
                message="target SKILL.md missing",
                evidence=[str(skill_md)],
            )
        else:
            contract_check["skipped_reason"] = "target_skill_md_optional_by_contract"
    elif self_mode:
        contract_check["skipped_reason"] = "self_mode_target_skill_surface_not_enforced"
    else:
        text = skill_md.read_text(encoding="utf-8")
        begin = markers["begin"]
        end = markers["end"]
        has_begin = begin in text
        has_end = end in text
        contract_check["has_begin"] = has_begin
        contract_check["has_end"] = has_end

        if not (require_injected_contract_markers or require_meta_mode_keywords):
            contract_check["skipped_reason"] = "target_no_trace_policy_contract_block_not_required"
        else:
            block = text
            if require_injected_contract_markers:
                if not has_begin or not has_end:
                    add_violation(
                        violations,
                        vid="target_contract_markers_missing",
                        severity="high",
                        message="target SKILL.md missing required governance contract markers",
                        evidence=[str(skill_md)],
                    )
                else:
                    block = text.split(begin, 1)[1].split(end, 1)[0]
                    contract_check["contract_block_chars"] = len(block)
                    if len(block.strip()) < 80:
                        add_violation(
                            violations,
                            vid="target_contract_block_too_short",
                            severity="medium",
                            message="required governance contract block is too short",
                            evidence=[str(skill_md)],
                        )

            if require_meta_mode_keywords:
                missing_keywords: list[str] = []
                for kw in required_keywords:
                    if kw and kw not in block:
                        missing_keywords.append(kw)
                contract_check["missing_keywords"] = missing_keywords
                if missing_keywords:
                    add_violation(
                        violations,
                        vid="target_contract_keywords_missing",
                        severity="high",
                        message="target SKILL.md required governance keywords are missing",
                        evidence=missing_keywords,
                    )

        if require_self_maintenance_entry:
            section_contract: dict[str, Any] = {
                "heading": self_maintenance_entry_heading,
                "required_tokens": self_maintenance_entry_required_tokens,
                "has_heading": bool(self_maintenance_entry_heading and self_maintenance_entry_heading in text),
                "missing_tokens": [],
            }
            contract_check["self_maintenance_entry"] = section_contract

            if not section_contract["has_heading"]:
                add_violation(
                    violations,
                    vid="target_self_maintenance_entry_missing",
                    severity="high",
                    message="target SKILL.md missing required self-maintenance entry heading",
                    evidence=[self_maintenance_entry_heading],
                )
            else:
                pattern = re.compile(rf"(?ms)^{re.escape(self_maintenance_entry_heading)}\n.*?(?=^## |\Z)")
                match = pattern.search(text)
                section_text = match.group(0) if match else ""
                missing_tokens = [token for token in self_maintenance_entry_required_tokens if token and token not in section_text]
                section_contract["missing_tokens"] = missing_tokens
                if missing_tokens:
                    add_violation(
                        violations,
                        vid="target_self_maintenance_entry_tokens_missing",
                        severity="high",
                        message="target SKILL.md self-maintenance entry is missing required navigation tokens",
                        evidence=missing_tokens,
                    )

    checks["skill_contract_check"] = contract_check

    missing_docs: list[str] = []
    missing_runtime_files: list[str] = []
    missing_scripts: list[str] = []
    doc_non_empty_failures: list[dict[str, Any]] = []
    machine_map_missing_or_parse_fail: list[str] = []
    machine_map_missing_fields: list[str] = []
    anchor_field_invalid: list[str] = []
    anchor_path_unresolvable: list[str] = []
    tool_anchor_unknown: list[str] = []
    l1_chain_doc_contract_failures: list[str] = []
    l2_chain_doc_contract_failures: list[str] = []
    script_search_roots: list[Path] = []
    if scripts_dir.is_dir():
        script_search_roots.append(scripts_dir)
    fallback_scripts = target_skill_dir / "scripts"
    if self_mode and fallback_scripts.is_dir():
        script_search_roots.append(fallback_scripts)

    reg_path = runtime_dir / "TOOL_REGISTRY.yaml"
    docs_path = runtime_dir / "TOOL_DOCS_STRUCTURED.yaml"
    reg_payload: Any = {}
    reg_parse_error = ""
    if reg_path.is_file():
        try:
            reg_payload = load_yaml(reg_path)
        except Exception as exc:
            reg_payload = {}
            reg_parse_error = str(exc)
    reg_ids = parse_tool_ids(reg_payload)

    for name in required_docs:
        p = docs_dir / name
        if not p.is_file():
            missing_docs.append(str(p))
            continue

        content = p.read_text(encoding="utf-8")
        non_ws_chars = len(re.sub(r"\s+", "", content))
        bad_tokens = [token for token in forbidden_tokens if token and token in content]
        if non_ws_chars < min_chars or bad_tokens:
            doc_non_empty_failures.append(
                {
                    "path": str(p),
                    "non_ws_chars": non_ws_chars,
                    "min_required": min_chars,
                    "forbidden_tokens_found": bad_tokens,
                }
            )

        mm = extract_machine_map(content)
        if not isinstance(mm, dict):
            machine_map_missing_or_parse_fail.append(str(p))
            continue

        missing_fields = [field for field in required_machine_map_fields if field not in mm]
        if missing_fields:
            machine_map_missing_fields.append(f"{name}:missing={missing_fields}")

        for field in required_anchor_fields:
            values = ensure_list(mm.get(field))
            if not values:
                anchor_field_invalid.append(f"{name}:{field}:empty_or_invalid")
                continue

            if field == "tool_anchor_refs" and reg_ids:
                unknown = [token for token in values if token not in reg_ids]
                if unknown:
                    tool_anchor_unknown.append(f"{name}:{field}:unknown={unknown}")

        for field in anchor_path_fields:
            values = ensure_list(mm.get(field))
            if not values:
                continue
            for token in values:
                if not anchor_path_resolvable(token, instance_root=instance_root, target_skill_dir=target_skill_dir):
                    anchor_path_unresolvable.append(f"{name}:{field}:{token}")

        if name == "L1/README.md":
            chains = ensure_list(mm.get("milestone_chains"))
            l1_chain_docs = mm.get("l1_chain_docs")
            if not isinstance(l1_chain_docs, dict):
                l1_chain_doc_contract_failures.append("L1/README.md:l1_chain_docs_missing")
            else:
                for chain_id in chains:
                    expected_rel = f"docs/L1/chains/{chain_slug(chain_id)}.md"
                    actual_rel = str(l1_chain_docs.get(chain_id, "")).strip()
                    if actual_rel != expected_rel:
                        l1_chain_doc_contract_failures.append(
                            f"L1/README.md:map_mismatch:{chain_id}:expected={expected_rel}:actual={actual_rel}"
                        )
                    if not anchor_path_resolvable(expected_rel, instance_root=instance_root, target_skill_dir=target_skill_dir):
                        l1_chain_doc_contract_failures.append(f"L1/README.md:path_unresolvable:{expected_rel}")

        if name == "L2/README.md":
            packets = mm.get("l2_sub_milestone_packets")
            chain_ids = sorted(list(packets.keys())) if isinstance(packets, dict) else []
            l2_chain_docs = mm.get("l2_chain_docs")
            if not isinstance(l2_chain_docs, dict):
                l2_chain_doc_contract_failures.append("L2/README.md:l2_chain_docs_missing")
            else:
                for chain_id in chain_ids:
                    expected_rel = f"docs/L2/chains/{chain_slug(chain_id)}/README.md"
                    actual_rel = str(l2_chain_docs.get(chain_id, "")).strip()
                    if actual_rel != expected_rel:
                        l2_chain_doc_contract_failures.append(
                            f"L2/README.md:map_mismatch:{chain_id}:expected={expected_rel}:actual={actual_rel}"
                        )
                    if not anchor_path_resolvable(expected_rel, instance_root=instance_root, target_skill_dir=target_skill_dir):
                        l2_chain_doc_contract_failures.append(f"L2/README.md:path_unresolvable:{expected_rel}")

    for name in required_runtime_files:
        p = runtime_dir / name
        if not p.is_file():
            missing_runtime_files.append(str(p))

    for name in required_scripts:
        found = False
        for root in script_search_roots:
            if (root / name).is_file():
                found = True
                break
        if not found:
            missing_scripts.append(name)

    add_violation_if(
        violations,
        condition=bool(missing_docs),
        vid="required_docs_missing",
        severity="high",
        message="required L0-L13 docs are missing",
        evidence=missing_docs,
    )
    add_violation_if(
        violations,
        condition=bool(missing_runtime_files),
        vid="required_runtime_files_missing",
        severity="high",
        message="required runtime files are missing",
        evidence=missing_runtime_files,
    )
    add_violation_if(
        violations,
        condition=bool(missing_scripts),
        vid="required_toolbox_scripts_missing",
        severity="high",
        message="required injected governance toolbox scripts are missing",
        evidence=[f"missing={name}" for name in missing_scripts],
    )
    add_violation_if(
        violations,
        condition=bool(doc_non_empty_failures),
        vid="docs_non_empty_contract_failed",
        severity="high",
        message="one or more docs are too short or still contain forbidden placeholder tokens",
        evidence=[json.dumps(x, ensure_ascii=False) for x in doc_non_empty_failures],
    )
    add_violation_if(
        violations,
        condition=bool(machine_map_missing_or_parse_fail),
        vid="docs_machine_map_missing_or_parse_fail",
        severity="high",
        message="one or more docs are missing machine map section or machine map yaml is not parseable",
        evidence=machine_map_missing_or_parse_fail,
    )
    add_violation_if(
        violations,
        condition=bool(machine_map_missing_fields),
        vid="docs_machine_map_required_fields_missing",
        severity="high",
        message="one or more docs miss required machine map fields",
        evidence=machine_map_missing_fields[:80],
    )
    add_violation_if(
        violations,
        condition=bool(anchor_field_invalid),
        vid="docs_machine_map_anchor_fields_invalid",
        severity="high",
        message="one or more docs have empty/invalid anchor fields in machine map",
        evidence=anchor_field_invalid[:80],
    )
    add_violation_if(
        violations,
        condition=bool(anchor_path_unresolvable),
        vid="docs_machine_map_anchor_paths_unresolvable",
        severity="high",
        message="one or more anchor refs cannot be resolved from instance root or target skill root",
        evidence=anchor_path_unresolvable[:80],
    )
    add_violation_if(
        violations,
        condition=bool(tool_anchor_unknown),
        vid="docs_machine_map_tool_anchor_unknown",
        severity="high",
        message="one or more tool_anchor_refs are not present in TOOL_REGISTRY",
        evidence=tool_anchor_unknown[:80],
    )
    add_violation_if(
        violations,
        condition=bool(l1_chain_doc_contract_failures),
        vid="l1_chain_doc_contract_failed",
        severity="high",
        message="L1 chain document contract failed (one parent chain per doc under docs/L1/chains)",
        evidence=l1_chain_doc_contract_failures[:80],
    )
    add_violation_if(
        violations,
        condition=bool(l2_chain_doc_contract_failures),
        vid="l2_chain_doc_contract_failed",
        severity="high",
        message="L2 chain packet contract failed (one L2 packet doc per L1 chain under docs/L2/chains)",
        evidence=l2_chain_doc_contract_failures[:80],
    )
    add_violation_if(
        violations,
        condition=bool(reg_parse_error),
        vid="tool_registry_parse_failed",
        severity="high",
        message="TOOL_REGISTRY.yaml parse failed; tool_anchor_refs validation is unreliable",
        evidence=[reg_parse_error],
    )

    checks["instance_files_check"] = {
        "missing_docs": missing_docs,
        "missing_runtime_files": missing_runtime_files,
        "missing_scripts": missing_scripts,
        "script_search_roots": [str(p) for p in script_search_roots],
        "doc_non_empty_failures": doc_non_empty_failures,
        "required_machine_map_fields": required_machine_map_fields,
        "required_anchor_fields": required_anchor_fields,
        "anchor_path_fields": anchor_path_fields,
        "machine_map_missing_or_parse_fail": machine_map_missing_or_parse_fail,
        "machine_map_missing_fields": machine_map_missing_fields,
        "anchor_field_invalid": anchor_field_invalid,
        "anchor_path_unresolvable": anchor_path_unresolvable,
        "tool_anchor_unknown": tool_anchor_unknown,
        "l1_chain_doc_contract_failures": l1_chain_doc_contract_failures,
        "l2_chain_doc_contract_failures": l2_chain_doc_contract_failures,
        "tool_registry_parse_error": reg_parse_error,
    }

    structured_check: dict[str, Any] = {
        "registry_tool_count": 0,
        "docs_tool_count": 0,
        "registry_only": [],
        "docs_only": [],
        "section_violations": [],
    }

    if reg_path.is_file() and docs_path.is_file():
        docs_payload = load_yaml(docs_path)
        docs_ids = parse_tool_ids(docs_payload)
        docs_rows = tool_docs_by_id(docs_payload)

        registry_only = sorted(set(reg_ids) - set(docs_ids))
        docs_only = sorted(set(docs_ids) - set(reg_ids))

        structured_check.update(
            {
                "registry_tool_count": len(reg_ids),
                "docs_tool_count": len(docs_ids),
                "registry_only": registry_only,
                "docs_only": docs_only,
            }
        )

        add_violation_if(
            violations,
            condition=bool(registry_only or docs_only),
            vid="tool_registry_structured_docs_out_of_sync",
            severity="high",
            message="TOOL_REGISTRY and TOOL_DOCS_STRUCTURED tool_id sets differ",
            evidence=[f"registry_only={registry_only}", f"docs_only={docs_only}"],
        )

        section_violations: list[str] = []
        for tid in reg_ids:
            row = docs_rows.get(tid)
            if row is None:
                section_violations.append(f"{tid}:missing_tool_row")
                continue

            for section in required_sections:
                if not isinstance(row.get(section), dict):
                    section_violations.append(f"{tid}:missing_section:{section}")

            usage = row.get("usage", {}) if isinstance(row.get("usage"), dict) else {}
            for key in required_usage_keys:
                val = usage.get(key)
                if key == "summary":
                    if not str(val or "").strip():
                        section_violations.append(f"{tid}:usage.summary.empty")
                elif key in {"command_examples", "inputs", "outputs"}:
                    if not isinstance(val, list) or not [str(x).strip() for x in val if str(x).strip()]:
                        section_violations.append(f"{tid}:usage.{key}.empty")
                elif val is None:
                    section_violations.append(f"{tid}:usage.{key}.missing")

            for token in forbidden_tokens:
                if not token:
                    continue
                summary = str((usage or {}).get("summary", ""))
                if token in summary:
                    section_violations.append(f"{tid}:usage.summary.contains:{token}")

        structured_check["section_violations"] = section_violations
        add_violation_if(
            violations,
            condition=bool(section_violations),
            vid="structured_docs_sections_incomplete",
            severity="high",
            message="TOOL_DOCS_STRUCTURED has incomplete required sections/fields",
            evidence=section_violations[:80],
        )
    else:
        add_violation(
            violations,
            vid="structured_docs_files_missing",
            severity="high",
            message="TOOL_REGISTRY.yaml or TOOL_DOCS_STRUCTURED.yaml missing for structured validation",
            evidence=[str(reg_path), str(docs_path)],
        )

    checks["structured_docs_check"] = structured_check

    traceability_check: dict[str, Any] = {}

    ledger_path = runtime_dir / "TOOL_CHANGE_LEDGER.jsonl"
    ledger_records, ledger_errors = parse_jsonl(ledger_path)
    traceability_check["tool_change_ledger"] = {
        "path": str(ledger_path),
        "record_count": len(ledger_records),
        "parse_errors": ledger_errors,
    }

    add_violation_if(
        violations,
        condition=(trace_rules["require_nonempty_tool_change_ledger"] and len(ledger_records) == 0),
        vid="tool_change_ledger_empty",
        severity="high",
        message="TOOL_CHANGE_LEDGER.jsonl is empty; governance changes are not traceable",
        evidence=[str(ledger_path)],
    )

    add_violation_if(
        violations,
        condition=(trace_rules["require_valid_jsonl_tool_change_ledger"] and bool(ledger_errors)),
        vid="tool_change_ledger_jsonl_invalid",
        severity="high",
        message="TOOL_CHANGE_LEDGER.jsonl contains invalid JSONL records",
        evidence=ledger_errors[:40],
    )

    required_ledger_keys = trace_rules["required_tool_change_ledger_keys"]
    missing_key_rows: list[str] = []
    for idx, row in enumerate(ledger_records, start=1):
        missing = [k for k in required_ledger_keys if k not in row]
        if missing:
            missing_key_rows.append(f"line={idx}:missing={missing}")
    traceability_check["ledger_missing_key_rows"] = missing_key_rows
    add_violation_if(
        violations,
        condition=bool(missing_key_rows),
        vid="tool_change_ledger_keys_missing",
        severity="high",
        message="TOOL_CHANGE_LEDGER entries missing required keys",
        evidence=missing_key_rows[:40],
    )

    runtime_root = detect_runtime_root()
    audit_dir = runtime_root / "Meta-skills-tooling-governance" / "runtime" / "governance_audit"
    timeline_path = audit_dir / "GOVERNANCE_AUDIT_LOG.jsonl"
    runs_dir = audit_dir / "runs"

    timeline_records, timeline_errors = parse_jsonl(timeline_path)
    traceability_check["governance_audit_timeline"] = {
        "path": str(timeline_path),
        "record_count": len(timeline_records),
        "parse_errors": timeline_errors,
    }

    add_violation_if(
        violations,
        condition=(trace_rules["require_governance_audit_timeline"] and not timeline_path.is_file()),
        vid="governance_audit_timeline_missing",
        severity="high",
        message="governance audit timeline file missing",
        evidence=[str(timeline_path)],
    )

    add_violation_if(
        violations,
        condition=(trace_rules["require_valid_governance_audit_jsonl"] and bool(timeline_errors)),
        vid="governance_audit_timeline_jsonl_invalid",
        severity="high",
        message="governance audit timeline contains invalid JSONL entries",
        evidence=timeline_errors[:40],
    )

    schema_version = trace_rules["governance_audit_event_schema_version"]
    schema_mismatch_rows: list[str] = []
    for idx, row in enumerate(timeline_records, start=1):
        if row.get("schema_version") != schema_version:
            schema_mismatch_rows.append(f"line={idx}:schema_version={row.get('schema_version')}")
    traceability_check["audit_schema_mismatch_rows"] = schema_mismatch_rows
    add_violation_if(
        violations,
        condition=(trace_rules["require_valid_governance_audit_jsonl"] and bool(schema_mismatch_rows)),
        vid="governance_audit_event_schema_mismatch",
        severity="medium",
        message="governance audit timeline has schema_version mismatch rows",
        evidence=schema_mismatch_rows[:40],
    )

    target_trace_found = False
    target_dir_text = str(target_skill_dir)
    for row in timeline_records:
        details = row.get("details") if isinstance(row.get("details"), dict) else {}
        detail_skill = str(details.get("target_skill", "")).strip()
        detail_path = str(details.get("target_path", "")).strip()
        if detail_skill == target_skill or detail_path == target_dir_text:
            target_trace_found = True
            break

    if not target_trace_found and runs_dir.is_dir():
        for p in sorted(runs_dir.glob("*.json")):
            try:
                payload = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            target = payload.get("governance_target") if isinstance(payload.get("governance_target"), dict) else {}
            skill = str(target.get("skill", "")).strip()
            path = str(target.get("path", "")).strip()
            if skill == target_skill or path == target_dir_text:
                target_trace_found = True
                break

    traceability_check["target_trace_found"] = target_trace_found
    add_violation_if(
        violations,
        condition=(trace_rules["require_target_trace_in_governance_audit"] and not target_trace_found),
        vid="governance_audit_target_trace_missing",
        severity="high",
        message="governance audit artifacts do not contain target skill trace",
        evidence=[f"target_skill={target_skill}", f"target_path={target_dir_text}"],
    )

    checks["traceability_check"] = traceability_check

    counts = severity_counts(violations)
    status = "PASS" if not violations else "FAIL"

    payload = {
        "status": status,
        "scope": "mstg_target_governance_outcome",
        "target_skill": target_skill,
        "target_skill_dir": str(target_skill_dir),
        "instance_root": str(instance_root),
        "instance_name": instance_name,
        "checks": checks,
        "violation_counts": {
            "total": len(violations),
            "high": counts["high"],
            "medium": counts["medium"],
            "low": counts["low"],
        },
        "violations": violations,
    }

    if args.pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
