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
  reason: The playbook treats doc-structure governance as a mandatory architectural decision.
---

# Skill Architecture Playbook

## 设计目标
- 让新 skill 从第一版起就具备 `facade -> routing -> topic atom` 的稳定主路径。
- 让 `basic` 与 `staged_cli_first` 共享同一套文档结构治理，再按 profile 拉开合同深度。
- 让模板包、生成器、tooling docs、回归测试和 anchors 始终围绕同一套结构演进。
- 让门面 contract 与入口之后的文档树 contract 分别落在正确的治理技能里。

## 基线架构
- 顶层 `SKILL.md` 只做 entry facade。
- 第二层至少存在一个单轴 routing doc，负责把读者继续送入更窄域的治理文档。
- 深层规则落到单 topic 文档，避免一个文档同时承担 profile 选择、工具说明和工作流细节。
- 索引文档只负责目录树与导航，不承担主规则正文。
- 顶层门面 contract 由模板技能定义，入口之后的树形分层由 `SkillsManager-Doc-Structure` 落地。

## 为什么必须接入 SkillsManager-Doc-Structure
- 模板技能如果不显式接入 `SkillsManager-Doc-Structure`，生成器很容易继续输出“巨型门面 + 补丁式拆分”。
- 对既有 skill 的治理也不能只修 `SKILL.md`；必须同时考虑 routing docs、atomic docs、anchors 与 graph。
- 因此，文档结构治理不是附属建议，而是模板包本身的架构硬约束。

## Profile 选择原则
- `basic`
  - 目标是单主轴 control plane。
  - 需要 facade、至少一层 routing，以及最小治理原子文档。
  - 若没有运行态规则，不强制 runtime contract。
- `staged_cli_first`
  - 目标是多阶段 control plane。
  - 需要在 basic 的 facade/routing/governance 基线上，再增加 runtime contract、stage index、resident docs 和 stage contract 四件套。
  - 阶段切换时显式丢弃上一阶段 focus。

## 模板包治理顺序
1. 先改 runtime contract，明确新的结构合同。
2. 再改治理文档树，保证 facade、routing、atomic docs 的分工清楚。
3. 再改模板资产，让生成骨架与治理树一致。
4. 再改生成器和 `Cli_Toolbox`，保证输出与读取入口同步。
5. 最后补 tooling docs、anchors、graph 与回归测试。

## 反模式
- 保留一个继续混装 facade、规则正文、模板资产说明的 `SKILL.md`。
- 只改模板 markdown，不同步生成器、tooling docs 和测试。
- 为兼容旧写法继续保留模糊中间层，而不是直接建立清晰的新路由树。
- 把 `技能本体 / 规则说明` 双段式当作继续膨胀门面的理由。
