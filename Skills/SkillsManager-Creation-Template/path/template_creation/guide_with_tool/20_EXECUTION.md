---
doc_id: skill_creation_template.path.template_creation.guide_with_tool.execution
doc_type: topic_atom
topic: Execution for guide_with_tool template creation
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validation closes the action loop.
---

# Guide With Tool Execution

## 当前动作怎么做
1. 明确目标 skill 的真实业务主轴。
2. 先对照 `12_TEMPLATE.md` 确认目标技能模板结构。
3. 先渲染一个默认主入口，再按需要扩展其他平行入口。
4. 让每个入口都保持 `contract -> tools -> execution -> validation` 单线闭环。
5. 让命令脚本本体进入 `scripts/`，把命令说明写在各入口自己的 `tools` 节点里。
6. 保持工具面为辅助面，而不是额外控制层。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
