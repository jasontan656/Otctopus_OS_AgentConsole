# Feature Layer Rules

适用阶段：`mother_doc`

## Role

- `features/` 承载当前容器的功能文档层。
- 单个功能文档不要求与单个代码文件机械 1:1 对齐。
- 单个文档可以覆盖一个功能，也可以覆盖一个语义等价的多文件实现切片。

## Fixed Files

- `feature_catalog.md`
- `active_requirements.md`
- `open_questions.md`

## Writing Rule

- `feature_catalog.md` 负责列出当前容器已有或规划中的功能项。
- `active_requirements.md` 负责承载这轮需求直接影响的功能内容。
- `open_questions.md` 负责承载 direct_writeback 后仍未收口的问题，供 question_backfill 逐轮关闭。
