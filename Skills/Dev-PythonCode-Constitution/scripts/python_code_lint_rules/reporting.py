from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from python_code_lint_rules.shared import is_nested_scope_path, is_test_fixture_path


def _default_category(gate: str, reason: str) -> str:
    if gate == "hardcoded_asset_gate":
        return "embedded_multiline_asset"
    if "windows" in reason:
        return "windows_absolute_path_literal"
    if "file_uri" in reason:
        return "file_uri_literal"
    if "escape" in reason:
        return "repo_escape_relative_path"
    if "absolute_paths" in reason or "user_absolute_paths" in reason:
        return "user_absolute_path_literal"
    return reason


def _default_why_flagged(gate: str, reason: str) -> str:
    if gate == "hardcoded_asset_gate":
        return "executable file contains a large inline asset-like block"
    if gate == "absolute_path_gate":
        return "tracked file contains a path literal that violates the repository path policy"
    return f"{gate} flagged this file because it matched rule {reason}"


def _default_suggested_fix(gate: str, path_text: str, issue_kind: str) -> str:
    if issue_kind == "duplicated_vendor_issue":
        return "batch the vendored subtree decision first; avoid fixing each duplicated copy independently"
    if issue_kind == "rule_scope_issue":
        return "check nested assets/tests/references lint scope before editing flagged files"
    if gate == "hardcoded_asset_gate":
        return "move embedded prompt/template content to an external asset or mark intentional fixtures explicitly"
    if gate == "absolute_path_gate":
        return "replace absolute path literals with repo-relative, config-driven, or contract-derived references"
    return "apply the rule-specific remediation without introducing compatibility-only scaffolding"


def _classify_issue_kind(path_text: str) -> str:
    if "gitnexus_core" in path_text:
        return "duplicated_vendor_issue"
    if is_nested_scope_path(path_text):
        return "rule_scope_issue"
    return "real_content_issue"


def _default_cluster_key(gate: str, category: str, reason: str, issue_kind: str) -> str:
    if issue_kind == "duplicated_vendor_issue":
        return f"{gate}:duplicated_vendor:{category}"
    if issue_kind == "rule_scope_issue":
        return f"{gate}:rule_scope:{category}"
    return f"{gate}:{reason}"


def _cluster_pattern(cluster_key: str, category: str) -> str:
    suffix = cluster_key.split(":", 1)[-1]
    return category or suffix.replace(":", "_")


def _shared_root_cause(issue_kind: str, gate: str) -> str:
    if issue_kind == "duplicated_vendor_issue":
        return "same vendored subtree is copied into multiple managed targets, so one underlying pattern fans out into repeated violations"
    if issue_kind == "rule_scope_issue":
        return "nested assets/tests/references under skill directories are being linted as source because skip policy only applies at the repo root"
    if gate == "hardcoded_asset_gate":
        return "real executable files still embed large prompt/template bodies instead of loading them from external assets"
    if gate == "absolute_path_gate":
        return "real tracked files still contain literal absolute filesystem paths that violate repo boundary policy"
    return "source content matches the active lint rule semantics"


def _batch_fix(issue_kind: str, gate: str) -> str:
    if issue_kind == "duplicated_vendor_issue":
        return "decide whether the vendored subtree should stay in lint scope, then batch the surviving fixes across every mirrored copy"
    if issue_kind == "rule_scope_issue":
        return "decide whether nested assets/tests/references should be excluded before editing flagged content"
    if gate == "hardcoded_asset_gate":
        return "externalize embedded prompt/template assets and keep executable files as loaders"
    if gate == "absolute_path_gate":
        return "replace literal absolute paths with repo-relative or runtime-derived references"
    return "apply the matching fix at the narrowest valid source of truth"


def _normalize_line_hits(value: Any) -> list[int]:
    if not isinstance(value, list):
        return []
    hits: list[int] = []
    for item in value:
        if isinstance(item, int) and item not in hits:
            hits.append(item)
    return hits


def _normalize_violation_detail(gate: dict[str, Any], violation: dict[str, Any]) -> dict[str, Any]:
    path_text = str(violation.get("path", ""))
    reason = str(violation.get("reason", "unknown_reason"))
    gate_name = str(gate.get("gate", "unknown_gate"))
    rule_file = str(gate.get("rule_file") or "")
    issue_kind = _classify_issue_kind(path_text)
    category = str(violation.get("category") or _default_category(gate_name, reason))
    cluster_key = str(violation.get("cluster_key") or _default_cluster_key(gate_name, category, reason, issue_kind))
    is_test_fixture = bool(violation.get("is_likely_test_fixture", is_test_fixture_path(path_text)))
    is_embedded_asset = bool(violation.get("is_likely_embedded_asset", gate_name == "hardcoded_asset_gate"))
    is_repo_policy_violation = bool(
        violation.get("is_likely_repo_policy_violation", issue_kind == "real_content_issue" and not is_test_fixture)
    )
    return {
        "gate": gate_name,
        "rule_file": rule_file,
        "path": path_text,
        "reason": reason,
        "category": category,
        "line_hits": _normalize_line_hits(violation.get("line_hits")),
        "matched_text_preview": str(violation.get("matched_text_preview") or ""),
        "why_flagged": str(violation.get("why_flagged") or _default_why_flagged(gate_name, reason)),
        "is_likely_test_fixture": is_test_fixture,
        "is_likely_embedded_asset": is_embedded_asset,
        "is_likely_repo_policy_violation": is_repo_policy_violation,
        "issue_kind": issue_kind,
        "cluster_key": cluster_key,
        "suggested_fix": str(violation.get("suggested_fix") or _default_suggested_fix(gate_name, path_text, issue_kind)),
    }


