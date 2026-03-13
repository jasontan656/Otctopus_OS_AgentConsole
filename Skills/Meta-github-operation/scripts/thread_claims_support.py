from __future__ import annotations

import json
import os
from pathlib import Path


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Meta-github-operation script path")
    return repo_root.parent


DEFAULT_RUNTIME_ROOT = (_resolve_product_root() / "Codex_Skill_Runtime").resolve()
SKILL_RUNTIME_ROOT = (
    Path(os.environ.get("CODEX_SKILL_RUNTIME_ROOT", str(DEFAULT_RUNTIME_ROOT))).expanduser().resolve()
    / "meta-github-operation"
)
CLAIMS_DIR = SKILL_RUNTIME_ROOT / "claims"
LEGACY_RUNTIME_ROOT = DEFAULT_RUNTIME_ROOT
CLAIM_PATTERN = "Meta-github-operation_thread_owned_paths*.json"


def latest_claims_file() -> Path | None:
    candidates = sorted(CLAIMS_DIR.glob(CLAIM_PATTERN), key=lambda item: item.stat().st_mtime, reverse=True)
    if candidates:
        return candidates[0]
    legacy_candidates = sorted(LEGACY_RUNTIME_ROOT.glob(CLAIM_PATTERN), key=lambda item: item.stat().st_mtime, reverse=True)
    if legacy_candidates:
        return legacy_candidates[0]
    return None


def load_claim_paths(claims_path: Path, repo_name: str) -> list[str]:
    payload = json.loads(claims_path.read_text(encoding="utf-8"))
    repos = payload.get("repos")
    if not isinstance(repos, dict):
        return []
    raw_paths = repos.get(repo_name, [])
    if not isinstance(raw_paths, list):
        return []
    return [str(item) for item in raw_paths if isinstance(item, str) and item.strip()]
