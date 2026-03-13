---
doc_id: "ui.dev.rules.product_mother_doc_lint"
doc_type: "ui_dev_guide"
topic: "Workflow for linting product-owned frontend mother docs through Dev-VUE3-WebUI-Frontend"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workflow belongs to the frontend rules branch."
  - target: "../positioning/SCREEN_SPATIAL_BLUEPRINT_CONTRACT.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Blueprint completeness is one of the primary lint dimensions."
  - target: "UI_PRODUCT_SEMANTIC_SPLIT_GATE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Semantic split is part of the same product mother doc gate."
---

# UI Product Mother Doc Lint Workflow

## 目标
- 读取目标产品的 `Development_Docs/mother_doc`，而不是只检查 skill 自己的规则文本。
- 基于目标文档树的 `doc_links`、markdown links、frontmatter 和 identifier 集合，生成该项目专属的 frontend lint profile。
- 用脚本直接发现 layout、surface、component、panel blueprint 与 property contract 的缺口。

## 必用命令
- `npm run cli -- build-product-doc-graph --docs-root <development_docs_root> [--write-assets] --json`
- `npm run cli -- lint-product-mother-doc --docs-root <development_docs_root> [--write-assets] --json`

## 检查维度
- `layout completeness`
  - 提到布局、panel 编排、坐标、split、overlay 等语义时，必须存在 blueprint 落点。
- `surface completeness`
  - 提到背景、颜色、边框、阴影、radius、surface 时，必须挂到 visual token / surface matrix。
- `component completeness`
  - 提到组件、props、slot、toolbar、legend、action 等时，必须挂到 registry seed 或 component property matrix。
- `identifier coverage`
  - `panel.*`、`cmp.*`、`container.*`、`surface.*` 不能只被引用，不被定义。
- `panel coverage`
  - panel catalog 中的每个 panel 都必须有详细 blueprint 和 component property coverage。

## 产物
- `graph/frontend_mother_doc_graph.json`
- `graph/frontend_mother_doc_lint_profile.json`
- `graph/frontend_mother_doc_lint_report.json`

## 责任边界
- 该 lint 属于前端 skill 的专项门禁，不属于 `Workflow-OctopusOS-DevFlow` 的规则本体。
- `Workflow` 可以消费 lint 结果，但不应内置这些前端裁决标准。
