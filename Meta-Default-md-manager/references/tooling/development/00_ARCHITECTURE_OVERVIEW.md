# Architecture Overview

- `contract`：读取 `references/runtime/SKILL_RUNTIME_CONTRACT.json`，输出技能级 machine-readable 合同。
- `directive`：读取 `references/stages/<stage>/DIRECTIVE.json`，输出阶段级 machine-readable 指引。
- `render-audit-docs`：根据 machine-readable 合同重建 markdown 审计文档。
- `scan`：source root -> 扫描默认文档集合（忽略排除目录与托管目录）-> 只更新 `scan_report.json`。
- `collect`：scan report -> 完整复制到 `assets/managed_targets/` -> 更新 registry 和 index。
- `push`：registry -> 选择托管副本 -> 回写到原始 `source_path`。
- `registry`：只读查看当前托管映射。

核心边界：
- 运行态模型必须先走 `contract/directive`，禁止直接把 markdown 当规则源。
- markdown 文档只做审计镜像，来源是 machine-readable JSON。
- `scan / collect / push` 通过 `assets/managed_targets/.cli.lock` 串行化。
- `scan` 不写托管副本。
- `collect` 不重新扫描。
- `push` 不绕过 registry。
- `assets/managed_targets/index.md` 是人工快速浏览面。
- 原始文件只在 `push` 阶段被覆盖。
