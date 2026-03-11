---
doc_id: "skill_creation_template.governance.doc_structure_enforcement"
doc_type: "topic_atom"
topic: "Mandatory adoption contract for skill-doc-structure inside skill creation and governance"
anchors:
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "expands"
    direction: "upstream"
    reason: "The runtime contract names doc-structure governance as mandatory."
  - target: "../routing/TASK_ROUTING.md"
    relation: "details"
    direction: "upstream"
    reason: "Task routing sends create/govern flows here."
  - target: "SKILL_AUTHORING_CONTRACT.md"
    relation: "implements"
    direction: "downstream"
    reason: "The authoring contract incorporates this mandatory doc-structure rule."
---

# Skill-Doc-Structure Enforcement

## 强制声明
- `skill-doc-structure` 是本技能的显式治理组成部分。
- 任何“创建新 skill”或“治理既有 skill”的动作，都必须把 `skill-doc-structure` 当作必读、必用、必验证的方法论，而不是口头默认。
- 若 skill 当前结构与 `skill-doc-structure` 冲突，优先重建清晰的 facade、routing、topic atom 与 anchor graph，不为旧混装写法保留模糊兼容层。

## 创建新 skill 时必须做到
- 先产出极简 facade，而不是大而全 `SKILL.md`。
- 至少补齐一层 routing doc，让模型知道下一步该进入哪个语义分支。
- 将深规则拆到单 topic 原子文档，并补齐 `doc_structure` frontmatter 与 anchors。
- 若 skill 有运行态规则，再补 CLI-first runtime contract。

## 治理既有 skill 时必须做到
- 先识别当前门面是否混装多个轴线。
- 先拆 tree，再补 graph；不要只在原文上堆补丁。
- 逐项核对 references、assets、scripts、tests 是否与新结构一致。
- 只要模板结构变了，就要同步更新生成器与回归，而不是停在文档说明层。

## 双段式约定的归位
- 既有 `技能本体 / 规则说明` 双段式约定不丢弃。
- 但它不再成为顶层 facade 膨胀的理由。
- 推荐归位方式：
  - facade：极简路由，不扩正文。
  - routing doc：必要时轻量说明当前分叉轴线。
  - topic atom：保留双段式，承载真正的章节规则与写法边界。

## 验证要求
- 对目标 skill 运行 `skill-doc-structure` 的 anchors lint、split lint 与 anchor graph build。
- 若 lint 指向结构冲突，先修结构，再进入其他治理动作。
