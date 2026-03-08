#!/usr/bin/env python3
"""Shared helpers and contracts for mstg_target_skill_audit."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import stat
import subprocess
from typing import Any

import mstg_yaml as yaml

REQUIRED_DOCS = [
    "L0/README.md",
    "L1/README.md",
    "L2/README.md",
    "L3/README.md",
    "L4/README.md",
    "L5/README.md",
    "L6/README.md",
    "L7/README.md",
    "L8/README.md",
    "L9/README.md",
    "L10/README.md",
    "L11/README.md",
    "L12/README.md",
    "L13/README.md",
]

REQUIRED_RUNTIME = [
    "TOOL_REGISTRY.yaml",
    "TOOL_DOCS_STRUCTURED.yaml",
    "TOOL_CHANGE_LEDGER.jsonl",
    "TOOLING_GOVERNANCE_STATE.yaml",
]

PROCESS_KEYWORDS = [
    "tooling_governance_apply_change.py",
    "tooling_governance_auto_writeback.py",
    "tooling_docs_record.py",
    "tooling_change_ledger.py",
    "TOOL_DOCS_STRUCTURED.yaml",
    "TOOL_CHANGE_LEDGER.jsonl",
    "docs_pre_update",
    "ledger_append",
    "full_gate_lint",
]

SEVERITY_RANK = {"high": 3, "medium": 2, "low": 1}

SCRIPT_EXTENSIONS = {
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".js",
    ".ts",
    ".mjs",
    ".cjs",
    ".rb",
    ".pl",
    ".php",
    ".lua",
    ".cmd",
    ".bat",
}

OUTCOME_OVERRIDE: dict[str, dict[str, Any]] = {
    "required_docs_missing": {
        "domain": "基线结构",
        "title": "必需 L0-L13 文档缺失",
        "message": "治理实例的层级文档不完整，无法形成完整开发与运维追溯链。",
        "steps": [
            "补齐缺失的 L0-L13 文档文件（docs/Lx/README.md）。",
            "补齐 L1/L2 分链文档（docs/L1/chains/*.md 与 docs/L2/chains/*/README.md）。",
            "确保每份文档包含 Machine Map 且字段完整。",
        ],
    },
    "required_runtime_files_missing": {
        "domain": "基线结构",
        "title": "必需 runtime 合同文件缺失",
        "message": "治理实例 runtime 合同文件缺失，脚本链路无法稳定运行。",
        "steps": [
            "补齐 runtime 合同文件（registry/docs/ledger/state/manifest）。",
            "确认路径位于实例 runtime 目录下。",
        ],
    },
    "required_toolbox_scripts_missing": {
        "domain": "工具注入",
        "title": "治理工具箱脚本缺失",
        "message": "目标技能未完整注入标准治理脚本，后续自治理将漂移。",
        "steps": [
            "通过 mode3 或初始化脚本重新注入标准治理工具箱。",
            "确认缺失脚本均存在于 tooling_governance/<instance>/scripts。",
        ],
    },
    "docs_non_empty_contract_failed": {
        "domain": "文档质量",
        "title": "文档非空合同未通过",
        "message": "至少一份治理文档仍为空洞或包含占位符，无法作为维护手册。",
        "steps": [
            "按当前技能真实状态填充文档内容，移除占位符。",
            "补充可执行操作与验收证据。",
        ],
    },
    "docs_machine_map_missing_or_parse_fail": {
        "domain": "锚点与映射",
        "title": "Machine Map 缺失或无法解析",
        "message": "文档 Machine Map 不可用，脚本无法做结构化锚点消费。",
        "steps": [
            "补全或修正 Machine Map YAML 语法。",
            "保证 Machine Map 位于文档固定区块并可被脚本解析。",
        ],
    },
    "docs_machine_map_required_fields_missing": {
        "domain": "锚点与映射",
        "title": "Machine Map 必填字段缺失",
        "message": "Machine Map 字段不完整，合同层无法闭环。",
        "steps": [
            "补齐 required_fields 中的所有字段。",
            "将字段值改为可追踪、可验证内容。",
        ],
    },
    "docs_machine_map_anchor_fields_invalid": {
        "domain": "锚点与映射",
        "title": "锚点字段为空或无效",
        "message": "tool/script/asset/evidence 锚点字段缺失有效值，影响锚点优先治理。",
        "steps": [
            "补齐 tool_anchor_refs/script_anchor_refs/asset_anchor_refs/evidence_anchor_refs。",
            "确保每个字段至少有一个可用锚点。",
        ],
    },
    "docs_machine_map_anchor_paths_unresolvable": {
        "domain": "锚点与映射",
        "title": "锚点路径不可解析",
        "message": "至少一个锚点路径无法在实例根或目标技能根解析。",
        "steps": [
            "修正错误路径或回填缺失文件。",
            "优先使用实例内相对路径，保持稳定可解析。",
        ],
    },
    "docs_machine_map_tool_anchor_unknown": {
        "domain": "锚点与映射",
        "title": "tool_anchor_refs 未映射到 TOOL_REGISTRY",
        "message": "文档 tool_anchor_refs 与 runtime 注册表不一致。",
        "steps": [
            "将文档 tool_anchor_refs 对齐到 TOOL_REGISTRY 的 tool_id。",
            "必要时先补齐 TOOL_REGISTRY 对应条目再回写文档。",
        ],
    },
    "tool_registry_structured_docs_out_of_sync": {
        "domain": "结构化文档",
        "title": "TOOL_REGISTRY 与 TOOL_DOCS_STRUCTURED 不一致",
        "message": "tool_id 集合不一致，会导致工具手册与实际脚本映射漂移。",
        "steps": [
            "对齐 registry 与 structured docs 的 tool_id 集合。",
            "缺失项补齐 usage/modification/development 三段。",
        ],
    },
    "structured_docs_sections_incomplete": {
        "domain": "结构化文档",
        "title": "结构化工具文档段落不完整",
        "message": "至少一个工具缺少 usage/modification/development 必需字段。",
        "steps": [
            "补齐 usage.summary/command_examples/inputs/outputs。",
            "补齐 modification 与 development 记录。",
        ],
    },
    "tool_change_ledger_empty": {
        "domain": "可追溯性",
        "title": "TOOL_CHANGE_LEDGER 为空",
        "message": "历史治理变更不可追溯，后续排错与审计会失真。",
        "steps": [
            "回填缺失治理事件到 TOOL_CHANGE_LEDGER.jsonl。",
            "后续所有脚本变更通过统一入口自动写入 ledger。",
        ],
    },
    "tool_change_ledger_jsonl_invalid": {
        "domain": "可追溯性",
        "title": "TOOL_CHANGE_LEDGER JSONL 非法",
        "message": "ledger 存在坏行，无法机械读取。",
        "steps": [
            "修复 JSONL 非法行并保证每行是 JSON object。",
            "修复后重跑 outcome lint。",
        ],
    },
    "tool_change_ledger_keys_missing": {
        "domain": "可追溯性",
        "title": "TOOL_CHANGE_LEDGER 关键字段缺失",
        "message": "ledger 事件字段不完整，追踪链断裂。",
        "steps": [
            "补齐 event_id/timestamp_utc/tool_id/change_type/summary 等字段。",
            "统一使用标准写入脚本，避免手工写错字段。",
        ],
    },
    "governance_audit_target_trace_missing": {
        "domain": "可追溯性",
        "title": "governance_audit 缺失目标技能轨迹",
        "message": "治理日志未包含目标技能过程，审计证据不完整。",
        "steps": [
            "确保 start/step/finish 事件写入 governance_audit。",
            "检查 target_skill 与 target_path 字段是否正确填充。",
        ],
    },
}


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_compact() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def run_json_cmd(cmd: list[str], cwd: Path) -> tuple[int, dict[str, Any], str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    out = (proc.stdout or "").strip()
    payload: dict[str, Any]
    try:
        payload = json.loads(out) if out else {}
        if not isinstance(payload, dict):
            payload = {"raw_stdout": out}
    except Exception:
        payload = {"raw_stdout": out}
    return proc.returncode, payload, (proc.stderr or "")[-1600:]


def normalize_text_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    rows: list[str] = []
    for item in raw:
        token = str(item).strip()
        if token:
            rows.append(token)
    return rows


def _path_has_segment(path: Path, segment: str) -> bool:
    needle = segment.strip().lower()
    if not needle:
        return False
    return any(str(part).lower() == needle for part in path.parts)


def _has_shebang(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            return fh.read(2) == b"#!"
    except Exception:
        return False


def _is_executable(path: Path) -> bool:
    try:
        mode = path.stat().st_mode
    except Exception:
        return False
    return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def _sample(rows: list[str], limit: int) -> list[str]:
    if limit <= 0:
        return []
    return rows[:limit]


def collect_recursive_script_footprint(target_skill_dir: Path, sample_limit: int = 20) -> dict[str, Any]:
    """
    Collect script footprint from full skill tree instead of scripts/ only.

    Script candidates are files that satisfy at least one condition:
    - path contains a `scripts` segment,
    - file extension looks script-like,
    - file starts with shebang,
    - file has executable mode bits.
    """

    scripts_dir_files: list[str] = []
    scripts_dir_script_files: list[str] = []
    script_extension_files: list[str] = []
    shebang_files: list[str] = []
    executable_files: list[str] = []

    script_candidates_set: set[str] = set()
    scripts_dir_set: set[str] = set()

    for file_path in target_skill_dir.rglob("*"):
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(target_skill_dir)
        rel_token = str(rel).replace("\\", "/")

        in_scripts_dir = _path_has_segment(rel, "scripts")
        by_extension = file_path.suffix.lower() in SCRIPT_EXTENSIONS
        by_shebang = _has_shebang(file_path)
        by_exec = _is_executable(file_path)

        if in_scripts_dir:
            scripts_dir_files.append(rel_token)
            scripts_dir_set.add(rel_token)
        if by_extension:
            script_extension_files.append(rel_token)
        if by_shebang:
            shebang_files.append(rel_token)
        if by_exec:
            executable_files.append(rel_token)

        if in_scripts_dir or by_extension or by_shebang or by_exec:
            script_candidates_set.add(rel_token)
        if in_scripts_dir and (by_extension or by_shebang or by_exec):
            scripts_dir_script_files.append(rel_token)

    scripts_dir_files = sorted(set(scripts_dir_files))
    scripts_dir_script_files = sorted(set(scripts_dir_script_files))
    script_extension_files = sorted(set(script_extension_files))
    shebang_files = sorted(set(shebang_files))
    executable_files = sorted(set(executable_files))
    script_candidates = sorted(script_candidates_set)
    scripts_outside_scripts_dir = sorted([p for p in script_candidates if p not in scripts_dir_set])

    return {
        "scan_root": str(target_skill_dir),
        "scripts_dir_file_count": len(scripts_dir_files),
        "scripts_dir_script_file_count": len(scripts_dir_script_files),
        "script_extension_file_count": len(script_extension_files),
        "shebang_file_count": len(shebang_files),
        "executable_file_count": len(executable_files),
        "recursive_script_candidate_count": len(script_candidates),
        "recursive_script_outside_scripts_dir_count": len(scripts_outside_scripts_dir),
        "samples": {
            "scripts_dir_files": _sample(scripts_dir_files, sample_limit),
            "scripts_dir_script_files": _sample(scripts_dir_script_files, sample_limit),
            "script_extension_files": _sample(script_extension_files, sample_limit),
            "shebang_files": _sample(shebang_files, sample_limit),
            "executable_files": _sample(executable_files, sample_limit),
            "recursive_script_candidates": _sample(script_candidates, sample_limit),
            "scripts_outside_scripts_dir": _sample(scripts_outside_scripts_dir, sample_limit),
        },
    }


def summarize_gate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Keep gate payload machine-readable while avoiding verbose narrative leakage."""
    if not isinstance(payload, dict):
        return {}
    out: dict[str, Any] = {}
    for key in (
        "status",
        "scope",
        "checks",
        "failing_scripts",
        "violation_counts",
    ):
        if key in payload:
            out[key] = payload.get(key)

    violations = payload.get("violations")
    if isinstance(violations, list):
        out["violation_ids"] = [
            str(v.get("id", "")).strip()
            for v in violations
            if isinstance(v, dict) and str(v.get("id", "")).strip()
        ]

    results = payload.get("results")
    if isinstance(results, list):
        compact_rows: list[dict[str, Any]] = []
        for row in results:
            if not isinstance(row, dict):
                continue
            compact: dict[str, Any] = {}
            for key in ("script", "status", "scope", "exit_code", "error_count", "checks"):
                if key in row:
                    compact[key] = row.get(key)
            nested = row.get("payload")
            if isinstance(nested, dict):
                if "violation_counts" in nested:
                    compact["violation_counts"] = nested.get("violation_counts")
                nested_violations = nested.get("violations")
                if isinstance(nested_violations, list):
                    ids = [
                        str(v.get("id", "")).strip()
                        for v in nested_violations
                        if isinstance(v, dict) and str(v.get("id", "")).strip()
                    ]
                    if ids:
                        compact["violation_ids"] = ids
            compact_rows.append(compact)
        out["results"] = compact_rows
    return out


