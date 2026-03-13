---
doc_id: dev_octopusos_constitution_projectstructure.tooling.architecture_overview
doc_type: topic_atom
topic: Tooling architecture overview for the OctopusOS project-structure constitution skill
anchors:
- target: ../Cli_Toolbox_DEVELOPMENT.md
  relation: implements
  direction: upstream
  reason: The development entry routes into this overview.
---

# Architecture Overview

- 当前工具架构为“静态 contract reader”：
  - `scripts/Cli_Toolbox.py` 只负责读取并输出 `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
  - 结构规则和命名宪法仍以下沉治理文档为源
- 若未来新增工具，其职责只能是消费本技能已有的项目级结构合同，输出 lint 或检查结果，不能反向成为规则源。
