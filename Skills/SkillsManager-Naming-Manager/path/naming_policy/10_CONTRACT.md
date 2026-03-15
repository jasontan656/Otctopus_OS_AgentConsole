---
doc_id: skillsmanager_naming_manager.path.naming_policy.contract
doc_type: topic_atom
topic: Naming policy contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Naming rules are expanded in the execution doc.
---

# 命名规范合同

## 当前动作要完成什么
- 为所有技能定义统一、可长期治理的命名结构。
- 避免目录名、frontmatter `name`、调用名与 family 归属彼此漂移。

## 当前动作必须满足什么
- 新增技能时，先定 `prefix / family / role_tag`，再落 `canonical_id` 与展示层名字。
- 不允许把局部展示习惯误当成全局命名规则。
- 目录名与 frontmatter `name` 不得长期分离。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
