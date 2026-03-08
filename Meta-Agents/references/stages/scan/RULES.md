# Scan Rules

- 只允许写 `scan_report.json`。
- 运行前必须拿到技能内 `.cli.lock`，抢不到锁就显式报错。
- 禁止写 `registry.json`、`index.md` 和托管副本。
- 必须忽略 `Human_Work_Zone/`。
- 必须忽略技能自身 `assets/managed_agents/`。
