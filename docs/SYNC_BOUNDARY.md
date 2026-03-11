# 同步边界

## 核心原则

章鱼 OS 仓库现在同时包含：

- 技能内核
- 产品门面
- 产品工具

其中只有技能内核允许同步到 `~/.codex/skills`。

## 允许进入 codex 安装目录的对象

- 顶层包含 `SKILL.md` 的技能目录
- `.system/` 系统技能根

## 不允许进入 codex 安装目录的对象

- `README.md`
- `docs/`
- `product_tools/`
- `.git/`
- `.tooling_runtime/`
- 任意产品化说明、安装说明、品牌文案和发布辅助资产

## 当前同步策略

`skill-mirror-to-codex` 的 `scope=all` 已收敛为：

1. 扫描仓库顶层
2. 仅发现真正可同步的技能根
3. 对每个技能根分别执行 `rsync`
4. 不再把整个 repo 根目录直接镜像进 `~/.codex/skills`

## 设计收益

- 产品层可以自由演进
- codex 安装目录只保留技能执行面
- 提交历史可以承载产品迭代说明，不会污染技能安装目录
