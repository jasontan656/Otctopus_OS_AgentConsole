from __future__ import annotations

from pathlib import Path
import re

from constitution_lint_rules.shared import IGNORE_DIRS, make_gate, read_text, rel, should_skip

EXEC_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".sh", ".bash"}
ALLOW_MARKERS = ("INLINE_LITERAL_OK", "LINT_ALLOW_HARDCODED_ASSET=")
TRIPLE_QUOTE_RE = re.compile(r'("""|\'\'\')([\s\S]*?)\1', re.MULTILINE)
BACKTICK_RE = re.compile(r"`([\s\S]*?)`", re.MULTILINE)
ASSET_TOKENS = (
    "you are",
    "你是",
    "system prompt",
    "agents.md",
    "goal:",
    "workflow",
    "输出契约",
    "必须",
    "禁止",
    "## ",
    "name:",
    "description:",
)


def _iter_exec_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in EXEC_EXTS:
            continue
        if any(part in IGNORE_DIRS for part in path.parts) or should_skip(path, root):
            continue
        yield path


def _iter_string_blocks(text: str):
    for match in TRIPLE_QUOTE_RE.finditer(text):
        yield match.group(2)
    for match in BACKTICK_RE.finditer(text):
        block = match.group(1)
        if "\n" in block:
            yield block


def _is_audit_asset(block: str) -> bool:
    normalized = block.strip()
    if not normalized:
        return False
    line_count = sum(1 for line in normalized.splitlines() if line.strip())
    char_count = len(normalized)
    lowered = normalized.lower()
    has_asset_signal = any(token in lowered for token in ASSET_TOKENS)
    has_markdown_shape = normalized.startswith("---") or "## " in normalized or "- " in normalized
    return (line_count >= 8 or char_count >= 280) and (has_asset_signal or has_markdown_shape)


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in _iter_exec_files(root):
        checked += 1
        text = read_text(path)
        if any(marker in text for marker in ALLOW_MARKERS):
            continue
        for block in _iter_string_blocks(text):
            if _is_audit_asset(block):
                violations.append({"path": rel(path, root), "reason": "hardcoded_audit_asset_in_executable"})
                break
    return make_gate("hardcoded_asset_gate", violations, checked)
