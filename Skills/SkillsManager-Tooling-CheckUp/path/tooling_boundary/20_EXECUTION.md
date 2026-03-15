---
doc_id: skillsmanager_tooling_checkup.path.tooling_boundary.execution
doc_type: topic_atom
topic: Execution for tooling boundary checking
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: tooling boundary execution ends in validation.
---

# Tooling 职责边界检查实施

## 当前动作怎么做
1. 把目标 tooling 文件映射到它的实际角色。
2. 检查它是否已经吸收了目标技能自己的域内规则、流程路由或迁移语义。
3. 若越权成立，只标出最小需要缩小或拆分的范围。
4. 保持外部行为不变，不因整理而把域内语义抽空。

## 当前动作不能做什么
- 不能借“统一整理”之名，把目标技能域内合同强塞进 tooling 模块。
- 不能把语言风格问题混入职责边界结论。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
