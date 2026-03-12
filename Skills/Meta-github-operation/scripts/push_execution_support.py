from __future__ import annotations

import fcntl
from contextlib import contextmanager
from pathlib import Path

from entry_support import runtime_governance_payload


TRACEABILITY_MESSAGE_KEYWORDS = (
    "problem",
    "issue",
    "resolved",
    "resolve",
    "fixed",
    "fix",
    "root cause",
    "impact",
    "risk",
    "问题",
    "解决",
    "修复",
    "根因",
    "影响",
    "风险",
)


def normalize_traceability_message(message: str) -> str:
    normalized = message.strip()
    if not normalized:
        raise ValueError("traceability_message_empty")

    lines = [line.rstrip() for line in normalized.splitlines()]
    subject = next((line.strip() for line in lines if line.strip()), "")
    body_lines = [line.strip() for line in lines[1:] if line.strip()]
    if not subject:
        raise ValueError("traceability_message_missing_subject")
    if len(body_lines) < 2:
        raise ValueError(
            "traceability_message_requires_development_log_details: provide a short subject plus at least two detail lines"
        )

    body_text = " ".join(body_lines).lower()
    if not any(keyword in body_text for keyword in TRACEABILITY_MESSAGE_KEYWORDS):
        raise ValueError(
            "traceability_message_must_describe_problem_or_resolution: include what problem was solved, risk reduced, or impact delivered"
        )
    return normalized


@contextmanager
def serial_push_lock(repo_name: str, operation: str) -> dict[str, str]:
    runtime_governance = runtime_governance_payload()
    lock_dir = Path(runtime_governance["push_lock_dir"]).resolve()
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{repo_name}.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield {
                "repo": repo_name,
                "operation": operation,
                "lock_path": str(lock_path),
            }
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
