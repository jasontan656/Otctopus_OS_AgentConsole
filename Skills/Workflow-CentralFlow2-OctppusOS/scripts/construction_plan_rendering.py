from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


OFFICIAL_PLAN_KIND = "official_plan"
PREVIEW_PLAN_KIND = "preview_skeleton"
PREVIEW_PLAN_STATE = "preview_only"
OFFICIAL_INITIAL_PLAN_STATE = "planned_unused"


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return cleaned or "execution_atom_pack"


def _split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def design_steps_from_plan(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    steps: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = _split_row(line)
        if len(cells) < 9 or cells[0] in {"design_step_id", "---"} or not cells[0].startswith("`"):
            continue
        steps.append(
            {
                "design_step_id": cells[0].strip("`"),
                "target_requirement_atoms": cells[1],
                "dependencies": cells[2],
                "implementation_actions": cells[3],
                "stage_assertions": cells[4],
                "stage_tests": cells[5],
                "stage_acceptance": cells[6],
                "live_delivery_witness": cells[7],
                "rollback_or_risk": cells[8],
            }
        )
    return steps


def default_steps() -> list[dict[str, str]]:
    return [
        {
            "design_step_id": "DESIGN-PREVIEW-01",
            "target_requirement_atoms": "preview_only",
            "dependencies": "none",
            "implementation_actions": "preview skeleton only",
            "stage_assertions": "preview only",
            "stage_tests": "not applicable",
            "stage_acceptance": "not executable",
            "live_delivery_witness": "preview tree only",
            "rollback_or_risk": "must be replaced by official plan before implementation",
        }
    ]


def _plan_state(plan_kind: str) -> str:
    return PREVIEW_PLAN_STATE if plan_kind == PREVIEW_PLAN_KIND else OFFICIAL_INITIAL_PLAN_STATE


def _execution_eligible(plan_kind: str) -> bool:
    return plan_kind == OFFICIAL_PLAN_KIND


def _state_sync_eligible(plan_kind: str) -> bool:
    return plan_kind == OFFICIAL_PLAN_KIND


def _pack_entry(index: int, step: dict[str, str], plan_kind: str) -> dict[str, object]:
    pack_slug = f"{index:02d}_{slugify(step['design_step_id'])}"
    return {
        "pack_id": f"PACK-{index:02d}",
        "design_step_id": step["design_step_id"],
        "pack_dir": pack_slug,
        "plan_kind": plan_kind,
        "pack_state": _plan_state(plan_kind),
        "execution_eligible": _execution_eligible(plan_kind),
        "state_sync_eligible": _state_sync_eligible(plan_kind),
        "reusable_as_official_plan": False,
        "machine_manifest": f"{pack_slug}/pack_manifest.yaml",
        "progress_ledger": f"{pack_slug}/phase_status.jsonl",
        "evidence_registry": f"{pack_slug}/evidence_registry.json",
    }


def render_pack_registry(steps: list[dict[str, str]], design_plan_path: Path, plan_kind: str) -> str:
    payload = {
        "plan_kind": plan_kind,
        "plan_state": _plan_state(plan_kind),
        "execution_eligible": _execution_eligible(plan_kind),
        "state_sync_eligible": _state_sync_eligible(plan_kind),
        "reusable_as_official_plan": False,
        "design_plan_path": design_plan_path.name,
        "design_step_ids": [step["design_step_id"] for step in steps],
        "packs": [_pack_entry(index, step, plan_kind) for index, step in enumerate(steps, start=1)],
    }
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)


