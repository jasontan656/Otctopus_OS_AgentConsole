from __future__ import annotations

import re
from typing import Any

from runtime_pain_observability import normalize_text

_SUSPECT_PLACEHOLDER_RE = re.compile(r"<[^>\s]+>")
_SELF_REPAIR_RE = re.compile(r"\bruntime_pain_batch\.py\b", re.IGNORECASE)
_REPAIR_SAFE_CONTROL_COMMANDS = {
    "write_stdin",
    "write_stdout",
    "write_stderr",
}


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _strip_signature_prefix(signature: str) -> str:
    normalized = str(signature or "").strip()
    if not normalized:
        return ""

    if "|runtime|" in normalized:
        normalized = normalized.split("|runtime|", 1)[1]

    prefixes = ("tool_failure_any|", "exec_command|", "runtime|")
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :]

    return normalized.strip()


def _contains_unreplaced_placeholder(command: str) -> bool:
    return bool(_SUSPECT_PLACEHOLDER_RE.search(command))


def _looks_like_diagnostic_runtime_probe(command: str) -> bool:
    lowered = command.lower()
    return bool(_SELF_REPAIR_RE.search(lowered)) or "optimization-list --max-results" in lowered


def _normalize_candidate(command: str) -> str:
    cmd = str(command or "").strip()
    if not cmd:
        return ""

    if cmd.startswith("`") and cmd.endswith("`") and len(cmd) >= 2:
        cmd = cmd[1:-1].strip()

    if cmd.endswith("\\"):
        cmd = cmd[:-1].rstrip()

    if "\n" in cmd:
        return cmd.strip()
    return " ".join(cmd.split())


def _looks_like_executable_command(command: str) -> bool:
    tokens = command.strip().split()
    if not tokens:
        return False

    first = tokens[0].strip()
    if first.startswith("(") and ")" not in first and len(tokens) > 1:
        first = tokens[1].strip()

    return first not in _REPAIR_SAFE_CONTROL_COMMANDS


def _looks_like_thread_scope_status_command(command: str) -> bool:
    lowered = str(command or "").lower()
    if "meta_github_operation_family.py" not in lowered:
        return False
    if " status " not in f" {lowered} ":
        return False
    if "--snapshot-scope thread-owned" in lowered:
        return True
    if "--snapshot-scope run-owned" in lowered:
        return True
    if "--snapshot-scope=thread-owned" in lowered:
        return True
    if "--snapshot-scope=run-owned" in lowered:
        return True
    return False


def _iter_raw_candidates(group: dict[str, Any]) -> list[str]:
    outputs: list[str] = []

    diagnosis_card = _as_dict(group.get("diagnosis_card_v2"))
    for row in _as_list(diagnosis_card.get("fact_evidence_samples")):
        row_dict = _as_dict(row)
        outputs.append(str(row_dict.get("command_preview", "") or "").strip())
        outputs.append(str(row_dict.get("command_signature", "") or "").strip())

    for row in _as_list(group.get("events")):
        row_dict = _as_dict(row)
        outputs.append(str(row_dict.get("command_preview_raw", "") or "").strip())
        outputs.append(str(row_dict.get("command_signature_raw", "") or "").strip())
        outputs.append(str(row_dict.get("command_signature", "") or "").strip())
        outputs.append(str(row_dict.get("command_preview", "") or "").strip())

    repair_strategy = _as_dict(diagnosis_card.get("repair_strategy_v2"))
    for row in _as_list(repair_strategy.get("verification_runbook_v1")):
        row_dict = _as_dict(row)
        outputs.append(str(row_dict.get("command_hint", "") or "").strip())

    return outputs


def extract_group_repair_commands(group: dict[str, Any]) -> list[str]:
    if not isinstance(group, dict):
        return []

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in _iter_raw_candidates(group):
        normalized = _normalize_candidate(_strip_signature_prefix(candidate))
        if not normalized:
            continue
        if "... " in normalized or normalized.startswith("..."):
            continue
        if normalized.lower() == "python3 - <<'py'":
            continue
        if "<" in normalized and _contains_unreplaced_placeholder(normalized):
            continue
        if _looks_like_diagnostic_runtime_probe(normalized):
            continue
        if _looks_like_thread_scope_status_command(normalized):
            continue
        if not _looks_like_executable_command(normalized):
            continue

        key = normalize_text(normalized, limit=260).lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(normalized)

    return deduped
