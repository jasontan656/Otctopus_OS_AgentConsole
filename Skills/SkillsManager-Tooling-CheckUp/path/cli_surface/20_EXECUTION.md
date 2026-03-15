---
doc_id: skillsmanager_tooling_checkup.path.cli_surface.execution
doc_type: topic_atom
topic: Execution for CLI surface checking
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: CLI surface execution ends in validation.
---

# CLI Surface 检查实施

## 当前动作怎么做
1. 确认目标技能是否真的打算对外暴露受管 CLI surface。
2. 检查命令命名、参数命名、JSON 模式与错误返回是否稳定。
3. 若目标技能带 `path/`，执行 `read-contract-context` 检查它是否按文档真源编译链路。
4. 记录入口缺失、参数含糊、JSON 不稳定、链路编译失效等缺口。

## 当前动作不能做什么
- 不能因为目标技能没有复用本技能命令名就判违规。
- 不能把内部 helper 脚本误判成必须暴露的公共 CLI。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
