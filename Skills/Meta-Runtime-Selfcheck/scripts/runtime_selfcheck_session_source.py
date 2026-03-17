from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
import re
import shlex
from pathlib import Path
from typing import Callable
from typing import Any

from runtime_pain_observability import normalize_text
from runtime_pain_types import SessionExecEvent
from runtime_pain_types import ExpectedFailureRule
from runtime_pain_types import SessionFallbackQueue
from runtime_pain_types import TurnEvidence
from runtime_selfcheck_command_governance import analyze_runtime_failure
from runtime_selfcheck_command_governance import derive_command_context
from runtime_selfcheck_store import load_turn_audit


SESSION_ID_RE = re.compile(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$")
EXIT_CODE_RE = re.compile(r"Process exited with code (?P<code>\d+)")
UNKNOWN_OPTION_RE = re.compile(r"No such option:\s+(--[A-Za-z0-9][A-Za-z0-9-]*)")
UNKNOWN_COMMAND_RE = re.compile(r"(?:No such command|invalid choice):?\s+'?([A-Za-z0-9_-]+)'?")


@dataclass
class PendingToolCall:
    call_id: str
    tool_name: str
    raw_input: str
    timestamp: str
    parsed_command: "ParsedExecCommand"


@dataclass(frozen=True)
class ParsedExecCommand:
    command: str
    signature: str
    trigger_script: str
    trigger_node: str


def _latest_turn(turns: list[TurnEvidence]) -> TurnEvidence:
    ordered = sorted(
        turns,
        key=lambda row: (
            str(row.get("completed_at", "") or row.get("started_at", "") or ""),
            str(row.get("turn_id", "") or ""),
        ),
        reverse=True,
    )
    return ordered[0] if ordered else {}


def resolve_codex_home(override: str | None = None) -> Path:
    candidates: list[Path] = []
    if override:
        candidates.append(Path(os.path.expanduser(override)))
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        candidates.append((repo_root.parent / ".codex").resolve())
    env_home = str(os.environ.get("CODEX_HOME", "") or "").strip()
    if env_home:
        candidates.append(Path(os.path.expanduser(env_home)))
    candidates.append(Path.home() / ".codex")
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate.resolve()
    raise FileNotFoundError("Cannot resolve Codex home from override, workspace, $CODEX_HOME, or ~/.codex")


def _latest_named_path(root: Path, *, predicate: Callable[[Path], bool]) -> Path | None:
    candidates = [path for path in root.iterdir() if predicate(path)]
    return max(candidates, key=lambda path: path.name, default=None)


def _find_latest_session_file_structured(sessions_path: Path) -> Path | None:
    if not sessions_path.exists():
        return None

    years = sorted(
        [path for path in sessions_path.iterdir() if path.is_dir() and path.name.isdigit()],
        key=lambda path: path.name,
        reverse=True,
    )
    for year_dir in years:
        months = sorted(
            [path for path in year_dir.iterdir() if path.is_dir() and path.name.isdigit()],
            key=lambda path: path.name,
            reverse=True,
        )
        for month_dir in months:
            days = sorted(
                [path for path in month_dir.iterdir() if path.is_dir() and path.name.isdigit()],
                key=lambda path: path.name,
                reverse=True,
            )
            for day_dir in days:
                latest_file = _latest_named_path(day_dir, predicate=lambda path: path.is_file() and path.suffix == ".jsonl")
                if latest_file is not None:
                    return latest_file
    return None


def find_session_files(
    codex_home: Path,
    session_id_filter: str | None = None,
    *,
    newest_first: bool = False,
    limit: int | None = None,
) -> list[Path]:
    sessions_path = codex_home / "sessions"
    if not sessions_path.exists():
        return []
    if session_id_filter:
        matches = sorted(
            (path for path in sessions_path.rglob(f"*{session_id_filter}*.jsonl") if path.is_file()),
            reverse=newest_first,
        )
        return matches[:limit] if limit is not None else matches
    if newest_first and limit == 1:
        latest_file = _find_latest_session_file_structured(sessions_path)
        return [latest_file] if latest_file is not None else []
    matches = sorted((path for path in sessions_path.rglob("*.jsonl") if path.is_file()), reverse=newest_first)
    return matches[:limit] if limit is not None else matches


def _session_id_from_path(path: Path) -> str | None:
    match = SESSION_ID_RE.search(path.stem)
    return match.group(1) if match else None


def _trim_message(text: str, limit: int = 220) -> str:
    return normalize_text(text, limit=limit)


def _normalize_command_signature(command: str) -> str:
    text = str(command or "").strip()
    if not text:
        return ""
    text = re.sub(r"/[^ ]+?/(?:\\.codex/skills|AI_Projects/Otctopus_OS_AgentConsole/Skills)/", "<SKILL_ROOT>/", text)
    text = re.sub(r"([0-9a-f]{8}-[0-9a-f-]{20,})", "<ID>", text)
    text = re.sub(r"\s+", " ", text)
    return text[:360]


def _extract_exec_command(raw_input: str) -> str:
    try:
        payload = json.loads(raw_input)
    except json.JSONDecodeError:
        return ""
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("cmd", "") or "").strip()


