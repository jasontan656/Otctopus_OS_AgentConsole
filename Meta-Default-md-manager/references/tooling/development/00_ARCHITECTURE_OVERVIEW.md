# Architecture Overview

- `scan`：source root -> 扫描默认文档集合（忽略排除目录与托管目录）-> 只更新 `scan_report.json`。
- `collect`：scan report -> 完整复制到 `assets/managed_targets/` -> 更新 registry 和 index。
- `push`：registry -> 选择托管副本 -> 回写到原始 `source_path`。
- `registry`：只读查看当前托管映射。

核心边界：
- `scan / collect / push` 通过 `assets/managed_targets/.cli.lock` 串行化。
- `scan` 不写托管副本。
- `collect` 不重新扫描。
- `push` 不绕过 registry。
- `assets/managed_targets/index.md` 是人工快速浏览面。
- 原始文件只在 `push` 阶段被覆盖。
