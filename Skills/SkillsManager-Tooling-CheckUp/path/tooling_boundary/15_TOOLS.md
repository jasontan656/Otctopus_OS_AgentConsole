---
doc_id: skillsmanager_tooling_checkup.path.tooling_boundary.tools
doc_type: topic_atom
topic: Tools for tooling boundary checking
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: tooling boundary tools are applied in the execution step.
---

# Tooling 职责边界检查工具

## 当前动作会用到什么
- 目标技能的 CLI 入口、parser、schema、helper、lint、test、glue 文件
- 目标技能对应的文档链与域内合同

## 当前动作必须满足什么
- 只有当文件职责真的越过边界时，才进入整理或整改。
- 不能把跨文件复用本身当成问题；只在它变成隐藏规则 owner 时才定性。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
