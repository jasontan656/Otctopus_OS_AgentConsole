#!/usr/bin/env python3
"""Layer-specific render helpers for MSTG L0-L13 composite writeback."""

from __future__ import annotations

import re
from typing import Any

from mstg_l0_l13_linear_composite import write_composite_governance_artifacts


def chain_objective(chain_id: str, chain_objectives: dict[str, str]) -> str:
    return chain_objectives.get(chain_id, "该链用于目标技能工具文档回填与闭环维护，需在 L2 定义子里程碑并在 L13 验收。")


def chain_slug(chain_id: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_-]+", "_", chain_id).strip("_").lower()
    return token or "chain"


def chain_focus(chain_id: str) -> str:
    focus_map = {
        "chain_tool_inventory_baseline": "工具盘点与分类基线（tool_id/entrypoint/domain/owner）",
        "chain_usage_contract_backfill": "工具使用文档回填（命令、输入、输出、usage锚点）",
        "chain_modification_development_backfill": "工具修改与开发文档回填（workflow、required_docs、development记录）",
        "chain_sync_traceability_closure": "工具文档同步闭环（registry/docs/anchors/ledger/gate）",
        "chain_batch_governance_rollout": "多技能批量工具文档治理与审计同步",
    }
    return focus_map.get(chain_id, "目标技能工具文档维护链")


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_str_list(value: Any) -> list[str]:
    rows: list[str] = []
    for item in _safe_list(value):
        token = str(item).strip()
        if token:
            rows.append(token)
    return rows


