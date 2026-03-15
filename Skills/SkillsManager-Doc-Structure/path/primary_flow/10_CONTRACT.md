---
doc_id: skillsmanager_doc_structure.path.primary_flow.contract
doc_type: topic_atom
topic: Contract for the primary doc-structure governance flow
anchors:
- target: 00_PRIMARY_FLOW_ENTRY.md
  relation: implements
  direction: upstream
  reason: The flow contract is reached from the primary entry.
- target: 15_TOOLS.md
  relation: routes_to
  direction: downstream
  reason: Tooling follows after the contract is clear.
---

# 主治理链路合同

## 当前动作要完成什么
- 判断目标技能属于哪一种文档组织形态。
- 用固定预期结构去读取目标技能，而不是从零自由解释。
- 对不符合预期的根目录、门面职责、路径衔接和 anchors 给出 lint 结果。
- 不把各层正文内容写死成模板字符串。

## 当前动作必须满足什么
- 目标技能根目录只能保留其目标态所允许的根节点。
- `SKILL.md` 只做门面，不承载后续链路正文。
- 规则必须跟着对应步骤下沉，不能重新长回总则。
- 本技能本身也必须遵守同样的组织方式。
- CLI 只检查结构违规；正文是否符合该层职责，交由模型沿链路做语义检查。

## 下一跳列表
- [tool/lint 能力面]：`15_TOOLS.md`