def render_root_index(steps: list[dict[str, str]], plan_kind: str) -> str:
    plan_state = _plan_state(plan_kind)
    execution_eligible = "true" if _execution_eligible(plan_kind) else "false"
    state_sync_eligible = "true" if _state_sync_eligible(plan_kind) else "false"
    lines = [
        "# Execution_atom_plan&validation_packs Index",
        "",
        "## 1. 根目录职责",
        "- plan_root_role: 把设计阶段计划拆成按 pack 执行、按 pack 验证、按 pack 回写的独立闭环目录。",
        "- designer_plan_source: `../08_dev_execution_plan.md`",
        f"- plan_kind: `{plan_kind}`",
        f"- plan_state: `{plan_state}`",
        f"- execution_eligible: `{execution_eligible}`",
        f"- state_sync_eligible: `{state_sync_eligible}`",
        "- reusable_as_official_plan: `false`",
        "- pack_execution_rule: implementation 期间一次只激活一个 official pack，并在 pack 内部再按 inner phase 推进。",
        "",
        "## 2. pack 顺序",
        "| pack_dir | design_step_id | plan_kind | pack_state | pack_goal | machine_entry |",
        "|---|---|---|---|---|---|",
    ]
    for index, step in enumerate(steps, start=1):
        pack_slug = f"{index:02d}_{slugify(step['design_step_id'])}"
        lines.append(
            f"| `{pack_slug}` | `{step['design_step_id']}` | `{plan_kind}` | `{plan_state}` | {step['implementation_actions']} | `{pack_slug}/pack_manifest.yaml` |"
        )
    lines.extend(
        [
            "",
            "## 3. implementation 读取规则",
            "- active_pack_only: 一次只读取并更新当前 official pack 目录。",
            "- preview_skeleton_block: `plan_kind=preview_skeleton` 的 pack 树不能用于 implementation、state sync 或 active pack 选择。",
            "- official_plan_block: 已进入 `accepted` / `retired` 的 official pack 树不能回到新的 construction plan 输入；新一轮必须重建新的 official plan。",
            "- mother_doc_read_boundary: 只允许读取 active pack 显式声明的 `source_mother_doc_refs`，不得通读整个 mother_doc 树。",
            "- writeback_boundary: phase_status.jsonl、evidence_registry.json 与 markdown 章节分别回写，不得混堆。",
            "",
        ]
    )
    return "\n".join(lines)


