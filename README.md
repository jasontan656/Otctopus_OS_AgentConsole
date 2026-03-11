# 章鱼 OS

章鱼 OS 是一个自然语言驱动的多 Agent 控制台。

这个仓库是章鱼 OS 的产品化基座。它同时承担两类职责：

- 对外：作为未来可开源的产品仓，承载定位、安装模型、工作区镜像与产品迭代说明。
- 对内：继续作为 `codex` 技能体系的唯一迭代源，并保留把技能推送到 `~/.codex/skills` 的能力。

当前状态：

- 仍处于高速迭代中的 Alpha 阶段。
- 适合学习、测试、试用，不建议直接用于关键生产流程。
- 产品门面已经开始收敛，但内部技能内核仍然保持原有的 codex 技能组织方式。

## 仓库心智模型

不要把这里理解成普通的 skill mirror。

更准确的理解是：

- 技能目录：章鱼 OS 的能力内核
- `skill-mirror-to-codex`：把内核推送进 `~/.codex/skills` 的内部桥接器
- `docs/`、`product_tools/`：产品层，不应被同步进 codex 安装目录
- 提交历史：产品迭代与设计思路的外置日志

## 关键边界

- 产品层文件可以持续增长，但不能污染 `~/.codex/skills`
- 技能层仍然必须可被 `skill-mirror-to-codex` 单独或批量推送
- 一键安装与一键清理必须基于 manifest，而不是猜测性删除

## 入口文档

- `docs/PRODUCT_IDENTITY.md`
- `docs/SYNC_BOUNDARY.md`
- `docs/INSTALL_AND_CLEANUP_MODEL.md`
- `docs/PRODUCT_ITERATION_LOGGING.md`

## 当前目录过渡说明

产品工程名已经收敛为 `octopus-os-agent-console`，但为了兼容既有 runtime、合同和脚本路径，当前仓库仍保留 `Codex_Skills_Mirror` 兼容入口。

这是一层过渡兼容，而不是继续把仓库定义为“镜像产品”。
