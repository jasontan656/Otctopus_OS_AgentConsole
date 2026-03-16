from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

from mother_doc_contract import (
    MOTHER_DOC_ALLOWED_BRANCH_FAMILIES,
    MOTHER_DOC_ALLOWED_CONTENT_FAMILIES,
    MOTHER_DOC_ALLOWED_DOC_KINDS,
)
from mother_doc_lint_support import mother_doc_lint_summary
from mother_doc_state_support import iter_atomic_markdown_files, parse_frontmatter
from skill_runtime_context import mother_doc_audit_registry_path


class AuditDebt(TypedDict, total=False):
    doc_ref: str
    severity: str
    debt_kind: str
    summary: str
    evidence: list[str]
    recommended_action: str
    suggested_doc_kind: str
    suggested_branch_family_candidates: list[str]
    suggested_content_family_candidates: list[str]
    registry_update_required: bool
    block_further_semantic_read: bool


class ShadowSplitNode(TypedDict, total=False):
    relative_path: str
    thumb_title: str
    doc_kind: str
    branch_family: str
    content_family: str
    focus: str
    registry_update_required: bool


class ShadowSplitProposal(TypedDict, total=False):
    proposal_id: str
    source_doc_ref: str
    source_content_family: str
    source_doc_kind: str
    severity: str
    debt_kinds: list[str]
    matched_registry_rule_id: str
    proposal_mode: str
    target_host_directory: str
    source_rewrite: dict[str, object]
    shadow_tree: dict[str, object]
    decision_basis: list[str]
    registry_update_required: bool
    summary: str


SEMANTIC_SECTION_TITLES = {
    "## 来源",
    "## 当前节点职责",
    "## 当前内容",
    "## 当前规则",
    "## 当前配置",
    "## 当前延伸规则",
    "## 当前延伸边界",
    "## 当前承载边界",
    "## 非目标",
}

FAMILY_CONTRACT_SIGNALS = {
    "overview_narrative": {"## 当前规则", "## 当前配置"},
    "overview_mapping": {"## 当前规则", "## 当前配置"},
}

LINE_LIST_PATTERN = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
TABLE_ROW_PATTERN = re.compile(r"^\|.+\|$")
PATH_SIGNAL_PATTERN = re.compile(r"(?:^|\s)(?:src/|docs/|Skills/|path/|scripts/)")
SEVERITY_ORDER = {
    "blocking": 3,
    "major": 2,
    "minor": 1,
    "observed": 0,
}
SPLIT_DECISION_REGISTRY_PATH = mother_doc_audit_registry_path()


def _detect_mother_doc_root(path: Path) -> tuple[Path, bool]:
    resolved = path.resolve()
    if resolved.is_dir():
        return resolved, False
    if resolved.name == "00_index.md":
        return resolved.parent, False
    return resolved, resolved.name == "mother_doc.md"


def _parse_sections(body: str) -> tuple[dict[str, list[str]], list[str]]:
    sections: dict[str, list[str]] = {}
    h3_headings: list[str] = []
    current_h2: str | None = None
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            current_h2 = stripped
            sections.setdefault(current_h2, [])
            continue
        if stripped.startswith("### "):
            h3_headings.append(stripped)
        if current_h2 is not None:
            sections[current_h2].append(raw_line)
    return sections, h3_headings


def _count_semantic_units(lines: list[str]) -> int:
    count = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if LINE_LIST_PATTERN.match(stripped):
            count += 1
            continue
        if TABLE_ROW_PATTERN.match(stripped):
            count += 1
    return count


def _collect_inline_code_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for item in INLINE_CODE_PATTERN.findall(text):
        token = item.strip()
        if token:
            tokens.add(token)
    return tokens


def _parallel_cluster_hits(text: str) -> list[str]:
    hits: list[str] = []
    for token in _collect_inline_code_tokens(text):
        if len([part for part in re.split(r"\s*/\s*|\s*->\s*", token) if part.strip()]) >= 3:
            hits.append(token)
            continue
        if len(re.findall(r"\b[A-Z]{2,}\b", token)) >= 3:
            hits.append(token)
    return hits


