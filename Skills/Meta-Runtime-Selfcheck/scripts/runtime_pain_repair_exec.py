from __future__ import annotations

import os
import shlex
import subprocess
import time
import re
from pathlib import Path
from typing import Any

from runtime_pain_observability import normalize_text

_COMMAND_PATH_RE = re.compile(r"(?:(?<=\s)|^)((?:~?/|\.\./|\./|/)[^ '\"`|&;<>$()]+)")
_SHELL_OPERATOR_RE = re.compile(r"(?:\|\||&&|[|;])")
_SKILL_DIR_CASE_ALIASES = {
    "Governance-Ruleset": "Governance-Ruleset",
    "meta-github-operation": "Meta-github-operation",
}
_LEGACY_PYTHON_ENTRYPOINT_ALIASES = {
    "constitution_lint.py": "governance_gate.py",
    "run_constitution_lint.py": "governance_gate.py",
    "meta_github_operation.py": "meta_github_operation_family.py",
}
_LEGACY_SED_SUFFIX_ALIASES = (
    ("/postrun/status.json", "/postrun_manifest.json"),
    ("/postrun/errors.json", "/postrun_manifest.json"),
    ("/constitution_lint_rules/governance_rules.py", "/constitution_lint_rules/registry.py"),
)
_MIRROR_DIR_ALIASES = ("octopus-os-agent-console", "Codex_Skills_Mirror")


def _build_known_multi_repo_container_paths() -> frozenset[Path]:
    candidates: set[Path] = set()

    env_workspace_root = str(os.environ.get("CODEX_WORKSPACE_ROOT", "") or "").strip()
    if env_workspace_root:
        try:
            candidates.add(Path(env_workspace_root).expanduser().resolve())
        except Exception:
            pass

    probe_roots: list[Path] = []
    try:
        probe_roots.append(Path.cwd().resolve())
    except Exception:
        pass
    try:
        probe_roots.append(Path.home().resolve())
    except Exception:
        pass

    visited: set[Path] = set()
    for root in probe_roots:
        for candidate in [root, *root.parents]:
            if candidate in visited:
                continue
            visited.add(candidate)
            mirror_exists = any((candidate / name).exists() for name in _MIRROR_DIR_ALIASES)
            runtime_path = candidate / "Codex_Skill_Runtime"
            if not mirror_exists and not runtime_path.exists():
                continue
            candidates.add(candidate.resolve())
            if runtime_path.exists():
                try:
                    candidates.add(runtime_path.resolve())
                except Exception:
                    pass

    return frozenset(candidates)


_KNOWN_MULTI_REPO_CONTAINER_PATHS = _build_known_multi_repo_container_paths()


def _extract_command_paths(command: str) -> list[str]:
    extracted: list[str] = []
    seen: set[str] = set()
    for match in _COMMAND_PATH_RE.findall(command):
        token = str(match or "").strip().strip("\"'")
        if not token:
            continue

        if token.startswith("~"):
            token = str(Path(token).expanduser())

        try:
            path = Path(token).expanduser().resolve()
        except Exception:
            continue

        base = str(path.parent if path.is_file() else path)
        if base and base not in seen:
            seen.add(base)
            extracted.append(base)

        if len(extracted) >= 8:
            break

    return extracted


def _resolve_runtime_path(path_token: str, workdir: str | None) -> Path:
    candidate = Path(path_token).expanduser()
    if not candidate.is_absolute():
        base = Path(str(workdir or "").strip() or ".")
        candidate = base / candidate
    return candidate.resolve()


def _extract_sed_target(tokens: list[str]) -> str:
    if len(tokens) < 3:
        return ""

    for token in reversed(tokens[1:]):
        value = str(token or "").strip()
        if value and value not in {"-", "--"} and not value.startswith("-"):
            return value
    return ""


def _extract_positional_targets(tokens: list[str]) -> list[str]:
    if len(tokens) <= 1:
        return []

    targets: list[str] = []
    options_ended = False
    for token in tokens[1:]:
        value = str(token or "").strip()
        if not value:
            continue
        if value == "--" and not options_ended:
            options_ended = True
            continue
        if not options_ended and value.startswith("-"):
            continue
        targets.append(value)
    return targets


def _looks_like_glob(path_token: str) -> bool:
    value = str(path_token or "").strip()
    return any(ch in value for ch in "*?[")


