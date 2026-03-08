# 技能模板契约 v1

## 目标
使用“模板优先、确定性执行”的契约来创建或规范化技能，保证结构稳定、触发行为可预测。

## 必需文件
- `SKILL.md`
- `agents/openai.yaml`

## 可选但推荐
- `scripts/`
- `references/`
- `assets/`

## SKILL.md 章节契约（1-7）
1. 目标
2. 可用工具
3. 工作流约束
4. 规则约束
5. 方法论约束
6. 内联导航索引
7. 架构契约

## 必须/可选规则
- 必须：`1-7` 章节条目完整存在（标题不可缺失）
- 强制填充：`1.目标`、`6.内联导航索引`、`7.架构契约`
- 可选填充：`2.可用工具`、`3.工作流约束`、`4.规则约束`、`5.方法论约束`（不适用时写 `N/A`）
- 标签语义边界：上述“必须/可选”仅用于模板填充规则，不属于生成技能正文标签；生成的 `SKILL.md` 标题不得携带 `（必须）/（可选）` 字样。
- 工具命名：技能内工具统一使用 `Cli_Toolbox.<tool_name>` 命名。
- 工具文档同步：每个工具必须同时维护使用文档与开发文档。
- 示例命令契约：工具使用文档中的示例命令必须是“一行可复制”完整命令，且必须以 `cd <skill_root> &&` 开头并包含管道，附最小用途描述。
- 开发文档结构化：复杂 Toolbox 必须采用“入口 + 分类 + 模块”分层文档。

## 约束护栏
- 每个技能只能有一个主决策目标，且该目标必须是技能运行态目标，不得写入“创建技能/改写模板”等建模流程目标。
- SKILL 主体应保持精简并面向路由。
- 避免将长篇参考资料直接嵌入 SKILL。
- 对重复初始化动作使用确定性脚本。
- references 与 SKILL 保持一跳可达。
- 工具文档推荐固定路径：`references/tooling/Cli_Toolbox_USAGE.md` 与 `references/tooling/Cli_Toolbox_DEVELOPMENT.md`。
- 复杂 Toolbox 推荐固定路径：
  - `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - `references/tooling/development/modules/`

## 验收清单
- frontmatter 中存在 `name` 与 `description` 字段。
- `1-7` 章节标题完整存在且可读。
- `1/6/7` 内容必须可执行或可验证。
- `2/3/4/5` 内容可执行/可验证，或明确标注 `N/A`（允许占位，不允许缺失条目）。
- `2.可用工具` 章节必须存在：有工具时需显式声明 `Cli_Toolbox` 命名规则；无工具时写 `N/A`。
- 若技能包含工具，必须存在 `references/tooling/Cli_Toolbox_USAGE.md` 与 `references/tooling/Cli_Toolbox_DEVELOPMENT.md`。
- `Cli_Toolbox_USAGE.md` 必须包含“示例命令（强制）”章节：`cd` 开头、一行可复制、包含管道、附最小用途描述。
- 若 Toolbox 涉及多模块，必须存在开发分类索引与模块目录（`20_CATEGORY_INDEX.md` + `10_MODULE_CATALOG.yaml`）。
- 必需文件中不存在未替换占位符（如 `[TODO]`、`<...>`、`TBD`）。
- 接口元数据与技能目标一致。
- 创建或更新的文件以明确路径形式输出。
