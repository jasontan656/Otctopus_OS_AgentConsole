from __future__ import annotations

import re

from session_locator_support import AssistantMessage, trim_text


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


def tokenize_query(text: str) -> list[str]:
    terms: list[str] = []
    for token in TOKEN_RE.findall(text.lower()):
        if token in STOPWORDS or len(token) <= 1:
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) >= 4:
            for index in range(len(token) - 1):
                seg = token[index : index + 2]
                if seg in STOPWORDS or len(seg) <= 1:
                    continue
                terms.append(seg)
            continue
        terms.append(token)
    return sorted(set(terms))


def score_text_against_query(
    text: str,
    query_terms: list[str],
    keyword: str,
    case_sensitive: bool,
) -> tuple[float, list[str]]:
    hay = text if case_sensitive else text.casefold()
    needle = keyword if case_sensitive else keyword.casefold()

    score = 0.0
    matched_terms: list[str] = []
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
        term_probe = term if case_sensitive else term.casefold()
        if term_probe in hay:
            score += 1.2
            matched_terms.append(term)
            term_hits += 1

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
    evidence_rows: list[dict[str, object]],
    question: str,
    keyword: str,
    case_sensitive: bool,
    evidence_limit: int,
) -> list[dict[str, object]]:
    query_terms = tokenize_query(f"{question} {keyword}")
    scored_rows: list[dict[str, object]] = []
    total = max(1, len(evidence_rows))
    source_weights = {
        "message:assistant": 1.0,
        "message:user": 0.75,
        "tool_call": 0.65,
        "tool_output": 0.45,
    }

    for idx, row in enumerate(evidence_rows):
        score, matched_terms = score_text_against_query(str(row["text"]), query_terms, keyword, case_sensitive)
        recency_bonus = (idx / total) * 0.5
        source_weight = source_weights.get(str(row["source_type"]), 0.6)
        size_penalty = 0.6 if row["source_type"] == "tool_output" and len(str(row["text"])) > 2200 else 0.0
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
                "snippet": trim_text(str(row["text"]), max_len=520),
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
                "snippet": trim_text(str(fallback["text"]), max_len=520),
            }
        )

    scored_rows.sort(key=lambda row: (row["score"], row["timestamp"]), reverse=True)
    return scored_rows[: max(1, evidence_limit)]


def select_message(
    messages: list[AssistantMessage],
    keyword: str | None,
    case_sensitive: bool,
) -> AssistantMessage | None:
    if not messages:
        return None
    if not keyword:
        selected = dict(messages[-1])
        selected["keyword"] = ""
        selected["keyword_matched"] = False
        return selected

    if case_sensitive:
        matched = [message for message in messages if keyword in str(message["text"])]
    else:
        needle = keyword.casefold()
        matched = [message for message in messages if needle in str(message["text"]).casefold()]

    if not matched:
        return None

    selected = dict(matched[-1])
    selected["keyword"] = keyword
    selected["keyword_matched"] = True
    return selected


def select_message_by_question(messages: list[AssistantMessage], question: str) -> AssistantMessage | None:
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
        score, matched_terms = score_text_against_query(str(msg["text"]), query_terms, "", False)
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
