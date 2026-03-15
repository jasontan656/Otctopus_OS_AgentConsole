---
doc_id: skillsmanager_tooling_checkup.path.remediation.contract
doc_type: topic_atom
topic: Contract for tooling remediation
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: remediation contract is followed by the applicable tools.
---

# 整改合同

## 当前动作要完成什么
- 在行为保持的前提下修正目标技能的 tooling 问题。
- 问题来源可能是：依赖基线重叠、输出治理缺口、CLI 契约失效、tooling 边界越权。

## 当前动作必须满足什么
- 只有当证据已经证明问题成立时，才能进入整改。
- 优先删除或缩小冗余自实现，避免叠加兼容层。
- 若问题只是 Python / TypeScript 语言规范，本线路不处理，应交回对应 constitution。
- 若涉及输出治理，整改必须同时覆盖代码路径、默认回退、文档声明与历史迁移责任。

## 下一跳列表
- [tools]：`15_TOOLS.md`
