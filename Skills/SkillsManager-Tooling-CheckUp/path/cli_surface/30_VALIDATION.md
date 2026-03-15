---
doc_id: skillsmanager_tooling_checkup.path.cli_surface.validation
doc_type: topic_atom
topic: Validation for CLI surface checking
---

# CLI Surface 检查校验

## 当前动作如何判定完成
- 入口是否明确、参数是否稳定、JSON 是否可机器消费、已声明的链路编译能力是否真实可执行，这四类结论都要给清楚。

## 通过标准
- 对 path 技能，不存在“只给路径不编译正文”的伪 `read-contract-context`。
- 对非 path 技能，不额外强加链路编译要求。
