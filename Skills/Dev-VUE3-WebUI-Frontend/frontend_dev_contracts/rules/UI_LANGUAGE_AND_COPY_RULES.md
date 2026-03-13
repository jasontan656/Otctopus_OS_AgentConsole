---
doc_id: "ui.dev.rules.language"
doc_type: "tooling_usage"
topic: "Language rules for the showroom UI"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This language rule belongs to the frontend rules branch."
  - target: "../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The product-runtime handoff stage must follow the language and copy boundary."
  - target: "../positioning/UI_TOOL_POSITIONING.md"
    relation: "supports"
    direction: "downstream"
    reason: "The positioning contract must reflect the same language boundary."
---

# UI Language Rules

## Visible UI Surface
- All visible page copy must be written in English.
- No Chinese is allowed in navigation labels, panel titles, buttons, empty states, helper text, or runtime status text.

## Source Code Surface
- Source code must use English naming.
- Code comments must use English only.
- Temporary bilingual comments or mixed-language placeholders are forbidden.

## Documentation Boundary
- Generic frontend contracts may remain Chinese-first because they are internal governance docs.
- Product-owned development docs may explain implementation intent in Chinese, but any quoted future UI copy must be written in English.

## Enforcement Intent
- This rule is active immediately even while the skill stores only contracts.
- When product UI code is implemented, this rule becomes a blocking implementation contract.
