---
doc_id: "ui.viewer.stack"
doc_type: "tooling_architecture"
topic: "Viewer stack, layout rules, and reuse contract for skill-local graph pages"
anchors:
  - target: "../UI_DEV_ENTRY.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc implements the dedicated UI dev entry."
  - target: "rules/UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Layout adjustment rules complement the stack design."
---

# Viewer Stack Reuse Contract

## 技术栈
- `TypeScript`
- `Vue3`
- `Vue Flow`
- `Vite`
- `express + ws + chokidar`

## 页面规则
- 默认选中 `SKILL.md`。
- 左侧是文档索引，中间是 graph，右侧是正文与 anchor 关系。
- 页面只显示真实 payload，不做静态复制。
- 所有 UI 结构调整都应先落到 `ui-dev/docs/`，再反映到组件代码。

## 复用规则
- 后续别的技能若采用同一 frontmatter 合同与 graph 结构，可直接复用这套 viewer。
- viewer target 通过 `TARGET_SKILL_ROOT` 切换。
- 只要目标技能也实现相同 contract，页面不需要重写，只需要换 target。
