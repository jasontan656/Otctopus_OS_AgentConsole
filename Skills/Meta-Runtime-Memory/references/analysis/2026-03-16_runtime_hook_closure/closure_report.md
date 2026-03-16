# Meta-Runtime-Memory Runtime Hook Closure

## 1. 设计缺陷清单

1. 缺少 turn-start 自动 hook 到当前 `session_id/turn_id` 的审计归因链路。
2. 缺少任务层自动绑定与 durable task memory 自动形成的证明链路。
3. 缺少 turn-end writeback check 在 `skipped` 时仍保留自动审计记录的链路。
4. `--codex-home` 显式 override 会静默回退到 `~/.codex`，会污染会话边界。
5. `apply_patch` 相对路径未按 session `cwd` 解析，会把真实 applied turn 误判为 `skipped`。
6. 普通 `exec_command` stdout 中的绝对路径会被误记为 `changed_paths`，存在 applied 假阳性。

## 2. 架构收敛决策

- 以 Codex session JSONL 作为自动 hook 的 canonical runtime feed。
- 在受管 store 中新增 `ACTIVE_RUNTIME.json`、`sessions/<session_id>/SESSION_MEMORY.json`、`sessions/<session_id>/turns/<turn_id>.json`、`watcher/OBSERVER_STATE.json`、`logs/machine.jsonl`、`logs/human.log`。
- 在首个真实 `user_message` 到达时自动派生 `task_id` 并绑定 durable task memory。
- turn-end 无论 `applied` 还是 `skipped` 都必须写 turn audit，并同步 machine/human log。
- `changed_paths` 只接受显式写操作事件；相对路径必须用 session `cwd` 归一化。

## 3. 最小切片施工计划

1. 实现 watcher、审计模型、存储路径与 CLI 入口。
2. 接入自动 task binding、durable task memory、turn delta、recall/search。
3. 用真实后台 watcher + 真实 `codex exec` + `pytest` 回归收口。

## 4. 真实实现与验证证据

### 4.1 关键实现文件

- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/memory_session_runtime.py`
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/memory_store.py`
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/memory_models.py`
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py`
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/tests/test_cli_toolbox.py`

### 4.2 关键命令

```bash
/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 -m pytest \
  /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/tests/test_cli_toolbox.py
```

```bash
export CODEX_SKILL_RUNTIME_ROOT=/tmp/meta_runtime_memory_validation_live5.9qXxI1/runtime
export CODEX_SKILL_RESULT_ROOT=/tmp/meta_runtime_memory_validation_live5.9qXxI1/result
/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 \
  /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py \
  watch-codex-sessions --codex-home /tmp/meta_runtime_memory_validation_live5.9qXxI1/codex_home \
  --poll-interval-ms 200 --idle-exit-seconds 40 --json
```

```bash
printf '%s\n' '只读检查当前目录下 note.txt 的内容并简短回答，不要修改任何文件，也不要运行测试。' \
| CODEX_HOME=/tmp/meta_runtime_memory_validation_live5.9qXxI1/codex_home \
  /home/jasontan656/.npm-global/bin/codex exec --skip-git-repo-check \
  -C /tmp/meta_runtime_memory_validation_live5.9qXxI1/workspace -
```

```bash
printf '%s\n' '把 note.txt 改成两行内容：第一行是 runtime hook validation，第二行是 applied turn。改完后读取文件确认结果，并简短汇报。' \
| CODEX_HOME=/tmp/meta_runtime_memory_validation_live5.9qXxI1/codex_home \
  /home/jasontan656/.npm-global/bin/codex exec --skip-git-repo-check \
  -C /tmp/meta_runtime_memory_validation_live5.9qXxI1/workspace -
```

```bash
/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 \
  /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py \
  show-turn-audit --session-id 019cf5ed-ca6b-7ac3-8351-649edc4a28d0 \
  --turn-id 019cf5ed-ca74-72c2-bb39-4b3a595a839c --json
```

```bash
/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 \
  /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py \
  recall-memory --task-id note-txt-runtime-hook-validation-applied-turn-019cf5ed --json
```

```bash
/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 \
  /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Memory/scripts/Cli_Toolbox.py \
  search-memory --query "runtime hook validation" --json
```

### 4.3 真实可观察证据

- 后台 watcher 最终输出：`processed_turns` 含一个 `skipped` 与一个 `applied`，路径在 `/tmp/meta_runtime_memory_validation_live5.9qXxI1/...` 下完全隔离。
- machine log：`/tmp/meta_runtime_memory_validation_live5.9qXxI1/runtime/Meta-Runtime-Memory/logs/machine.jsonl`
  - `turn_start_loaded` 对应 `session_id=019cf5ed-8416-7d10-8970-bc890b5f0dc1` 与 `session_id=019cf5ed-ca6b-7ac3-8351-649edc4a28d0`
  - `turn_end_checked` 分别给出 `writeback_decision=skipped` 与 `writeback_decision=applied`
- skipped turn audit：`/tmp/meta_runtime_memory_validation_live5.9qXxI1/result/Meta-Runtime-Memory/sessions/019cf5ed-8416-7d10-8970-bc890b5f0dc1/turns/019cf5ed-8445-7123-bd05-bb845f83e360.json`
  - `turn_start_status=applied`
  - `writeback_decision=skipped`
  - `next_actions` 非空
- applied turn audit：`/tmp/meta_runtime_memory_validation_live5.9qXxI1/result/Meta-Runtime-Memory/sessions/019cf5ed-ca6b-7ac3-8351-649edc4a28d0/turns/019cf5ed-ca74-72c2-bb39-4b3a595a839c.json`
  - `turn_start_status=applied`
  - `changed_paths=["/tmp/meta_runtime_memory_validation_live5.9qXxI1/workspace/note.txt"]`
  - `writeback_decision=applied`
- durable task memory：`/tmp/meta_runtime_memory_validation_live5.9qXxI1/result/Meta-Runtime-Memory/tasks/note-txt-runtime-hook-validation-applied-turn-019cf5ed/TASK_MEMORY.json`
  - `current_state` 含 session/turn 完成与 changed_paths
  - `artifacts` 含文件路径与 audit 路径
- recall/search：
  - `recall-memory --task-id ...` 能读回 applied turn 的 `TASK_MEMORY` 与 `TURN_DELTA`
  - `recall-memory --session-id 019cf5ed-8416-7d10-8970-bc890b5f0dc1` 能读回 skipped turn audit
  - `search-memory --query "runtime hook validation"` 命中 applied task 与 applied turn

## 5. 失败对照

- live2 失败：`apply_patch` 输出为 `A note.txt / D note.txt` 相对路径，旧实现未用 session `cwd` 归一化，导致 applied turn 被误判为 `skipped`。
- live4 失败：`--codex-home` 指向不存在目录时静默回退 `~/.codex`，并且隔离目录未带认证态导致 `codex exec` 401。
- live4 次级缺陷：普通 `exec_command` 输出中的绝对路径会被误记为 changed_paths，存在 applied 假阳性。
- live5 修复后结果：skipped/applied/audit/durable memory/recall/search 全部成立。

## 6. 剩余风险

- 当前 changed_paths 对显式写操作事件覆盖最好，对“完全由 `exec_command` 自写文件且没有明确写操作事件”的场景仍是保守检测。
- 隔离 `CODEX_HOME` 的真实验证依赖最小认证文件；如果平台后续更改认证形态，需要同步更新验证脚手架。
