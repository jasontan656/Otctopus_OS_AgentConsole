# Task Binding

- 每个任务一个目录：`tasks/<task_id>/`
- `ACTIVE_TASK.json` 是当前任务唯一指针。
- 绑定任务时：
  - 规范化 `task_id`
  - 若目录不存在则创建
  - 更新 `ACTIVE_TASK.json`
  - 可选写入 `task_goal`
  - 立刻重编译 active memory
