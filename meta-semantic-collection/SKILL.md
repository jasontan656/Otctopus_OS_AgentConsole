---
name: "meta-semantic-collection"
description: "用户歧义语义集合技能。用于当用户希望模型先读取一组稳定的常用词映射、AI 易偏差理解和语义翻译规则，再把 prompt 翻译成更贴近用户真实意图的执行语义时使用。"
---

# meta-semantic-collection

## 1. 目标
- 本技能用途为用户歧义语义集合，整合了用户常用词和 AI 理解偏差集合进行了翻译和映射。
- 先用本技能对照当前 prompt 的表达，再继续执行后续任务。

## 2. 集合（json payload structure）
```json
{
  "term": "清理掉",
  "normalized_intent": "删掉 + 不留痕",
  "must_include": [
    "删除目标对象",
    "删除直接残留"
  ],
  "must_exclude": [
    "备份后删除",
    "注释掉替代删除",
    "保留兼容层",
    "保留占位空壳"
  ],
  "notes": "用户语义优先于模型默认保守解释"
}
```

- 集合中的每个条目至少包含：
  - `term`
  - `normalized_intent`
  - `must_include`
  - `must_exclude`
  - `notes`
- 若当前 prompt 命中集合条目，优先使用集合定义覆盖模型默认理解。

## 3. 维护规则
- 所有语义集合内容只写在 `SKILL.md`，不向后延伸文档。
- 新增语义条目时，优先补充“模型最容易误译”的高频词。
- 每个条目都必须同时写清楚“应该翻译成什么”和“绝对不要翻译成什么”。
- 若本轮 prompt 给出了更具体的语义定义，以本轮定义覆盖集合内旧定义。
