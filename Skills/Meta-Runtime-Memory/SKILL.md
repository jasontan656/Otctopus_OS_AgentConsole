---
name: "Meta-Runtime-Memory"
description: "面向整个回合的常驻 runtime memory contract。默认在 turn start 强制加载用户层与任务层 memory，在 turn end 强制检查是否需要写回，只保留长期目标、当前现状与稳定行为约束。"
metadata:
  doc_structure:
    doc_id: "meta_runtime_memory.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the Meta-Runtime-Memory skill"
    anchors:
      - target: "references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The facade must route execution to the CLI-first runtime contract."
      - target: "references/runtime_contracts/TURN_START_LOAD_CONTRACT_human.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "Turn-start loading is the primary runtime hook branch."
      - target: "references/runtime_contracts/TURN_END_WRITEBACK_CONTRACT_human.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "Turn-end writeback governance is the primary closure branch."
---

# Meta-Runtime-Memory

## 1. 工具入口
- 本技能运行时统一入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py runtime-contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py paths --json`
- 本技能自动 hook / recall 入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py watch-codex-sessions --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py show-turn-audit --session-id <session_id> --turn-id <turn_id> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py recall-memory --task-id <task_id> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py recall-memory --session-id <session_id> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py search-memory --query "<text>" --json`
- 本技能持久化与写回入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py init-store --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py compile-active-memory --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py upsert-user-memory --patch-json '<json>' --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py upsert-task-memory --task-id <task_id> --patch-json '<json>' --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py bind-task --task-id <task_id> --title "<title>" --goal "<goal>" --json`（仅保留为人工修复/迁移入口，不再是默认 turn-start 路径）
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py append-turn-delta --summary "<summary>" --task-memory-update "<delta>" --next-action "<next>" --writeback-decision applied --json`（仅保留为人工修复/迁移入口）
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py validate-store --json`
- 模型读取 runtime contract、directive、路径与数据模型时必须优先走 CLI JSON；`SKILL.md` 只做门面。

## 2. 适用域
- 适用于：把 memory 定义为常驻 runtime turn hook contract，而不是随缘回忆或临时摘要。
- 适用于：只保留真正跨回合有价值的内容，即 `长期目标 + 当前现状 + 稳定行为约束`。
- 适用于：用户层常驻偏好、沟通风格、做事风格、协同方式、使用习惯，以及任务层目标、现状、约束、心智模型、后续推进状态。
- 适用于：需要把 memory source of truth 固定为 JSON，并同步渲染 Markdown human mirror 的场景。
- 不适用于：把完整聊天历史、完整工具输出、一次性细节噪声或低信号碎片全部塞进 memory。
- 不适用于：把技能代码目录当作用户可变 runtime 数据落点。

## 3. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py runtime-contract --json`。
2. 在 turn start 或用户显式调用本技能时，立即读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py directive --topic turn-start-load --json`
3. 若当前任务尚未绑定或需要切换任务，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py directive --topic task-binding --json`
4. 运行时默认由 session-stream watcher 自动消费 `~/.codex/sessions/**/*.jsonl` 中的 `task_started -> user_message -> task_complete` 事件链，自动完成 turn-start 归因、任务绑定、turn-end writeback check 与 recall 索引。
5. 若涉及 payload 边界、写回字段、路径或 source of truth，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py directive --topic payload-governance --json`
6. 在 turn end 或 final reply 前，必须读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py directive --topic turn-end-writeback --json`
7. 当 final reply 需要反映 memory 已更新、未更新原因或残余缺口时，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py directive --topic final-reply-guard --json`
8. 只有当 CLI JSON 仍留下真实语义缺口时，才打开 human mirrors。

## 4. 运行边界
- 默认触发：本技能是 turn hook，`turn start` 强制加载，`turn end` 强制检查；写回则按条件发生。
- source of truth：`Codex_Skills_Result/Meta-Runtime-Memory` 下的 JSON 文件；Markdown 只做 human mirror。
- 自动归因链：turn-start / turn-end 的真实触发源不是手工 CLI，而是 Codex session stream 中的 `session_id + turn_id + task_started/task_complete` 事件链。
- 审计链：至少保留 `ACTIVE_RUNTIME.json`、`sessions/<session_id>/SESSION_MEMORY.json`、`sessions/<session_id>/turns/<turn_id>.json`、`tasks/<task_id>/TURN_DELTA.json`、`runtime/logs/machine.jsonl`、`runtime/logs/human.log`。
- 顶层用户常驻层：至少覆盖 `通用偏好 / 沟通风格 / 做事风格 / 协同方式 / 整体使用习惯 / 稳定约束 / 长期目标`。
- 任务层：至少覆盖 `常驻目标 / 当前现状 / 工作方式 / 限制 / 心智模型 / 后续推进状态`。
- 写回原则：优先更新 snapshot，再追加 turn delta；禁止用增量日志替代当前真相。
- 路径原则：runtime 编译产物放在 `Codex_Skill_Runtime/Meta-Runtime-Memory`；durable memory 放在 `Codex_Skills_Result/Meta-Runtime-Memory`。
- 约束原则：不得持久化完整 transcript、不得把 Markdown 当唯一真相源、不得把用户可变 memory 写进技能代码目录。

## 5. 结构索引
```text
Meta-Runtime-Memory/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── templates/
├── references/
│   └── runtime_contracts/
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── memory_bind_task.py
│   ├── memory_compile.py
│   ├── memory_models.py
│   ├── memory_store.py
│   ├── memory_validate.py
│   └── memory_writeback.py
└── tests/
```