def write_pack(pack_dir: Path, step: dict[str, str], index: int, plan_kind: str) -> None:
    pack_id = f"PACK-{index:02d}"
    pack_state = _plan_state(plan_kind)
    execution_eligible = _execution_eligible(plan_kind)
    state_sync_eligible = _state_sync_eligible(plan_kind)
    pack_dir.mkdir(parents=True, exist_ok=True)
    pack_dir.joinpath("00_index.md").write_text(
        (
            "# Execution Atom Pack Index\n\n"
            "## 1. Pack Identity\n"
            f"- pack_id: {pack_id}\n"
            f"- design_step_id: {step['design_step_id']}\n"
            f"- plan_kind: {plan_kind}\n"
            f"- pack_state: {pack_state}\n"
            f"- execution_eligible: {'true' if execution_eligible else 'false'}\n"
            f"- state_sync_eligible: {'true' if state_sync_eligible else 'false'}\n"
            "- reusable_as_official_plan: false\n"
            f"- pack_goal: {step['implementation_actions']}\n\n"
            "## 2. Read/Write Contract\n"
            "- human_anchor_docs:\n"
            "  - `01_scope_and_intent.md`\n"
            "  - `02_inner_dev_phases.md`\n"
            "  - `03_validation_and_writeback.md`\n"
            "- machine_anchor_files:\n"
            "  - `pack_manifest.yaml`\n"
            "  - `inner_phase_plan.json`\n"
            "  - `phase_status.jsonl`\n"
            "  - `evidence_registry.json`\n"
        ),
        encoding="utf-8",
    )
    pack_dir.joinpath("01_scope_and_intent.md").write_text(
        (
            "# Scope And Intent\n\n"
            "## 1. Scope\n"
            f"- target_requirement_atoms: {step['target_requirement_atoms']}\n"
            f"- implementation_actions: {step['implementation_actions']}\n"
            "- changed_files_boundary: current pack owned source, test, config, and runtime files only\n\n"
            "## 2. Design Intent\n"
            f"- design_plan_refs: `{step['design_step_id']}`\n"
            "- source_mother_doc_refs:\n"
            "  - `08_dev_execution_plan.md`\n"
            f"- plan_kind: `{plan_kind}`\n"
            f"- pack_state: `{pack_state}`\n"
            f"- execution_eligible: `{'true' if execution_eligible else 'false'}`\n"
            f"- state_sync_eligible: `{'true' if state_sync_eligible else 'false'}`\n"
            f"- design_intent_proof_target: {step['stage_assertions']}\n"
            f"- stage_acceptance_target: {step['stage_acceptance']}\n"
        ),
        encoding="utf-8",
    )
    pack_dir.joinpath("02_inner_dev_phases.md").write_text(
        (
            "# Inner Dev Phases\n\n"
            "| inner_phase_id | phase_goal | implementation_slice | validation_slice | evidence_writeback_slice | phase_exit_signal |\n"
            "|---|---|---|---|---|---|\n"
            f"| `PHASE-01` | 固化本 pack 的框架与边界 | {step['implementation_actions']} | {step['stage_assertions']} | 更新 `pack_manifest.yaml` 与 `inner_phase_plan.json` | 边界与改动面固定 |\n"
            f"| `PHASE-02` | 落真实实现与局部验证 | {step['implementation_actions']} | {step['stage_tests']} | 追加 `phase_status.jsonl` | 当前切片实现可验证 |\n"
            f"| `PHASE-03` | 分域证据回写与阶段验收 | 分域整理 code/tests/runtime/log/db/mq/redis/operator_notes 证据 | {step['stage_acceptance']} | 更新 `evidence_registry.json` 与 `03_validation_and_writeback.md` | 当前 pack 可切换到下一个 pack |\n"
        ),
        encoding="utf-8",
    )
    pack_dir.joinpath("03_validation_and_writeback.md").write_text(
        (
            "# Validation And Writeback\n\n"
            "## 1. Validation Contract\n"
            f"- tests_run_target: {step['stage_tests']}\n"
            f"- test_why_it_proves_design: {step['stage_assertions']}\n"
            f"- stage_acceptance_rule: {step['stage_acceptance']}\n"
            f"- pack_state: `{pack_state}`\n\n"
            "## 2. Writeback Contract\n"
            "- phase_status_jsonl_usage: 每个 inner phase 完成后追加一行结构化状态。\n"
            "- evidence_registry_usage: 按 code/tests/runtime/logs/db/mq/redis/operator_notes 分域登记证据。\n"
            "- divergence_escalation_rule: 若 pack 意图变化，先回写本 pack，再回写 mother doc 设计阶段计划。\n"
        ),
        encoding="utf-8",
    )
    pack_manifest = {
        "pack_id": pack_id,
        "design_step_id": step["design_step_id"],
        "plan_kind": plan_kind,
        "pack_state": pack_state,
        "execution_eligible": execution_eligible,
        "state_sync_eligible": state_sync_eligible,
        "reusable_as_official_plan": False,
        "pack_goal": step["implementation_actions"],
        "design_plan_refs": [step["design_step_id"]],
        "source_mother_doc_refs": ["08_dev_execution_plan.md"],
        "target_requirement_atoms": [step["target_requirement_atoms"]],
        "implementation_actions": [step["implementation_actions"]],
        "changed_files_boundary": ["current pack owned source, test, config, and runtime files only"],
        "stage_acceptance_target": [step["stage_acceptance"]],
        "machine_files": {
            "inner_phase_plan": "inner_phase_plan.json",
            "phase_status_ledger": "phase_status.jsonl",
            "evidence_registry": "evidence_registry.json",
        },
    }
    pack_dir.joinpath("pack_manifest.yaml").write_text(
        yaml.safe_dump(pack_manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    inner_phase_plan = {
        "pack_id": pack_id,
        "design_step_id": step["design_step_id"],
        "plan_kind": plan_kind,
        "pack_state": pack_state,
        "execution_eligible": execution_eligible,
        "inner_phases": [
            {
                "inner_phase_id": "PHASE-01",
                "phase_goal": "框架与边界固定",
                "implementation_slice": [step["implementation_actions"]],
                "validation_slice": [step["stage_assertions"]],
                "evidence_writeback_slice": ["pack_manifest.yaml", "inner_phase_plan.json"],
                "phase_exit_signal": "边界固定",
            },
            {
                "inner_phase_id": "PHASE-02",
                "phase_goal": "真实实现与局部验证",
                "implementation_slice": [step["implementation_actions"]],
                "validation_slice": [step["stage_tests"]],
                "evidence_writeback_slice": ["phase_status.jsonl"],
                "phase_exit_signal": "实现可验证",
            },
            {
                "inner_phase_id": "PHASE-03",
                "phase_goal": "证据回写与阶段验收",
                "implementation_slice": ["分域整理 code/tests/runtime/log/db/mq/redis/operator_notes 证据"],
                "validation_slice": [step["stage_acceptance"]],
                "evidence_writeback_slice": ["evidence_registry.json", "03_validation_and_writeback.md"],
                "phase_exit_signal": "pack 验收完成",
            },
        ],
    }
    pack_dir.joinpath("inner_phase_plan.json").write_text(
        json.dumps(inner_phase_plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    pack_dir.joinpath("phase_status.jsonl").write_text(
        json.dumps(
            {
                "pack_id": pack_id,
                "inner_phase_id": "PHASE-00",
                "status": pack_state,
                "plan_kind": plan_kind,
                "execution_eligible": execution_eligible,
                "notes": "pack created from design plan",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    pack_dir.joinpath("evidence_registry.json").write_text(
        json.dumps(
            {
                "pack_id": pack_id,
                "plan_kind": plan_kind,
                "pack_state": pack_state,
                "evidence_domains": {
                    "code": [],
                    "tests": [],
                    "runtime": [],
                    "logs": [],
                    "db": [],
                    "mq": [],
                    "redis": [],
                    "operator_notes": [],
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
