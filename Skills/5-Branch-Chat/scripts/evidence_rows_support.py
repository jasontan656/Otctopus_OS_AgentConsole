from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

from session_locator_support import content_to_text


def iter_session_evidence(session_files: Iterable[Path]) -> List[Dict[str, str | int]]:
    evidence_rows: List[Dict[str, str | int]] = []

    for path in session_files:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "response_item":
                    continue

                payload = entry.get("payload") or {}
                payload_type = payload.get("type")
                text = ""
                source_type = ""

                if payload_type == "message":
                    role = payload.get("role", "")
                    if role not in {"assistant", "user"}:
                        continue
                    text = content_to_text(payload.get("content"))
                    source_type = f"message:{role}"
                elif payload_type in {"function_call", "custom_tool_call"}:
                    text = f"{payload.get('name', '')}".strip()
                    source_type = "tool_call"
                elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                    text = str(payload.get("output", "")).strip()
                    if '"audit_trace": "branch_chat_toolbox"' in text or "trace_id:print_json" in text:
                        continue
                    source_type = "tool_output"
                else:
                    continue

                if not text:
                    continue
                evidence_rows.append(
                    {
                        "timestamp": entry.get("timestamp", ""),
                        "source_file": str(path),
                        "line_number": line_no,
                        "source_type": source_type,
                        "text": text,
                    }
                )

    evidence_rows.sort(key=lambda row: (str(row.get("timestamp", "")), str(row["source_file"]), int(row["line_number"])))
    return evidence_rows
