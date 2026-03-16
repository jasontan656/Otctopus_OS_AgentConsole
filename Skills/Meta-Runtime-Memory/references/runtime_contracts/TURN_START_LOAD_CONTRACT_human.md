# Turn Start Load

- `turn start` 先确保 store 存在。
- 读取 `ACTIVE_TASK.json`、`user/USER_MEMORY.json`、当前任务的 `TASK_MEMORY.json`。
- 产出 `Codex_Skill_Runtime/Meta-Runtime-Memory/compiled/ACTIVE_MEMORY.json` 与 Markdown mirror。
- 若用户本轮切换任务，先重新绑定任务，再重新编译 active memory。
