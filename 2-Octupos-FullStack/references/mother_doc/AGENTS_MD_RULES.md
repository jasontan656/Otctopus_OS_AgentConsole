# AGENTS.md Rules

## 当前唯一允许的外部目标

- 当前只允许一个外部 AGENTS runtime entry：`Octopus_OS/AGENTS.md`。
- `Octopus_OS` 其他目录下的 `AGENTS.md` 都属于历史错误结构，应由统一 push 清理。

## 内外形态

- 外部 `Octopus_OS/AGENTS.md` 只保留 `Part A`，作为给运行时 hook 的薄入口。
- mirror 内部受管资产是：
- `assets/managed_targets/Octopus_OS/AGENTS_human.md`
- `assets/managed_targets/Octopus_OS/AGENTS_machine.json`
- 其中 human 文件承载 `Part A + Part B`，machine 文件承载 `Part B only` payload。

## 运行时原则

- 模型执行时必须优先使用 CLI 返回的 target-contract / branch-contract / registry JSON。
- markdown 只作为人类审计和写作载体，不是第一运行时主源。
- 若未来要扩展更多外部 AGENTS 目标，必须先在 mirror 的 managed payload 中完成定义，再由统一 push 写回。
