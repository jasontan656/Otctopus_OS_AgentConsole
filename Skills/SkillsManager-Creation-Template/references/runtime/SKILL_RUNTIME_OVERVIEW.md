---
doc_id: skill_creation_template.runtime.overview
doc_type: topic_atom
topic: Runtime overview for the skill-mode governed template system
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The facade routes readers here for the runtime contract mirror.
- target: ../routing/TASK_ROUTING.md
  relation: routes_to
  direction: downstream
  reason: Task routing remains the first narrowing step after the contract.
- target: ../routing/PROFILE_ROUTING.md
  relation: routes_to
  direction: downstream
  reason: Skill-mode routing decides the target shape branch.
---

# Skill Runtime Overview

## 运行时入口
- 主入口：`./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`
- `SKILL.md` 只负责门面与路由；真实运行合同以同名 JSON 为准。

## 门面合同总览
- `guide_with_tool` 与 `executable_workflow_skill` 的 `SKILL.md` 只保留两段：
  - `Immediate Contract`
  - `Structured Entry`
- `Immediate Contract` 只承载立刻生效的边界、真实规则源与强约束。
- `Structured Entry` 只承载必读顺序与第一层入口。
- 详细命令清单、结构索引、规则正文与长解释必须下沉到 routing、topic、index 或 tooling docs。

## skill_mode 总览
- `guide_only`
  - 只生成 `SKILL.md`
  - 不要求文档树、runtime contract、专属 CLI
  - `SkillsManager-Doc-Structure` 与 `SkillsManager-Tooling-CheckUp` 的 shape 审计都应显式跳过
- `guide_with_tool`
  - 生成 facade、routing、governance、tooling docs
  - 继续受 `SkillsManager-Doc-Structure` 治理
  - 可拥有 lint/audit/check 工具，但不要求 CLI-first dual-file runtime_contracts
- `executable_workflow_skill`
  - 在 `guide_with_tool` 基线上补齐 runtime contract、stages、resident docs 与 stage contract 四件套
  - 必须受 `SkillsManager-Doc-Structure` 与 `SkillsManager-Tooling-CheckUp` 的完整治理

## 读取顺序
1. `runtime-contract --json`
2. `references/routing/TASK_ROUTING.md`
3. `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
4. `references/routing/PROFILE_ROUTING.md`（当需要选择 `skill_mode` 时）
5. `contract-reference`
6. `architecture-playbook`
7. `executable-workflow-reference`（仅 `executable_workflow_skill`）

## 验证闭环
- 生成 `guide_only`、`guide_with_tool`、`executable_workflow_skill` 三类 sandbox。
- 对后两类运行 `SkillsManager-Doc-Structure` lint。
- 验证 `guide_only` 在 `Doc-Structure` 与 `Tooling-CheckUp` 中返回显式 skip/exempt。
