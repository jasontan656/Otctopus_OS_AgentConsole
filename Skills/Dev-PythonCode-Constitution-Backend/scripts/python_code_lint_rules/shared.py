from __future__ import annotations

import ast
import configparser
from functools import lru_cache
from pathlib import Path
import tomllib
from typing import Any, Iterable, Iterator

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    ".venv-wsl",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "htmlcov",
    "tmp",
    "temp",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".tox",
    ".nox",
    ".eggs",
    ".idea",
    ".vscode",
    ".turbo",
    ".next",
    ".nuxt",
    ".parcel-cache",
    ".sass-cache",
}
IGNORE_DIR_PREFIXES = (
    ".venv",
    "venv-",
    "venv_",
    ".tmp",
    "tmp-",
    "tmp_",
    ".temp",
    "temp-",
    "temp_",
)
IGNORE_DIR_SUFFIXES = (".egg-info",)
TEXT_EXTS = {".py", ".json", ".yaml", ".yml", ".md", ".sql", ".toml", ".sh", ".bash"}
SOURCE_EXTS = {".py", ".sql", ".yaml", ".yml", ".json", ".md", ".toml"}
SKIP_PREFIXES = {("references",), ("tests",), ("scripts", "python_code_lint_rules")}
NESTED_SKIP_DIRS = {"references", "tests"}
IO_PATTERNS = ("requests.", "httpx.", "fetch(", "axios(", "sqlalchemy", "psycopg", "redis.", "pymongo", "subprocess", "socket", "aiohttp", "requests.get(", "httpx.get(")
RAW_PAYLOAD_PATTERNS = ("telegram_update", "callback_query", "webapp_data", "raw_payload", "raw_update", "incoming_update")
PYTHON_PATH_HINTS = (
    "python",
    "pyproject",
    "pytest",
    "ruff",
    "mypy",
    "pydantic",
    "fastapi",
    "django",
    "flask",
    "sqlalchemy",
    "alembic",
    "typer",
)
PYTHON_TEXT_HINTS = (
    "python",
    ".py",
    "pytest",
    "ruff",
    "mypy",
    "pydantic",
    "fastapi",
    "django",
    "flask",
    "sqlalchemy",
    "alembic",
    "typer",
    "async def ",
    "from ",
    "import ",
)


def is_ignored_dir_name(name: str) -> bool:
    lowered = name.lower()
    return (
        lowered in IGNORE_DIRS
        or any(lowered.startswith(prefix) for prefix in IGNORE_DIR_PREFIXES)
        or any(lowered.endswith(suffix) for suffix in IGNORE_DIR_SUFFIXES)
    )


def is_ignored_path(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    if not parts:
        return False
    directory_parts = parts if path.is_dir() else parts[:-1]
    return any(is_ignored_dir_name(part) for part in directory_parts)


def should_skip(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    if any(parts[:len(prefix)] == prefix for prefix in SKIP_PREFIXES):
        return True
    return any(part in NESTED_SKIP_DIRS for part in parts[:-1])


def iter_tree(root: Path) -> Iterator[Path]:
    for path in root.rglob("*"):
        if is_ignored_path(path, root) or should_skip(path, root):
            continue
        yield path


@lru_cache(maxsize=None)
def _python_reference_texts(root_text: str) -> tuple[str, ...]:
    root = Path(root_text)
    references = []
    for path in iter_tree(root):
        if not path.is_file() or path.suffix.lower() != ".py":
            continue
        references.append(read_text(path))
    return tuple(references)


def _has_python_scope_hint(path: Path, root: Path, text: str | None = None) -> bool:
    rel_text = rel(path, root).replace("\\", "/").lower()
    if any(token in rel_text for token in PYTHON_PATH_HINTS):
        return True
    payload = (text if text is not None else read_text(path)).lower()
    return any(token in payload for token in PYTHON_TEXT_HINTS)


def _is_referenced_by_python(path: Path, root: Path) -> bool:
    rel_text = rel(path, root).replace("\\", "/")
    basename = path.name
    candidates = {rel_text, basename}
    return any(candidate in text for text in _python_reference_texts(str(root)) for candidate in candidates)


def is_python_governed_file(path: Path, root: Path, *, text: str | None = None) -> bool:
    if path.suffix.lower() == ".py":
        return True
    if _has_python_scope_hint(path, root, text):
        return True
    return _is_referenced_by_python(path, root)


def iter_files(root: Path, exts: Iterable[str] | None = None) -> Iterator[Path]:
    allowed = set(exts or TEXT_EXTS)
    for path in iter_tree(root):
        if not path.is_file():
            continue
        if allowed and path.suffix.lower() not in allowed:
            continue
        if not is_python_governed_file(path, root):
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def parse_python_ast(path: Path) -> tuple[ast.AST | None, str]:
    text = read_text(path)
    try:
        return ast.parse(text), text
    except SyntaxError:
        return None, text


def load_toml(path: Path) -> dict[str, Any] | None:
    try:
        return tomllib.loads(read_text(path))
    except tomllib.TOMLDecodeError:
        return None


def load_ini_sections(path: Path) -> configparser.ConfigParser | None:
    parser = configparser.ConfigParser()
    try:
        parser.read_string(read_text(path))
    except (configparser.Error, OSError):
        return None
    return parser


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def line_hits_from_span(text: str, start: int, end: int) -> list[int]:
    if start < 0:
        start = 0
    if end < start:
        end = start
    start_line = text.count("\n", 0, start) + 1
    end_line = text.count("\n", 0, end) + 1
    return list(range(start_line, end_line + 1))


def preview_from_span(text: str, start: int, end: int, *, limit: int = 160) -> str:
    snippet = text[start:end].strip().replace("\n", " ")
    if not snippet:
        return ""
    compact = " ".join(snippet.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def line_hits_from_node(node: ast.AST) -> list[int]:
    start_line = getattr(node, "lineno", None)
    end_line = getattr(node, "end_lineno", start_line)
    if not isinstance(start_line, int):
        return []
    if not isinstance(end_line, int) or end_line < start_line:
        end_line = start_line
    return list(range(start_line, end_line + 1))


def preview_from_node(text: str, node: ast.AST, *, limit: int = 160) -> str:
    snippet = ast.get_source_segment(text, node) or ""
    compact = " ".join(snippet.split())
    if not compact:
        return ""
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def has_package_ancestor(path: Path, root: Path) -> bool:
    current = path.parent
    while current != root and current != current.parent:
        if (current / "__init__.py").exists():
            return True
        current = current.parent
    return False


def is_nested_scope_path(path_text: str) -> bool:
    parts = Path(path_text).parts
    if not parts:
        return False
    return any(part in {"assets", "tests", "references"} for part in parts[1:])


def is_test_fixture_path(path_text: str) -> bool:
    parts = Path(path_text).parts
    if "tests" in parts:
        return True
    lowered = path_text.lower()
    return lowered.endswith("_test.py") or lowered.endswith("test_.py") or lowered.endswith(".spec.py")


def make_violation(path: str, reason: str, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"path": path, "reason": reason}
    payload.update(extra)
    return payload


def make_gate(gate: str, violations: list[dict[str, Any]], checked: int, *, rule_file: str | None = None) -> dict[str, object]:
    return {
        "gate": gate,
        "status": "pass" if not violations else "fail",
        "checked": checked,
        "violations": violations,
        "rule_file": rule_file,
    }