def _family_recommendation(content_family: str) -> tuple[str, str, list[str], list[str]]:
    if content_family in {"overview_narrative", "overview_mapping"}:
        return (
            "horizontal_branch",
            "branch_root",
            ["domain_branch", "decision_branch", "contract_branch"],
            ["branch_overview", "contract_spec_doc"],
        )
    if content_family in {"branch_overview", "layer_taxonomy_root"}:
        return (
            "split_under_registered_family",
            "branch_root",
            ["framework_branch", "contract_branch", "execution_binding_branch"],
            ["branch_overview", "layer_item_doc", "contract_spec_doc"],
        )
    return (
        "support_split",
        "trunk_node",
        ["execution_binding_branch", "contract_branch"],
        ["layer_item_doc", "container_item_doc", "contract_spec_doc"],
    )


def _registry_update_required(
    suggested_doc_kind: str,
    branch_candidates: list[str],
    family_candidates: list[str],
) -> bool:
    if suggested_doc_kind not in MOTHER_DOC_ALLOWED_DOC_KINDS:
        return True
    if any(item not in MOTHER_DOC_ALLOWED_BRANCH_FAMILIES for item in branch_candidates):
        return True
    if any(item not in MOTHER_DOC_ALLOWED_CONTENT_FAMILIES for item in family_candidates):
        return True
    return False


def _build_debt(
    *,
    doc_ref: str,
    severity: str,
    debt_kind: str,
    summary: str,
    evidence: list[str],
    content_family: str,
) -> AuditDebt:
    recommended_action, suggested_doc_kind, branch_candidates, family_candidates = (
        _family_recommendation(content_family)
    )
    return {
        "doc_ref": doc_ref,
        "severity": severity,
        "debt_kind": debt_kind,
        "summary": summary,
        "evidence": evidence,
        "recommended_action": recommended_action,
        "suggested_doc_kind": suggested_doc_kind,
        "suggested_branch_family_candidates": branch_candidates,
        "suggested_content_family_candidates": family_candidates,
        "registry_update_required": _registry_update_required(
            suggested_doc_kind,
            branch_candidates,
            family_candidates,
        ),
        "block_further_semantic_read": severity == "blocking",
    }


@lru_cache(maxsize=1)
def _load_split_decision_registry() -> dict[str, object]:
    if not SPLIT_DECISION_REGISTRY_PATH.exists():
        return {
            "registry_name": "MOTHER_DOC_AUDIT_SPLIT_DECISION_REGISTRY",
            "registry_version": "missing",
            "default_host_strategy": "nested_source_stem_directory",
            "recipes": [],
        }
    return json.loads(SPLIT_DECISION_REGISTRY_PATH.read_text(encoding="utf-8"))


def _select_primary_debt(debts: list[AuditDebt]) -> AuditDebt:
    return sorted(
        debts,
        key=lambda item: (
            -SEVERITY_ORDER[item["severity"]],
            item["debt_kind"],
        ),
    )[0]


def _match_registry_recipe(
    content_family: str,
    debt_kind: str,
    severity: str,
) -> dict[str, object] | None:
    registry = _load_split_decision_registry()
    for recipe in registry.get("recipes", []):
        if not isinstance(recipe, dict):
            continue
        match = recipe.get("match", {})
        if not isinstance(match, dict):
            continue
        content_families = match.get("content_families", [])
        debt_kinds = match.get("debt_kinds", [])
        severities = match.get("severities", [])
        if (
            content_family in content_families
            and debt_kind in debt_kinds
            and severity in severities
        ):
            return recipe
    return None


def _fallback_recipe(primary_debt: AuditDebt, content_family: str) -> dict[str, object]:
    branch_candidates = primary_debt.get("suggested_branch_family_candidates", []) or ["decision_branch"]
    content_candidates = primary_debt.get("suggested_content_family_candidates", []) or ["branch_overview"]
    return {
        "recipe_id": "fallback_generic_split",
        "source_rewrite": {
            "action": "rewrite_source_as_branch_root",
            "doc_kind": primary_debt.get("suggested_doc_kind", "branch_root"),
            "content_family": content_candidates[0],
            "branch_family": branch_candidates[0],
            "rewrite_goal": "收薄当前节点，只保留单一入口语义与下游导航。",
        },
        "shadow_tree": {
            "child_nodes": [
                {
                    "slug": "10_domain_scope",
                    "thumb_title_suffix": "Domain Scope",
                    "doc_kind": "branch_root",
                    "branch_family": branch_candidates[0],
                    "content_family": content_candidates[0],
                    "focus": f"围绕 {content_family} 下沉第一组独立语义。",
                },
                {
                    "slug": "20_contract_surface",
                    "thumb_title_suffix": "Contract Surface",
                    "doc_kind": "contract_doc",
                    "branch_family": "contract_branch",
                    "content_family": "contract_spec_doc",
                    "focus": "抽离规则、配置与稳定边界。",
                },
            ]
        },
    }