def _split_command_tokens(command: str) -> tuple[str, ...]:
    try:
        return tuple(shlex.split(command))
    except ValueError:
        return ()


def _infer_trigger_script(tokens: tuple[str, ...]) -> str:
    for token in tokens[1:]:
        if token.endswith(".py"):
            return Path(token).name
    return str(tokens[0] if tokens else "").strip()


def _infer_trigger_node(command: str, tokens: tuple[str, ...]) -> str:
    script = _infer_trigger_script(tokens)
    if script:
        return script
    return str(command.split(" ", 1)[0]).strip()


def _parse_exec_command(raw_input: str) -> ParsedExecCommand:
    command = _extract_exec_command(raw_input)
    tokens = _split_command_tokens(command)
    return ParsedExecCommand(
        command=command,
        signature=_normalize_command_signature(command),
        trigger_script=_infer_trigger_script(tokens),
        trigger_node=_infer_trigger_node(command, tokens),
    )


def _parse_exec_event(
    *,
    session_id: str,
    turn_id: str,
    session_file: Path,
    timestamp: str,
    line_no: int,
    cwd: str | None,
    tool: PendingToolCall,
    output_text: str,
) -> SessionExecEvent:
    exit_match = EXIT_CODE_RE.search(output_text)
    exit_code = int(exit_match.group("code")) if exit_match else 0
    status = "error" if exit_code != 0 or "Traceback" in output_text else "ok"
    return {
        "session_id": session_id,
        "turn_id": turn_id,
        "timestamp": timestamp,
        "session_file": str(session_file),
        "citation": f"{session_file}:{line_no}",
        "cwd": str(cwd or ""),
        "tool_name": tool.tool_name,
        "call_id": tool.call_id,
        "raw_input": tool.raw_input,
        "command_preview": _trim_message(tool.parsed_command.command, limit=420),
        "command_signature": tool.parsed_command.signature,
        "trigger_script": tool.parsed_command.trigger_script,
        "trigger_node": tool.parsed_command.trigger_node,
        "output_preview": _trim_message(output_text, limit=400),
        "output_raw": output_text,
        "status": status,
        "exit_code": exit_code,
    }


