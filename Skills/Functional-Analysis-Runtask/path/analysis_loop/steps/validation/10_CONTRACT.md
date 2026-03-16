---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.validation.contract
doc_type: action_contract_doc
topic: Validation contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 validation 合同，再看工具。
---

# validation 阶段合同

- validation 负责检查对象完整性、引用有效性、阶段状态一致性与 Human_Work_Zone 写回状态。
- validation 同时负责检查 `task_runtime.yaml` 是否已完整闭环，且不会错误阻塞下一任务。
- 若阶段沉淀文档或方案文档路径已声明，validation 必须检查对应路径存在。
- 不得把“暂时没写回”伪装成阶段完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
