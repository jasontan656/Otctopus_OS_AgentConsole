# Graph Node Edge Model

适用阶段：`evidence > graph`

## Node Families

- 容器节点
- 目录节点
- `README.md` 用途节点
- `AGENTS.md` 导航节点
- `<folder_name>.md` 实体节点
- `overview/*.md` narrative 节点
- `features/*.md` semantic feature 节点
- `shared/*.md` contract 节点
- `common/**` abstraction 节点
- code module / helper / function / API 节点
- implementation batch / deployment checkpoint / witness 节点

## Edge Families

- `contains`
- `explains`
- `binds_to`
- `depends_on`
- `implements`
- `verifies`
- `belongs_to_container`
- `surfaces_in_frontend`

## Layer Rule

- `narrative_layer`: container summaries, overview, feature intent.
- `contract_layer`: AGENTS navigation, shared contracts, API/event relations.
- `implementation_layer`: code modules, helper edges, abstraction leaves.
- `evidence_layer`: logs, witnesses, deployment checkpoints, lifecycle state indexes.
