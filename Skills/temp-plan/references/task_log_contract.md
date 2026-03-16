# 任务日志合同

## 默认结果根
- `/home/jasontan656/AI_Projects/Codex_Skills_Result/temp-plan`

## 目录规则
- 一次任务一个目录。
- 目录名格式：`tasks/<YYYYMMDD>-<task-slug>`。
- `task-slug` 使用小写英文、数字、连字符。
- 同一任务后续继续时，复用原目录，不重复新建。

## 根级文件
- `ACTIVE_TASK.md`
  - 指向当前上下文正在服从的任务目录。
  - 当用户切换、暂停、结束任务时，必须更新。

## 任务级文件
- `TASK.md`
  - 当前有效快照。
  - 记录当前真相，不堆旧版本。
- `TURN_LOG.md`
  - 回合增量。
  - 每次使用本技能后，至少追加一条极简 delta。

## 最小流程
1. 判断 `new_task` 或 `continue_task`。
2. 归一化任务名，拿到 task slug。
3. 确保结果根与任务目录存在。
4. 更新 `ACTIVE_TASK.md`。
5. 更新 `TASK.md`。
6. 追加 `TURN_LOG.md`。
7. 在本回合剩余工作中服从 `TASK.md`。

## `TASK.md` 的核心栏目
- `collaboration_mode`
- `work_preference`
- `task_goal`
- `common_rules`
- `user_taste`
- `task_mindset`
- `extra_axes`

## `extra_axes` 推荐方向
- `scope_boundary`
- `decision_style`
- `deliverable_shape`
- `risk_guardrails`
- `open_questions`
- `artifacts`

## 更新策略
- 新信息覆盖旧信息时：
  - 直接改 `TASK.md`。
  - 再在 `TURN_LOG.md` 记一条“changed/added/removed”。
- 任务切换时：
  - 先更新 `ACTIVE_TASK.md`，再继续工作。
- 任务完成时：
  - 把 `status` 改为 `done` 或 `archived`。
  - 不删除历史目录。

## 风格硬规则
- 最小语义。
- 结论优先。
- 关键词优先。
- 允许英语碎片。
- 禁止长篇大论。
