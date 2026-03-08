# Architecture Overview

- `scan-collect`：source root -> 扫描 `AGENTS.md`（忽略 `Human_Work_Zone/` 与托管目录）-> 完整复制到 `assets/managed_agents/` -> 更新 registry 和 index。
- `sync-out`：registry -> 选择托管副本 -> 回写到原始 `source_path`。
- `registry`：只读查看当前托管映射。

核心边界：
- 托管副本目录是唯一集中管理面。
- `assets/managed_agents/index.md` 是人工快速浏览面。
- 原始文件只在 `sync-out` 阶段被覆盖。