def _top_patterns(details: list[dict[str, Any]]) -> list[str]:
    counter = Counter(str(detail["category"]) for detail in details if detail.get("category"))
    return [pattern for pattern, _count in counter.most_common(3)]


def _recommended_first_action(gate_name: str, details: list[dict[str, Any]]) -> str:
    if not details:
        return "no action needed"
    issue_kinds = Counter(str(detail["issue_kind"]) for detail in details)
    if issue_kinds["rule_scope_issue"] or issue_kinds["duplicated_vendor_issue"]:
        return "check nested assets/tests/references scope and duplicated vendored copies before editing flagged files"
    if gate_name == "hardcoded_asset_gate":
        return "move real embedded prompt/template bodies out of executable files"
    if gate_name == "absolute_path_gate":
        return "replace real absolute path literals with repo-relative or runtime-derived references"
    return "fix the dominant cluster first instead of editing isolated violations one by one"


def _build_clusters(details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for detail in details:
        grouped[str(detail["cluster_key"])].append(detail)

    clusters: list[dict[str, Any]] = []
    for cluster_key, rows in sorted(grouped.items()):
        sample = rows[0]
        clusters.append(
            {
                "cluster_key": cluster_key,
                "gate": sample["gate"],
                "issue_kind": sample["issue_kind"],
                "pattern": _cluster_pattern(cluster_key, str(sample.get("category") or "")),
                "file_count": len({str(row["path"]) for row in rows}),
                "paths": sorted({str(row["path"]) for row in rows}),
                "shared_root_cause": _shared_root_cause(str(sample["issue_kind"]), str(sample["gate"])),
                "suggested_batch_fix": _batch_fix(str(sample["issue_kind"]), str(sample["gate"])),
            }
        )
    return clusters


def build_report(root: Path, gates: list[dict[str, Any]], rule_files: dict[str, str]) -> dict[str, Any]:
    enriched_gates: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []

    for gate in gates:
        gate_copy = dict(gate)
        gate_name = str(gate_copy.get("gate", ""))
        gate_copy["rule_file"] = gate_copy.get("rule_file") or rule_files.get(gate_name, "")
        gate_copy["violations"] = [dict(violation) for violation in gate_copy.get("violations", [])]
        enriched_gates.append(gate_copy)
        for violation in gate_copy["violations"]:
            details.append(_normalize_violation_detail(gate_copy, violation))

    clusters = _build_clusters(details)
    cluster_by_key = {str(cluster["cluster_key"]): cluster for cluster in clusters}
    for detail in details:
        cluster = cluster_by_key.get(str(detail["cluster_key"]))
        if cluster is not None:
            detail["shared_root_cause"] = cluster["shared_root_cause"]

    gate_diagnostics: list[dict[str, Any]] = []
    details_by_gate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    clusters_by_gate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for detail in details:
        details_by_gate[str(detail["gate"])].append(detail)
    for cluster in clusters:
        clusters_by_gate[str(cluster["gate"])].append(cluster)

    for gate in enriched_gates:
        gate_name = str(gate["gate"])
        gate_details = details_by_gate.get(gate_name, [])
        gate_clusters = clusters_by_gate.get(gate_name, [])
        gate_diagnostics.append(
            {
                "gate": gate_name,
                "status": gate["status"],
                "checked": gate["checked"],
                "violation_count": len(gate_details),
                "deduped_cluster_count": len(gate_clusters),
                "dominant_patterns": _top_patterns(gate_details),
                "recommended_first_action": _recommended_first_action(gate_name, gate_details),
                "rule_file": gate.get("rule_file") or "",
            }
        )

    cluster_issue_kinds = Counter(str(cluster["issue_kind"]) for cluster in clusters)
    failed = [gate for gate in enriched_gates if gate["status"] != "pass"]
    summary_enhanced = {
        "failed_gate_count": len(failed),
        "total_violation_count": len(details),
        "deduped_issue_count": len(clusters),
        "likely_rule_scope_issues": cluster_issue_kinds["rule_scope_issue"],
        "likely_real_code_issues": cluster_issue_kinds["real_content_issue"],
        "likely_duplicated_vendor_issues": cluster_issue_kinds["duplicated_vendor_issue"],
    }

    return {
        "target": str(root),
        "gates": enriched_gates,
        "summary": {"total": len(enriched_gates), "failed": len(failed), "passed": len(enriched_gates) - len(failed)},
        "summary_enhanced": summary_enhanced,
        "gate_diagnostics": gate_diagnostics,
        "violation_details": details,
        "clusters": clusters,
    }
