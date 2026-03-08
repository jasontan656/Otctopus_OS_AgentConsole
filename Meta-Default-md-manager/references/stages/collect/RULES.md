# Collect Rules

- 只允许消费 `scan_report.json`，禁止重新扫描文件系统。
- 运行前必须拿到技能内 `.cli.lock`，抢不到锁就显式报错。
- `scan_report.json` 不存在、为空或无条目时，必须显式报错。
- 必须完整复制文件内容，不做语义改写。
- 必须刷新 `registry.json` 和 `index.md`。
- 必须只处理扫描报告里的条目。
