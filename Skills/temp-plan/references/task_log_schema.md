# 任务日志结构

## 目录结构
```text
/home/jasontan656/AI_Projects/Codex_Skills_Result/temp-plan/
├── ACTIVE_TASK.md
└── tasks/
    └── 20260316-example-task/
        ├── TASK.md
        └── TURN_LOG.md
```

## `ACTIVE_TASK.md`
- 作用：告诉模型当前上下文默认服从哪个任务目录。
- 建议字段：

```markdown
# Active Task
- task_name: <human-readable name>
- task_slug: <YYYYMMDD-task-slug>
- status: active
- task_path: tasks/<YYYYMMDD-task-slug>
- updated_at: <YYYY-MM-DD>
- note: <one-line reason>
```

## `TASK.md`
- 作用：当前有效快照。
- 推荐模板：`assets/templates/TASK.template.md`
- 示例风格：

```markdown
# Task Snapshot
- task_name: temp-plan log refit
- status: active
- started_at: 2026-03-16
- updated_at: 2026-03-16

## collaboration_mode
- direct edit first
- inspect before conclusion

## work_preference
- conclusion first
- short accurate report
- reject wrong assumption

## task_goal
- refit temp-plan to maintain long-task logs

## common_rules
- minimal semantics
- one task one dir
- AI maintain markdown logs

## user_taste
- concise
- structured

## task_mindset
- task log = active truth
- not essay memory

## extra_axes
- scope_boundary: skill source in repo, then sync to codex
- deliverable_shape: short final summary
```

## `TURN_LOG.md`
- 作用：只记 delta，不重抄快照。
- 推荐模板：`assets/templates/TURN_LOG.template.md`
- 单条建议结构：

```markdown
# Turn Log

## 2026-03-16
- created: task directory + active pointer
- changed: skill scope from intent-only to task-log-governed
- added: result-root contract, minimal markdown templates
```

## 写入原则
- `TASK.md` 可重写。
- `TURN_LOG.md` 只追加。
- 如果一个字段已经失效，优先删掉旧词，不要做“新旧并存”。
