# Direct Writeback Branch

适用阶段：`mother_doc`

## Entry

- [项目级基线路由规则](PROJECT_BASELINE_ROUTING_RULES.md)
- [入口规则](MOTHER_DOC_ENTRY_RULES.md)
- [回填规则](MOTHER_DOC_WRITEBACK_RULES.md)
- [总览层规则](OVERVIEW_LAYER_RULES.md)
- [功能层规则](FEATURE_LAYER_RULES.md)
- [共享层规则](SHARED_LAYER_RULES.md)
- [状态规则](DOC_STATUS_RULES.md)

## Use

- 进入这里时，只写用户已经明确描述的内容。
- 受影响容器内优先回填：
  - `overview/`
  - `features/`
  - `shared/`
  - `common/`
- 项目级目标、当前开发说明、影响面裁决与动态增长原则优先回填到 `Mother_Doc/project_baseline/`。
- 缺失细节允许留 `replace_me`、占位段或问题缺口，但不得自行假装收口。

## Output

- 更新后的当前状态文档
- `modified / developed / null` 生命周期状态块
- 供后续 `question_backfill` 或 `implementation` 使用的明确缺口
