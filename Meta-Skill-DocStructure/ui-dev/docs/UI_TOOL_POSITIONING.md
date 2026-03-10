---
doc_id: "ui.tool.positioning"
doc_type: "ui_dev_guide"
topic: "Positioning of the embedded UI tool inside Meta-Skill-DocStructure"
anchors:
  - target: "../UI_DEV_ENTRY.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This positioning guide belongs to the UI tool root."
  - target: "UI_FILE_ORGANIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
---

# UI Tool Positioning

## 定位
- `ui-dev/` 是技能内部的一个工具，不是技能主体本身。
- 技能主体负责文档治理规则；UI 工具负责把真实文档和 graph 投影成可读视图。
- UI 工具不能重新定义文档治理规则，只能消费根技能暴露出的文档结构结果。

## 边界
- 根技能之外不应出现 UI payload、UI service contract、UI tests。
- UI 工具可以读取 skill root 中的 markdown、json、yaml，但不能把自己的实现细节散回根技能。
- 若要调整交互、布局、视觉层级，应先更新 `ui-dev/docs/`，再改代码。
