---
doc_id: meta_runtime_memory.runtime_contract.human
doc_type: runtime_contract_human
topic: "CLI-first runtime contract for Meta-Runtime-Memory"
---

# Meta-Runtime-Memory Runtime Contract

## 用途
- 这是 `Meta-Runtime-Memory` 的 human mirror。
- 真正运行时指令以 `scripts/Cli_Toolbox.py runtime-contract --json` 输出为准。

## 核心定义
- memory 只保留三类真相：
  - 长期目标
  - 当前现状
  - 稳定行为约束
- 运行时至少维护两层：
  - 用户常驻层
  - 任务层

## 默认执行
1. `turn start` 强制加载 active memory。
2. 若任务未绑定，先绑定任务。
3. 正常执行主任务。
4. `turn end` 强制检查是否有稳定信号需要写回。
5. 若发生写回，必须先更新 JSON snapshot，再同步 Markdown mirror，再重编译 active memory。

## 关键命令
- `runtime-contract --json`
- `directive --topic <topic> --json`
- `init-store --json`
- `bind-task --task-id <task_id> --json`
- `compile-active-memory --json`
- `upsert-user-memory --patch-json '<json>' --json`
- `upsert-task-memory --task-id <task_id> --patch-json '<json>' --json`
- `append-turn-delta --summary "<summary>" --json`
- `validate-store --json`
