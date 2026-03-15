---
doc_id: skillsmanager_tooling_checkup.path.tooling_boundary.validation
doc_type: topic_atom
topic: Validation for tooling boundary checking
---

# Tooling 职责边界检查校验

## 当前动作如何判定完成
- 每个被标记的文件都必须说明：
  - 它当前实际承担了什么角色
  - 它哪里越过了 tooling 边界
  - 这些越权内容应该回到哪里

## 通过标准
- 没有把域内规则误导成 tooling 规则。
- 没有把语言专属 code-style 问题越权纳入本线路。
