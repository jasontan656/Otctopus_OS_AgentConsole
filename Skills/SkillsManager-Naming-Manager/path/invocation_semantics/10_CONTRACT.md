---
doc_id: skillsmanager_naming_manager.path.invocation_semantics.contract
doc_type: topic_atom
topic: Invocation semantics contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Invocation semantics rules are expanded in the execution doc.
---

# 调用语义合同

## 当前动作要完成什么
- 把自然语言中的技能集合调用收敛成可重复解析的语义。
- 避免把 `display_name`、family、prefix 与技能族混成临时猜测。

## 当前动作必须满足什么
- 解析优先级固定：`canonical_id` > `prefix/family` > `family` > 有限上下文推断。
- 未注册技能不应自动算进任何 family / prefix 集合。
- “全技能”默认只包含 registry 中 `status=active` 的技能。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
