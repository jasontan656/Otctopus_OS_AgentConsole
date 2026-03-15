---
doc_id: skillsmanager_production_form.path.append_iteration_log.validation
doc_type: validation_doc
topic: Append iteration log validation
---

# 追加迭代日志校验

## 当前动作完成条件
- 新日志写入 active runtime log。
- 日志结构符合模板。
- `append-iteration-log --json` 返回写入路径、runtime root 与 result root。
