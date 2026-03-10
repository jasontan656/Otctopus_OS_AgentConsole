---
name: "meta-semantic-collection"
description: "用户歧义语义集合技能。用于当用户希望模型先读取一组稳定的常用词映射、AI 易偏差理解和语义翻译规则，再把 prompt 翻译成更贴近用户真实意图的执行语义时使用。"
---

# meta-semantic-collection

## 1. 目标
- 本技能用途为用户歧义语义集合，整合了用户常用词和 AI 理解偏差集合进行了翻译和映射。
- 先用本技能对照当前 prompt 的表达，再继续执行后续任务。
- 当用户在多轮交互中补充澄清语义、纠正 AI 误解、停止当前动作并重新解释真实意图时，优先触发本技能。

## 2. 集合（json payload structure）
```json
{
  "collection": [
    "清理掉",
    "删掉",
    "去掉"
  ],
  "action_semantic_description": "删除目标对象及其直接残留，不做备份，不做注释保留，不保留兼容层或占位空壳。"
}
```

- 集合中的每个条目至少包含：
  - `collection`
  - `action_semantic_description`
- `collection` 是用户原词集合，用于持续扩写同一语义下的不同说法。
- `action_semantic_description` 是该集合统一指向的动作语义描述，默认保持稳定，不轻易拆分。
- 多个词可以指向 1 个 `action_semantic_description`。
- 1 个词不能同时指向多个 `action_semantic_description`。
- 若当前 prompt 命中已有集合中的任一用户原词，优先使用该集合对应的动作语义描述覆盖模型默认理解。

## 3. 维护规则
- 所有语义集合内容只写在 `SKILL.md`，不向后延伸文档。
- 当用户澄清“不是这个意思”“我的意思是……”“这里应该理解成……”这类内容时，提取：
  - 用户原词
  - 争议内容
  - 最终澄清后的动作语义
- 若澄清后的动作语义已存在，则把新的用户原词并入已有 `collection`。
- 若澄清后的动作语义不存在，则新建一个新的集合条目。
- 同一语义的不同描述方式，应收入同一个 `collection` 并指向同一个 `action_semantic_description`。
- 若一个用户原词与已有集合发生语义冲突，必须先更新映射归属，再删除旧归属，不能让一个词同时挂到多个描述下。
- 新增或更新时，优先处理“模型最容易误译”的高频词和高频澄清场景。
