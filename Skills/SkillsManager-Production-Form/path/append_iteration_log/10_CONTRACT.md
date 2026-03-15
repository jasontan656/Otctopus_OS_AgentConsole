---
doc_id: skillsmanager_production_form.path.append_iteration_log.contract
doc_type: contract_doc
topic: Append iteration log contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the contract, read the append commands and template.
---

# 追加迭代日志合同

## 当前动作的目标
- 让新的 console 产品化判断以固定结构写入 active runtime log。

## 当前动作必须满足的约束
- 只有真正的产品边界、命名、工作流或错误方向收敛，才应追加日志。
- 日志不得退回 skill 目录。
- 日志格式必须稳定，可供后续 `latest-log` 读取。

## 下一跳列表
- [tools]：`15_TOOLS.md`
