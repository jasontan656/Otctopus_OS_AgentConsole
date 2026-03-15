---
doc_id: skillsmanager_naming_manager.path.registry_governance.contract
doc_type: topic_atom
topic: Registry governance contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Registry rules are expanded in the execution doc.
---

# 注册治理合同

## 当前动作要完成什么
- 为所有技能提供统一注册模型。
- 让“这个技能属于哪个 prefix / family、能否被某句自然语言一次性调度”有稳定依据。

## 当前动作必须满足什么
- registry 默认按 `canonical_id` 执行 upsert。
- 命中已登记技能时，更新已有记录，不重复新增第二条。
- registry 只回答当前名字、主 prefix、主 family、角色与触发摘要，不混入历史迁移噪音。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