def list_instance_roots(target_skill_dir: Path) -> list[Path]:
    rows: list[Path] = []
    root = target_skill_dir / "tooling_governance"
    if root.is_dir():
        for p in sorted(root.iterdir()):
            if p.is_dir() and (p / "docs").is_dir() and (p / "runtime").is_dir():
                rows.append(p.resolve())

    # Self-governance fallback for MSTG itself.
    self_instance = target_skill_dir / "governance_instance" / "self"
    if self_instance.is_dir() and (self_instance / "docs").is_dir() and (self_instance / "runtime").is_dir():
        rows.append(self_instance.resolve())

    return rows


def choose_instance(instance_roots: list[Path], instance_name: str) -> Path | None:
    if not instance_roots:
        return None
    if instance_name:
        for p in instance_roots:
            if p.name == instance_name:
                return p
    if len(instance_roots) == 1:
        return instance_roots[0]
    for preferred in ("default", "self", "tooling_governance"):
        for p in instance_roots:
            if p.name == preferred:
                return p
    return instance_roots[0]


def parse_tool_ids(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return []
    ids: list[str] = []
    for row in tools:
        if not isinstance(row, dict):
            continue
        token = str(row.get("tool_id", "")).strip()
        if token:
            ids.append(token)
    return sorted(set(ids))


def add_finding(
    findings: list[dict[str, Any]],
    *,
    fid: str,
    severity: str,
    domain: str,
    title: str,
    message: str,
    evidence: list[str],
    steps: list[str] | None = None,
    verify_commands: list[str] | None = None,
    source: dict[str, Any] | None = None,
) -> None:
    findings.append(
        {
            "id": fid,
            "severity": severity,
            "domain": domain,
            "title": title,
            "message": message,
            "evidence": evidence,
            "failure_guidance": {
                "steps": steps or [],
                "verify_commands": verify_commands or [],
            },
            "source": source or {},
        }
    )


def severity_summary(findings: list[dict[str, Any]]) -> dict[str, int]:
    out = {"high": 0, "medium": 0, "low": 0}
    for row in findings:
        sev = str(row.get("severity", "")).lower()
        if sev in out:
            out[sev] += 1
    return out


def domain_summary(findings: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in findings:
        domain = str(row.get("domain", "未分类")).strip() or "未分类"
        out[domain] = out.get(domain, 0) + 1
    return out


def sort_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        findings,
        key=lambda row: (
            -SEVERITY_RANK.get(str(row.get("severity", "")).lower(), 0),
            str(row.get("domain", "")),
            str(row.get("id", "")),
        ),
    )


def decide_readiness(findings: list[dict[str, Any]]) -> str:
    counts = severity_summary(findings)
    if counts["high"] > 0:
        return "blocked"
    if counts["medium"] > 0:
        return "conditional"
    return "ready"


def readiness_label_zh(readiness_code: str) -> str:
    mapping = {
        "blocked": "阻塞",
        "conditional": "有条件通过",
        "ready": "可进入下一阶段",
    }
    return mapping.get(readiness_code, readiness_code)


def severity_label_zh(severity: str) -> str:
    mapping = {
        "high": "高",
        "medium": "中",
        "low": "低",
    }
    return mapping.get(str(severity).lower(), str(severity))


def infer_outcome_domain(violation_id: str) -> str:
    vid = violation_id.strip()
    rules = [
        ("基线结构", lambda s: s.startswith("required_") or "instance_" in s),
        ("锚点与映射", lambda s: "anchor" in s or "machine_map" in s),
        ("结构化文档", lambda s: "structured_docs" in s or "tool_registry" in s),
        ("可追溯性", lambda s: "ledger" in s or "trace" in s or "audit" in s),
        ("目标技能表面合同", lambda s: "target_contract" in s or "target_skill_md" in s),
    ]
    for domain, cond in rules:
        if cond(vid):
            return domain
    return "治理合同"


def default_outcome_guidance(violation_id: str, instance_root: Path) -> tuple[list[str], list[str]]:
    steps = [
        f"按证据定位违规 `{violation_id}` 对应的文件并修复。",
        "修复后重跑目标结果校验，确认违规消失。",
    ]
    verify = [
        f"python3 scripts/mstg_target_governance_outcome_lint.py --instance-root {instance_root} --pretty",
        f"python3 scripts/mstg_l0_l13_full_gate_lint.py --instance-root {instance_root}",
    ]
    return steps, verify


def merge_outcome_violations(
    findings: list[dict[str, Any]],
    *,
    payload: dict[str, Any],
    instance_root: Path,
) -> int:
    violations = payload.get("violations")
    if not isinstance(violations, list):
        return 0

    added = 0
    for row in violations:
        if not isinstance(row, dict):
            continue
        vid = str(row.get("id", "")).strip()
        if not vid:
            continue

        severity = str(row.get("severity", "high")).lower()
        if severity not in SEVERITY_RANK:
            severity = "high"

        override = OUTCOME_OVERRIDE.get(vid, {})
        domain = str(override.get("domain", infer_outcome_domain(vid))).strip() or infer_outcome_domain(vid)
        title = str(override.get("title", f"目标结果违规：{vid}")).strip()
        message = str(override.get("message", f"目标结果校验发现违规 `{vid}`，需要修复后再推进。"))

        evidence = normalize_text_list(row.get("evidence"))
        lint_message = str(row.get("message", "")).strip()
        if lint_message:
            evidence = [f"lint_message={lint_message}", *evidence]

        if isinstance(override.get("steps"), list) and override.get("steps"):
            steps = [str(x).strip() for x in override.get("steps", []) if str(x).strip()]
        else:
            steps, _ = default_outcome_guidance(vid, instance_root)

        if isinstance(override.get("verify"), list) and override.get("verify"):
            verify = [str(x).strip() for x in override.get("verify", []) if str(x).strip()]
        else:
            _, verify = default_outcome_guidance(vid, instance_root)

        add_finding(
            findings,
            fid=f"outcome::{vid}",
            severity=severity,
            domain=domain,
            title=title,
            message=message,
            evidence=evidence,
            steps=steps,
            verify_commands=verify,
            source={"kind": "target_outcome_lint", "violation_id": vid},
        )
        added += 1
    return added


def add_full_gate_script_failures(
    findings: list[dict[str, Any]],
    *,
    full_gate_payload: dict[str, Any],
    instance_root: Path,
) -> int:
    results = full_gate_payload.get("results")
    if not isinstance(results, list):
        return 0

    added = 0
    for row in results:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status", "")).upper()
        if status == "PASS":
            continue

        script = str(row.get("script", "unknown_script"))
        exit_code = row.get("exit_code")
        nested = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        violations_raw = nested.get("violations") if isinstance(nested, dict) else []
        violations = violations_raw if isinstance(violations_raw, list) else []
        violation_ids = [
            str(v.get("id", "")).strip()
            for v in violations
            if isinstance(v, dict) and str(v.get("id", "")).strip()
        ]

        evidence = [f"script={script}", f"exit_code={exit_code}"]
        if violation_ids:
            evidence.append(f"violation_ids={','.join(violation_ids)}")

        add_finding(
            findings,
            fid=f"full_gate::{script}",
            severity="medium",
            domain="门禁执行",
            title=f"full gate 子脚本失败：{script}",
            message="full gate 中至少一个子脚本未通过，需按失败脚本逐项修复。",
            evidence=evidence,
            steps=[
                "先单独执行失败脚本并读取完整输出。",
                "按脚本返回的违规项逐条修复后再重跑 full gate。",
            ],
            verify_commands=[
                f"python3 scripts/{script} --instance-root {instance_root} --pretty",
                f"python3 scripts/mstg_l0_l13_full_gate_lint.py --instance-root {instance_root}",
            ],
            source={"kind": "full_gate", "script": script},
        )
        added += 1
    return added


def build_failure_guides(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    guides: list[dict[str, Any]] = []
    for row in findings:
        guide = row.get("failure_guidance") if isinstance(row.get("failure_guidance"), dict) else {}
        steps = normalize_text_list(guide.get("steps"))
        verify = normalize_text_list(guide.get("verify_commands"))
        if not steps and not verify:
            continue
        guides.append(
            {
                "finding_id": row.get("id", ""),
                "severity": row.get("severity", ""),
                "domain": row.get("domain", ""),
                "title": row.get("title", ""),
                "steps": steps,
                "verify_commands": verify,
            }
        )
    return guides


def build_markdown_report(report: dict[str, Any]) -> str:
    target = report.get("target", {})
    summary = report.get("summary", {})
    findings = report.get("findings", [])
    recommendations = report.get("recommendations", [])
    failure_guides = report.get("failure_guides", [])
    domain_stats = summary.get("domain_counts", {}) if isinstance(summary.get("domain_counts"), dict) else {}

    lines = [
        f"# MSTG 目标技能审计报告 — {target.get('skill_name', 'unknown')}",
        "",
        "## 概览",
        f"- generated_at_utc: {report.get('generated_at_utc', '')}",
        f"- 审计就绪态: {summary.get('readiness', '')}",
        f"- 审计就绪态代码: {summary.get('readiness_code', '')}",
        f"- selected_instance: {summary.get('selected_instance', 'N/A')}",
        f"- scripts_dir_script_file_count: {summary.get('tool_script_count', 0)}",
        f"- recursive_script_candidate_count: {summary.get('recursive_script_candidate_count', 0)}",
        f"- recursive_script_outside_scripts_dir_count: {summary.get('recursive_script_outside_scripts_dir_count', 0)}",
        f"- 发现总数: {summary.get('total_findings', 0)}",
        f"- 高/中/低: {summary.get('high_count', 0)}/{summary.get('medium_count', 0)}/{summary.get('low_count', 0)}",
        "",
        "## 审计覆盖域",
    ]
    if domain_stats:
        for name, count in sorted(domain_stats.items(), key=lambda x: x[0]):
            lines.append(f"- {name}: {count}")
    else:
        lines.append("- 无")

    lines.extend(["", "## 发现项"])
    if findings:
        for idx, row in enumerate(findings, start=1):
            lines.extend(
                [
                    f"### F{idx} [{severity_label_zh(str(row.get('severity', '')))}][{row.get('domain', '未分类')}] {row.get('title', '')}",
                    f"- id: {row.get('id', '')}",
                    f"- 说明: {row.get('message', '')}",
                    "- 证据:",
                ]
            )
            evidence = row.get("evidence", [])
            if isinstance(evidence, list) and evidence:
                for e in evidence:
                    lines.append(f"  - {e}")
            else:
                lines.append("  - 无")
            lines.append("")
    else:
        lines.append("- 无")
        lines.append("")

    lines.append("## 失败指引")
    if isinstance(failure_guides, list) and failure_guides:
        for idx, guide in enumerate(failure_guides, start=1):
            lines.append(
                f"### G{idx} [{severity_label_zh(str(guide.get('severity', '')))}][{guide.get('domain', '未分类')}] {guide.get('title', '')}"
            )
            lines.append(f"- 对应 finding: {guide.get('finding_id', '')}")
            lines.append("- 修复步骤:")
            steps = guide.get("steps", [])
            if isinstance(steps, list) and steps:
                for s in steps:
                    lines.append(f"  - {s}")
            else:
                lines.append("  - 无")
            lines.append("- 验证命令:")
            verify = guide.get("verify_commands", [])
            if isinstance(verify, list) and verify:
                for cmd in verify:
                    lines.append(f"  - `{cmd}`")
            else:
                lines.append("  - 无")
            lines.append("")
    else:
        lines.append("- 无")
        lines.append("")

    lines.append("## 建议动作")
    if recommendations:
        for rec in recommendations:
            lines.append(f"- {rec}")
    else:
        lines.append("- 无")

    lines.append("")
    lines.append("## 决策门")
    lines.append("- 下一步进入计划创建与施工前，必须由用户显式给出 `continue`。")
    return "\n".join(lines) + "\n"
