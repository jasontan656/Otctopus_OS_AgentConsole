---
doc_id: workflow_realstate_posting_web.subskills_workflow_realstate_posting_web_headed_references_house_sale_headed_workflow
doc_type: topic_atom
topic: HouseSale Headed Publish Workflow (Fixed)
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# HouseSale Headed Publish Workflow (Fixed)

## Scope
- Applies only in `有头模式` for house-listing tasks.
- Runtime: `win_chrome_devtools` with Windows Edge.
- Browser bridge mode is independent from publish business flow; publish steps do not depend on fixed `127.0.0.1` endpoint.

## Canonical Asset Root
- `/home/jasontan656/AI_Projects/Human_Work_Zone/HouseSale`

## Inputs
- Listing payload:
  - `listings/active/<property_id>.yaml`
- Images:
  - `assets/properties/<property_id>/images/*.jpg`

## Platform Order
1. OnePropertee
2. Facebook Marketplace (when required)

## OnePropertee Contract
- Start URL: `https://onepropertee.com/dashboard/listings/create`
- Success marker:
  - `Your property has been posted`
  - listing page shows owner controls including `More Actions`.
- If listing already exists and is inactive, `Reactivate` is an allowed live-publish path.

## Facebook Marketplace Contract
- Start URL: `https://www.facebook.com/marketplace/create/rental`
- Success marker:
  - listing appears under `https://www.facebook.com/marketplace/you/selling`
- Rollback marker:
  - deleted listing URL resolves to unavailable page.

## Evidence Writeback
- Append/update:
  - `execution_logs/2026-02-18-template-driven-validation.md` (or current run log)
  - `platforms/onepropertee/workflow.yaml`
  - `platforms/facebook_marketplace/workflow.yaml`

## Read-Only Compatibility Check (2026-02-18)
- HouseSale workflow files are still structurally compatible with current headed runtime:
  - `platforms/onepropertee/workflow.yaml`
  - `platforms/facebook_marketplace/workflow.yaml`
- No direct dependency on old bridge endpoint (`127.0.0.1:9333`) was found in workflow definitions.
- Optional cleanup item (non-blocking):
  - `platforms/onepropertee/workflow.yaml` currently contains an old `required_asset` example path (`C:\\Windows\\Temp\\...`), while canonical asset root is `HouseSale/assets/properties/<property_id>/images`.
  - Recommend aligning this field text in a dedicated workflow content update turn.
