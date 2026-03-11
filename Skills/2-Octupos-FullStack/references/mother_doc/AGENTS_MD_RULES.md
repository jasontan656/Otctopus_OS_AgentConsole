# AGENTS.md Rules

- 当前只治理一个外部 AGENTS 目标：`Octopus_OS/AGENTS.md`。
- mirror 内部只保留：
- `assets/managed_targets/Octopus_OS/AGENTS_human.md`
- `assets/managed_targets/Octopus_OS/AGENTS_machine.json`
- 外部 `Octopus_OS/AGENTS.md` 只保留 `Part A`。
- 内部 human 文件承载 `Part A + Part B`，machine 文件承载 `Part B only`。
- 当前运行时入口固定为 branch contract、stage directive、target contract 三组 CLI JSON。
