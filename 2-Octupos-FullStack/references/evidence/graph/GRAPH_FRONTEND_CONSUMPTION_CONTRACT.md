# Graph Frontend Consumption Contract


## Contract Header
- `contract_name`: `2_octupos_fullstack_references_evidence_graph_graph_frontend_consumption_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

适用阶段：`evidence > graph`

## Frontend View Rule

- 默认显示第一层：`narrative summary`
- 首次展开：`contract / relationship`
- 再次展开：`mechanical implementation`

## Source Rule

- narrative summary 主要来自 `overview/`、`README.md`、实体文档摘要。
- contract/relationship 主要来自 `shared/`、`AGENTS.md`、document edges。
- mechanical implementation 主要来自 code bindings、module/helper/function edges。

## Consumption Rule

- 前端消费 `frontend_views/` 聚合产物，而不是直接拼源 markdown。
- CLI 仍然消费碎片化 registry / indexes / reports。