def _title_with_suffix(base_title: str, suffix: str) -> str:
    suffix = suffix.strip()
    if not suffix:
        return base_title
    if base_title.endswith(suffix):
        return base_title
    return f"{base_title} {suffix}"


def _build_shadow_split_proposal(
    root: Path,
    file_path: Path,
    metadata: dict[str, object],
    debts: list[AuditDebt],
) -> ShadowSplitProposal | None:
    actionable_debts = [
        item for item in debts if item["severity"] in {"blocking", "major"}
    ]
    if not actionable_debts:
        return None

    primary_debt = _select_primary_debt(actionable_debts)
    relative_doc = str(file_path.relative_to(root))
    source_content_family = str(metadata.get("content_family") or "")
    source_doc_kind = str(metadata.get("doc_kind") or "trunk_node")
    recipe = _match_registry_recipe(
        source_content_family,
        primary_debt["debt_kind"],
        primary_debt["severity"],
    ) or _fallback_recipe(primary_debt, source_content_family)

    source_stem_path = Path(relative_doc).with_suffix("")
    host_directory = str(source_stem_path)
    source_title = str(metadata.get("thumb_title") or source_stem_path.name.replace("_", " ").title())

    source_rewrite = dict(recipe.get("source_rewrite", {}))
    rewrite_branch_family = str(source_rewrite.get("branch_family") or "")
    rewrite_doc_kind = str(source_rewrite.get("doc_kind") or source_doc_kind)
    rewrite_content_family = str(source_rewrite.get("content_family") or source_content_family)

    child_nodes: list[ShadowSplitNode] = []
    registry_update_required = _registry_update_required(
        rewrite_doc_kind,
        [rewrite_branch_family] if rewrite_branch_family else [],
        [rewrite_content_family] if rewrite_content_family else [],
    )
    for child in recipe.get("shadow_tree", {}).get("child_nodes", []):
        if not isinstance(child, dict):
            continue
        relative_path = str(source_stem_path / f"{child['slug']}.md")
        branch_family = str(child.get("branch_family") or "")
        content_family = str(child.get("content_family") or "branch_overview")
        doc_kind = str(child.get("doc_kind") or "branch_root")
        node_registry_update_required = _registry_update_required(
            doc_kind,
            [branch_family] if branch_family else [],
            [content_family] if content_family else [],
        )
        registry_update_required = registry_update_required or node_registry_update_required
        child_nodes.append(
            {
                "relative_path": relative_path,
                "thumb_title": _title_with_suffix(
                    source_title,
                    str(child.get("thumb_title_suffix") or ""),
                ),
                "doc_kind": doc_kind,
                "branch_family": branch_family,
                "content_family": content_family,
                "focus": str(child.get("focus") or ""),
                "registry_update_required": node_registry_update_required,
            }
        )

    debt_kinds = sorted({item["debt_kind"] for item in actionable_debts})
    decision_basis: list[str] = []
    for item in actionable_debts:
        decision_basis.extend(item.get("evidence", []))
    decision_basis = sorted(set(decision_basis))
    proposal_id = hashlib.sha1(
        f"{relative_doc}:{recipe.get('recipe_id', 'fallback')}".encode("utf-8")
    ).hexdigest()[:12]

    return {
        "proposal_id": proposal_id,
        "source_doc_ref": relative_doc,
        "source_content_family": source_content_family,
        "source_doc_kind": source_doc_kind,
        "severity": primary_debt["severity"],
        "debt_kinds": debt_kinds,
        "matched_registry_rule_id": str(recipe.get("recipe_id") or "fallback_generic_split"),
        "proposal_mode": str(primary_debt.get("recommended_action") or "support_split"),
        "target_host_directory": host_directory,
        "source_rewrite": {
            "path": relative_doc,
            "action": str(source_rewrite.get("action") or "rewrite_source_as_branch_root"),
            "target_doc_kind": rewrite_doc_kind,
            "target_content_family": rewrite_content_family,
            "target_branch_family": rewrite_branch_family,
            "rewrite_goal": str(source_rewrite.get("rewrite_goal") or ""),
        },
        "shadow_tree": {
            "root_dir": host_directory,
            "root_index_path": str(source_stem_path / "00_index.md"),
            "host_strategy": _load_split_decision_registry().get(
                "default_host_strategy",
                "nested_source_stem_directory",
            ),
            "child_nodes": child_nodes,
        },
        "decision_basis": decision_basis,
        "registry_update_required": registry_update_required,
        "summary": (
            f"将 {relative_doc} 收薄为单一入口，并在 {host_directory}/ 下生成 shadow 子树，"
            "让后续 mother_doc 写回按 recipe 拆分。"
        ),
    }


