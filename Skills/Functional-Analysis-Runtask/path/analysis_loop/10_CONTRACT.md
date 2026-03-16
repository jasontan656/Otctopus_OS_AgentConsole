---
doc_id: functional_analysis_runtask.path.analysis_loop.contract
doc_type: action_contract_doc
topic: Analysis loop contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读全局合同，再看工具与运行时辅助面。
---

# analysis_loop 全局合同

## 全局职责
- 本技能唯一主闭环为：`research_baseline -> architecture_convergence -> plan -> implementation -> validation`。
- 主入口统一，但每个阶段都必须有单独入口、单独 checklist、单独 lint 焦点与单独退出条件。
- 小型对象是事实层，阶段沉淀文档是汇总层；不得只改文档不改对象。

## 执行模式
- `continuous`
  - 按固定阶段顺序推进，阶段状态必须显式切换。
- `single_stage`
  - 在同一技能内只进入 1 个阶段，仅读取该阶段合同要求的最小对象与前置证据。

## 全局边界
- 不拆分成多个平行技能。
- 不用聊天摘要代替对象化写回。
- 不绕过 plan 直接让实现代码定义真实意图。

## 当前闭环常驻项
- 旧分析方法论文档与旧技能收敛方案。
- 当前 workspace 对象：manifest、evidence registry、architecture decisions、plan slices、implementation ledger。
- 当前阶段 checklist 与 stage-specific lint 结果。

## 下一跳列表
- [tools]：`15_TOOLS.md`
