---
doc_id: skillsmanager_runstates_manager.references.tooling.cli_toolbox_development
doc_type: topic_atom
topic: Development notes for SkillsManager-RunStates-Manager tooling
---

# Cli_Toolbox Development

## 主要模块
- `contract_payloads.py`
  - 读取 runtime contract 与 directive。
- `governed_type_registry.py`
  - 维护 supported governed types、所需 checklist、模板路径与成功标准。
- `target_inspector.py`
  - 识别 target skill 的 profile、是否 workflow-bearing、是否更像 skill-flow orchestrator。
- `runstate_scaffolder.py`
  - 生成 target skill 的 runstate contract、模板与成功判定文档。
- `runstate_auditor.py`
  - 验证 target skill 是否真正满足 runstate 方法要求。

## 维护规则
- 只要 governed_type、checklist schema 或 CLI 命令面变化，就必须同步更新：
  - `references/runtime_contracts/`
  - `references/tooling/`
  - `tests/`
- 不要把 `Skills_runtime_checklist` 塞进 `metadata.skill_profile`。
- 审计逻辑要保持 contract-first，但必须补充 host markdown 的真实消费证据检查。
