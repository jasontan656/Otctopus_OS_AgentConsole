---
doc_id: skillsmanager_tooling_checkup.path.tooling_boundary.contract
doc_type: topic_atom
topic: Contract for tooling boundary checking
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: tooling boundary contract is followed by the applicable tools.
---

# Tooling 职责边界检查合同

## 当前动作要完成什么
- 检查目标技能中的 tooling 文件是否仍只承担自己的角色。
- 明确哪些职责属于 tooling，哪些必须留在目标技能的域内工作流或合同里。

## 当前动作必须满足什么
- parser 可以解析和标准化外部表示，但不能变成域内策略引擎。
- schema / validation 可以约束已声明结构，但不能吸收工作流路由、迁移策略或业务语义。
- helper / lint / test / glue 应保持窄职责，不能偷偷变成隐藏的规则 owner。
- 语言专属代码规范不在本线路裁决。

## 下一跳列表
- [tools]：`15_TOOLS.md`
