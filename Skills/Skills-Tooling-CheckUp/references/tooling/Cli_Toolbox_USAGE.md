---
doc_id: "skills_tooling_checkup.tooling.toolbox_usage"
doc_type: "topic_atom"
topic: "Tooling entry contract for a skill that intentionally has no local CLI"
anchors:
  - target: "Cli_Toolbox_DEVELOPMENT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development templates should be maintained together."
  - target: "../governance/SKILL_DOCSTRUCTURE_POLICY.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "Generated tool docs should also respect doc-structure governance."
---

# Cli_Toolbox 使用文档

适用技能：`Skills-Tooling-CheckUp`

## 命名约束
- 本技能当前故意不提供本地 `Cli_Toolbox.py`。
- 因此不存在 `Cli_Toolbox.<tool_name>` 别名集合；若未来新增本地工具，必须先证明无法由目标 skill 既有工具链完成。

## 工具清单
- 无本地工具。
- 实际执行时，只能复用：
  - 目标 skill 已存在的 CLI / scripts / tests / lint 命令
  - repo 已治理的 `*_skills` 环境
  - repo 已存在的治理技能命令

## 叙事式使用说明（固定格式）

### 无本地工具入口
- 人类叙事版输入：
  - “检查某个已安装 skill 的 tooling code 有没有绕开现成依赖在重复造轮子，并在必要时修正。”
- 电脑动作发生了什么：
  - 先读取本技能门面、routing、execution rules 与依赖基线。
  - 若目标技能会落盘日志或产物，再读取本技能的 observability / output governance 原子文档。
  - 再进入目标 skill 自己的门面和 tooling/runtime 文档。
  - 然后使用目标 skill 已有命令完成验证，而不是调用本技能自带命令。
- 人类叙事版输出：
  - 输出“哪里存在可疑重复造轮子、日志与产物落点是否合规、为何成立、做了什么修正、如何验证”。

## 参数与结果（供 AI/工程使用）
- 输入：
  - 目标 skill 路径
  - 目标文件范围
  - repo 当前必用 tech stack 基线
- 输出：
  - 语义级问题判断
  - runtime 日志与产物落点治理判断
  - 是否进入修正
  - 修正后的验证结果
- 失败码约定：
  - 无本地失败码；失败由目标 skill 的既有命令负责返回

## 同步维护要求
- 若未来真的引入本地工具，必须同步更新本文件、`Cli_Toolbox_DEVELOPMENT.md`、模块目录和对应文档。
- 只要本技能继续保持“无本地工具”，就必须显式保留这一事实，避免模型脑补不存在的命令。
