---
doc_work_state: modified
doc_pack_refs: []
doc_role: root_index
thumb_title: Root Index
thumb_summary: 顶层常驻根入口，自动维护目录级结构图，不展示文件清单。
display_layer: overview
always_read: true
anchors_down: []
anchors_support: []
---

# Mother Doc Root Index

## 当前职责
- 作为 `mother_doc` 的固定根入口存在。
- 本文件不手工维护完整目录、章节清单或结构总表。
- 后续脚本应通过遍历当前 folder 结构自动生成目录级结构图，不展示文件。

## 根入口约束
- `doc_role` 必须保持为 `root_index`。
- `always_read` 必须保持为 `true`。
- 所有 `anchors_down` 与 `anchors_support` 必须保持空数组。
- 根入口不承载具体设计细节，只承载最小根说明与脚本挂点。
- 当 folder 结构变化时，应重新运行 `mother-doc-refresh-root-index`。

## 后续维护方式
- 允许在文档树中自由新增、插入、重排原子文档。
- 不允许把文档树重新收敛回固定章节模板。
- 若需要阶段设计计划，使用独立 `doc_role=design_plan` 文档承载，而不是把设计计划塞回本根文件。

## 下一跳列表
- [由 `mother-doc-refresh-root-index` 自动生成目录图；本模板根入口不手工维护下游列表。]