def _collect_turns_from_session_file(
    session_file: Path,
    *,
    session_id: str,
    turn_id_filter: str | None = None,
) -> list[TurnEvidence]:
    turns: list[TurnEvidence] = []
    pending_tools: dict[str, PendingToolCall] = {}
    current_turn: TurnEvidence | None = None
    current_cwd = ""
    with session_file.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = entry.get("payload", {})
            if not isinstance(payload, dict):
                continue
            entry_type = str(entry.get("type", "") or "")
            timestamp = str(entry.get("timestamp", "") or "")
            if entry_type == "session_meta":
                current_cwd = str(payload.get("cwd", "") or current_cwd)
                continue
            if entry_type == "turn_context":
                current_cwd = str(payload.get("cwd", "") or current_cwd)
                if current_turn is not None:
                    current_turn["cwd"] = current_cwd
                continue
            if entry_type == "event_msg":
                event_type = str(payload.get("type", "") or "")
                if event_type == "task_started":
                    turn_id = str(payload.get("turn_id", "") or "").strip()
                    if turn_id_filter and turn_id != turn_id_filter:
                        current_turn = None
                        pending_tools.clear()
                        continue
                    current_turn = {
                        "session_id": session_id,
                        "turn_id": turn_id,
                        "session_file": str(session_file),
                        "started_at": timestamp,
                        "completed_at": "",
                        "cwd": current_cwd,
                        "user_message": "",
                        "assistant_messages": [],
                        "tool_events": [],
                        "final_reply": "",
                        "status": "active",
                    }
                    turns.append(current_turn)
                    pending_tools.clear()
                    continue
                if current_turn is None:
                    continue
                if event_type == "user_message":
                    current_turn["user_message"] = str(payload.get("message", "") or "")
                    continue
                if event_type == "agent_message":
                    message = str(payload.get("message", "") or "").strip()
                    if message:
                        current_turn["assistant_messages"].append(message)
                    continue
                if event_type == "task_complete":
                    current_turn["completed_at"] = timestamp
                    current_turn["final_reply"] = str(payload.get("last_agent_message", "") or "")
                    current_turn["status"] = "completed"
                    continue
            if entry_type != "response_item" or current_turn is None:
                continue
            payload_type = str(payload.get("type", "") or "")
            if payload_type == "function_call":
                tool_name = str(payload.get("name", "") or "")
                pending_tools[str(payload.get("call_id", "") or "")] = PendingToolCall(
                    call_id=str(payload.get("call_id", "") or ""),
                    tool_name=tool_name,
                    raw_input=str(payload.get("arguments", "") or ""),
                    timestamp=timestamp,
                    parsed_command=_parse_exec_command(str(payload.get("arguments", "") or ""))
                    if tool_name == "exec_command"
                    else ParsedExecCommand(command="", signature="", trigger_script="", trigger_node=""),
                )
                continue
            if payload_type == "function_call_output":
                call_id = str(payload.get("call_id", "") or "")
                tool = pending_tools.pop(call_id, None)
                if tool is None or tool.tool_name != "exec_command":
                    continue
                current_turn["tool_events"].append(
                    _parse_exec_event(
                        session_id=session_id,
                        turn_id=str(current_turn.get("turn_id", "") or ""),
                        session_file=session_file,
                        timestamp=timestamp,
                        line_no=line_no,
                        cwd=str(current_turn.get("cwd", "") or ""),
                        tool=tool,
                        output_text=str(payload.get("output", "") or ""),
                    )
                )
                continue
            if payload_type == "message" and payload.get("role") == "assistant":
                chunks = payload.get("content", [])
                if isinstance(chunks, list):
                    rendered = "\n".join(
                        str(item.get("text", "") or "").strip()
                        for item in chunks
                        if isinstance(item, dict) and str(item.get("text", "") or "").strip()
                    ).strip()
                    if rendered:
                        current_turn["assistant_messages"].append(rendered)
    return turns


def load_target_turn_evidence(
    *,
    codex_home_override: str | None = None,
    session_id_filter: str | None = None,
    turn_id_filter: str | None = None,
) -> TurnEvidence | None:
    codex_home = resolve_codex_home(codex_home_override)
    if session_id_filter:
        session_files = find_session_files(codex_home, session_id_filter=session_id_filter, newest_first=True)
    elif turn_id_filter:
        session_files = find_session_files(codex_home, newest_first=True)
    else:
        session_files = find_session_files(codex_home, newest_first=True, limit=1)

    for session_file in session_files:
        session_id = _session_id_from_path(session_file)
        if session_id is None:
            continue
        turns = _collect_turns_from_session_file(
            session_file,
            session_id=session_id,
            turn_id_filter=turn_id_filter,
        )
        if turns:
            return _latest_turn(turns)
    return None


