---
doc_id: "tooling.module.runtime_contract"
doc_type: "module_doc"
topic: "Runtime contract module behavior in Meta-Skill-DocStructure"
anchors:
  - target: "../../../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "documents"
    direction: "upstream"
    reason: "This module exists to expose the runtime contract."
  - target: "../../Cli_Toolbox_DEVELOPMENT.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This module doc is part of the development tree."
---

# runtime_contract 模块

## 职责
- 读取 `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`。
- 原样输出 machine-readable 合同。

## 输入输出
- 输入：无
- 输出：完整 runtime contract JSON
- 失败模式：
  - runtime contract 文件缺失
  - runtime contract JSON 不合法
