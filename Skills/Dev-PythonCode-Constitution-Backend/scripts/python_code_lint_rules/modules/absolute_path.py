from __future__ import annotations

from pathlib import Path
import re

from python_code_lint_rules.shared import (
    iter_files,
    is_nested_scope_path,
    is_test_fixture_path,
    line_hits_from_span,
    make_gate,
    make_violation,
    preview_from_span,
    read_text,
    rel,
)

SCAN_EXTS = {".py", ".sh", ".bash", ".yaml", ".yml", ".json", ".toml"}
ALLOW_MARKERS = ("PATH_LITERAL_OK", "LINT_ALLOW_ABSOLUTE_PATH=")
UNIX_ABS_RE = re.compile(r'(?<![A-Za-z0-9_])/(?:home|Users|opt|var|tmp|etc|srv|mnt|Volumes)/[^\s"\'`]+')
WINDOWS_ABS_RE = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:\\\\[^\s"\'`]+')
FILE_URI_RE = re.compile(r'file:///[^\s"\'`]+')
OCTOPUS_ESCAPE_RE = re.compile(r'["\'`](?:\.\./){2,}[^"\'`\n]*["\'`]')
WORKSPACE_MANAGER_ROOTS = {"Codex_Skills_Mirror", "octopus-os-agent-console", "AI_Projects"}
RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/absolute_path.py"
def _has_ai_projects_prefix(text: str) -> bool:
    return "AI_Projects/" in text or "/AI_Projects/" in text or "AI_Projects\\" in text


def _category_for_reason(reason: str) -> str:
    mapping = {
        "octopus_os_forbids_unix_absolute_paths": "user_absolute_path_literal",
        "non_octopus_repo_forbids_user_absolute_paths": "user_absolute_path_literal",
        "octopus_os_forbids_windows_absolute_paths": "windows_absolute_path_literal",
        "non_octopus_repo_forbids_windows_absolute_paths": "windows_absolute_path_literal",
        "octopus_os_forbids_file_uri_paths": "file_uri_literal",
        "non_octopus_repo_forbids_file_uri_paths": "file_uri_literal",
        "octopus_os_forbids_ai_projects_prefix": "repo_boundary_prefix_literal",
        "octopus_os_forbids_repo_escape_relative_paths": "repo_escape_relative_path",
    }
    return mapping.get(reason, "absolute_path_literal")


def _cluster_key(path_text: str, reason: str) -> str:
    if "gitnexus_core" in path_text and is_test_fixture_path(path_text):
        return "absolute_path:vendored_gitnexus_tests"
    if "gitnexus_core" in path_text:
        return "absolute_path:vendored_gitnexus_runtime"
    if is_test_fixture_path(path_text):
        return "absolute_path:test_fixture_literal"
    if "agents/openai.yaml" in path_text:
        return "absolute_path:agent_prompt_literal"
    if "templates/" in path_text:
        return "absolute_path:template_runtime_path"
    if "stage_contract_registry.py" in path_text:
        return "absolute_path:stage_registry_workspace_path"
    if is_nested_scope_path(path_text):
        return "absolute_path:nested_scope_path_literal"
    return f"absolute_path:{_category_for_reason(reason)}"


def _suggested_fix(path_text: str, reason: str) -> str:
    if "gitnexus_core" in path_text:
        return "decide whether nested vendored assets/tests should be excluded before editing duplicated path fixtures"
    if is_test_fixture_path(path_text):
        return "replace fixture-only absolute paths with policy-safe placeholders or mark the case with an explicit allow token if policy permits"
    if "agents/openai.yaml" in path_text:
        return "replace hardcoded user paths in the agent prompt with repo-relative or contract-derived placeholders"
    if "templates/" in path_text:
        return "replace literal runtime filesystem paths with configurable temp-path variables or placeholders"
    if "stage_contract_registry.py" in path_text:
        return "derive workspace roots from runtime context instead of embedding user absolute paths"
    if "repo_escape_relative_path" in _category_for_reason(reason):
        return "keep references inside the repo boundary and remove escape-style relative path literals"
    if is_nested_scope_path(path_text):
        return "check nested assets/tests/references scope before editing flagged literals"
    return "replace absolute path literals with repo-relative, config-driven, or contract-derived references"


def _why_flagged(reason: str) -> str:
    mapping = {
        "octopus_os_forbids_unix_absolute_paths": "Octopus_OS forbids embedded unix absolute paths in tracked files",
        "non_octopus_repo_forbids_user_absolute_paths": "non-Octopus repos forbid embedded user absolute paths such as /home/... and /tmp/...",
        "octopus_os_forbids_windows_absolute_paths": "Octopus_OS forbids embedded Windows absolute paths",
        "non_octopus_repo_forbids_windows_absolute_paths": "non-Octopus repos forbid embedded Windows absolute paths",
        "octopus_os_forbids_file_uri_paths": "Octopus_OS forbids embedded file URI literals",
        "non_octopus_repo_forbids_file_uri_paths": "non-Octopus repos forbid embedded file URI literals",
        "octopus_os_forbids_ai_projects_prefix": "Octopus_OS forbids direct AI_Projects workspace path prefixes",
        "octopus_os_forbids_repo_escape_relative_paths": "Octopus_OS forbids relative path literals that escape the repo root",
    }
    return mapping.get(reason, "path literal violates the active repository boundary policy")


def _make_path_violation(path_text: str, reason: str, text: str, start: int, end: int) -> dict[str, object]:
    return make_violation(
        path_text,
        reason,
        category=_category_for_reason(reason),
        line_hits=line_hits_from_span(text, start, end),
        matched_text_preview=preview_from_span(text, start, end),
        why_flagged=_why_flagged(reason),
        is_likely_test_fixture=is_test_fixture_path(path_text),
        is_likely_embedded_asset=False,
        is_likely_repo_policy_violation=not is_test_fixture_path(path_text) and not is_nested_scope_path(path_text),
        cluster_key=_cluster_key(path_text, reason),
        suggested_fix=_suggested_fix(path_text, reason),
    )


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    repo_name = root.name
    is_octopus_root = repo_name == "Octopus_OS"
    is_workspace_manager = repo_name in WORKSPACE_MANAGER_ROOTS

    for path in iter_files(root, SCAN_EXTS):
        checked += 1
        text = read_text(path)
        if any(marker in text for marker in ALLOW_MARKERS):
            continue

        path_text = rel(path, root)
        unix_matches = list(UNIX_ABS_RE.finditer(text))
        windows_matches = list(WINDOWS_ABS_RE.finditer(text))
        file_uri_matches = list(FILE_URI_RE.finditer(text))
        escape_match = OCTOPUS_ESCAPE_RE.search(text)
        ai_projects_index = text.find("AI_Projects/")
        if ai_projects_index == -1:
            ai_projects_index = text.find("/AI_Projects/")
        if ai_projects_index == -1:
            ai_projects_index = text.find("AI_Projects\\")
        has_ai_projects = _has_ai_projects_prefix(text)

        if is_octopus_root:
            if unix_matches:
                first = unix_matches[0]
                violations.append(_make_path_violation(path_text, "octopus_os_forbids_unix_absolute_paths", text, first.start(), first.end()))
            if windows_matches:
                first = windows_matches[0]
                violations.append(_make_path_violation(path_text, "octopus_os_forbids_windows_absolute_paths", text, first.start(), first.end()))
            if file_uri_matches:
                first = file_uri_matches[0]
                violations.append(_make_path_violation(path_text, "octopus_os_forbids_file_uri_paths", text, first.start(), first.end()))
            if has_ai_projects and ai_projects_index >= 0:
                violations.append(
                    _make_path_violation(
                        path_text,
                        "octopus_os_forbids_ai_projects_prefix",
                        text,
                        ai_projects_index,
                        ai_projects_index + len("AI_Projects/"),
                    )
                )
            if escape_match:
                violations.append(
                    _make_path_violation(
                        path_text,
                        "octopus_os_forbids_repo_escape_relative_paths",
                        text,
                        escape_match.start(),
                        escape_match.end(),
                    )
                )
            continue

        if windows_matches:
            first = windows_matches[0]
            violations.append(_make_path_violation(path_text, "non_octopus_repo_forbids_windows_absolute_paths", text, first.start(), first.end()))
        if file_uri_matches:
            first = file_uri_matches[0]
            violations.append(_make_path_violation(path_text, "non_octopus_repo_forbids_file_uri_paths", text, first.start(), first.end()))

        for match in unix_matches:
            match_text = match.group(0)
            if "/AI_Projects/" in match_text or match_text.endswith("/AI_Projects"):
                if is_workspace_manager or has_ai_projects:
                    continue
            violations.append(
                _make_path_violation(
                    path_text,
                    "non_octopus_repo_forbids_user_absolute_paths",
                    text,
                    match.start(),
                    match.end(),
                )
            )
            break

    return make_gate("absolute_path_gate", violations, checked, rule_file=RULE_FILE)
