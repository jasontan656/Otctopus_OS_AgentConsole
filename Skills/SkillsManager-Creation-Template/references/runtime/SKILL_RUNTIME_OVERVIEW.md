---
doc_id: skill_creation_template.runtime.contract_audit
doc_type: runtime_contract
topic: Audit copy of the SkillsManager-Creation-Template runtime contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This runtime contract governs the facade.
- target: ../routing/TASK_ROUTING.md
  relation: routes_to
  direction: downstream
  reason: The required read sequence enters task routing after loading this contract.
- target: ../governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md
  relation: routes_to
  direction: downstream
  reason: Doc-structure enforcement is a mandatory contract branch.
---

# SkillsManager-Creation-Template Runtime Contract

## Contract Header
- `contract_name`: `META_SKILL_TEMPLATE_RUNTIME_CONTRACT`
- `contract_version`: `v4`
- `validation_mode`: `cli_first_doc_structure`

## Authoring Model
- `SKILL.md` 角色：`entry_only_facade`
- 本节是目标 skill 的门面 contract 权威来源。
- facade 固定章节：
  - `技能定位`
  - `必读顺序`
  - `分类入口`
  - `适用域`
  - `执行入口`
  - `读取原则`
  - `结构索引`
- facade 只承载稳定边界与下一层入口，不承载治理正文。

## Routing Protocol
- 第一入口命令：`./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`
- 第一层路由：`references/routing/TASK_ROUTING.md`
- profile 路由：`references/routing/PROFILE_ROUTING.md`
- 读取顺序：
  1. `runtime-contract`
  2. `TASK_ROUTING.md`
  3. `SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
  4. `PROFILE_ROUTING.md`（仅在需要 profile 分流时）
  5. `contract-reference`
  6. `architecture-playbook`
  7. `staged-skill-reference`（仅 `staged_cli_first`）
  8. `create-skill-from-template`

## Doc-Structure Governance
- 强制方法论：`SkillsManager-Doc-Structure`
- 强制适用范围：
  - 创建新 skill
  - 治理既有 skill
  - 重排模板包
- 结构基线：
  - `facade -> routing -> topic atom`
  - `index doc` 可选，但只做导航
- `SkillsManager-Doc-Structure` 在这里从入口 handoff 之后开始组织文档树。
- `SKILL.md` 的结构元数据写在 `metadata.doc_structure`
- 必读治理文档：
  - `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
  - `references/governance/SKILL_AUTHORING_RULES.md`
  - `references/governance/SKILL_ARCHITECTURE_PLAYBOOK.md`

## Profile Support
- `basic`
  - 至少生成：facade、task routing、doc-structure policy、execution rules、tooling docs。
  - 若有运行态规则，再补 runtime contract。
- `staged_cli_first`
  - 在 basic 基线上，额外生成 runtime contract、stage index、stage system README、stage contract 四件套。

## Tool Contracts
- `Cli_Toolbox.runtime_contract`
  - 输出本技能运行合同。
- `Cli_Toolbox.contract_reference`
  - 输出作者合同。
- `Cli_Toolbox.architecture_playbook`
  - 输出架构手册。
- `Cli_Toolbox.staged_skill_reference`
  - 输出 staged profile 参考。
- `Cli_Toolbox.skill_template`
  - 输出已接入 doc-structure 治理的 basic 门面模板。
- `Cli_Toolbox.staged_skill_template`
  - 输出 staged 门面模板。
- `Cli_Toolbox.runtime_contract_template`
  - 输出 staged runtime contract 模板。
- `Cli_Toolbox.create_skill_from_template`
  - 生成或重构 skill 骨架。

## Governance Rules
- `SKILL.md` 必须保持极简 facade。
- 目标 skill 的门面 contract 由本运行合同与模板资产共同定义。
- `SkillsManager-Doc-Structure` 不是建议项，而是显式执行合同。
- 先形成清晰 tree，再用 anchors 补 graph。
- `技能本体 / 规则说明` 双段式约定可保留，但应下沉到 routing 或 topic 文档。
- 模板结构变化时，同步更新 facade、contracts、references、assets、生成器、tooling docs 与测试。

## Validation Closure
- 运行 `Cli_Toolbox` 自检与生成器回归。
- 对本 skill 运行 doc-structure lint 与 anchor graph build。
- 生成 basic / staged sandbox，并再次运行 doc-structure lint。
- 验证 staged 输出包含 stage checklist 与合同四件套。
