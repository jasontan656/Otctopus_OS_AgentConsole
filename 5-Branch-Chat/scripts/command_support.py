from __future__ import annotations

from typing import Any

from answer_packet_support import build_answer_packet, print_json
from evidence_rows_support import iter_session_evidence
from query_match_support import collect_topic_evidence, select_message, select_message_by_question
from session_locator_support import find_session_files, iter_assistant_messages, resolve_codex_home, resolve_query_id


def cmd_locate_session(args: Any) -> int:
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
            "session_files": [str(path) for path in files],
            "file_count": len(files),
        }
    )
    return 0


def cmd_extract_final_reply(args: Any) -> int:
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
                "sample_latest_timestamps": [item["timestamp"] for item in messages[-5:]],
            }
        )
        return 3

    print_json(
        {
            "status": "ok",
            "session_id": query_id,
            "keyword": args.keyword or "",
            "codex_home": str(codex_home),
            "session_files": [str(path) for path in files],
            "assistant_message_count": len(messages),
            "selected_message": selected,
        }
    )
    return 0


def cmd_answer_question(args: Any) -> int:
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
