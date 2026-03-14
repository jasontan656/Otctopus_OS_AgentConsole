---
doc_id: skill_creation_template.governance.authoring_contract
doc_type: topic_atom
topic: Authoring contract for governed skills generated or refactored by this template
anchors:
- target: ../runtime/SKILL_RUNTIME_OVERVIEW.md
  relation: expands
  direction: upstream
  reason: The runtime contract declares this contract as a required governance source.
- target: SKILL_DOCSTRUCTURE_ENFORCEMENT.md
  relation: governed_by
  direction: upstream
  reason: Doc-structure governance is a mandatory part of this authoring contract for non-guide_only skills.
- target: ../routing/PROFILE_ROUTING.md
  relation: details
  direction: upstream
  reason: Skill-mode routing decides which branch this contract should be combined with.
---

# Skill Authoring Contract

## 合同目标
- 用受治理模板创建或重构 skill，不接受“先生成一个胖门面，再靠后补丁慢慢拆”的做法。
- 这里约束的是稳定的技能结构，不是一次性写作格式。
- `SKILL.md` 的入口门面 contract 由本技能负责；`SkillsManager-Doc-Structure` 从入口节点往下治理 `guide_with_tool` 与 `executable_workflow_skill` 的文档树。

## 顶层 skill_mode 契约
- 每个新 skill 都必须在 `SKILL.md` 顶层 frontmatter 声明：
  - `skill_mode: guide_only`
  - `skill_mode: guide_with_tool`
  - `skill_mode: executable_workflow_skill`
- 旧 `profile` 参数只允许作为生成器兼容输入，不允许继续写回目标 skill。

## 门面契约
- `guide_only`
  - `SKILL.md` 就是技能本体。
  - 不要求额外 routing doc、runtime contract 或专属 CLI。
- `guide_with_tool`
  - `SKILL.md` 必须是 `entry-only facade`。
  - 门面只能保留两段：
    - `Immediate Contract`
    - `Structured Entry`
- `executable_workflow_skill`
  - 在 `guide_with_tool` 的两段 façade 规则上，再补 runtime/stage 合同入口。
  - 阶段正文不得回填到门面。
- `Immediate Contract` 只保留：
  - 技能主轴与最小职责边界
  - 真实规则源优先级
  - 立即生效的硬约束
  - 影响后续分流的 mode/stage 轴线
  - 明确排除域
- `Structured Entry` 只保留：
  - 必读顺序
  - 第一层 routing/index/runtime/tooling 入口
  - 最小可执行入口命令
- 详细命令清单、结构索引、长篇适用域说明、解释性规则正文，都必须下沉到 routing、topic atom、index 或 tooling docs。

## 文档结构契约
- `guide_only`
  - 不受 `SkillsManager-Doc-Structure` 的 tree/anchor/split lint 约束。
- `guide_with_tool`
  - 必须具备 facade -> routing -> topic atom 的清晰主路径。
  - 所有下沉 markdown 文档都必须具备 frontmatter 与 anchors。
- `executable_workflow_skill`
  - 与 `guide_with_tool` 共用文档树基线，再叠加 runtime/stage 合同树。

## 工具与运行时契约
- `guide_only`
  - 不要求 `agents/openai.yaml`
  - 不要求 `references/runtime*`
  - `SkillsManager-Tooling-CheckUp` 对其不执行 CLI/runtime-contract shape 审计
- `guide_with_tool`
  - 可有专属 lint/audit/check 工具
  - 不要求 CLI-first dual-file runtime_contracts
- `executable_workflow_skill`
  - 必须具备 CLI-first runtime contracts
  - 必须具备 stage index 与 stage contract 四件套

## 验收门禁
- `skill_mode` 与实际文件树一致。
- `guide_only` 只有 `SKILL.md`。
- `guide_with_tool` 与 `executable_workflow_skill` 的 `SKILL.md` 只保留 `Immediate Contract` 与 `Structured Entry` 两段。
- `guide_with_tool` 与 `executable_workflow_skill` 已形成清晰 tree，anchors 已补齐 graph。
- `executable_workflow_skill` 的 runtime/stage 合同面完整。
