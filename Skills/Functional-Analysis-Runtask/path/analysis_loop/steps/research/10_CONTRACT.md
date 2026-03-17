---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.research.contract
doc_type: action_contract_doc
topic: Research contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 research 合同，再看工具。
---

# research 阶段合同

- 必须显式继承旧分析方法论文档、旧技能收敛方案与旧 research 时代的问题链密度，不能把它们当成无关背景。
- 必须先通过 `Functional-HumenWorkZone-Manager` 解析当前 task artifacts 的受管落点，再初始化 workspace 对象骨架。
- 新任务启动前必须先执行 `task-gate-check`，确认不存在未闭合历史任务，再生成 `task_runtime.yaml` 骨架。
- research 必须先整理“目标意图、范围边界、默认全相关起始判断、强制追问问题链、显式假设、未收口问题”，再进入证据采样。
- `research/001_research_report.md` 必须至少写透：调研目标与范围、输入资产与当前前提、问题框架与强制追问、证据登记、显式推导链、阶段结论、未收口问题与进入 architect 的门禁。
- `research/evidence_registry.yaml` 与 report 之间必须是“证据登记 -> 报告引用 -> 结论推导”的显式链路。
- 证据、推断、假设、未收口问题与本地改写建议必须分层记录，不能混写成单段叙事。
- research 完成前，禁止提前写 architect/design/impact/plan/implementation/validation/final_delivery 的完成态内容。

## 下一跳列表
- [tools]：`15_TOOLS.md`