def collect_turn_evidence(
    *,
    codex_home_override: str | None = None,
    session_id_filter: str | None = None,
    turn_id_filter: str | None = None,
) -> list[TurnEvidence]:
    codex_home = resolve_codex_home(codex_home_override)
    session_files = find_session_files(codex_home, session_id_filter=session_id_filter)
    turns: list[TurnEvidence] = []
    for session_file in session_files:
        session_id = _session_id_from_path(session_file)
        if session_id is None:
            continue
        turns.extend(
            _collect_turns_from_session_file(
                session_file,
                session_id=session_id,
                turn_id_filter=turn_id_filter,
            )
        )
    return turns


def _repo_truth_candidate(installed_path: str) -> str:
    if "/.codex/skills/" not in installed_path:
        return ""
    before, _, after = installed_path.partition("/.codex/skills/")
    skill_name, _, suffix = after.partition("/")
    if not skill_name:
        return ""
    candidate = Path(before) / "AI_Projects" / "Otctopus_OS_AgentConsole" / "Skills" / skill_name / suffix
    return str(candidate.resolve()) if candidate.exists() else ""


def _rewrite_installed_copy_command(command: str) -> str:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return ""
    changed = False
    rewritten: list[str] = []
    for token in tokens:
        if "/.codex/skills/" not in token:
            rewritten.append(token)
            continue
        candidate = _repo_truth_candidate(token)
        if candidate:
            rewritten.append(candidate)
            changed = True
        else:
            rewritten.append(token)
    if not changed:
        return ""
    return shlex.join(rewritten)


def _remove_flag(command: str, flag: str) -> str:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return ""
    result: list[str] = []
    skip_next = False
    changed = False
    for index, token in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue
        if token == flag:
            changed = True
            skip_next = index + 1 < len(tokens) and not str(tokens[index + 1]).startswith("-")
            continue
        if token.startswith(f"{flag}="):
            changed = True
            continue
        result.append(token)
    return shlex.join(result) if changed else ""


def _replace_cli_subcommand(command: str, *, from_name: str, to_name: str) -> str:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return ""
    for index, token in enumerate(tokens):
        if token.endswith(".py") and index + 1 < len(tokens) and tokens[index + 1] == from_name:
            tokens[index + 1] = to_name
            return shlex.join(tokens)
    return ""


def _build_fix_surface(
    *,
    issue_kind: str,
    issue_subkind: str,
    command: str,
) -> dict[str, str]:
    if issue_subkind == "installed_copy_product_root_mismatch":
        return {
            "owner_surface": "skill_runtime_surface",
            "canonical_fix_surface": "repo_truth_source_routing",
            "repair_boundary": "rewrite_runtime_command_only",
            "evidence_route": "session_exec_output",
        }
    if issue_subkind in {"unknown_option", "unknown_subcommand"}:
        return {
            "owner_surface": "cli_contract_and_preflight",
            "canonical_fix_surface": "command_surface_semantics",
            "repair_boundary": "bounded_command_normalization",
            "evidence_route": "session_exec_output",
        }
    if issue_kind == "trial_and_error_loop":
        return {
            "owner_surface": "turn_hook_retry_policy",
            "canonical_fix_surface": "retry_and_fallback_policy",
            "repair_boundary": "governed_retry_stop_rule",
            "evidence_route": "session_command_repetition",
        }
    if "git -C" in command:
        return {
            "owner_surface": "path_and_workdir_preflight",
            "canonical_fix_surface": "repo_root_resolution",
            "repair_boundary": "preflight_block_or_retarget",
            "evidence_route": "session_exec_output",
        }
    return {
        "owner_surface": "runtime_turn_hook",
        "canonical_fix_surface": "turn_local_issue_mapping",
        "repair_boundary": "local_diagnose_and_disclose",
        "evidence_route": "session_exec_output",
    }


