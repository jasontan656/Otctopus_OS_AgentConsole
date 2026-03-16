from __future__ import annotations

from pathlib import Path

from doc_models import Issue, TargetProfile


def lint_references(target_root: Path, profile: TargetProfile) -> list[Issue]:
    if profile.doc_topology == "inline":
        return []
    issues: list[Issue] = []
    references_root = target_root / "references"
    if not references_root.is_dir():
        issues.append(Issue("references", "missing references/ root"))
        return issues
    routing_doc = references_root / "routing" / "TASK_ROUTING.md"
    if not routing_doc.is_file():
        issues.append(Issue("references", "missing references/routing/TASK_ROUTING.md"))
    policies_root = references_root / "policies"
    governance_root = references_root / "governance"
    has_policy_doc = (policies_root.is_dir() and any(policies_root.glob("*.md"))) or (
        governance_root.is_dir() and any(governance_root.glob("*.md"))
    )
    if not has_policy_doc:
        issues.append(Issue("references", "missing policy or governance markdown under references/"))
    if profile.tooling_surface != "none":
        runtime_contract_json = references_root / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT.json"
        runtime_contract_human = references_root / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT_human.md"
        tooling_root = references_root / "tooling"
        tests_root = target_root / "tests"
        if not runtime_contract_json.is_file():
            issues.append(Issue("references", "missing runtime contract json"))
        if not runtime_contract_human.is_file():
            issues.append(Issue("references", "missing runtime contract human doc"))
        if not tooling_root.is_dir() or not any(tooling_root.rglob("*.md")):
            issues.append(Issue("references", "missing tooling docs under references/tooling"))
        if not tests_root.is_dir() or not any(tests_root.rglob("test_*.py")):
            issues.append(Issue("references", "missing tests/ for scripted skill"))
    return issues
