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
- 本技能唯一主闭环为：`research -> architect -> preview -> design -> impact -> plan -> implementation -> validation -> final_delivery`。
- 主入口统一，但每个阶段都必须有单独入口、单独 checklist、单独 lint 焦点与单独退出条件。
- 小型对象是事实层，阶段沉淀文档是汇总层；不得只改文档不改对象。
- 九个阶段都必须各自形成：问题框架、显式推导链、前序正式产物引用、阶段结论、未收口问题与进入下一阶段的门禁。
- 新任务必须先检查 `Codex_Skill_Runtime/Functional-Analysis-Runtask` 是否存在未闭合 task runtime；只有历史任务全部 closed 后才允许新建任务。

## 执行模式
- `continuous`
  - 按固定阶段顺序推进；后阶段只能在前阶段正式产物完成、被显式消费并写回后启动。
- `single_stage`
  - 在同一技能内只进入 1 个阶段，但仍必须满足该阶段要求的全部前序正式产物与消费链。

## 全局边界
- 不拆分成多个平行技能。
- 不用聊天摘要代替对象化写回。
- 不绕过任一正式阶段直接让实现代码定义真实意图。
- 不允许把 task artifacts 直接写进 `Otctopus_OS_AgentConsole/Skills/Functional-Analysis-Runtask/` 技能目录。
- 任何报告、计划、阶段沉淀文档落盘前，必须先联动 `Functional-HumenWorkZone-Manager`，把 workspace root 解析到 `Human_Work_Zone` 受管区。
- 不允许后阶段补写或偷渡前阶段应完成的问题、判断或证据。
- 不允许用 generic 占位话术替代阶段专属问题框架、判断链与写回合同。
- 不允许一次性预写九阶段内容后直接进入 implementation。

## 当前闭环常驻项
- 旧分析方法论文档与旧技能收敛方案。
- 当前 workspace 对象：manifest、evidence registry、architect assessment、preview projection、design decisions、impact map、milestone packages、implementation ledger。
- 当前 task runtime 对象：`Codex_Skill_Runtime/Functional-Analysis-Runtask/NNN_task_slug/task_runtime.yaml`。
- 当前阶段 checklist、stage-specific lint、显式承接链与写回状态结果。

## 下一跳列表
- [tools]：`15_TOOLS.md`
