---
doc_id: skill_creation_template.asset.stage_instruction_template
doc_type: template_doc
topic: Template for one stage instruction document
anchors:
- target: WORKFLOW.md
  relation: pairs_with
  direction: lateral
  reason: Stage instruction and workflow should be authored together.
- target: ../00_STAGE_INDEX_TEMPLATE.md
  relation: implements
  direction: upstream
  reason: The stage index routes readers into stage instruction.
---

# <stage_name> Instruction Template

## 阶段目标
- [当前阶段唯一目标]

## 合同入口
- `CHECKLIST.json`
- `DOC_CONTRACT.json`
- `COMMAND_CONTRACT.json`
- `GRAPH_CONTRACT.json`

## 读取顺序
1. 先读取 `CHECKLIST.json`
2. 再读取 `DOC_CONTRACT.json`
3. 再读取 `COMMAND_CONTRACT.json`
4. 最后读取 `GRAPH_CONTRACT.json`

## 禁止项
- [禁止跨阶段读取无关文档]
- [禁止绕过当前阶段 checklist 直接执行]
