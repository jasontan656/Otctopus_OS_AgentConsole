---
doc_id: skill_creation_template.governance.doc_structure_enforcement
doc_type: topic_atom
topic: Mandatory adoption contract for SkillsManager-Doc-Structure inside skill creation and governance
anchors:
- target: ../runtime/SKILL_RUNTIME_OVERVIEW.md
  relation: expands
  direction: upstream
  reason: The runtime contract names doc-structure governance as mandatory.
- target: ../routing/TASK_ROUTING.md
  relation: details
  direction: upstream
  reason: Task routing sends create/govern flows here.
- target: SKILL_AUTHORING_RULES.md
  relation: implements
  direction: downstream
  reason: The authoring contract incorporates this mandatory doc-structure rule.
---

# SkillsManager-Doc-Structure Enforcement

## 强制声明
- `SkillsManager-Doc-Structure` 是本技能的显式治理组成部分。
- 任何“创建新 skill”或“治理既有 skill”的动作，都必须把 `SkillsManager-Doc-Structure` 当作必读、必用、必验证的方法论，而不是口头默认。
- 它治理的是目标 skill 入口节点之后的文档树、metadata、anchors 与 graph 组织。

## 创建新 skill 时必须做到
- 以模板给出的 `SKILL.md` 入口合同作为文档树 tree root。
- 从入口节点向下补齐 routing docs、index docs、topic atoms 与 anchor graph。
- 将深规则拆到单 topic 原子文档，并补齐 frontmatter 与 anchors。
- 若 skill 有运行态规则，再补 CLI-first runtime contract。

## 治理既有 skill 时必须做到
- 先识别当前入口节点之后的文档树是否缺少必要分层。
- 先拆 tree，再补 graph；不要只在原文上堆补丁。
- 逐项核对 references、assets、scripts、tests 是否与新结构一致。
- 只要模板结构变了，就要同步更新生成器与回归，而不是停在文档说明层。

## 验证要求
- 对目标 skill 运行 `SkillsManager-Doc-Structure` 的 anchors lint、split lint 与 anchor graph build。
- 若 lint 指向结构冲突，先修结构，再进入其他治理动作。
