#!/usr/bin/env python3
"""
@scenario: tooling
@dept: codex_skill
@purpose: cli_entry
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable, List, Dict, Any, Set

OBSERVABILITY_CHANNELS = {
    "machine_log": "Codex_Skill_Runtime/4-Branch-Chat/machine.jsonl",
    "human_log": "Codex_Skill_Runtime/4-Branch-Chat/human.log",
    "result_anchor": "Codex_Skills_Result/4-Branch-Chat",
    "project_machine_log": "logs/machine.jsonl",
    "project_human_log": "logs/human.log",
}

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]+")
STOPWORDS = {
    "the",
    "a",
    "an",
    "to",
    "of",
    "in",
    "for",
    "and",
    "or",
    "is",
    "are",
    "我",
    "你",
    "他",
    "她",
    "它",
    "这个",
    "那个",
    "什么",
    "怎么",
    "为什么",
    "一下",
    "一下子",
    "里面",
    "最新",
    "几次",
    "时候",
    "非常",
    "想要",
    "知道",
}


def resolve_query_id(session_id: str | None, resume_id: str | None) -> str:
    value = (session_id or resume_id or "").strip()
    if not value:
        raise ValueError("Missing id. Provide --session-id or --resume-id.")
    return value


def resolve_codex_home(override: str | None) -> Path:
    candidates = []
    if override:
        candidates.append(Path(os.path.expanduser(override)))
    env_home = os.getenv("CODEX_HOME")
    if env_home:
        candidates.append(Path(os.path.expanduser(env_home)))
    candidates.append(Path.home() / ".codex")

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    raise FileNotFoundError("Cannot resolve Codex home. Checked --codex-home, $CODEX_HOME, ~/.codex")


def find_session_files(codex_home: Path, session_id: str) -> List[Path]:
    sessions_root = codex_home / "sessions"
    if not sessions_root.exists():
        raise FileNotFoundError(f"Sessions root not found: {sessions_root}")
    pattern = f"*{session_id}*.jsonl"
    return sorted(p for p in sessions_root.rglob(pattern) if p.is_file())


def content_to_text(content: Any) -> str:
    if not isinstance(content, list):
        return ""
    chunks: List[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            chunks.append(text.strip())
    return "\n".join(chunks).strip()


def trim_text(text: str, max_len: int = 600) -> str:
    clean = text.strip()
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3] + "..."


def tokenize_query(text: str) -> List[str]:
    terms: List[str] = []
    for token in TOKEN_RE.findall(text.lower()):
        if token in STOPWORDS or len(token) <= 1:
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) >= 4:
            for i in range(len(token) - 1):
                seg = token[i : i + 2]
                if seg in STOPWORDS or len(seg) <= 1:
                    continue
                terms.append(seg)
            continue
        terms.append(token)
    return sorted(set(terms))


def iter_assistant_messages(session_files: Iterable[Path]) -> List[Dict[str, Any]]:
    # trace: side-effect function that reads session logs and builds audit-ready rows.
    trace_id = "trace_id:iter_assistant_messages"
    run_id = "run_id:branch_chat_extract"
    _ = (trace_id, run_id)
    messages: List[Dict[str, Any]] = []
    for path in session_files:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if entry.get("type") != "response_item":
                    continue
                payload = entry.get("payload") or {}
                if payload.get("type") != "message" or payload.get("role") != "assistant":
                    continue

                text = content_to_text(payload.get("content"))
                if not text:
                    continue

                messages.append(
                    {
                        "timestamp": entry.get("timestamp", ""),
                        "source_file": str(path),
                        "line_number": line_no,
                        "text": text,
                    }
                )

    messages.sort(key=lambda m: (m.get("timestamp", ""), m["source_file"], m["line_number"]))
    return messages


def iter_session_evidence(session_files: Iterable[Path]) -> List[Dict[str, Any]]:
    # audit: gather multi-source evidence for topic-oriented answering.
    trace_id = "trace_id:iter_session_evidence"
    run_id = "run_id:branch_chat_topic"
    _ = (trace_id, run_id)
    evidence_rows: List[Dict[str, Any]] = []

    for path in session_files:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "response_item":
                    continue
                payload = entry.get("payload") or {}
                payload_type = payload.get("type")
                timestamp = entry.get("timestamp", "")
                text = ""
                source_type = ""

                if payload_type == "message":
                    role = payload.get("role", "")
                    if role not in {"assistant", "user"}:
                        continue
                    text = content_to_text(payload.get("content"))
                    source_type = f"message:{role}"
                elif payload_type in {"function_call", "custom_tool_call"}:
                    call_name = payload.get("name", "")
                    # Keep only tool name to reduce query-echo noise from long call arguments.
                    text = f"{call_name}".strip()
                    source_type = "tool_call"
                elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                    output_text = payload.get("output", "")
                    text = str(output_text).strip()
                    if '"audit_trace": "branch_chat_toolbox"' in text or "trace_id:print_json" in text:
                        continue
                    source_type = "tool_output"
                else:
                    continue

                if not text:
                    continue
                evidence_rows.append(
                    {
                        "timestamp": timestamp,
                        "source_file": str(path),
                        "line_number": line_no,
                        "source_type": source_type,
                        "text": text,
                    }
                )

    evidence_rows.sort(key=lambda r: (r.get("timestamp", ""), r["source_file"], r["line_number"]))
    return evidence_rows


def score_text_against_query(
    text: str,
    query_terms: List[str],
    keyword: str,
    case_sensitive: bool,
) -> tuple[float, List[str]]:
    if case_sensitive:
        hay = text
        needle = keyword
    else:
        hay = text.casefold()
        needle = keyword.casefold()

    score = 0.0
    matched_terms: List[str] = []
    keyword_hit = False
    if needle:
        if needle in hay:
            score += 8.0
            matched_terms.append(f"keyword:{keyword}")
            keyword_hit = True
        else:
            return 0.0, matched_terms

    term_hits = 0
    for term in query_terms:
        term_hit = term if case_sensitive else term.casefold()
        if term_hit in hay:
            score += 1.2
            matched_terms.append(term)
            term_hits += 1

    # Avoid noisy matches from generic process logs when no query semantics matched.
    if query_terms and term_hits == 0 and not keyword_hit:
        return 0.0, matched_terms

    if term_hits > 0 or keyword_hit:
        if "external-lint-all" in hay or "lint-all" in hay:
            score += 1.8
            matched_terms.append("signal:lint_all")
        if "Total output lines" in text or "Original token count" in text:
            score += 1.0
            matched_terms.append("signal:large_output")
        if "Process exited with code" in text:
            score += 0.8
            matched_terms.append("signal:exit_code")
        if "blocked_count" in hay or "lint_count" in hay:
            score += 1.0
            matched_terms.append("signal:lint_stats")

    return score, matched_terms


def collect_topic_evidence(
    evidence_rows: List[Dict[str, Any]],
    question: str,
    keyword: str,
    case_sensitive: bool,
    evidence_limit: int,
) -> List[Dict[str, Any]]:
    query_terms = tokenize_query(f"{question} {keyword}")
    scored_rows: List[Dict[str, Any]] = []
    total = max(1, len(evidence_rows))
    source_weights = {
        "message:assistant": 1.0,
        "message:user": 0.75,
        "tool_call": 0.65,
        "tool_output": 0.45,
    }

    for idx, row in enumerate(evidence_rows):
        score, matched_terms = score_text_against_query(row["text"], query_terms, keyword, case_sensitive)
        recency_bonus = (idx / total) * 0.5
        source_weight = source_weights.get(row["source_type"], 0.6)
        size_penalty = 0.0
        if row["source_type"] == "tool_output" and len(row["text"]) > 2200:
            size_penalty = 0.6
        final_score = (score * source_weight) + recency_bonus - size_penalty
        if final_score <= 0:
            continue
        scored_rows.append(
            {
                "score": round(final_score, 3),
                "matched_terms": matched_terms,
                "source_type": row["source_type"],
                "timestamp": row["timestamp"],
                "source_file": row["source_file"],
                "line_number": row["line_number"],
                "snippet": trim_text(row["text"], max_len=520),
            }
        )

    if not scored_rows and evidence_rows:
        fallback = evidence_rows[-1]
        scored_rows.append(
            {
                "score": 0.001,
                "matched_terms": ["fallback:latest_evidence"],
                "source_type": fallback["source_type"],
                "timestamp": fallback["timestamp"],
                "source_file": fallback["source_file"],
                "line_number": fallback["line_number"],
                "snippet": trim_text(fallback["text"], max_len=520),
            }
        )

    scored_rows.sort(key=lambda r: (r["score"], r["timestamp"]), reverse=True)
    return scored_rows[: max(1, evidence_limit)]


def select_message(messages: List[Dict[str, Any]], keyword: str | None, case_sensitive: bool) -> Dict[str, Any] | None:
    if not messages:
        return None
    if not keyword:
        selected = dict(messages[-1])
        selected["keyword"] = ""
        selected["keyword_matched"] = False
        return selected

    if case_sensitive:
        matched = [m for m in messages if keyword in m["text"]]
    else:
        needle = keyword.casefold()
        matched = [m for m in messages if needle in m["text"].casefold()]

    if not matched:
        return None

    selected = dict(matched[-1])
    selected["keyword"] = keyword
    selected["keyword_matched"] = True
    return selected


def select_message_by_question(messages: List[Dict[str, Any]], question: str) -> Dict[str, Any] | None:
    if not messages:
        return None
    query_terms = tokenize_query(question)
    if not query_terms:
        selected = dict(messages[-1])
        selected["keyword"] = ""
        selected["keyword_matched"] = False
        selected["selection_mode"] = "fallback_latest"
        return selected

    best = None
    best_score = -1.0
    total = max(1, len(messages))
    for idx, msg in enumerate(messages):
        score, matched_terms = score_text_against_query(msg["text"], query_terms, "", False)
        score += (idx / total) * 0.3
        if score > best_score:
            best_score = score
            best = dict(msg)
            best["matched_terms"] = matched_terms

    if best is None:
        best = dict(messages[-1])
        best["matched_terms"] = []
    best["keyword"] = ""
    best["keyword_matched"] = False
    best["selection_mode"] = "question_topic"
    return best


def extract_signal_tags(evidence_bundle: List[Dict[str, Any]]) -> List[str]:
    tags: Set[str] = set()
    for row in evidence_bundle:
        for term in row.get("matched_terms", []):
            if isinstance(term, str) and term.startswith("signal:"):
                tags.add(term.split(":", 1)[1])
    return sorted(tags)


def build_grounded_draft(
    question: str,
    core_claim: str,
    answer_mode: str,
    signal_tags: List[str],
    evidence_bundle: List[Dict[str, Any]],
) -> str:
    question_lc = question.casefold()
    asks_perf = any(
        token in question_lc for token in ["慢", "slow", "性能", "performance", "lint", "全扫", "full scan"]
    )
    has_lint_all = "lint_all" in signal_tags
    has_large_output = "large_output" in signal_tags
    has_exit_code = "exit_code" in signal_tags
    has_lint_stats = "lint_stats" in signal_tags

    if asks_perf and (has_lint_all or has_large_output or has_exit_code or has_lint_stats):
        reasons: List[str] = []
        if has_lint_all:
            reasons.append("证据显示存在 `lint-all/external-lint-all` 类型的批量执行链路")
        if has_large_output:
            reasons.append("日志里出现大体量输出（`Total output lines` / `Original token count`）")
        if has_exit_code:
            reasons.append("流程包含多次子进程执行与退出码采集")
        if has_lint_stats:
            reasons.append("输出包含 `lint_count/blocked_count` 统计，说明扫描维度较宽")
        reason_text = "；".join(reasons) if reasons else "批量执行链路较重"
        return (
            f"Grounded answer: 结合会话证据，这些 lint 脚本的核心工作方式是批量调用多个 lint scope 并汇总输出。"
            f"你感觉“全扫很慢”通常来自三类叠加开销：批量 scope 串行执行、重复扫描目标文件、以及大体量日志序列化与打印。"
            f"本次命中证据指向：{reason_text}。建议优先检查是否可做增量扫描、并行化执行，以及压缩默认日志粒度。"
        )

    evidence_hint = ""
    if evidence_bundle:
        first = evidence_bundle[0]
        evidence_hint = f" Top evidence source: {first.get('source_type', '')}#{first.get('line_number', 0)}."

    return (
        f"Grounded answer: 在 `{answer_mode}` 模式下，命中历史回复主张为 '{core_claim}'。"
        f"针对问题 '{question}'，先按该主张解释，再结合证据逐条验证。{evidence_hint}"
    )


def build_answer_packet(
    selected_message: Dict[str, Any],
    question: str,
    session_id: str,
    answer_mode: str,
    evidence_bundle: List[Dict[str, Any]],
) -> Dict[str, Any]:
    text = selected_message["text"]
    keyword = selected_message.get("keyword", "")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    core_claim = lines[0] if lines else "No core claim extracted from the matched message."
    signal_tags = extract_signal_tags(evidence_bundle)
    evidence_lines = "\n".join(
        f"- [{row.get('source_type', '')}] {row.get('source_file', '')}:{row.get('line_number', 0)}"
        f" | matched={','.join(row.get('matched_terms', []))}"
        f" | snippet={row.get('snippet', '')}"
        for row in evidence_bundle[:6]
    )
    prompt = (
        "Answer the user question using retrieved session evidence as grounding.\n\n"
        f"session_id: {session_id}\n"
        f"answer_mode: {answer_mode}\n"
        f"keyword: {keyword}\n"
        f"user_question: {question}\n\n"
        "Retrieved assistant message (primary anchor):\n"
        f"{text}\n\n"
        "Topic evidence bundle:\n"
        f"{evidence_lines}\n\n"
        "Output requirements:\n"
        "1) Direct answer to the question\n"
        "2) Grounding sentence from the retrieved reply and evidence bundle\n"
        "3) Uncertainty or missing evidence (if any)\n"
        "4) If discussing performance/slowness, include likely bottlenecks and verification steps"
    )
    direct_answer = build_grounded_draft(
        question=question,
        core_claim=core_claim,
        answer_mode=answer_mode,
        signal_tags=signal_tags,
        evidence_bundle=evidence_bundle,
    )
    uncertainty = ""
    if len(evidence_bundle) < 2:
        uncertainty = "Evidence is limited; inspect raw session logs for stronger confirmation."

    return {
        "session_id": session_id,
        "answer_mode": answer_mode,
        "keyword": keyword,
        "question": question,
        "signal_tags": signal_tags,
        "assistant_final_reply": text,
        "evidence_bundle": evidence_bundle,
        "direct_answer_draft": direct_answer,
        "uncertainty_note": uncertainty,
        "answer_prompt": prompt,
    }


def print_json(payload: Dict[str, Any]) -> None:
    audit_payload = dict(payload)
    audit_payload.setdefault("audit_trace", "branch_chat_toolbox")
    audit_payload.setdefault("run_id", "run_id:branch_chat_cli")
    audit_payload.setdefault("trace_id", "trace_id:print_json")
    audit_payload.setdefault("log_channel_machine", OBSERVABILITY_CHANNELS["machine_log"])
    audit_payload.setdefault("log_channel_human", OBSERVABILITY_CHANNELS["human_log"])
    audit_payload.setdefault("project_log_channel_machine", OBSERVABILITY_CHANNELS["project_machine_log"])
    audit_payload.setdefault("project_log_channel_human", OBSERVABILITY_CHANNELS["project_human_log"])
    audit_payload.setdefault("result_anchor", OBSERVABILITY_CHANNELS["result_anchor"])
    print(json.dumps(audit_payload, ensure_ascii=False, indent=2))


def cmd_locate_session(args: argparse.Namespace) -> int:
    try:
        query_id = resolve_query_id(args.session_id, args.resume_id)
    except ValueError as exc:
        print_json({"status": "error", "message": str(exc)})
        return 2

    codex_home = resolve_codex_home(args.codex_home)
    files = find_session_files(codex_home, query_id)
    if not files:
        print_json(
            {
                "status": "error",
                "message": "Session files not found",
                "session_id": query_id,
                "codex_home": str(codex_home),
                "hint": "Check session_id or pass --codex-home explicitly.",
            }
        )
        return 2

    print_json(
        {
            "status": "ok",
            "session_id": query_id,
            "codex_home": str(codex_home),
            "session_files": [str(p) for p in files],
            "file_count": len(files),
        }
    )
    return 0


def cmd_extract_final_reply(args: argparse.Namespace) -> int:
    try:
        query_id = resolve_query_id(args.session_id, args.resume_id)
    except ValueError as exc:
        print_json({"status": "error", "message": str(exc)})
        return 2

    codex_home = resolve_codex_home(args.codex_home)
    files = find_session_files(codex_home, query_id)
    if not files:
        print_json(
            {
                "status": "error",
                "message": "Session files not found",
                "session_id": query_id,
                "codex_home": str(codex_home),
            }
        )
        return 2

    messages = iter_assistant_messages(files)
    selected = select_message(messages, args.keyword, args.case_sensitive)
    if selected is None:
        print_json(
            {
                "status": "error",
                "message": "No assistant message matched the keyword",
                "session_id": query_id,
                "keyword": args.keyword or "",
                "assistant_message_count": len(messages),
                "sample_latest_timestamps": [m["timestamp"] for m in messages[-5:]],
            }
        )
        return 3

    print_json(
        {
            "status": "ok",
            "session_id": query_id,
            "keyword": args.keyword or "",
            "codex_home": str(codex_home),
            "session_files": [str(p) for p in files],
            "assistant_message_count": len(messages),
            "selected_message": selected,
        }
    )
    return 0


def cmd_answer_question(args: argparse.Namespace) -> int:
    try:
        query_id = resolve_query_id(args.session_id, args.resume_id)
    except ValueError as exc:
        print_json({"status": "error", "message": str(exc)})
        return 2

    codex_home = resolve_codex_home(args.codex_home)
    files = find_session_files(codex_home, query_id)
    if not files:
        print_json(
            {
                "status": "error",
                "message": "Session files not found",
                "session_id": query_id,
                "codex_home": str(codex_home),
            }
        )
        return 2

    messages = iter_assistant_messages(files)
    evidence_rows = iter_session_evidence(files)
    keyword = (args.keyword or "").strip()
    answer_mode = "keyword_match" if keyword else "topic_evidence"

    if keyword:
        selected = select_message(messages, keyword, args.case_sensitive)
        if selected is None:
            print_json(
                {
                    "status": "error",
                    "message": "No assistant message matched the keyword",
                    "session_id": query_id,
                    "keyword": keyword,
                    "assistant_message_count": len(messages),
                }
            )
            return 3
    else:
        selected = select_message_by_question(messages, args.question)
        if selected is None:
            print_json(
                {
                    "status": "error",
                    "message": "No assistant messages available for topic selection",
                    "session_id": query_id,
                    "assistant_message_count": len(messages),
                }
            )
            return 3

    evidence_bundle = collect_topic_evidence(
        evidence_rows=evidence_rows,
        question=args.question,
        keyword=keyword,
        case_sensitive=args.case_sensitive,
        evidence_limit=args.evidence_limit,
    )

    packet = build_answer_packet(
        selected_message=selected,
        question=args.question,
        session_id=query_id,
        answer_mode=answer_mode,
        evidence_bundle=evidence_bundle,
    )
    print_json(
        {
            "status": "ok",
            "session_id": query_id,
            "keyword": keyword,
            "answer_mode": answer_mode,
            "assistant_message_count": len(messages),
            "session_evidence_count": len(evidence_rows),
            "selected_message": selected,
            "evidence_bundle": evidence_bundle,
            "answer_packet": packet,
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cli_Toolbox for 4-Branch-Chat")
    subparsers = parser.add_subparsers(dest="command", required=True)

    locate = subparsers.add_parser("locate-session", help="Locate session files by session/resume id")
    locate.add_argument("--session-id", default="")
    locate.add_argument("--resume-id", default="")
    locate.add_argument("--codex-home", default=None)
    locate.set_defaults(func=cmd_locate_session)

    extract = subparsers.add_parser("extract-final-reply", help="Extract assistant final reply by keyword")
    extract.add_argument("--session-id", default="")
    extract.add_argument("--resume-id", default="")
    extract.add_argument("--keyword", default="")
    extract.add_argument("--codex-home", default=None)
    extract.add_argument("--case-sensitive", action="store_true")
    extract.set_defaults(func=cmd_extract_final_reply)

    answer = subparsers.add_parser("answer-question", help="Locate reply and prepare a direct answer payload")
    answer.add_argument("--session-id", default="")
    answer.add_argument("--resume-id", default="")
    answer.add_argument("--keyword", default="")
    answer.add_argument("--question", required=True)
    answer.add_argument("--evidence-limit", type=int, default=8)
    answer.add_argument("--codex-home", default=None)
    answer.add_argument("--case-sensitive", action="store_true")
    answer.set_defaults(func=cmd_answer_question)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