def _is_known_multi_repo_container(path_value: Path) -> bool:
    try:
        resolved = path_value.resolve()
    except Exception:
        return False
    return resolved in _KNOWN_MULTI_REPO_CONTAINER_PATHS


def _normalize_skill_dir_case(path_value: Path) -> Path:
    raw = Path(path_value)
    parts = list(raw.parts)
    for idx, part in enumerate(parts):
        if part != "skills" or idx + 1 >= len(parts):
            break
        raw_skill_name = str(parts[idx + 1] or "").strip()
        canonical_skill_name = _SKILL_DIR_CASE_ALIASES.get(raw_skill_name.lower())
        if canonical_skill_name and canonical_skill_name != raw_skill_name:
            parts[idx + 1] = canonical_skill_name
            return Path(*parts)
        break
    return raw


def _suggest_legacy_python_entrypoint(resolved_script: Path) -> Path | None:
    case_normalized = _normalize_skill_dir_case(resolved_script)
    legacy_target = _LEGACY_PYTHON_ENTRYPOINT_ALIASES.get(case_normalized.name.lower())
    if legacy_target:
        case_normalized = case_normalized.with_name(legacy_target)

    if case_normalized != resolved_script and case_normalized.exists():
        return case_normalized
    return None


def _split_shell_segments(command: str) -> list[str]:
    cmd = str(command or "").strip()
    if not cmd:
        return []
    segments = [segment.strip() for segment in _SHELL_OPERATOR_RE.split(cmd) if str(segment or "").strip()]
    return segments or [cmd]


def _extract_flag_value(tokens: list[str], flag: str) -> str:
    for idx, token in enumerate(tokens):
        value = str(token or "").strip()
        if not value:
            continue
        if value == flag:
            return str(tokens[idx + 1] or "").strip() if idx + 1 < len(tokens) else ""
        if value.partition("=")[0] == flag and "=" in value:
            return value.partition("=")[2].strip()
    return ""


def _suggest_legacy_sed_target(resolved_target: Path) -> Path | None:
    target_text = str(resolved_target)
    alias_candidates = [
        Path(target_text.removesuffix(old_suffix) + new_suffix)
        for old_suffix, new_suffix in _LEGACY_SED_SUFFIX_ALIASES
        if target_text.endswith(old_suffix)
    ]
    first_candidate = alias_candidates[0] if alias_candidates else None
    return first_candidate if bool(first_candidate and first_candidate.exists()) else None