def _doc_audit_debts(root: Path, file_path: Path) -> list[AuditDebt]:
    metadata, body, parse_errors = parse_frontmatter(file_path)
    if parse_errors:
        return []

    relative_doc = str(file_path.relative_to(root))
    if metadata.get("doc_role") == "root_index":
        return []

    content_family = str(metadata.get("content_family") or "")
    if not content_family:
        return []

    sections, h3_headings = _parse_sections(body)
    semantic_sections = {key: value for key, value in sections.items() if key in SEMANTIC_SECTION_TITLES}
    semantic_unit_count = sum(_count_semantic_units(lines) for lines in semantic_sections.values())
    extra_h2_titles = [title for title in sections if title not in SEMANTIC_SECTION_TITLES]
    anchors_total = len(metadata.get("anchors_down") or []) + len(metadata.get("anchors_support") or [])
    inline_code_tokens = _collect_inline_code_tokens(body)
    parallel_clusters = _parallel_cluster_hits(body)
    pressure_score = 0
    evidence: list[str] = []

    if semantic_unit_count >= 6:
        pressure_score += 2
        evidence.append(f"semantic_unit_count={semantic_unit_count}")
    elif semantic_unit_count >= 4:
        pressure_score += 1
        evidence.append(f"semantic_unit_count={semantic_unit_count}")

    if len(extra_h2_titles) >= 1:
        pressure_score += 1
        evidence.append(f"extra_h2_titles={extra_h2_titles}")

    if len(h3_headings) >= 3:
        pressure_score += 1
        evidence.append(f"h3_heading_count={len(h3_headings)}")

    if len(inline_code_tokens) >= 6:
        pressure_score += 1
        evidence.append(f"inline_code_token_count={len(inline_code_tokens)}")

    if parallel_clusters:
        pressure_score += 2
        evidence.append(f"parallel_clusters={parallel_clusters}")

    if anchors_total == 0 and pressure_score >= 2:
        pressure_score += 1
        evidence.append("anchor_gap=no_down_or_support_targets")

    debts: list[AuditDebt] = []
    if content_family in FAMILY_CONTRACT_SIGNALS:
        family_signal_hits = [item for item in FAMILY_CONTRACT_SIGNALS[content_family] if item in sections]
        if family_signal_hits:
            debts.append(
                _build_debt(
                    doc_ref=relative_doc,
                    severity="major",
                    debt_kind="family_drift",
                    summary="当前文档使用了更适合下沉为规则/配置分支的结构信号。",
                    evidence=[f"family_signal_hits={family_signal_hits}"],
                    content_family=content_family,
                )
            )
        if PATH_SIGNAL_PATTERN.search(body):
            debts.append(
                _build_debt(
                    doc_ref=relative_doc,
                    severity="major",
                    debt_kind="family_drift",
                    summary="overview 类文档已经开始承载明显路径/实现落点，建议下沉到更外层承载位。",
                    evidence=["path_like_implementation_signal_detected"],
                    content_family=content_family,
                )
            )

    if content_family in {"overview_narrative", "overview_mapping"}:
        if pressure_score >= 4:
            debts.append(
                _build_debt(
                    doc_ref=relative_doc,
                    severity="blocking",
                    debt_kind="semantic_pressure",
                    summary="overview 节点已经承载过多并行语义，继续深读会污染后续 growth 和 impact 判断。",
                    evidence=evidence,
                    content_family=content_family,
                )
            )
        elif pressure_score >= 3:
            debts.append(
                _build_debt(
                    doc_ref=relative_doc,
                    severity="major",
                    debt_kind="semantic_pressure",
                    summary="overview 节点接近饱和，建议先外长分支再继续把它当主语义入口消费。",
                    evidence=evidence,
                    content_family=content_family,
                )
            )
    elif content_family in {"branch_overview", "layer_taxonomy_root", "layer_item_doc", "container_item_doc"}:
        if pressure_score >= 5 and anchors_total == 0:
            debts.append(
                _build_debt(
                    doc_ref=relative_doc,
                    severity="blocking",
                    debt_kind="unexpanded_semantic_cluster",
                    summary="当前节点已经聚集了多个可独立阅读的语义簇，但树上还没有对应承载位。",
                    evidence=evidence,
                    content_family=content_family,
                )
            )
        elif pressure_score >= 4:
            debts.append(
                _build_debt(
                    doc_ref=relative_doc,
                    severity="major",
                    debt_kind="unexpanded_semantic_cluster",
                    summary="当前节点已经出现可继续拆分的平行语义簇，建议优先在已注册家族内外长。",
                    evidence=evidence,
                    content_family=content_family,
                )
            )

    return debts


