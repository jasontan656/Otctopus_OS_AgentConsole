---
doc_id: workflow_centralflow2_octppusos.path.development_loop.workflow_index
doc_type: workflow_index_doc
topic: Development loop workflow index
reading_chain:
- key: mother_doc_audit
  target: steps/mother_doc_audit/00_MOTHER_DOC_AUDIT_ENTRY.md
  hop: branch
  reason: mother_doc_audit 是固定前置治理阶段，先做树审计与 growth debt 清理。
- key: mother_doc
  target: steps/mother_doc/00_MOTHER_DOC_ENTRY.md
  hop: branch
  reason: mother_doc 是 audit 之后的正式需求写回阶段，且自身是复合子 workflow。
- key: construction_plan
  target: steps/construction_plan/00_CONSTRUCTION_PLAN_ENTRY.md
  hop: branch
  reason: construction_plan 负责 packs 正式落盘。
- key: implementation
  target: steps/implementation/00_IMPLEMENTATION_ENTRY.md
  hop: branch
  reason: implementation 只消费 active pack 并回填证据。
- key: acceptance
  target: steps/acceptance/00_ACCEPTANCE_ENTRY.md
  hop: branch
  reason: acceptance 负责真实 witness 与 closeout。
---

# 开发闭环阶段索引

## 当前入口的复合阶段
1. [mother_doc_audit]：`steps/mother_doc_audit/00_MOTHER_DOC_AUDIT_ENTRY.md`
2. [mother_doc]：`steps/mother_doc/00_MOTHER_DOC_ENTRY.md`
3. [construction_plan]：`steps/construction_plan/00_CONSTRUCTION_PLAN_ENTRY.md`
4. [implementation]：`steps/implementation/00_IMPLEMENTATION_ENTRY.md`
5. [acceptance]：`steps/acceptance/00_ACCEPTANCE_ENTRY.md`

## 下一跳列表
- [mother_doc_audit]：`steps/mother_doc_audit/00_MOTHER_DOC_AUDIT_ENTRY.md`
- [mother_doc]：`steps/mother_doc/00_MOTHER_DOC_ENTRY.md`
- [construction_plan]：`steps/construction_plan/00_CONSTRUCTION_PLAN_ENTRY.md`
- [implementation]：`steps/implementation/00_IMPLEMENTATION_ENTRY.md`
- [acceptance]：`steps/acceptance/00_ACCEPTANCE_ENTRY.md`
