---
doc_id: skillsmanager_tooling_checkup.path.output_governance.validation
doc_type: topic_atom
topic: Validation for output governance checking
---

# 输出落点检查校验

## 当前动作如何判定完成
- 只有当代码路径、默认回退、显式参数、文档声明与历史迁移责任五者闭合时，才能判定通过。

## 通过标准
- 没有遗漏任意一类输出语义。
- 没有把目标技能的输出治理误写成“本技能自身的运行日志”。
