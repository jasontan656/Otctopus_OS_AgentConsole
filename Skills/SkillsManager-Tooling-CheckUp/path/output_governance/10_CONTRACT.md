---
doc_id: skillsmanager_tooling_checkup.path.output_governance.contract
doc_type: topic_atom
topic: Contract for output governance checking
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: output governance contract is followed by the applicable tools.
---

# 输出落点检查合同

## 当前动作要完成什么
- 检查目标技能是否把 runtime 日志、审计痕迹、默认结果与定向产物落到受管位置。
- 检查默认回退、显式落点参数、文档声明与历史迁移责任是否同时成立。

## 当前动作必须满足什么
- 目标技能的 runtime 侧落盘应治理到 `/home/jasontan656/AI_Projects/Codex_Skill_Runtime`。
- 目标技能的通用结果与默认产物应治理到 `/home/jasontan656/AI_Projects/Codex_Skills_Result`。
- 定向产物技能必须支持或要求显式落点；未指定时，默认值也必须可追溯。
- 本线路治理的是目标技能输出，不表示本技能自身会在这些根路径下持久化结果。

## 下一跳列表
- [tools]：`15_TOOLS.md`
