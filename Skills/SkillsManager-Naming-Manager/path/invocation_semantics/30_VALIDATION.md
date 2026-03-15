---
doc_id: skillsmanager_naming_manager.path.invocation_semantics.validation
doc_type: topic_atom
topic: Invocation semantics validation
---

# 调用语义校验

## 当前动作如何判定完成
- 模型能判断一句自然语言是在请求单技能、family 技能集还是 prefix 全族。
- `deprecated` 与 `draft` 不再被默认误拉进“全技能”。
- family code 的含义可以直接落回 registry，而不是靠记忆临时猜。
