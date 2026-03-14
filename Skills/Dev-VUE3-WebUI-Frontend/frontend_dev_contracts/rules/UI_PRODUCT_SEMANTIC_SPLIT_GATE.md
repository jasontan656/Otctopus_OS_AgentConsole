---
doc_id: "ui.dev.rules.product_semantic_split_gate"
doc_type: "ui_dev_guide"
topic: "Semantic split gate for frontend-heavy product mother docs"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This split gate belongs to the frontend rules branch."
  - target: "UI_PRODUCT_MOTHER_DOC_LINT_WORKFLOW.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The split gate is enforced through the product mother doc lint workflow."
---

# UI Product Semantic Split Gate

## 来源思路
- 继承 `SkillsManager-Doc-Structure` 的 `tree first, graph second` 方法，但这里的执行主体是前端 skill。
- 判断标准不是“文档长不长”，而是“一个前端合同文档是否混入了多个独立裁决轴线”。

## 阻断语义
- 当一个文档同时混入过多的：
  - layout / blueprint
  - surface / token
  - component / props
  - service boundary / runtime handoff
  - projection / viewer dependency
- 且正文已经存在多个并列 `##` 语义块时，应视为高概率应拆未拆。

## 处理原则
- 优先把合同拆成更深一层目录或新的原子文档。
- 新文档必须继续挂回原有合同主轴，不允许另起一棵脱节的树。
- 若暂不拆分，必须有明确理由；默认不接受“先放在一起以后再说”。

## 与产品 mother doc 的关系
- 这是前端专项语义拆分门禁，目标是降低 AI 阅读成本和实现漂移。
- 它不替代 `Workflow-CentralFlow1-OctopusOS` 的阶段治理，也不替代 `SkillsManager-Doc-Structure` 的方法论本体。
