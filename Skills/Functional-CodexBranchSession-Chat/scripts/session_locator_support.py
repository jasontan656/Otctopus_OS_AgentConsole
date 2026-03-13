from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List


def resolve_query_id(session_id: str | None, resume_id: str | None) -> str:
    value = (session_id or resume_id or "").strip()
    if not value:
        raise ValueError("Missing id. Provide --session-id or --resume-id.")
    return value


def resolve_codex_home(override: str | None) -> Path:
    candidates = []
    if override:
        candidates.append(Path(os.path.expanduser(override)))
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        candidates.append((repo_root.parent / ".codex").resolve())
    env_home = os.getenv("CODEX_HOME")
    if env_home:
        candidates.append(Path(os.path.expanduser(env_home)))
    candidates.append(Path.home() / ".codex")

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        "Cannot resolve Codex home. Checked --codex-home, <root>/.codex, $CODEX_HOME, ~/.codex"
    )


def find_session_files(codex_home: Path, session_id: str) -> List[Path]:
    sessions_root = codex_home / "sessions"
    if not sessions_root.exists():
        raise FileNotFoundError(f"Sessions root not found: {sessions_root}")
    pattern = f"*{session_id}*.jsonl"
    return sorted(path for path in sessions_root.rglob(pattern) if path.is_file())


def content_to_text(content: Any) -> str:
    if not isinstance(content, list):
        return ""
    chunks: List[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            chunks.append(text.strip())
    return "\n".join(chunks).strip()


def trim_text(text: str, max_len: int = 600) -> str:
    clean = text.strip()
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3] + "..."


def iter_assistant_messages(session_files: Iterable[Path]) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []
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
                if payload.get("type") != "message" or payload.get("role") != "assistant":
                    continue

                text = content_to_text(payload.get("content"))
                if not text:
                    continue

                messages.append(
                    {
                        "timestamp": entry.get("timestamp", ""),
                        "source_file": str(path),
                        "line_number": line_no,
                        "text": text,
                    }
                )

    messages.sort(key=lambda item: (item.get("timestamp", ""), item["source_file"], item["line_number"]))
    return messages
