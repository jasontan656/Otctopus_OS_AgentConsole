---
doc_id: skill_creation_template.governance.architecture_playbook
doc_type: topic_atom
topic: Architecture playbook for template-pack governance and skill reconstruction
anchors:
- target: ../runtime/SKILL_RUNTIME_OVERVIEW.md
  relation: expands
  direction: upstream
  reason: The runtime contract points here for architecture methodology.
- target: SKILL_AUTHORING_RULES.md
  relation: pairs_with
  direction: lateral
  reason: The playbook operationalizes the authoring contract.
- target: SKILL_DOCSTRUCTURE_ENFORCEMENT.md
  relation: governed_by
  direction: upstream
  reason: The playbook treats doc-structure governance as a mandatory architectural decision for non-guide_only skills.
---

# Skill Architecture Playbook

## 设计目标
- 让新 skill 从第一版起就匹配明确的 `skill_mode`，而不是靠后续补丁猜类型。
- 让 `guide_with_tool` 与 `executable_workflow_skill` 共享同一套文档结构治理，再按执行深度拉开合同面。
- 让 `guide_only` 保持真正极简，不把“只多一个 references”当成可接受的架构漂移。

## 三类架构基线
- `guide_only`
  - 单文件方法论
  - 所有语义留在 `SKILL.md`
  - 不引入 shadow tree
- `guide_with_tool`
  - 顶层 `SKILL.md` 只做 entry facade
  - 第二层至少存在一个单轴 routing doc
  - 深规则落到单 topic 文档
  - 工具面可存在，但只是辅助
- `executable_workflow_skill`
  - 在 `guide_with_tool` 基线上增加 runtime contract、resident docs、stage index 与 stage contract 四件套
  - 阶段切换需要显式 discard policy

## 为什么不能继续用 profile 思维
- 这次变化不是“模板深浅”，而是“治理责任模型”变化。
- `guide_only` 不是旧 `basic` 的弱化版，而是显式豁免文档树和 CLI shape 治理的独立形态。
- 因此主合同必须升到 `skill_mode`，而不是继续在 `profile` 上堆例外。

## 模板包治理顺序
1. 先改 runtime contract，明确三类 `skill_mode` 合同。
2. 再改 routing/governance docs，保证门面、routing、原子文档、豁免边界清楚。
3. 再改模板资产，让生成骨架与合同一致。
4. 再改生成器与 `Cli_Toolbox`，保证输出和读取入口同步。
5. 最后补测试与验证脚本。

## 反模式
- 用 `guide_only` 生成单文件后，再偷偷补 references/doc tree。
- 让 `guide_with_tool` 被错误推成 CLI-first dual-file runtime_contracts。
- 继续把 `basic/staged_cli_first` 当成新技能的主命名。
- 只改文档不改生成器、只改生成器不改治理器。