def _auto_repair_for_issue(issue: dict[str, Any]) -> dict[str, Any]:
    source_event = issue.get("source_event", {}) if isinstance(issue.get("source_event", {}), dict) else {}
    command = str(source_event.get("command_preview", "") or "")
    subkind = str(issue.get("issue_subkind", "") or "")
    context = derive_command_context(command, workdir=str(source_event.get("cwd", "") or ""))

    def _with_context(payload: dict[str, Any]) -> dict[str, Any]:
        if not payload:
            return payload
        payload["workdir"] = str(context.get("workdir", "") or "")
        payload["change_detection_root"] = str(context.get("change_detection_root", "") or "")
        return payload

    if subkind == "installed_copy_product_root_mismatch":
        normalized = _rewrite_installed_copy_command(command)
        if normalized:
            return _with_context({"repair_type": "rerun_with_repo_truth_source", "command": normalized})
    if subkind == "unknown_subcommand":
        normalized = _replace_cli_subcommand(command, from_name="contract", to_name="runtime-contract")
        if normalized:
            return _with_context({"repair_type": "normalize_cli_subcommand", "command": normalized})
    if subkind == "unknown_option" and "--repo" in command and "push-contract" in command:
        normalized = _remove_flag(command, "--repo")
        if normalized:
            return _with_context({"repair_type": "drop_unknown_option", "command": normalized})
    return {}


def _issue_record(
    *,
    session_id: str,
    turn_id: str,
    timestamp: str,
    priority: str,
    issue_kind: str,
    issue_subkind: str,
    title: str,
    summary: str,
    why: str,
    suggested_action: str,
    source_event: dict[str, Any],
) -> dict[str, Any]:
    command_signature = str(source_event.get("command_signature", "") or "")
    optimization_id = hashlib.sha256(
        f"{session_id}|{turn_id}|{issue_kind}|{issue_subkind}|{command_signature}".encode("utf-8")
    ).hexdigest()[:24]
    fix_surface = _build_fix_surface(
        issue_kind=issue_kind,
        issue_subkind=issue_subkind,
        command=str(source_event.get("command_preview", "") or ""),
    )
    issue = {
        "optimization_id": optimization_id,
        "session_id": session_id,
        "thread_id": turn_id,
        "updated_at": timestamp,
        "priority": priority,
        "kind": issue_kind,
        "issue_subkind": issue_subkind,
        "pain_topic": f"{issue_kind}:{issue_subkind}",
        "pain_signature": f"{issue_kind}|{issue_subkind}|{command_signature}",
        "pain_consistency_hash": hashlib.sha256(f"{issue_kind}|{issue_subkind}|{command_signature}".encode("utf-8")).hexdigest()[:16],
        "title": title,
        "summary": summary,
        "why": why,
        "suggested_action": suggested_action,
        "citation": str(source_event.get("citation", "") or ""),
        "source_event": {
            **source_event,
            **fix_surface,
        },
    }
    auto_repair = _auto_repair_for_issue(issue)
    if auto_repair:
        issue["auto_repair"] = auto_repair
    return issue


