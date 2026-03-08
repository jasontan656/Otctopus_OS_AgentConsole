from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator

IGNORE_DIRS = {".git", ".venv", ".venv-wsl", "node_modules", "dist", "build", "coverage", "__pycache__", ".pytest_cache"}
TEXT_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".json", ".yaml", ".yml", ".md", ".sql", ".toml"}
SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".sql", ".yaml", ".yml", ".json", ".md"}
SKIP_PREFIXES = {("references",), ("assets",), ("tests",), ("scripts", "constitution_lint_rules")}
IO_PATTERNS = ("requests.", "httpx.", "fetch(", "axios(", "sqlalchemy", "psycopg", "redis.", "pymongo", "subprocess", "socket", "aiohttp", "requests.get(", "httpx.get(")
RAW_PAYLOAD_PATTERNS = ("telegram_update", "callback_query", "webapp_data", "raw_payload", "raw_update", "incoming_update")


def should_skip(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    return any(parts[:len(prefix)] == prefix for prefix in SKIP_PREFIXES)


def iter_files(root: Path, exts: Iterable[str] | None = None) -> Iterator[Path]:
    allowed = set(exts or TEXT_EXTS)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts) or should_skip(path, root):
            continue
        if allowed and path.suffix.lower() not in allowed:
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def make_gate(gate: str, violations: list[dict[str, str]], checked: int) -> dict[str, object]:
    return {
        "gate": gate,
        "status": "pass" if not violations else "fail",
        "checked": checked,
        "violations": violations,
    }
