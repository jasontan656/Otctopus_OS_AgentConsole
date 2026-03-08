# mod_collect

- 入口：`scripts/managed_collect.py`
- 职责：读取 `scan_report.json`，并完整复制到技能托管目录。
- 不变量：
  - 不重新扫描文件系统。
  - 不改写源文档内容。
  - 必须同步刷新 `assets/managed_targets/index.md`。
