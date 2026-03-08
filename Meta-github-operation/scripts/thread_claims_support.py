from __future__ import annotations

import json
from pathlib import Path


RUNTIME_ROOT = Path("/home/jasontan656/AI_Projects/Codex_Skill_Runtime")
CLAIM_PATTERN = "Meta-github-operation_thread_owned_paths*.json"


def latest_claims_file() -> Path | None:
    candidates = sorted(RUNTIME_ROOT.glob(CLAIM_PATTERN), key=lambda item: item.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def load_claim_paths(claims_path: Path, repo_name: str) -> list[str]:
    payload = json.loads(claims_path.read_text(encoding="utf-8"))
    repos = payload.get("repos")
    if not isinstance(repos, dict):
        return []
    raw_paths = repos.get(repo_name, [])
    if not isinstance(raw_paths, list):
        return []
    return [str(item) for item in raw_paths if isinstance(item, str) and item.strip()]
