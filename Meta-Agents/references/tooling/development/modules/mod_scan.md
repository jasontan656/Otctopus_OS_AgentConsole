# mod_scan

- 入口：`scripts/managed_scan.py`
- 职责：扫描 source root 下全部 `AGENTS.md`，生成 `scan_report.json`。
- 不变量：
  - 必须忽略 `Human_Work_Zone/`。
  - 不复制托管副本。
  - 不写 `registry.json` 与 `index.md`。
