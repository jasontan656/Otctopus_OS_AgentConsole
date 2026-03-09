# Graph Storage Layout

适用阶段：`evidence > graph`

## Fragment First

- 线下存储必须以碎片化节点、边、索引和报告为主。
- 不把前端的聚合展示直接写回源 markdown。

## Required Runtime Files

- `registry/document_nodes.json`
- `registry/evidence_nodes.json`
- `indexes/document_edges.json`
- `indexes/status_index.json`
- `frontend_views/layered_documents.json`
- `frontend_views/evidence_timeline.json`
- `reports/document_sync_report.json`
- `reports/evidence_sync_report.json`

## Layout Rule

- registry 只放节点清单。
- indexes 只放关系与查询索引。
- frontend_views 只放给前端消费的聚合物。
- 源 authored docs 仍然保留在 `Mother_Doc/docs/`。
