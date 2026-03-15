---
doc_id: skill_creation_template.path.template_creation.entry
doc_type: path_doc
topic: Behavior entry for template creation
anchors:
- target: ../00_SKILL_ENTRY.md
  relation: implements
  direction: upstream
  reason: The main skill entry routes readers here for template creation.
- target: guide_only/00_GUIDE_ONLY_ENTRY.md
  relation: routes_to
  direction: downstream
  reason: guide_only template creation has its own action loop.
- target: guide_with_tool/00_GUIDE_WITH_TOOL_ENTRY.md
  relation: routes_to
  direction: downstream
  reason: guide_with_tool template creation has its own action loop.
- target: executable_workflow_skill/00_EXECUTABLE_WORKFLOW_ENTRY.md
  relation: routes_to
  direction: downstream
  reason: executable_workflow_skill template creation has its own action loop.
---

# Template Creation Entry

## 这个入口是干什么的
- 本入口只处理模板创建行为。
- 你在这里先决定当前要走哪条 `skill_mode` 线路，再进入该线路自己的动作闭环。
- 所有新生成的 skill root 都必须遵守：`SKILL.md / path / agents / scripts`。
- 每条 `skill_mode` 线路内部都必须显式包含自己的模板节点，方便查看该模式要生成的目标技能形态。
- 技能创建完成后的文档组织、锚点写法与门面约束，不在本入口继续展开；后续统一交给 `SkillsManager-Doc-Structure`。

## 下一跳列表
- [guide_only]：`guide_only/00_GUIDE_ONLY_ENTRY.md`
- [guide_with_tool]：`guide_with_tool/00_GUIDE_WITH_TOOL_ENTRY.md`
- [executable_workflow_skill]：`executable_workflow_skill/00_EXECUTABLE_WORKFLOW_ENTRY.md`
