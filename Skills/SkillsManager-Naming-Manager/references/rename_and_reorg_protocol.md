---
doc_id: skillsmanager_naming_manager.references_rename_and_reorg_protocol
doc_type: topic_atom
topic: 重命名与重组协议
anchors:
- target: ../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# 重命名与重组协议

## 目标
- 当你未来想整体修改技能命名规范、prefix 体系或组织架构时，提供统一的治理顺序，避免只改名字不改消费语义。

## 变更类型
- 单技能重命名
- 整个 prefix 改名
- family 拆分或合并
- family code 建立、废弃或改名
- 展示名体系重写
- canonical_id 规则升级

## 固定顺序
1. 先定义新的命名规则。
2. 再定义新的 registry 结构。
3. 再明确自然语言调用语义如何迁移。
4. 最后才批量改技能目录与 frontmatter。

## 必查清单
- 哪些技能的 `canonical_id` 需要改
- 哪些技能只是 `display_name` 需要改
- 哪些 prefix/family 会受影响
- 哪些自然语言短语会因此产生歧义

## 风险提醒
- 只改目录名，不改 registry 语义，会导致安装名与调度语义脱节。
- 只改显示名，不改 family/prefix，会导致自然语言调用继续沿用旧结构。
- 在没有统一注册前谈“全技能集合”，容易把不该纳入的技能也拉进来。

## 完成标准
- 新规则能解释“新技能该如何命名与注册”。
- 旧技能能被映射到新结构，不会同时落在多套主规则下。
- 自然语言里关于 prefix/family 的说法有明确稳定的解析方式。
- 若建立了新 family code，例如 `[SKILL-GOV]`，registry 中至少要有一个明确成员。
