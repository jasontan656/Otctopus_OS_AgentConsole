# Question Backfill Branch

适用阶段：`mother_doc`

## Entry

- [项目级基线路由规则](PROJECT_BASELINE_ROUTING_RULES.md)
- [入口规则](MOTHER_DOC_ENTRY_RULES.md)
- [功能层规则](FEATURE_LAYER_RULES.md)
- [共享层规则](SHARED_LAYER_RULES.md)
- [回填规则](MOTHER_DOC_WRITEBACK_RULES.md)

## Use

- 进入这里时，当前文档已经完成一轮 `direct_writeback`。
- 模型必须把未收口问题整理成可回答的问题链，再向用户逐条追问。
- 问答结果回填时，覆盖写回原目标文档，不另开版本分支。

## Fixed Question Targets

- 容器内功能问题优先回填到 `features/open_questions.md`。
- 容器内共享/API/事件问题优先回填到 `shared/open_questions.md`。
- 项目级目标、影响面和当前试点范围问题优先回填到 `Mother_Doc/project_baseline/current_project_development_baseline.md`。
- 若问题已被回答，必须把对应 `open_questions.md` 条目改成已收口当前状态。
