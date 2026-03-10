from __future__ import annotations

from pathlib import Path
import re

from constitution_lint_rules.shared import (
    IGNORE_DIRS,
    is_nested_scope_path,
    is_test_fixture_path,
    line_hits_from_span,
    make_gate,
    make_violation,
    preview_from_span,
    read_text,
    rel,
    should_skip,
)

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
RULE_FILE = "Constitution-knowledge-base/scripts/constitution_lint_rules/modules/hardcoded_asset.py"


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
        yield match.group(2), match.start(2), match.end(2)
    for match in BACKTICK_RE.finditer(text):
        block = match.group(1)
        if "\n" in block:
            yield block, match.start(1), match.end(1)


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


def _category_for_block(block: str) -> str:
    lowered = block.lower()
    if "## " in block or block.strip().startswith("---"):
        return "embedded_markdown_template"
    if "you are" in lowered or "system prompt" in lowered or "你是" in lowered:
        return "embedded_prompt_block"
    return "embedded_multiline_asset"


def _cluster_key(path_text: str, category: str) -> str:
    if "gitnexus_core" in path_text:
        return "hardcoded_asset:vendored_gitnexus_asset"
    if is_test_fixture_path(path_text):
        return "hardcoded_asset:test_fixture_literal"
    if is_nested_scope_path(path_text):
        return "hardcoded_asset:nested_scope_asset"
    return f"hardcoded_asset:{category}"


def _suggested_fix(path_text: str) -> str:
    if "gitnexus_core" in path_text:
        return "decide whether nested vendored assets/tests should be excluded before editing duplicated copies"
    if is_test_fixture_path(path_text):
        return "move intentional fixture content to an allowed sample file or mark the test case with an explicit allow token if policy permits"
    if is_nested_scope_path(path_text):
        return "check whether nested assets/tests/references should stay in lint scope before rewriting embedded content"
    return "move the embedded asset or prompt body to assets/references and load it at runtime"


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in _iter_exec_files(root):
        checked += 1
        text = read_text(path)
        if any(marker in text for marker in ALLOW_MARKERS):
            continue
        path_text = rel(path, root)
        for block, start, end in _iter_string_blocks(text):
            if _is_audit_asset(block):
                violations.append(
                    make_violation(
                        path_text,
                        "hardcoded_audit_asset_in_executable",
                        category=_category_for_block(block),
                        line_hits=line_hits_from_span(text, start, end),
                        matched_text_preview=preview_from_span(text, start, end),
                        why_flagged="multi-line executable string matches markdown or prompt-style asset heuristics",
                        is_likely_test_fixture=is_test_fixture_path(path_text),
                        is_likely_embedded_asset=True,
                        is_likely_repo_policy_violation=not is_test_fixture_path(path_text) and not is_nested_scope_path(path_text),
                        cluster_key=_cluster_key(path_text, _category_for_block(block)),
                        suggested_fix=_suggested_fix(path_text),
                    )
                )
                break
    return make_gate("hardcoded_asset_gate", violations, checked, rule_file=RULE_FILE)
