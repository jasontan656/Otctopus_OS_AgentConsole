---
doc_id: "ui.dev.code_architecture.registry_guide"
doc_type: "ui_dev_guide"
topic: "Component registry guide for product frontend packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_PACKAGE_TEMPLATE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Registry rules belong to the package template branch."
  - target: "../../rules/UI_PACKAGE_SHAPE_LINT_WORKFLOW.md"
    relation: "enforced_by"
    direction: "downstream"
    reason: "Package registry rules are enforced by the package-shape lint workflow."
---

# Component Registry Guide

## registry 规则
- `ui-identity-registry.ts` 必须记录每个 component 的：
  - component id
  - layer id
  - container id
  - locator 短码
  - 主文件路径
  - package 目录路径
- 每个独立组件在真正开始实现前，就应先取得稳定 `component id` 并进入 registry；不允许先实现、后补登记。
- lint 必须校验 registry 和文件系统是否一致。
