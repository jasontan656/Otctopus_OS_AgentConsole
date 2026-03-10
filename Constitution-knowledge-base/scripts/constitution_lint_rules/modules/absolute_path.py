from __future__ import annotations

from pathlib import Path
import re

from constitution_lint_rules.shared import IGNORE_DIRS, make_gate, read_text, rel, should_skip

SCAN_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".sh", ".bash", ".yaml", ".yml", ".json", ".toml"}
ALLOW_MARKERS = ("PATH_LITERAL_OK", "LINT_ALLOW_ABSOLUTE_PATH=")
UNIX_ABS_RE = re.compile(r'(?<![A-Za-z0-9_])/(?:home|Users|opt|var|tmp|etc|srv|mnt|Volumes)/[^\s"\'`]+')
WINDOWS_ABS_RE = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:\\\\[^\s"\'`]+')
FILE_URI_RE = re.compile(r'file:///[^\s"\'`]+')
OCTOPUS_ESCAPE_RE = re.compile(r'["\'`](?:\.\./){2,}[^"\'`\n]*["\'`]')
WORKSPACE_MANAGER_ROOTS = {"Codex_Skills_Mirror", "AI_Projects"}


def _iter_scan_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCAN_EXTS:
            continue
        if any(part in IGNORE_DIRS for part in path.parts) or should_skip(path, root):
            continue
        yield path


def _has_ai_projects_prefix(text: str) -> bool:
    return "AI_Projects/" in text or "/AI_Projects/" in text or "AI_Projects\\" in text


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    repo_name = root.name
    is_octopus_root = repo_name == "Octopus_OS"
    is_workspace_manager = repo_name in WORKSPACE_MANAGER_ROOTS

    for path in _iter_scan_files(root):
        checked += 1
        text = read_text(path)
        if any(marker in text for marker in ALLOW_MARKERS):
            continue

        unix_matches = UNIX_ABS_RE.findall(text)
        windows_matches = WINDOWS_ABS_RE.findall(text)
        file_uri_matches = FILE_URI_RE.findall(text)
        has_ai_projects = _has_ai_projects_prefix(text)

        if is_octopus_root:
            if unix_matches:
                violations.append({"path": rel(path, root), "reason": "octopus_os_forbids_unix_absolute_paths"})
            if windows_matches:
                violations.append({"path": rel(path, root), "reason": "octopus_os_forbids_windows_absolute_paths"})
            if file_uri_matches:
                violations.append({"path": rel(path, root), "reason": "octopus_os_forbids_file_uri_paths"})
            if has_ai_projects:
                violations.append({"path": rel(path, root), "reason": "octopus_os_forbids_ai_projects_prefix"})
            if OCTOPUS_ESCAPE_RE.search(text):
                violations.append({"path": rel(path, root), "reason": "octopus_os_forbids_repo_escape_relative_paths"})
            continue

        if windows_matches:
            violations.append({"path": rel(path, root), "reason": "non_octopus_repo_forbids_windows_absolute_paths"})
        if file_uri_matches:
            violations.append({"path": rel(path, root), "reason": "non_octopus_repo_forbids_file_uri_paths"})

        for match in unix_matches:
            if "/AI_Projects/" in match or match.endswith("/AI_Projects"):
                if is_workspace_manager or has_ai_projects:
                    continue
            violations.append({"path": rel(path, root), "reason": "non_octopus_repo_forbids_user_absolute_paths"})
            break

    return make_gate("absolute_path_gate", violations, checked)
