---
doc_id: skillsmanager_production_form.path.append_iteration_log.protocol
doc_type: execution_doc
topic: Append iteration log protocol
reading_chain:
- key: template
  target: 25_LOG_ENTRY_TEMPLATE.md
  hop: next
  reason: Read the log entry template before validation.
---

# 追加日志协议

## 执行顺序
1. 锁定 title 与 summary。
2. 按需填充 decisions、affected_paths、risks、next_steps。
3. 若 active runtime log 不存在，则先从 seed snapshot 初始化。
4. 以固定 markdown section 追加到 active runtime log。

## 下一跳列表
- [template]：`25_LOG_ENTRY_TEMPLATE.md`
