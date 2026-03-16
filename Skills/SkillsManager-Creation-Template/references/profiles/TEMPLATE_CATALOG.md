---
doc_id: skillsmanager_creation_template.references.profiles.template_catalog
doc_type: topic_atom
topic: Supported scaffold catalog
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The catalog lists supported scaffold combinations.
---

# Template Catalog

| Name | doc_topology | tooling_surface | workflow_control | 推荐用途 |
| --- | --- | --- | --- | --- |
| `inline_minimal` | `inline` | `none` | `advisory` | 极薄门面技能 |
| `referenced_contract` | `referenced` | `contract_cli` | `guardrailed` | 文档真源 + 合同 CLI |
| `referenced_automation` | `referenced` | `automation_cli` | `guardrailed` | 文档真源 + 自动化 CLI |
| `workflow_contract` | `workflow_path` | `contract_cli` | `compiled` | 复合 workflow，自动化较弱 |
| `workflow_automation` | `workflow_path` | `automation_cli` | `compiled` | 复合 workflow + 自动化入口 |

## 默认推荐
- 未指定时，默认生成 `referenced_contract`。
- 只有在 target skill 明确需要 workflow compiler 时，才升级到 `workflow_path`。