def _detect_event_issues(
    event: dict[str, Any],
    *,
    stage: str | None = None,
    expected_failure_rules: list[ExpectedFailureRule] | None = None,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if str(event.get("status", "") or "") != "error":
        return issues
    output_raw = str(event.get("output_raw", "") or "")
    command = str(event.get("command_preview", "") or "")
    session_id = str(event.get("session_id", "") or "")
    turn_id = str(event.get("turn_id", "") or "")
    timestamp = str(event.get("timestamp", "") or "")
    lowered = output_raw.lower()
    governance_issue = analyze_runtime_failure(
        command=command,
        output_text=output_raw,
        workdir=str(event.get("cwd", "") or ""),
        stage=stage,
        expected_failure_rules=expected_failure_rules,
    )
    if governance_issue.get("matched"):
        issues.append(
            _issue_record(
                session_id=session_id,
                turn_id=turn_id,
                timestamp=timestamp,
                priority="p1",
                issue_kind=str(governance_issue.get("issue_kind", "") or "runtime_governance_gap"),
                issue_subkind=str(governance_issue.get("issue_subkind", "") or "governance_gap"),
                title=str(governance_issue.get("title", "") or "Runtime governance gap detected"),
                summary=str(governance_issue.get("summary", "") or ""),
                why=str(governance_issue.get("why", "") or ""),
                suggested_action=str(governance_issue.get("suggested_action", "") or ""),
                source_event=event,
            )
        )
        latest_issue = issues[-1]
        latest_issue["adjudication"] = str(governance_issue.get("adjudication", "") or "")
        latest_issue["expected_failure"] = governance_issue.get("expected_failure", {"matched": False})
        auto_repair = governance_issue.get("auto_repair", {})
        if isinstance(auto_repair, dict) and str(auto_repair.get("normalized_command", "") or "").strip():
            latest_issue["auto_repair"] = {
                "repair_type": ",".join(list(auto_repair.get("repair_types", []))) or "governed_command_normalization",
                "command": str(auto_repair.get("normalized_command", "") or ""),
                "workdir": str(auto_repair.get("context", {}).get("workdir", "") or event.get("cwd", "") or ""),
                "change_detection_root": str(auto_repair.get("context", {}).get("change_detection_root", "") or event.get("cwd", "") or ""),
                "decision": str(governance_issue.get("adjudication", "") or ""),
            }
        return issues

    if "cannot resolve product root" in lowered and "/.codex/skills/" in command:
        issues.append(
            _issue_record(
                session_id=session_id,
                turn_id=turn_id,
                timestamp=timestamp,
                priority="p0",
                issue_kind="wrong_runtime_surface",
                issue_subkind="installed_copy_product_root_mismatch",
                title="Installed skill copy was used as runtime source",
                summary="命令命中了 ~/.codex/skills 安装副本，脚本在安装态无法解析产品根，运行直接失败。",
                why="运行面选择错到了 installed copy，而不是 repo truth source。",
                suggested_action="把受管技能 CLI 重写到仓内真源，并在 preflight 阶段优先阻断安装副本路径。",
                source_event=event,
            )
        )
    unknown_option = UNKNOWN_OPTION_RE.search(output_raw)
    if unknown_option:
        option = unknown_option.group(1)
        issues.append(
            _issue_record(
                session_id=session_id,
                turn_id=turn_id,
                timestamp=timestamp,
                priority="p1",
                issue_kind="cli_semantic_mismatch",
                issue_subkind="unknown_option",
                title=f"CLI option is not supported: {option}",
                summary="命令参数在 CLI 表面不存在，失败发生在执行后而不是 preflight。",
                why="CLI 语义层没有被 turn hook 事前验证，导致多一次无效调用。",
                suggested_action="为受管 Python CLI 增加 help-introspection preflight，并输出 canonical option surface。",
                source_event=event,
            )
        )
    unknown_command = UNKNOWN_COMMAND_RE.search(output_raw)
    if unknown_command:
        subcommand = unknown_command.group(1)
        issues.append(
            _issue_record(
                session_id=session_id,
                turn_id=turn_id,
                timestamp=timestamp,
                priority="p1",
                issue_kind="cli_semantic_mismatch",
                issue_subkind="unknown_subcommand",
                title=f"CLI subcommand is not supported: {subcommand}",
                summary="命令子命令不存在，当前 turn hook 缺少 CLI 语义预判与 canonical 命令重写。",
                why="CLI facade 与实际 parser 不一致，导致运行期才暴露语义错配。",
                suggested_action="在 preflight 阶段校验 subcommand，并对受管 alias 输出 canonical 命令。",
                source_event=event,
            )
        )
    if "not a git repository" in lowered or "git -c target is not a git repository" in lowered:
        issues.append(
            _issue_record(
                session_id=session_id,
                turn_id=turn_id,
                timestamp=timestamp,
                priority="p1",
                issue_kind="path_misuse",
                issue_subkind="non_repo_git_target",
                title="Git command targeted a non-repository path",
                summary="命令工作目录或 git -C 目标不是仓库根，说明 path/workdir preflight 仍有漏洞。",
                why="当前 hook 还不能稳定把容器路径、repo 根和普通目录区分开。",
                suggested_action="补齐 repo root 解析与 git 容器路径阻断，并在 repair 时改写到 canonical repo root。",
                source_event=event,
            )
        )
    return issues


def build_session_fallback_queue(
    *,
    turns: list[TurnEvidence] | None = None,
    codex_home_override: str | None = None,
    session_id_filter: str | None = None,
    turn_id_filter: str | None = None,
    include_resolved: bool = True,
    max_results: int = 200,
    expected_failure_rules: list[ExpectedFailureRule] | None = None,
    stage: str | None = None,
) -> SessionFallbackQueue:
    selected_turns = turns
    if selected_turns is None:
        selected_turns = collect_turn_evidence(
            codex_home_override=codex_home_override,
            session_id_filter=session_id_filter,
            turn_id_filter=turn_id_filter,
        )
    items: list[dict[str, Any]] = []
    for turn in selected_turns:
        session_id = str(turn.get("session_id", "") or "")
        turn_id = str(turn.get("turn_id", "") or "")
        resolved_ids: set[str] = set()
        try:
            audit = load_turn_audit(session_id, turn_id)
        except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError):
            audit = {}
        if isinstance(audit, dict):
            resolved_ids = {
                str(item).strip()
                for item in list(audit.get("resolved_optimization_ids", []))
                if str(item).strip()
            }

        event_issues: list[dict[str, object]] = []
        failed_signatures: list[str] = []
        failed_signature_events: dict[str, dict[str, Any]] = {}
        for event in turn.get("tool_events", []):
            if not isinstance(event, dict):
                continue
            issues = _detect_event_issues(
                event,
                stage=stage,
                expected_failure_rules=expected_failure_rules,
            )
            event_issues.extend(issues)
            if str(event.get("status", "") or "") == "error":
                signature = str(event.get("command_signature", "") or "")
                if signature:
                    failed_signatures.append(signature)
                    failed_signature_events.setdefault(signature, event)

        for signature, count in Counter(failed_signatures).items():
            if count < 2:
                continue
            event = failed_signature_events.get(signature, {})
            event_issues.append(
                _issue_record(
                    session_id=session_id,
                    turn_id=turn_id,
                    timestamp=str(turn.get("completed_at", "") or turn.get("started_at", "") or ""),
                    priority="p1",
                    issue_kind="trial_and_error_loop",
                    issue_subkind="repeat_failed_command",
                    title="Same command failed repeatedly in one turn",
                    summary=f"同一命令签名在单回合内失败 {count} 次，说明 turn hook 缺少停止条件或回退分流。",
                    why="相同失败未被及时归因并阻断，模型只能靠当场试错收敛。",
                    suggested_action="为同签名失败增加 stop rule、fallback route 和 turn-local audit closeout。",
                    source_event=event,
                )
            )

        for issue in event_issues:
            issue["is_resolved"] = issue["optimization_id"] in resolved_ids
            expected_failure = issue.get("expected_failure", {})
            if isinstance(expected_failure, dict) and bool(expected_failure.get("matched")):
                issue["is_resolved"] = True
            if include_resolved or not issue["is_resolved"]:
                items.append(issue)

    items.sort(
        key=lambda row: (
            0 if bool(row.get("is_resolved", False)) else 1,
            {"p0": 3, "p1": 2, "p2": 1}.get(str(row.get("priority", "p2") or "p2"), 0),
            str(row.get("updated_at", "") or ""),
            str(row.get("optimization_id", "") or ""),
        ),
        reverse=True,
    )
    limited = items[: max(1, int(max_results))]
    return {
        "source_mode": "session_fallback",
        "total_items": len(limited),
        "pending_items": sum(1 for item in limited if not bool(item.get("is_resolved", False))),
        "resolved_items": sum(1 for item in limited if bool(item.get("is_resolved", False))),
        "session_scope_mode": "all_threads",
        "thread_id": turn_id_filter or "all_threads",
        "items": limited,
    }
