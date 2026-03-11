from __future__ import annotations

import json
from typing import Any, Dict, List, Set


OBSERVABILITY_CHANNELS = {
    "machine_log": "Codex_Skill_Runtime/Functional-CodexBranchSession-Chat/machine.jsonl",
    "human_log": "Codex_Skill_Runtime/Functional-CodexBranchSession-Chat/human.log",
    "result_anchor": "Codex_Skills_Result/Functional-CodexBranchSession-Chat",
    "project_machine_log": "logs/machine.jsonl",
    "project_human_log": "logs/human.log",
}


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
    has_lint_all = "lint_all" in signal_tags
    has_large_output = "large_output" in signal_tags
    has_exit_code = "exit_code" in signal_tags
    has_lint_stats = "lint_stats" in signal_tags

    if "lint" in question.casefold() and (has_lint_all or has_large_output or has_exit_code or has_lint_stats):
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
            "Grounded answer: 结合会话证据，这些 lint 脚本的核心工作方式是批量调用多个 lint scope 并汇总输出。"
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
    text = str(selected_message["text"])
    keyword = str(selected_message.get("keyword", ""))
    lines = [line.strip() for line in text.splitlines() if line.strip()]
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
