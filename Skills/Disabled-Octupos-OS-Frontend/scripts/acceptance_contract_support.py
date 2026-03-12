from __future__ import annotations

import csv
from pathlib import Path

from workflow_policy_contract import ACCEPTANCE_LINT_POLICY

# contract_name: octopus_frontend_acceptance_contract_support
# contract_version: 1.0.0
# validation_mode: strict
# required_fields:
#   - acceptance_lint_payload
# optional_fields: []


def _truthy(value: str) -> bool:
    return value.strip().lower().strip("`") in {"true", "yes", "pass", "completed"}


def _parse_markdown_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    lines = [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    header: list[str] | None = None
    for line in lines:
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if header and len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def _csv_cells(value: str) -> list[str]:
    parts = next(csv.reader([value], skipinitialspace=True), [])
    return [part.strip() for part in parts if part.strip()]


def _resolve_evidence_path(raw: str, codebase_root: Path, runtime_root: Path) -> Path | None:
    token = raw.strip().strip("`")
    if not token or "*" in token:
        return None
    path = Path(token)
    if path.is_absolute():
        return path
    for root in (codebase_root, runtime_root):
        candidate = root / token
        if candidate.exists():
            return candidate
    return codebase_root / token


def acceptance_lint_payload(matrix_path: Path, report_path: Path, codebase_root: Path, runtime_root: Path) -> dict:
    violations: list[dict[str, str]] = []
    matrix_rows = _parse_markdown_table(matrix_path)
    report_rows = _parse_markdown_table(report_path)

    for row in matrix_rows:
        requirement_atom_id = row.get("requirement_atom_id", "").strip() or "<missing>"
        blocked_state = row.get("blocked_state", "").strip().strip("`")
        evidence_paths = [
            _resolve_evidence_path(part, codebase_root, runtime_root) for part in _csv_cells(row.get("evidence_refs", ""))
        ]
        existing_paths = [path for path in evidence_paths if path and path.exists()]
        existing_non_doc = [path for path in existing_paths if "/docs/" not in str(path) and path.suffix.lower() != ".md"]
        existing_tests = [path for path in existing_paths if "/tests/" in str(path)]
        if ACCEPTANCE_LINT_POLICY["implemented_true_requires_existing_non_doc_evidence"] and _truthy(
            row.get("implemented", "")
        ) and not existing_non_doc:
            violations.append(
                {
                    "scope": "acceptance_matrix",
                    "row_id": requirement_atom_id,
                    "reason": "implemented_true_without_existing_non_doc_evidence",
                }
            )
        if ACCEPTANCE_LINT_POLICY["tested_true_requires_existing_test_evidence"] and _truthy(
            row.get("tested", "")
        ) and not existing_tests:
            violations.append(
                {
                    "scope": "acceptance_matrix",
                    "row_id": requirement_atom_id,
                    "reason": "tested_true_without_existing_test_evidence",
                }
            )
        if (
            ACCEPTANCE_LINT_POLICY["witnessed_true_forbidden_when_blocked_state_needs_real_env"]
            and _truthy(row.get("witnessed", ""))
            and blocked_state == "needs_real_env"
        ):
            violations.append(
                {
                    "scope": "acceptance_matrix",
                    "row_id": requirement_atom_id,
                    "reason": "witnessed_true_conflicts_with_needs_real_env",
                }
            )

    for row in report_rows:
        package_id = row.get("plan_step_id", "").strip() or row.get("package_id", "").strip() or "<missing>"
        implemented_files = [
            _resolve_evidence_path(part, codebase_root, runtime_root) for part in _csv_cells(row.get("implemented_files", ""))
        ]
        tests_run = [_resolve_evidence_path(part, codebase_root, runtime_root) for part in _csv_cells(row.get("tests_run", ""))]
        if implemented_files and not any(path and path.exists() for path in implemented_files):
            violations.append(
                {
                    "scope": "acceptance_report",
                    "row_id": package_id,
                    "reason": "implemented_files_missing_on_disk",
                }
            )
        if tests_run and not any(path and path.exists() for path in tests_run):
            violations.append(
                {
                    "scope": "acceptance_report",
                    "row_id": package_id,
                    "reason": "tests_run_missing_on_disk",
                }
            )

    status = "pass" if not violations else "fail"
    return {
        "status": status,
        "matrix_path": str(matrix_path),
        "report_path": str(report_path),
        "violations": violations,
        "acceptance_gate_allowed": status == "pass",
        "policy": ACCEPTANCE_LINT_POLICY,
    }
