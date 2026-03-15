---
doc_id: skillsmanager_tooling_checkup.path.output_governance.execution
doc_type: topic_atom
topic: Execution for output governance checking
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: output governance execution ends in validation.
---

# 输出落点检查实施

## 当前动作怎么做
1. 锁定目标技能的写入入口、默认输出逻辑与显式落点参数。
2. 区分 runtime 日志、审计痕迹、默认结果与定向产物的语义。
3. 确认每类输出都有明确落点，而不是散落到工作目录、skill 目录或 home 临时路径。
4. 检查目标技能文档是否把这些落点显式说清。
5. 若存在旧路径，补出迁移策略或处置声明。

## 当前动作不能做什么
- 不能把临时 debug 输出放任留在任意工作目录。
- 不能只改新路径而不处理历史产物处置责任。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
