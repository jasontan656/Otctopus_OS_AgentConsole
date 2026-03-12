# 当前 console 产品意图

## 当前产品身份
- 产品品牌：`Octopus OS`
- 当前工程仓名称：`octopus-os-agent-console`
- 当前 console 根目录：`Skills/`
- 当前维护对象：`将 Skills 目录持续维护为 console 产品形态`

## 当前核心判断
- `Skills/` 目录不应继续被当成零散 skill 堆放区，而应被维护成具有明确边界、命名、注册与运行面规则的 console 产品源面。
- `octopus-os-agent-console` 同时承担：
  - console 产品门面
  - skills mirror authoring source
  - skill governance runtime entry
- 技能依然必须先在本仓演进，再通过受管同步流向 `~/.codex/skills`。
- codex 安装目录是部署面，不是 console 产品化的直接编辑面。
- console 产品化不仅是 UI 或 README 问题，还包括：
  - skill 命名与 registry
  - runtime contract
  - tooling 入口
  - 文档边界
  - mirror / install / Git 留痕流程
- 技能管理面必须服务“把 skill 目录当作 console 产品的一部分来运营”，而不是只维护孤立脚本。
- 当 console 产品化决策触及 root file 受管文件时，文件正文必须通过 `$Meta-RootFile-Manager` 的受管流程维护，而不是在当前技能上下文直接编辑。
- active console continuity log 必须写入 `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form/ITERATION_LOG.md`，而不是继续写回 skill 根目录。
- 未来若本技能新增文件型结果或定向产物，也必须以 `/home/jasontan656/AI_Projects/Codex_Skills_Result/skill-production-form` 为默认结果根。

## 当前目录边界判断
- `Skills/` 下的 skill 根应保持可注册、可同步、可验证。
- 产品门面、产品文档、产品工具不能进入 codex 安装目录污染技能执行面。
- root file 受管文件属于独立治理链；本技能可以声明这些文件为何重要，但不得绕过 `$Meta-RootFile-Manager` 直接维护它们的外部真源正文。
- 技能命名必须能同时解释：
  - canonical 安装名
  - 展示层名字
  - family / prefix 归属
  - 自然语言调用语义
- 当目录、命名、family 或 console 职责变化时，必须同步修改 runtime contract、tooling docs、tests 与 registry。

## 当前施工目标
- 将 `production-form` 收敛为围绕 console 产品化语义的 `Skill-Production-Form / skill-production-form`。
- 用稳定的本地历史记录 console 产品化判断，而不是让这些判断散落在 unrelated skills 或临时聊天里。
- 让 AI 在推进 skill 管理时，先理解当前 console 产品目标、最近决策和已收敛边界。
- 保持 `Skills/` 目录在结构、命名、同步和运行面上的整齐一致。

## 当前语言边界
- 对外产品 `README.md` 与 `docs/`：英文
- 面向终端用户的 wizard / TUI：中英双语
- 内部 skill 内核、治理合同、内部开发记录：允许中文为主
- GitHub 上的产品迭代 commit subject 与迭代日志：优先英文

## 当前阶段性策略
- 在 console 产品形态继续收敛期间，关键设计历史先写入本地 markdown。
- 这个阶段的本地设计日志，是为了让 AI 持续读取“console 目录为什么现在长这样”的上下文。
- 一旦 console 产品形态足够稳定，主叙事可以逐步切回 GitHub，但本技能仍保留为 console 产品化 continuity layer。
