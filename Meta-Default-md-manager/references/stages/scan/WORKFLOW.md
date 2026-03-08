# Scan Workflow

1. 解析 `source_root`。
2. 扫描全部命中的默认文档目标。
3. 应用排除规则并去重。
4. 生成 `scan_report.json`，写入 `target_kind`、源路径和托管路径。
5. 不写托管副本。
