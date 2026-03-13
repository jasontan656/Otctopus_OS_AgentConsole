from __future__ import annotations

from pathlib import Path

from runtime_pain_types import CommandExecutionResult, RepairWriteResult


def empty_command_result(*, all_succeeded: bool) -> CommandExecutionResult:
    return {
        "total_commands": 0,
        "success_commands": 0,
        "failed_commands": 0,
        "all_succeeded": all_succeeded,
        "runs": [],
        "change_detection_supported": False,
        "all_changed_paths": [],
        "all_changed_path_count": 0,
        "preflight_failed_commands": 0,
        "preflight_reason_codes": [],
    }


def empty_write_result() -> RepairWriteResult:
    return {
        "total_writes": 0,
        "success_writes": 0,
        "failed_writes": 0,
        "writes": [],
    }


def sum_execution_results(values: list[CommandExecutionResult]) -> CommandExecutionResult:
    if not values:
        return empty_command_result(all_succeeded=False)

    aggregated_runs = []
    total_commands = 0
    total_success = 0
    total_failed = 0
    preflight_failed = 0
    preflight_reasons: set[str] = set()
    has_detection = False
    changed_paths: set[str] = set()
    for row in values:
        total_commands += int(row.get("total_commands", 0) or 0)
        total_success += int(row.get("success_commands", 0) or 0)
        total_failed += int(row.get("failed_commands", 0) or 0)
        preflight_failed += int(row.get("preflight_failed_commands", 0) or 0)
        preflight_reasons.update(
            str(reason_code or "").strip()
            for reason_code in row.get("preflight_reason_codes", [])
            if str(reason_code or "").strip()
        )
        has_detection = has_detection or bool(row.get("change_detection_supported", False))
        changed_paths.update(
            str(path_value)
            for path_value in row.get("all_changed_paths", [])
            if str(path_value).strip()
        )
        aggregated_runs.extend(row.get("runs", []))

    return {
        "total_commands": total_commands,
        "success_commands": total_success,
        "failed_commands": total_failed,
        "all_succeeded": total_failed == 0 and total_commands > 0,
        "runs": aggregated_runs,
        "change_detection_supported": has_detection,
        "all_changed_paths": sorted(changed_paths),
        "all_changed_path_count": len(changed_paths),
        "preflight_failed_commands": preflight_failed,
        "preflight_reason_codes": sorted(preflight_reasons),
    }


def normalize_manual_path_prefixes(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = str(raw or "").strip()
        if not value:
            continue
        normalized = value.replace("\\", "/")
        if normalized.startswith("./"):
            normalized = normalized[2:]
        normalized = normalized.rstrip("/")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def _strip_change_prefix(path_value: str) -> str:
    value = str(path_value or "").strip()
    if ":" in value:
        return value.split(":", 1)[1]
    return value


def _normalize_manual_prefix(prefix: str, repo_root: str) -> str:
    value = str(prefix or "").strip().replace("\\", "/").rstrip("/")
    if not value:
        return ""
    if value.startswith("./"):
        value = value[2:]

    root = str(repo_root or "").strip()
    if not root:
        return value

    try:
        root_path = Path(root).expanduser().resolve()
        value_path = Path(value).expanduser()
        if value_path.is_absolute():
            relative = value_path.resolve().relative_to(root_path)
            return str(relative).replace("\\", "/").rstrip("/")
    except (OSError, RuntimeError, ValueError):
        return value
    return value


def filter_changed_paths(paths: list[str], manual_path_prefixes: list[str], *, repo_root: str = "") -> list[str]:
    if not manual_path_prefixes:
        return [str(path_value) for path_value in paths if str(path_value).strip()]

    normalized_prefixes = [
        _normalize_manual_prefix(prefix, repo_root)
        for prefix in manual_path_prefixes
        if str(prefix or "").strip()
    ]

    filtered: list[str] = []
    seen: set[str] = set()
    for row in paths:
        text = str(row or "").strip()
        if not text:
            continue
        candidate = _strip_change_prefix(text).replace("\\", "/")
        if candidate.startswith("./"):
            candidate = candidate[2:]
        matched = any(
            candidate == normalized_prefix or candidate.startswith(f"{normalized_prefix}/")
            for normalized_prefix in normalized_prefixes
        )
        if not matched or text in seen:
            continue
        seen.add(text)
        filtered.append(text)
    return filtered
