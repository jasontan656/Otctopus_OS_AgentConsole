---
name: ${skill_name}
description: ${description}
skill_mode: guide_with_tool
doc_id: skill_creation_template.asset.guide_with_tool_skill_template
doc_type: template_doc
topic: Guide-with-tool skill facade template asset
anchors:
- target: references/routing/TASK_ROUTING_TEMPLATE.md
  relation: implements
  direction: downstream
  reason: This asset routes to the task routing template in the current template pack.
- target: references/governance/SKILL_DOCSTRUCTURE_POLICY_TEMPLATE.md
  relation: governed_by
  direction: downstream
  reason: The template pack governs guide_with_tool facades through the doc-structure policy template.
metadata:
  doc_structure:
    doc_id: ${skill_name}.entry.facade
    doc_type: skill_facade
    topic: Entry facade for ${skill_name}
    anchors:
    - target: references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The facade must route readers into the first task branch.
    - target: references/governance/SKILL_DOCSTRUCTURE_POLICY.md
      relation: governed_by
      direction: downstream
      reason: Doc-structure policy is a mandatory governance branch.
---

# ${skill_name}

## 1. Immediate Contract
- [本文件只做门面入口，且只保留 `Immediate Contract` 与 `Structured Entry` 两段。]
- [本技能采用 `guide_with_tool` 形态：核心仍是方法论，但允许专属 lint/audit/check 工具作为辅助面。]
- [写清本技能的唯一主轴与最小职责边界。]
- [写清真实规则源优先级：CLI JSON / machine-readable contract / markdown audit copy。]
- [写清立即生效的硬约束，例如禁止把正文留在门面。]
- [写清不适用域；若依赖 companion skill，只写职责边界。]
- [凡是不是“模型必须立刻知道”的内容，都必须下沉到 routing、topic atom、index 或 tooling docs。]

## 2. Structured Entry
1. [若有 runtime contract，先读取 runtime contract。]
2. 读取 `references/routing/TASK_ROUTING.md`。
3. 读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
4. [若任务还会继续按 mode / stage / language 等轴线分流，继续读取对应 routing 或 index doc。]
5. 再进入当前任务真正需要的 execution rules、tooling docs 或其他原子文档。
- 入口：
  - `references/routing/TASK_ROUTING.md`
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - [若存在 runtime contract、stage index 或其他第一层入口，写在这里]
  - [完整结构索引应放在 `references/indexes/DOC_TREE.md`，不要回填到门面]
