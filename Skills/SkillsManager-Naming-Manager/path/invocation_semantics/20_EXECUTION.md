---
doc_id: skillsmanager_naming_manager.path.invocation_semantics.execution
doc_type: topic_atom
topic: Invocation semantics execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validation closes the invocation semantics chain.
---

# 调用语义实施

## 核心句式
- `使用 <canonical_id> 完成本次任务`
  - 解析为单技能调用。
- `使用 <family> 系列技能`
  - 解析为单 family 范围内的技能集合。
- `使用 <family_code> 技能族`
  - 解析为显式 family code 对应的技能集合。
- `使用 <prefix> 系列全技能`
  - 解析为某 prefix 下所有 `active` 技能。
- `使用 <prefix>/<family> 系列技能`
  - 解析为某 prefix 下某 family 的活动技能。

## 特定 family code
- `[SKILL-GOV]`
  - 代表专门治理技能命名、注册、模板、镜像同步与同类治理动作的技能族。
- `[Skill_prod]`
  - 代表围绕 console 产品化与 `Skills/` 目录产品形态维护的技能族。

## 歧义处理
- 若自然语言短语同时可能指向 `display_name` 和 `family`，优先按 registry 显式字段解析。
- 若上下文无法判定，先回到注册语义，不要凭主观相似度硬拼集合。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
