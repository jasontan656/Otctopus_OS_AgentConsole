# Shared Layer Rules

适用阶段：`mother_doc`

## Role

- `shared/` 承载当前容器对外或跨容器共享的接口层。
- 这里覆盖 API、事件、共享合同、依赖关系和对应未收口问题。
- 这是 contract-layer 的主要文档来源之一。

## Fixed Files

- `api_surfaces.md`
- `event_and_message_flows.md`
- `shared_contracts.md`
- `cross_container_dependencies.md`
- `open_questions.md`

## Writing Rule

- 与其他容器交互的规则优先写到这里，而不是散落到功能正文里。
- 共享层内容必须支持后续 evidence 阶段转换成关系图和锚点绑定。
- 未收口的 API / event / dependency 问题写进 `open_questions.md`，由 question_backfill 继续关闭。
