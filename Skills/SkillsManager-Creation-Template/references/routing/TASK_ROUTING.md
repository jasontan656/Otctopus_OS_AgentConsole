---
doc_id: skillsmanager_creation_template.references.routing.task_routing
doc_type: topic_atom
topic: Task routing for scaffold profile selection
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This routing guide belongs to the governed skill tree under the facade.
---

# SkillsManager-Creation-Template Task Routing

## 何时选择哪种 profile
- `inline + none + advisory`
  - 适用于纯门面型或极薄技能。
  - 只生成 `SKILL.md / agents`，不额外生成 `references/`、`scripts/` 或 `tests/`。
- `referenced + contract_cli + guardrailed`
  - 适用于大多数治理型技能。
  - 规则真源落到 `references/`，CLI 只负责 contract 与 directive。
- `referenced + automation_cli + guardrailed`
  - 适用于既要保留文档真源，又要提供受治理自动化入口的技能。
  - 生成 `references/ + scripts/ + tests/`。
- `workflow_path + contract_cli + compiled`
  - 适用于需要高约束阅读链，但自动化动作有限的 workflow skill。
- `workflow_path + automation_cli + compiled`
  - 适用于复合 workflow 技能。
  - 同时生成 `references/` 与 `path/`；`path/` 只承载 workflow 正文，其他治理真源继续留在 `references/`。

## 选择规则
1. 先判断知识真源放在哪里：
   - 全部留在门面：`inline`
   - 下沉到原子文档：`referenced`
   - 需要可编译 workflow：`workflow_path`
2. 再判断是否真的需要机器入口：
   - 无：`none`
   - 只有 contract/directive：`contract_cli`
   - 需要实际动作命令：`automation_cli`
3. 最后判断 workflow 控制级别：
   - 描述性指导：`advisory`
   - 有明确治理门禁：`guardrailed`
   - 需要编译式 workflow：`compiled`

## 禁止事项
- 不要把旧 `skill_mode` 当作真相源。
- 不要默认禁止 `references/`、`tests/` 或 `assets/`。
- 不要为了兼容旧目录习惯保留额外 mapping 或 alias。