def mother_doc_audit_summary(path: Path) -> dict:
    root, single_file_input_detected = _detect_mother_doc_root(path)
    lint_summary = mother_doc_lint_summary(root)
    registry = _load_split_decision_registry()
    registry_summary = {
        "path": str(SPLIT_DECISION_REGISTRY_PATH),
        "registry_name": registry.get("registry_name"),
        "registry_version": registry.get("registry_version"),
        "recipe_count": len(registry.get("recipes", [])),
    }
    if single_file_input_detected or not root.exists():
        return {
            "path": str(path),
            "resolved_root": str(root),
            "status": "fail",
            "lint_status": lint_summary["status"],
            "audit_gate_allowed": False,
            "reason": "mother_doc_root_not_ready",
            "lint_summary": lint_summary,
            "blocking_debts": [],
            "major_debts": [],
            "minor_debts": [],
            "observed_debts": [],
            "shadow_split_proposals": [],
            "split_decision_registry": registry_summary,
        }
    if lint_summary["status"] != "pass":
        return {
            "path": str(path),
            "resolved_root": str(root),
            "status": "fail",
            "lint_status": lint_summary["status"],
            "audit_gate_allowed": False,
            "reason": "mother_doc_lint_failed",
            "needs_split_writeback": False,
            "docs_scanned": 0,
            "blocking_debts": [],
            "major_debts": [],
            "minor_debts": [],
            "observed_debts": [],
            "shadow_split_proposals": [],
            "split_decision_registry": registry_summary,
            "lint_summary": lint_summary,
            "recommended_next_actions": [
                "repair protocol lint failures first",
                "rerun mother-doc-refresh-root-index if the folder graph changed",
                "rerun mother-doc-audit only after mother-doc-lint returns pass",
            ],
        }

    debts: list[AuditDebt] = []
    file_paths = iter_atomic_markdown_files(root)
    proposal_candidates: list[tuple[Path, dict[str, object], list[AuditDebt]]] = []
    for file_path in file_paths:
        metadata, body, parse_errors = parse_frontmatter(file_path)
        if parse_errors:
            continue
        doc_debts = _doc_audit_debts(root, file_path)
        debts.extend(doc_debts)
        if doc_debts:
            proposal_candidates.append((file_path, metadata, doc_debts))

    grouped = {
        "blocking": [item for item in debts if item["severity"] == "blocking"],
        "major": [item for item in debts if item["severity"] == "major"],
        "minor": [item for item in debts if item["severity"] == "minor"],
        "observed": [item for item in debts if item["severity"] == "observed"],
    }
    shadow_split_proposals = [
        proposal
        for proposal in (
            _build_shadow_split_proposal(root, file_path, metadata, doc_debts)
            for file_path, metadata, doc_debts in proposal_candidates
        )
        if proposal is not None
    ]
    audit_gate_allowed = lint_summary["status"] == "pass" and not grouped["blocking"]
    status = "pass" if audit_gate_allowed else "fail"

    return {
        "path": str(path),
        "resolved_root": str(root),
        "status": status,
        "lint_status": lint_summary["status"],
        "audit_gate_allowed": audit_gate_allowed,
        "needs_split_writeback": bool(grouped["blocking"]),
        "docs_scanned": len(file_paths),
        "blocking_debts": grouped["blocking"],
        "major_debts": grouped["major"],
        "minor_debts": grouped["minor"],
        "observed_debts": grouped["observed"],
        "shadow_split_proposals": shadow_split_proposals,
        "split_decision_registry": registry_summary,
        "lint_summary": lint_summary,
        "recommended_next_actions": [
            "repair protocol lint failures first" if lint_summary["status"] != "pass" else "protocol lint clean",
            "for each blocking debt, split or migrate the overloaded semantics before deeper evidence reading",
            "use the matched shadow_split_proposals instead of ad hoc manual branching when the registry recipe fits",
            "if a split needs a new vertical layer, branch family, or content family, register it in the skill before writeback",
            "rerun mother-doc-audit after refresh-root-index and before entering mother_doc writeback stage",
        ],
    }
