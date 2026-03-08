# mod_collect

- 入口：`scripts/managed_collect.py`
- 职责：扫描 source root 下全部 `AGENTS.md`，并完整复制到技能托管目录。
- 不变量：
  - 不复制技能自身托管目录内的副本。
  - 不改写 `AGENTS.md` 内容。
