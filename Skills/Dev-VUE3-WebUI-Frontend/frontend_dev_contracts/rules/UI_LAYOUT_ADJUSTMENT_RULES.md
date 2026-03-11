---
doc_id: "ui.viewer.layout_adjustment"
doc_type: "ui_dev_guide"
topic: "Layout adjustment rules for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This guide belongs to the frontend rule branch."
  - target: "../containers/layout/10_APP_SHELL_AND_WORKSPACE_LAYOUT_AUTHORITY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Responsive rules refine the layout authority assigned to shell and workspace containers."
  - target: "../showroom_runtime/VIEWER_STACK_AND_REUSE.md"
    relation: "extends"
    direction: "upstream"
    reason: "Layout adjustments must extend the viewer stack contract."
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The rule branch is part of the frontend development contract set."
---

# UI Layout Adjustment Rules

## 目标
- 优先调整信息层级，再调整视觉装饰。
- 保持 `SKILL.md` 仍是默认进入正文。
- graph、文档列表、正文面板三者必须同时可见或可快速切换。
- 窄屏退化应由 workspace 容器统一裁决，不得让单个 panel 各自漂移。
