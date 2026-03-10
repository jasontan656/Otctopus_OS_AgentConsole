# Cli_Toolbox 使用文档

适用技能：`meta-topic-anchor-graph`

## 当前状态
- `v1` 为 reference-first 方法论技能。
- 当前没有 `Cli_Toolbox.py`，也没有任何强制脚本入口。
- 运行入口固定为：
  1. `SKILL.md`
  2. `references/topic-anchor-graph-contract.md`
  3. `assets/templates/*.md`

## 当前使用方式
- 创建新文档树时：
  - 先用 `ROOT_INDEX_TEMPLATE.md` 设计主路径与 child nodes。
  - 再用 `TOPIC_ATOM_TEMPLATE.md` 承载具体原子 topic。
- 改造已有大文档时：
  - 先做 topic 切片。
  - 再决定哪些内容上移为导航、哪些内容下沉为 atom、哪些关系改写成 anchor。

## 未来扩展位
- 若未来新增 `Cli_Toolbox.py`：
  - 工具统一命名为 `Cli_Toolbox.<tool_name>`。
  - 新增工具前先更新本文件。
  - 同回合同步更新 `Cli_Toolbox_DEVELOPMENT.md` 与 `references/tooling/development/*`。