def _preflight_sed(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    target = _extract_sed_target(tokens)
    resolved_target = _resolve_runtime_path(target, workdir) if target else None
    legacy_target = _suggest_legacy_sed_target(resolved_target) if resolved_target else None
    failed_check = next(
        (
            (reason_code, detail)
            for reason_code, detail, failed in [
                (
                    "preflight_missing_sed_target",
                    "sed target path token is missing",
                    bool(not target),
                ),
                (
                    "preflight_legacy_sed_target",
                    f"sed target path is legacy or moved: {resolved_target}; use {legacy_target}",
                    bool(resolved_target and (not resolved_target.exists()) and legacy_target),
                ),
                (
                    "preflight_missing_path",
                    f"sed target path does not exist: {resolved_target}",
                    bool(resolved_target and (not resolved_target.exists()) and (not legacy_target)),
                ),
            ]
            if failed
        ),
        ("", ""),
    )
    return {
        True: (False, failed_check[0], failed_check[1]),
        False: (True, "", ""),
    }[bool(failed_check[0])]


def _preflight_ls(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    ls_targets = _extract_positional_targets(tokens)
    if not ls_targets:
        return True, "", ""

    for target in ls_targets:
        if _looks_like_glob(target):
            continue
        resolved_target = _resolve_runtime_path(target, workdir)
        if resolved_target.exists():
            continue
        return (
            False,
            "preflight_missing_path",
            f"ls target path does not exist: {resolved_target}",
        )
    return True, "", ""


def _preflight_cd(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    cd_targets = _extract_positional_targets(tokens)
    if not cd_targets:
        return True, "", ""
    resolved_target = _resolve_runtime_path(cd_targets[0], workdir)
    if not resolved_target.exists():
        return False, "preflight_missing_path", f"cd target path does not exist: {resolved_target}"
    if not resolved_target.is_dir():
        return False, "preflight_not_directory", f"cd target is not a directory: {resolved_target}"
    return True, "", ""


def _preflight_python_passthrough(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    del tokens, workdir
    return True, "", ""


def _preflight_l2_structure_writeback(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    del workdir
    active_l2_topic = _extract_flag_value(tokens, "--active-l2-topic")
    active_mother_topic = _extract_flag_value(tokens, "--active-mother-topic")
    fill_mode = _extract_flag_value(tokens, "--fill-mode").lower()
    normalized_tokens = {str(token or "").strip().lower() for token in tokens}
    qa_confirmed = "--qa-confirmed" in normalized_tokens or "--qa-confirmed=true" in normalized_tokens
    failed_check = next(
        (
            (reason_code, detail)
            for reason_code, detail, failed in [
                (
                    "preflight_missing_required_flag",
                    "l2_structure_writeback requires --active-mother-topic when --active-l2-topic is provided",
                    bool(active_l2_topic and not active_mother_topic),
                ),
                (
                    "preflight_missing_required_flag",
                    "l2_structure_writeback qa mode requires --qa-confirmed",
                    bool(fill_mode == "qa" and not qa_confirmed),
                ),
                (
                    "preflight_missing_required_flag",
                    "l2_structure_writeback qa mode requires --qa-session-id",
                    bool(fill_mode == "qa" and not _extract_flag_value(tokens, "--qa-session-id")),
                ),
            ]
            if failed
        ),
        ("", ""),
    )
    return {
        True: (False, failed_check[0], failed_check[1]),
        False: (True, "", ""),
    }[bool(failed_check[0])]


def _preflight_memory_runtime(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    del workdir
    subcommand = str(tokens[2] if len(tokens) > 2 else "").strip().lower()
    requires_flush_args = subcommand == "pre-compaction-flush"
    failed_check = next(
        (
            (reason_code, detail)
            for reason_code, detail, failed in [
                (
                    "preflight_missing_required_flag",
                    "memory_runtime pre-compaction-flush requires --session-id",
                    bool(requires_flush_args and not _extract_flag_value(tokens, "--session-id")),
                ),
                (
                    "preflight_missing_required_flag",
                    "memory_runtime pre-compaction-flush requires --content",
                    bool(requires_flush_args and not _extract_flag_value(tokens, "--content")),
                ),
            ]
            if failed
        ),
        ("", ""),
    )
    return {
        True: (False, failed_check[0], failed_check[1]),
        False: (True, "", ""),
    }[bool(failed_check[0])]


_PYTHON_SCRIPT_PREFLIGHT_HANDLERS = {
    "l2_structure_writeback.py": _preflight_l2_structure_writeback,
    "memory_runtime.py": _preflight_memory_runtime,
}


def _preflight_python(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    script_token = str(tokens[1] or "").strip() if len(tokens) > 1 else ""
    if not script_token or script_token.startswith("-"):
        return True, "", ""

    resolved_script = _resolve_runtime_path(script_token, workdir)
    if not resolved_script.exists():
        suggested = _suggest_legacy_python_entrypoint(resolved_script)
        if suggested is not None:
            return (
                False,
                "preflight_legacy_python_entrypoint",
                f"python script path is legacy or case-mismatched: {resolved_script}; use {suggested}",
            )
        return (
            False,
            "preflight_missing_path",
            f"python script path does not exist: {resolved_script}",
        )

    task_context_token = _extract_flag_value(tokens, "--task-context")
    missing_task_context = bool(task_context_token) and (
        not _resolve_runtime_path(task_context_token, workdir).exists()
    )
    if missing_task_context:
        resolved_task_context = _resolve_runtime_path(task_context_token, workdir)
        return (
            False,
            "preflight_missing_path",
            f"python --task-context path does not exist: {resolved_task_context}",
        )

    if resolved_script.name != "meta_github_operation_family.py":
        handler = _PYTHON_SCRIPT_PREFLIGHT_HANDLERS.get(resolved_script.name, _preflight_python_passthrough)
        return handler(tokens, workdir)

    snapshot_scope = _extract_flag_value(tokens, "--snapshot-scope").lower()
    if snapshot_scope not in {"thread-owned", "run-owned"}:
        return True, "", ""
    return (
        False,
        "preflight_own_thread_scope_blocked",
        f"meta_github_operation with --snapshot-scope {snapshot_scope} is blocked in runtime selfcheck; use all_threads aggregation and apply_patch writeback flow",
    )

    return True, "", ""


def _preflight_git(tokens: list[str], workdir: str | None) -> tuple[bool, str, str]:
    candidates: list[str] = []
    for idx, token in enumerate(tokens):
        value = str(token or "").strip()
        if value == "-C":
            if idx + 1 >= len(tokens):
                return False, "preflight_git_c_missing_path", "git -C requires a path argument"
            candidates.append(str(tokens[idx + 1] or "").strip())
        elif value.startswith("-C") and len(value) > 2:
            candidates.append(value[2:])

    for candidate in candidates:
        resolved_target = _resolve_runtime_path(candidate, workdir)
        if not resolved_target.exists():
            return (
                False,
                "preflight_missing_path",
                f"git -C target path does not exist: {resolved_target}",
            )
        if not resolved_target.is_dir():
            return (
                False,
                "preflight_not_directory",
                f"git -C target is not a directory: {resolved_target}",
            )

        repo_root = _detect_repo_root(str(resolved_target), timeout_sec=3)
        is_container_path = _is_known_multi_repo_container(resolved_target)
        if is_container_path or not repo_root:
            reason_code = "preflight_git_container_path_blocked" if is_container_path else "preflight_not_git_repo"
            detail = (
                f"git -C target is a multi-repo container path, not a git repository root: {resolved_target}"
                if is_container_path
                else f"git -C target is not a git repository: {resolved_target}"
            )
            return (
                False,
                reason_code,
                detail,
            )
    return True, "", ""


def _preflight_segment(*, segment: str, workdir: str | None) -> tuple[bool, str, str]:
    try:
        tokens = shlex.split(segment)
    except ValueError as exc:
        return False, "preflight_parse_error", normalize_text(str(exc), limit=200)

    if not tokens:
        return False, "preflight_empty_command", "command has no executable token"

    executable = str(tokens[0] or "").strip().lower()
    handlers = {
        "sed": _preflight_sed,
        "ls": _preflight_ls,
        "cd": _preflight_cd,
        "python": _preflight_python,
        "python3": _preflight_python,
        "git": _preflight_git,
    }
    handler = handlers.get(executable)
    if handler is None:
        return True, "", ""
    return handler(tokens, workdir)


def preflight(*, command: str, workdir: str | None) -> tuple[bool, str, str]:
    cmd = str(command or "").strip()
    if not cmd:
        return False, "preflight_empty_command", "command is empty"

    active_workdir = str(workdir or "").strip() or None
    for segment in _split_shell_segments(cmd):
        ok, reason_code, detail = _preflight_segment(segment=segment, workdir=active_workdir)
        if not ok:
            return ok, reason_code, detail
        try:
            tokens = shlex.split(segment)
        except Exception:
            tokens = []
        executable = str(tokens[0] or "").strip().lower() if tokens else ""
        if executable == "cd":
            cd_targets = _extract_positional_targets(tokens)
            active_workdir = str(_resolve_runtime_path(cd_targets[0], active_workdir)) if cd_targets else active_workdir

    return True, "", ""


def _detect_repo_root(candidate_dir: str, timeout_sec: int) -> str:
    target = str(candidate_dir or "").strip()
    if not target:
        return ""

    try:
        proc = subprocess.run(
            ["git", "-C", target, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=max(1, int(timeout_sec)),
        )
    except Exception:
        return ""

    if proc.returncode != 0:
        return ""
    return str(proc.stdout or "").strip()


def _resolve_default_repo_root(change_detection_root: str, timeout_sec: int) -> str:
    direct = _detect_repo_root(change_detection_root, timeout_sec)
    if direct:
        return direct

    try:
        cwd = str(Path.cwd())
    except Exception:
        return ""

    return _detect_repo_root(cwd, timeout_sec)


def _git_path_snapshot(repo_root: str, timeout_sec: int) -> set[str]:
    if not repo_root:
        return set()

    paths: set[str] = set()
    commands = (
        (["git", "-C", repo_root, "diff", "--name-only"], "tracked"),
        (["git", "-C", repo_root, "ls-files", "--others", "--exclude-standard"], "untracked"),
    )
    for cmd, prefix in commands:
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max(1, int(timeout_sec)),
            )
        except Exception:
            continue

        if proc.returncode != 0:
            continue

        for line in (proc.stdout or "").splitlines():
            value = line.strip()
            if value:
                paths.add(f"{prefix}:{value}")

    return paths


def detect_preexisting_changes(
    *,
    change_detection_root: str | None,
    timeout_sec: int,
) -> dict[str, Any]:
    resolved_timeout = max(1, int(timeout_sec))
    repo_root = _resolve_default_repo_root(str(change_detection_root or "").strip(), resolved_timeout)
    snapshot = _git_path_snapshot(repo_root, resolved_timeout) if repo_root else set()
    return {
        "change_detection_supported": bool(repo_root),
        "repo_root": repo_root,
        "all_changed_paths": sorted(snapshot),
        "all_changed_path_count": len(snapshot),
    }


def execute_command_list(
    *,
    commands: list[str],
    timeout_sec: int,
    workdir: str,
    change_detection_root: str | None = None,
) -> dict[str, Any]:
    resolved_timeout = max(1, int(timeout_sec))
    resolved_workdir = str(workdir or "").strip() or None
    default_repo_root = _resolve_default_repo_root(str(change_detection_root or "").strip(), resolved_timeout)

    runs: list[dict[str, Any]] = []
    all_changed_paths: set[str] = set()
    change_detection_supported = bool(default_repo_root)
    preflight_reason_codes: list[str] = []
    preflight_failed_commands = 0

    for idx, command in enumerate(commands, start=1):
        cmd = str(command or "").strip()
        if not cmd:
            continue

        started_ts = time.time()
        preflight_ok, preflight_reason_code, preflight_detail = preflight(
            command=cmd,
            workdir=resolved_workdir,
        )
        if not preflight_ok:
            preflight_failed_commands += 1
            if preflight_reason_code:
                preflight_reason_codes.append(preflight_reason_code)
            runs.append(
                {
                    "index": idx,
                    "command": cmd,
                    "status": "preflight_blocked",
                    "exit_code": -1,
                    "duration_sec": round(max(0.0, time.time() - started_ts), 3),
                    "stdout_preview": "",
                    "stderr_preview": normalize_text(preflight_detail, limit=400),
                    "changed_paths": [],
                    "changed_file_count": 0,
                    "preflight_reason_code": preflight_reason_code,
                }
            )
            continue

        command_repo_root = ""
        for candidate in _extract_command_paths(cmd):
            command_repo_root = _detect_repo_root(candidate, resolved_timeout)
            if command_repo_root:
                break

        active_repo_root = command_repo_root or default_repo_root
        if active_repo_root:
            change_detection_supported = True

        before_snapshot = _git_path_snapshot(active_repo_root, resolved_timeout) if active_repo_root else set()

        status = "error"
        exit_code = -1
        stdout_preview = ""
        stderr_preview = ""

        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=resolved_workdir,
                timeout=resolved_timeout,
            )
            status = "ok" if proc.returncode == 0 else "error"
            exit_code = int(proc.returncode)
            stdout_preview = normalize_text((proc.stdout or "").strip(), limit=400)
            stderr_preview = normalize_text((proc.stderr or "").strip(), limit=400)
        except subprocess.TimeoutExpired as exc:
            status = "timeout"
            stdout_preview = normalize_text(str(exc.stdout or "").strip(), limit=400)
            stderr_preview = normalize_text(str(exc.stderr or "").strip(), limit=400)
        except Exception as exc:
            stderr_preview = normalize_text(str(exc), limit=400)

        after_snapshot = _git_path_snapshot(active_repo_root, resolved_timeout) if active_repo_root else set()
        changed_paths = sorted(after_snapshot.symmetric_difference(before_snapshot))
        if changed_paths:
            all_changed_paths.update(changed_paths)

        runs.append(
            {
                "index": idx,
                "command": cmd,
                "status": status,
                "exit_code": exit_code,
                "duration_sec": round(max(0.0, time.time() - started_ts), 3),
                "stdout_preview": stdout_preview,
                "stderr_preview": stderr_preview,
                "changed_paths": changed_paths,
                "changed_file_count": len(changed_paths),
            }
        )

    success = sum(1 for row in runs if str(row.get("status", "")).lower() == "ok")
    failed = sum(1 for row in runs if str(row.get("status", "")).lower() != "ok")
    return {
        "total_commands": len(runs),
        "success_commands": success,
        "failed_commands": failed,
        "all_succeeded": len(runs) > 0 and failed == 0,
        "change_detection_supported": change_detection_supported,
        "runs": runs,
        "all_changed_paths": sorted(all_changed_paths),
        "all_changed_path_count": len(all_changed_paths),
        "preflight_failed_commands": preflight_failed_commands,
        "preflight_reason_codes": sorted(set(x for x in preflight_reason_codes if str(x).strip())),
    }