def _profile_tools(toolbox_profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    obj = toolbox_profile.get("tools")
    if not isinstance(obj, dict):
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for tool_id, meta in obj.items():
        token = str(tool_id).strip()
        if not token:
            continue
        rows[token] = _safe_dict(meta)
    return rows


def _profile_domains(toolbox_profile: dict[str, Any]) -> dict[str, list[str]]:
    obj = toolbox_profile.get("domains")
    if not isinstance(obj, dict):
        return {}
    rows: dict[str, list[str]] = {}
    for domain, tool_ids in obj.items():
        d = str(domain).strip() or "unknown"
        ids = _safe_str_list(tool_ids)
        if ids:
            rows[d] = sorted(ids)
    return rows


def _profile_command_samples(toolbox_profile: dict[str, Any], *, limit: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in _safe_list(toolbox_profile.get("command_samples")):
        if not isinstance(item, dict):
            continue
        tool_id = str(item.get("tool_id", "")).strip()
        command = str(item.get("command", "")).strip()
        if not tool_id or not command:
            continue
        rows.append({"tool_id": tool_id, "command": command})
        if len(rows) >= limit:
            break
    return rows


def _domain_summary_lines(domains: dict[str, list[str]]) -> list[str]:
    if not domains:
        return ["- `unknown`: `0` tools"]
    lines: list[str] = []
    for domain in sorted(domains.keys()):
        lines.append(f"- `{domain}`: `{len(domains.get(domain, []))}` tools")
    return lines


def _sample_tool_detail_lines(
    tool_ids: list[str],
    tool_catalog: dict[str, str],
    tool_meta: dict[str, dict[str, Any]],
    *,
    limit: int,
) -> list[str]:
    lines: list[str] = []
    for tool_id in tool_ids[:limit]:
        meta = _safe_dict(tool_meta.get(tool_id))
        entrypoint = str(meta.get("entrypoint", "")).strip() or tool_catalog.get(tool_id, "")
        domain = str(meta.get("domain", "")).strip() or "unknown"
        owner = str(meta.get("owner", "")).strip() or str(meta.get("development_owner", "")).strip() or "unknown"
        usage_summary = str(meta.get("usage_summary", "")).strip()
        commands = _safe_str_list(meta.get("command_examples"))
        command_preview = commands[0] if commands else "see --help in runtime/TOOL_DOCS_STRUCTURED.yaml"
        lines.append(f"- `{tool_id}` | domain:`{domain}` | owner:`{owner}`")
        lines.append(f"  - entrypoint: `{entrypoint}`")
        lines.append(f"  - quick_command: `{command_preview}`")
        if usage_summary:
            lines.append(f"  - usage_summary: {usage_summary}")
    return lines


def render_dynamic_sections(
    layer_num: int,
    chain_packets: dict[str, list[str]],
    chain_objectives: dict[str, str],
    static_layer_sections: dict[int, dict[str, list[str]]],
    tool_catalog: dict[str, str],
    toolbox_profile: dict[str, Any],
) -> list[str]:
    chain_ids = list(chain_packets.keys())
    chain_count = len(chain_ids)
    tool_meta = _profile_tools(toolbox_profile)
    domains = _profile_domains(toolbox_profile)
    tool_ids = sorted(tool_meta.keys()) if tool_meta else sorted(tool_catalog.keys())
    tool_count = len(tool_ids)
    workflow_steps = _safe_str_list(toolbox_profile.get("workflow_steps_ranked"))
    required_docs_ranked = _safe_str_list(toolbox_profile.get("required_docs_ranked"))
    coverage = _safe_dict(toolbox_profile.get("section_coverage"))
    command_samples = _profile_command_samples(toolbox_profile, limit=10)
    toolbox_scripts_dir = str(toolbox_profile.get("toolbox_scripts_dir", "")).strip() or "tooling_governance/default/scripts"
    toolbox_instance_dir = str(toolbox_profile.get("toolbox_instance_dir", "")).strip() or "tooling_governance/default"
    sync_contract_pass = 0
    for meta in tool_meta.values():
        sync = _safe_dict(meta.get("sync_contract"))
        if (
            sync.get("require_tool_registry_docs_sync") is True
            and sync.get("require_machine_map_anchor_sync") is True
            and sync.get("require_tool_change_ledger_append") is True
        ):
            sync_contract_pass += 1
    blocks: list[str] = []

    if layer_num == 0:
        blocks.extend(
            [
                "## AI 阅读目录（目标技能 toolbox 视角）",
                "- 第一步：读 `Toolbox 能力总览`，先理解工具分层与能力边界。",
                "- 第二步：读 `快速使用入口`，直接复制命令验证工具。",
                "- 第三步：读 `开发过程（脚本反向推导写入）`，按固定链路做改动。",
                "- 第四步：读 `运行维护入口`，完成 gate 与闭环验收。",
                "",
                "## 文档链路总览",
                "- 骨干链路（backbone）: `1` 条",
                "  - `L0 -> L1 -> ... -> L13`",
                f"- 工具文档母链（L1/L2）: `{chain_count}` 条",
            ]
        )
        for chain_id in chain_ids:
            blocks.append(f"  - `{chain_id}`: {chain_objective(chain_id, chain_objectives)}")
        blocks.extend(
            [
                f"- 总链路数（骨干 + 里程碑）: `{chain_count + 1}`",
                "",
                "## Toolbox 能力总览（目标技能）",
                "- 主语约束：本层描述“本技能 toolbox 能做什么、如何开发与运维”，不是治理流程叙事。",
                f"- managed_tool_count: `{tool_count}`",
                f"- toolbox_scripts_dir: `{toolbox_scripts_dir}`",
                f"- toolbox_instance_dir: `{toolbox_instance_dir}`",
                "- source_of_truth: `runtime/TOOL_REGISTRY.yaml` + `runtime/TOOL_DOCS_STRUCTURED.yaml`",
            ]
        )
        blocks.extend(_domain_summary_lines(domains))
        if tool_ids:
            blocks.append("- representative_tools:")
            blocks.extend(_sample_tool_detail_lines(tool_ids, tool_catalog, tool_meta, limit=8))
        blocks.extend(
            [
                "",
                "## 快速使用入口（AI 直接执行）",
            ]
        )
        if command_samples:
            for row in command_samples:
                blocks.append(f"- `{row.get('tool_id', '')}` -> `{row.get('command', '')}`")
        else:
            blocks.append("- `python3 scripts/runtime_pain_batch.py --help`")
            blocks.append(f"- `python3 {toolbox_scripts_dir}/tooling_docs_query.py --help`")
        blocks.extend(
            [
                "",
                "## 开发过程（脚本反向推导写入）",
                "- Step 1: 更新 `runtime/TOOL_REGISTRY.yaml` 与 `runtime/TOOL_DOCS_STRUCTURED.yaml`，固定 tool_id 事实基线。",
                "- Step 2: 执行 docs-first 变更链（文档 -> 脚本 -> ledger -> gate）。",
                "- Step 3: 运行 `tooling_governance_auto_writeback.py` 回填 L0-L13。",
                "- Step 4: 运行 full gate + target outcome lint，确认路径和锚点可解析。",
                "- Step 5: 追加 `runtime/TOOL_CHANGE_LEDGER.jsonl` 并归档审计结果。",
                "",
                "## 运行维护入口",
                f"- `python3 {toolbox_scripts_dir}/mstg_l0_l13_full_gate_lint.py --instance-root {toolbox_instance_dir}`",
                f"- `python3 {toolbox_scripts_dir}/mstg_target_governance_outcome_lint.py --instance-root {toolbox_instance_dir}`",
                f"- `python3 {toolbox_scripts_dir}/tooling_docs_query.py --tool-id <tool_id>`",
                "",
            ]
        )
        return blocks

    if layer_num == 1:
        blocks.extend(
            [
                "## 工具文档母链定义（L1）",
                f"- milestone_chain_count: `{chain_count}`",
            ]
        )
        for idx, chain_id in enumerate(chain_ids, start=1):
            blocks.append(f"- chain_{idx}: `{chain_id}`")
            blocks.append(f"  - 里程碑目标: {chain_objective(chain_id, chain_objectives)}")
            blocks.append(f"  - 文档焦点: {chain_focus(chain_id)}")
            blocks.append(f"  - 文档承载: `docs/L1/chains/{chain_slug(chain_id)}.md`")
        blocks.extend(
            [
                "",
                "## Toolbox 接口面编排",
                "- AI 使用者入口：从 usage 段拿命令、输入、输出。",
                "- AI 开发者入口：从 modification/development 段拿更新顺序和 required_docs。",
                "- 运维入口：通过 `tooling_governance_apply_change.py` 执行统一变更链。",
                "",
                "## 工具文档维护入口（固定母线）",
                "- 每条母链都必须落到目标技能工具文档维护动作，不能只描述治理流程动作。",
                "- 目标技能脚本变更默认走 `tooling_governance_auto_writeback.py`（内部调用 `tooling_governance_apply_change.py`）。",
                "- 固定顺序：先文档更新，再脚本更新，再运维/ledger，最后 gate。",
                "- 工具自进化必须留痕：同步 `runtime/TOOL_DOCS_STRUCTURED.yaml`、`runtime/TOOL_REGISTRY.yaml`、machine-map anchors，并追加 `runtime/TOOL_CHANGE_LEDGER.jsonl`。",
                f"- 本层关键脚本目录：`{toolbox_scripts_dir}`。",
                "",
            ]
        )
        return blocks

    if layer_num == 2:
        blocks.append("## 工具文档子链包映射（L2）")
        for chain_id in chain_ids:
            blocks.append(f"- 对 `{chain_id}` 的细化里程碑:")
            for packet in chain_packets.get(chain_id, []):
                blocks.append(f"  - `{packet}`")
            blocks.append(f"  - 链路包文档: `docs/L2/chains/{chain_slug(chain_id)}/README.md`")
        blocks.extend(
            [
                "",
                "## Toolbox 字段合同覆盖率",
                f"- usage_coverage: `{coverage.get('usage', 0)}/{tool_count}`",
                f"- modification_coverage: `{coverage.get('modification', 0)}/{tool_count}`",
                f"- development_coverage: `{coverage.get('development', 0)}/{tool_count}`",
                "- 若任一覆盖率低于 tool_count，视为合同未闭环。",
                "",
                "## 结构化文档查询与写回接口",
                "- 结构化文档来源: `runtime/TOOL_DOCS_STRUCTURED.yaml`",
                "- 读取接口: `tooling_docs_query.py`",
                "- 写回接口: `tooling_docs_record.py / tooling_change_ledger.py`",
                "- 每个 tool_id 必须具备 `usage/modification/development` 三段。",
                "",
                "## 开发流水线（来自工具合同）",
            ]
        )
        for step in workflow_steps[:12]:
            blocks.append(f"- `{step}`")
        if not workflow_steps:
            blocks.append("- `docs_pre_update -> script_update -> tool_docs_registry_sync_check -> machine_map_anchor_sync -> ledger_append -> full_gate_lint`")
        blocks.extend(
            [
                "",
                "## 锚点映射合同（目标技能）",
                "- 被治理目标技能的 `L0-L13` 文档必须包含并维护：`tool_anchor_refs`、`script_anchor_refs`、`asset_anchor_refs`、`evidence_anchor_refs`。",
                "- 目标技能后续修改时，影响分析必须优先消费 machine map 锚点字段，仅在缺失时才允许回退到规则推断。",
                "- 每次工具演进必须同步工具文档锚点（`usage/modification/development`）与 machine-map 锚点，禁止脚本文档漂移。",
                "",
            ]
        )
        return blocks

    if layer_num == 3:
        blocks.extend(
            [
                "## 共享运行时与依赖策略（Toolbox）",
                f"- 治理脚本目录: `{toolbox_scripts_dir}`",
                "- 业务脚本（skill_tool）与治理脚本（governance_toolbox）必须分层，禁止职责混写。",
                "- 依赖策略：优先复用 shared tooling runtime，避免重复造轮子。",
                "- tool_id 对应脚本入口与文档锚点必须保持一致。",
                "",
                "## 依赖边界快照",
            ]
        )
        blocks.extend(_domain_summary_lines(domains))
        blocks.append("")
        return blocks

    if layer_num == 4:
        blocks.extend(
            [
                "## 决策与控制点",
                "- 任何需要环境变量/密钥的变更必须先声明决策依据与最小权限。",
                "- 涉及敏感信息的写回必须先通过策略审查再进入执行链。",
                "",
                "## 环境变量与密钥合同",
                "- 默认策略：toolbox 脚本不依赖 secret；如需要环境变量，必须文档显式声明最小权限。",
                "- 禁止硬编码 key/token/credential 到脚本、文档、ledger 和审计产物。",
                f"- strict_sync_contract_tools: `{sync_contract_pass}/{tool_count}`（三项同步约束全部为 true）。",
                "",
                "## 安全写回规则",
                "- 示例命令必须用占位符，不落敏感值。",
                "- gate 发现敏感信息时必须阻塞并先修复。",
                "",
            ]
        )
        return blocks

    if layer_num == 5:
        blocks.extend(
            [
                "## 执行规格",
                "- 本层规定状态资产的写入顺序与一致性约束。",
                "- 所有写入动作必须以 tool_id 为主键可回放。",
                "",
                "## 状态与存储合同（按资产拆分）",
                "- `runtime/TOOL_REGISTRY.yaml`: 工具清单与 entrypoint 权威源。",
                "- `runtime/TOOL_DOCS_STRUCTURED.yaml`: usage/modification/development 三段合同源。",
                "- `runtime/TOOL_CHANGE_LEDGER.jsonl`: 变更留痕源。",
                "- `runtime/TOOLING_GOVERNANCE_STATE.yaml`: 运行态与治理态记录。",
                "",
                "## required_docs 高频集合",
            ]
        )
        for doc_path in required_docs_ranked[:14]:
            blocks.append(f"- `{doc_path}`")
        if not required_docs_ranked:
            blocks.append("- `docs/L1/README.md` / `docs/L2/README.md` / `docs/L10/README.md` / `docs/L12/README.md` / `docs/L13/README.md`")
        blocks.append("")
        return blocks

    if layer_num == 6:
        blocks.extend(
            [
                "## 接口与数据契约",
                "- 输入输出必须对齐 `TOOL_DOCS_STRUCTURED.yaml` 的 usage/modification/development 三段结构。",
                "- 同一 tool_id 的接口字段变更必须同步到 docs 与 ledger。",
                "",
                "## 执行与幂等流程（docs-first）",
                "- 单次变更最小闭环：`docs_pre_update -> script_update -> machine_map_anchor_sync -> ledger_append -> full_gate_lint`。",
                "- 幂等要求：重复执行不应破坏已有锚点，不应产生冲突资产。",
                "- 中断恢复：从最近成功步骤继续并重跑 full gate。",
                "",
                "## 标准执行顺序（来自工具合同）",
            ]
        )
        for step in workflow_steps[:12]:
            blocks.append(f"- `{step}`")
        if not workflow_steps:
            blocks.append("- `docs_pre_update`")
            blocks.append("- `script_update`")
            blocks.append("- `tool_docs_registry_sync_check`")
            blocks.append("- `machine_map_anchor_sync`")
            blocks.append("- `ledger_append`")
            blocks.append("- `full_gate_lint`")
        blocks.extend(
            [
                "",
                "## 命令入口",
                f"- `python3 {toolbox_scripts_dir}/tooling_governance_apply_change.py --help`",
                f"- `python3 {toolbox_scripts_dir}/tooling_governance_auto_writeback.py --help`",
                "",
            ]
        )
        return blocks

    if layer_num == 7:
        blocks.extend(
            [
                "## 文件与资产映射",
                "- 每个故障点必须能映射到 docs/runtime/scripts 的具体路径。",
                "- 先修复映射缺口，再修复业务逻辑，避免二次漂移。",
                "",
                "## 失败模型与分诊",
                "- 失败类 1：registry 与 docs 不一致（tool_id 漂移/缺失）。",
                "- 失败类 2：machine-map 锚点字段缺失或路径不可解析。",
                "- 失败类 3：ledger 缺失导致变更不可追溯。",
                "- 失败类 4：target outcome lint 失败。",
                "",
                "## 分诊顺序（先证据后修复）",
                "- 先看 `runtime/L0_L13_LINEAR_INDEX.yaml` 识别层级链路问题。",
                "- 再看 `runtime/TOOL_DOCS_STRUCTURED.yaml` 与 `runtime/TOOL_REGISTRY.yaml` 校对 tool_id。",
                "- 最后看 `runtime/TOOL_CHANGE_LEDGER.jsonl` 判断是否丢失变更留痕。",
                "",
            ]
        )
        return blocks

    if layer_num == 8:
        blocks.extend(
            [
                "## 实施切片与写入计划",
                "- 先切分 contract/flow/mapping/evidence 四类写入切片，再逐项执行。",
                "- 每个切片完成后立即记录可观测证据，禁止批量盲写。",
                "",
                "## 可观测性与日志合同",
                "- 运行事件必须可追溯到 run_id、plan_id、tool_id、变更摘要。",
                "- 审计轨迹由 `GOVERNANCE_AUDIT_LOG.jsonl` + `runs/<run_id>.json` 组成。",
                "- 文档闭环证据需回指 L1/L2/L13 与 runtime 索引资产。",
                "",
                "## 观测指标（最低集）",
                f"- managed_tool_count: `{tool_count}`",
                f"- command_sample_count: `{len(command_samples)}`",
                f"- workflow_step_count: `{len(workflow_steps)}`",
                "",
            ]
        )
        return blocks

    if layer_num == 9:
        blocks.extend(
            [
                "## 测试与 Hazard 覆盖",
                "- 至少覆盖 functional/boundary/hazard/regression 四类风险。",
                "- gate 失败视为阻塞，不允许继续 release。",
                "",
                "## 测试与回归矩阵",
                "- functional: 业务工具命令可执行且输出结构化结果。",
                "- schema: L0-L13 machine-map 字段完整、锚点可解析。",
                "- regression: docs/registry/ledger 同步保持成立。",
                "- release_gate: full_gate + target_outcome_lint 同时 PASS。",
                "",
                "## 推荐最小回归命令",
                f"- `python3 {toolbox_scripts_dir}/tooling_governance_lint.py --instance-root {toolbox_instance_dir}`",
                f"- `python3 {toolbox_scripts_dir}/mstg_l0_l13_linear_lint.py --instance-root {toolbox_instance_dir}`",
                f"- `python3 {toolbox_scripts_dir}/mstg_l0_l13_layer_schema_lint.py --instance-root {toolbox_instance_dir}`",
                f"- `python3 {toolbox_scripts_dir}/mstg_l0_l13_full_gate_lint.py --instance-root {toolbox_instance_dir}`",
                "",
            ]
        )
        return blocks

    if layer_num == 10:
        blocks.extend(
            [
                "## 部署与回滚门禁",
                "- 发布前必须通过 full gate 与 target outcome lint。",
                "- 回滚后必须补写 ledger 并重跑 gate，确保状态回正。",
                "",
                "## 变更台账映射（L10）",
                "- 每次脚本或文档修改必须追加 ledger 记录。",
                "- ledger 最小字段：`event_id/timestamp_utc/tool_id/change_type/summary`。",
                "- 记录必须可回溯到 docs 与 gate 结果。",
                "",
                "## 高频 required_docs（影响面判定）",
            ]
        )
        for doc_path in required_docs_ranked[:12]:
            blocks.append(f"- `{doc_path}`")
        if not required_docs_ranked:
            blocks.append("- `docs/L10/README.md` 与 `docs/L13/README.md` 作为最小闭环文档。")
        blocks.append("")
        return blocks

    if layer_num == 11:
        blocks.extend(
            [
                "## 运行与审计 Runbook（Toolbox 运维）",
                "- 场景 A（新增/替换工具）：先更新 registry + structured docs，再执行 auto_writeback，再跑 gate。",
                "- 场景 B（调整工具用法）：更新 usage 段并同步 machine-map 锚点，再追加 ledger。",
                "- 场景 C（故障修复）：先跑 lint 定位，再按 docs-first 顺序修复，最后重跑 full gate。",
                "",
                "## 常用运维命令",
                f"- `python3 {toolbox_scripts_dir}/tooling_docs_query.py --help`",
                f"- `python3 {toolbox_scripts_dir}/tooling_docs_record.py --help`",
                f"- `python3 {toolbox_scripts_dir}/tooling_change_ledger.py --help`",
                f"- `python3 {toolbox_scripts_dir}/tooling_governance_auto_writeback.py --help`",
                "",
            ]
        )
        return blocks

    if layer_num == 12:
        blocks.extend(
            [
                "## 运营策略与例外处理",
                "- 例外只能在证据充分且可审计条件下触发，不得绕过基础门禁。",
                "- 任何例外都必须附带恢复路径与再验证命令。",
                "",
                "## Gate 与 lint 控制",
                "- Gate 顺序不可跳过：tooling_governance_lint -> linear_lint -> layer_schema_lint -> full_gate_lint -> target_outcome_lint。",
                "- 任一 gate FAIL，必须先修复再继续；不得带 FAIL 进入 release。",
                "- target outcome lint 是基础门禁，不允许人工豁免覆盖。",
                "",
                "## 目标技能结果门禁命令",
                f"- `python3 {toolbox_scripts_dir}/mstg_target_governance_outcome_lint.py --instance-root {toolbox_instance_dir}`",
                "",
            ]
        )
        return blocks

    if layer_num == 13:
        blocks.extend(
            [
                "## 验收证据与闭环归档",
                "- 必备证据: `mstg_l0_l13_full_gate_lint` PASS（包含 `mstg_target_governance_outcome_lint`）、`tooling_governance_lint` PASS、审计 run 终态 PASS。",
                "- 必备归档: `GOVERNANCE_AUDIT_LOG.jsonl` 与 `runs/<run_id>.json` 可追溯到本次治理目标与结果。",
                "- 必备一致性: L1 里程碑链、L2 子里程碑映射、L13 闭环声明三者保持一致。",
                f"- L2 子链闭环总数: `{chain_count}`（每条均需声明 `L2 -> L13`）。",
                "- 工具文档闭环要求: `runtime/TOOL_DOCS_STRUCTURED.yaml` 中每个 tool_id 均具备 usage/modification/development 且与 registry 对齐。",
                f"- section_coverage: usage `{coverage.get('usage', 0)}/{tool_count}` | modification `{coverage.get('modification', 0)}/{tool_count}` | development `{coverage.get('development', 0)}/{tool_count}`",
            ]
        )
        for chain_id in chain_ids:
            blocks.append(f"  - `{chain_id}`: 需提供 `L2 -> L13` 的闭环验收证据（gate + audit trace）。")
        blocks.extend(
            [
                "",
                "## 代码落地映射",
                "- 核心入口: `scripts/init_tooling_governance_instance.py`、`scripts/tooling_governance_apply_change.py`。",
                "- 审计入口: `scripts/governance_audit_log.py`。",
                "- 结构化落地: `runtime/TOOL_REGISTRY.yaml`、`runtime/TOOL_DOCS_STRUCTURED.yaml`、`runtime/TOOL_CHANGE_LEDGER.jsonl`。",
                "",
                "## 目标技能锚点验收",
                "- 验收时必须验证目标技能 `L0-L13` machine map 锚点字段齐全、非空且路径/工具可解析。",
                "- 任一锚点字段缺失或锚点不可解析，均视为治理未闭环。",
                "- 闭环通过后，L0-L13 作为后续 toolbox 开发与运维主手册（AI consume-first）。",
                "",
            ]
        )
        return blocks

    static_sections = static_layer_sections.get(layer_num, {})
    for title, bullets in static_sections.items():
        blocks.append(title)
        for bullet in bullets:
            blocks.append(f"- {bullet}")
        blocks.append("")
    return blocks


def layer_specific_map_fields(
    layer_num: int,
    chain_packets: dict[str, list[str]],
    anchor_field_keys: list[str],
    doc_files: dict[int, str],
    tool_catalog: dict[str, str],
    toolbox_profile: dict[str, Any],
) -> dict[str, Any]:
    chain_ids = list(chain_packets.keys())
    tool_ids = sorted(_profile_tools(toolbox_profile).keys()) or sorted(tool_catalog.keys())
    domains = _profile_domains(toolbox_profile)
    domain_counts = {domain: len(items) for domain, items in domains.items()}
    workflow_steps = _safe_str_list(toolbox_profile.get("workflow_steps_ranked"))
    required_docs_ranked = _safe_str_list(toolbox_profile.get("required_docs_ranked"))
    coverage = _safe_dict(toolbox_profile.get("section_coverage"))
    toolbox_scripts_dir = str(toolbox_profile.get("toolbox_scripts_dir", "")).strip() or "tooling_governance/default/scripts"

    base_fields = {
        "tool_domain_counts": domain_counts,
        "toolbox_scripts_dir": toolbox_scripts_dir,
        "workflow_steps_ranked": workflow_steps[:20],
    }
    if layer_num == 0:
        payload = {
            "doc_chain_topology": {
                "backbone_chain_count": 1,
                "milestone_chain_count": len(chain_ids),
                "milestone_chains": chain_ids,
            },
            "managed_tool_count": len(tool_ids),
            "managed_tool_ids": tool_ids,
            "quickstart_command_count": len(_profile_command_samples(toolbox_profile, limit=80)),
            "tool_docs_source_of_truth": ["runtime/TOOL_REGISTRY.yaml", "runtime/TOOL_DOCS_STRUCTURED.yaml"],
        }
        payload.update(base_fields)
        return payload
    if layer_num == 1:
        l1_chain_docs = {
            chain_id: f"docs/L1/chains/{chain_slug(chain_id)}.md" for chain_id in chain_ids
        }
        payload = {
            "milestone_chain_count": len(chain_ids),
            "milestone_chains": chain_ids,
            "l1_chain_docs": l1_chain_docs,
            "governance_entrypoint_contracts": ["toolbox_injection", "apply_change_sequence"],
            "tool_doc_chain_focus": {chain_id: chain_focus(chain_id) for chain_id in chain_ids},
        }
        payload.update(base_fields)
        return payload
    if layer_num == 2:
        l2_chain_docs = {
            chain_id: f"docs/L2/chains/{chain_slug(chain_id)}/README.md" for chain_id in chain_ids
        }
        payload = {
            "l2_sub_milestone_packets": chain_packets,
            "l2_chain_docs": l2_chain_docs,
            "structured_doc_contracts": ["tool_registry_sync", "tool_docs_structured_sync", "ledger_sync"],
            "target_docs_anchor_required": True,
            "required_anchor_fields": anchor_field_keys,
            "tool_doc_required_sections": ["usage", "modification", "development"],
            "tool_doc_section_coverage": {
                "usage": coverage.get("usage", 0),
                "modification": coverage.get("modification", 0),
                "development": coverage.get("development", 0),
            },
        }
        payload.update(base_fields)
        return payload
    if layer_num == 3:
        payload = {"shared_runtime_policy": ["shared_venv", "dependency_reuse", "non_conflicting_toolbox"]}
        payload.update(base_fields)
        return payload
    if layer_num == 4:
        payload = {"decision_gates": ["input_completeness_gate", "policy_gate", "evidence_gate"]}
        payload.update(base_fields)
        return payload
    if layer_num == 5:
        payload = {
            "execution_contracts": ["input_contract", "state_contract", "output_contract"],
            "required_docs_ranked": required_docs_ranked[:20],
        }
        payload.update(base_fields)
        return payload
    if layer_num == 6:
        payload = {
            "interface_contracts": ["request_response_contract", "schema_contract", "versioning_contract"],
            "canonical_docs_first_flow": workflow_steps[:10],
        }
        payload.update(base_fields)
        return payload
    if layer_num == 7:
        payload = {"asset_mappings": ["semantic_to_doc_map", "semantic_to_script_map", "anchor_trace_map"]}
        payload.update(base_fields)
        return payload
    if layer_num == 8:
        payload = {"write_slices": ["contract_slice", "flow_slice", "mapping_slice", "evidence_slice", "audit_trace_slice"]}
        payload.update(base_fields)
        return payload
    if layer_num == 9:
        payload = {"test_hazard_matrix": ["functional", "boundary", "hazard", "regression"]}
        payload.update(base_fields)
        return payload
    if layer_num == 10:
        payload = {
            "release_rollback_gates": ["pre_release_gate", "rollout_gate", "rollback_gate"],
            "required_docs_ranked": required_docs_ranked[:20],
        }
        payload.update(base_fields)
        return payload
    if layer_num == 11:
        payload = {
            "runbook_controls": ["observability", "alerting", "audit_trace", "incident_escalation"],
            "runbook_entry_scripts": [
                "tooling_docs_query.py",
                "tooling_docs_record.py",
                "tooling_change_ledger.py",
                "tooling_governance_auto_writeback.py",
            ],
        }
        payload.update(base_fields)
        return payload
    if layer_num == 12:
        payload = {"operation_exceptions": ["policy_enforcement", "manual_override", "exception_audit"]}
        payload.update(base_fields)
        return payload
    if layer_num == 13:
        payload = {
            "acceptance_evidence_pack": ["evidence_receipt", "mapping_trace", "closure_archive"],
            "target_docs_anchor_required": True,
            "required_anchor_fields": anchor_field_keys,
            "tool_doc_section_coverage": {
                "usage": coverage.get("usage", 0),
                "modification": coverage.get("modification", 0),
                "development": coverage.get("development", 0),
            },
            "milestone_chain_closure": {
                "required_final_layer": "L13",
                "chains": [
                    {
                        "chain_id": chain_id,
                        "from_layer": "L2",
                        "to_layer": "L13",
                        "acceptance_ref": "docs/L13/README.md#验收证据与闭环归档",
                    }
                    for chain_id in chain_ids
                ],
            },
        }
        payload.update(base_fields)
        return payload
    _ = doc_files
    return {}
