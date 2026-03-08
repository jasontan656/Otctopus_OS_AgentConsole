# Changelog

- v1: 初始版，支持组合式回收与回写，并引入 `assets/managed_targets/registry.json`。
- v2: 回收阶段同步维护 `assets/managed_targets/index.md`，提供路径与职责预览。
- v3: 重构为显式三阶段 `scan / collect / push`，并增加阶段隔离文档。
- v4: 为三阶段加入技能内互斥锁，并对被消费文件缺失/空内容做显式报错。
- v5: 升级为 `Meta-Default-md-manager`，默认纳管 `AGENTS.md`、`.gitignore`、后端 `README.md` 与 `Deployment_Guide.md`。
