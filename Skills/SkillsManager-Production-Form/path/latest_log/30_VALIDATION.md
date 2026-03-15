---
doc_id: skillsmanager_production_form.path.latest_log.validation
doc_type: validation_doc
topic: Latest log validation
---

# 最近迭代校验

## 当前动作完成条件
- `latest-log --json` 读取 runtime root 下的 active log。
- active log 缺失时，默认迁移 seed snapshot。
- repo 内 seed snapshot 只作为迁移种子，不继续追加。
