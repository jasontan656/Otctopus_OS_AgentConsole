# 技能模板契约 v1

## 目标
使用“模板优先、确定性执行”的契约来创建或规范化技能，保证结构稳定、触发行为可预测，并默认产出“抽象层 + 业务需求层”分域写法。

## 必需文件
- `SKILL.md`
- `agents/openai.yaml`

## 可选但推荐
- `scripts/`
- `references/`
- `assets/`

## Profile 契约
- `basic`
  - 适用于单目标、低阶段复杂度、弱运行态规则的技能。
  - 仍必须采用“抽象层 + 业务需求层”写法。
- `staged_cli_first`
  - 适用于多阶段、多合同、强运行态边界的复杂技能。
  - 业务需求层默认以阶段域承载。
  - 必须把“当前阶段该读什么、该做什么、能看什么”从 CLI 输出。
  - 必须提供 `references/stages/` 或等价的阶段化目录体系。

## SKILL.md 章节契约（1-7）
1. 目标
2. 可用工具
3. 工作流约束
4. 规则约束
5. 方法论约束
6. 内联导航索引
7. 架构契约

## 分层与分域契约
- 所有未来生成技能默认采用两层：
  - 抽象层
  - 业务需求层
- 业务需求层可继续细分为多个域；若是复杂技能，业务需求层默认以阶段域承载。
- `3/4/5/6` 四个章节必须遵循相同组织原则：
  - 先写抽象层
  - 再写各业务域
- 禁止任何可能的混写。
- 即便只有一个业务域，也必须显式独立成域，不得与抽象层混成一个段落。

## 工具与命令契约
- 工具命名：技能内工具统一使用 `Cli_Toolbox.<tool_name>` 命名。
- 工具入口：允许统一脚本入口，例如 `scripts/Cli_Toolbox.py`。
- 抽象功能：允许共享。
- 域命令：必须独立，不得串用。
- 不允许把某个业务域或阶段域的特定命令伪装成通用命令重复复用到其他域。

## 必须/可选规则
- 必须：`1-7` 章节条目完整存在（标题不可缺失）
- 强制填充：`1.目标`、`6.内联导航索引`、`7.架构契约`
- 可选填充：`2.可用工具`、`3.工作流约束`、`4.规则约束`、`5.方法论约束`（不适用时写 `N/A`）
- 标签语义边界：上述“必须/可选”仅用于模板填充规则，不属于生成技能正文标签；生成的 `SKILL.md` 标题不得携带 `（必须）/（可选）` 字样。
- 工具文档同步：每个工具必须同时维护使用文档与开发文档。
- 示例命令契约：工具使用文档中的示例命令必须是“一行可复制”完整命令，且必须以 `cd <skill_root> &&` 开头并包含管道，附最小用途描述。
- 开发文档结构化：复杂 Toolbox 必须采用“入口 + 分类 + 模块”分层文档。
- 若技能存在运行态规则、约束、指引：
  - 必须提供 CLI 输出入口。
  - 必须提供 machine-readable `json/yaml` 合同。
  - 必须提供 markdown 审计版。
  - 必须在 `SKILL.md` 明示：模型禁止直接阅读 markdown 获取运行指引。
  - 更新时必须同步两份，且建议以 machine-readable 合同刷新 markdown。
- 若技能属于 `staged_cli_first`：
  - 必须定义显式阶段顺序或阶段集合。
  - 必须定义 top-level resident docs，且数量应尽量少、固定。
  - 必须定义阶段切换时的 drop/discard 规则。
  - 必须将阶段级规则拆成多个独立文件或独立 CLI 合同，禁止堆成单文件大纲。
  - 阶段合同至少应覆盖：`checklist`、`doc contract`、`command contract`、`graph contract` 中的适用子集。
  - 若某类合同依赖真实项目状态，必须显式标为 dynamic contract，不得伪装成纯静态模板。

## 目录深度与模板簇契约
- 目录层级不仅是组织手段，也是模型的适用域收拢器。
- 当规则、模板、工作流跨多个阶段或角色时，优先加深目录层级，不要继续扩写单文件。
- 复杂技能推荐将内容拆为：
  - 门面入口
  - runtime 合同
  - stages 阶段目录
  - rules/workflow references
  - assets/templates 模板簇
- 模板簇中，人类叙事 markdown 与 machine files 应显式分离，不得混成一个巨型模板。

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
- 若技能存在运行态规则，推荐固定路径：
  - `references/runtime/`
  - `references/stages/`
- 若技能属于 `staged_cli_first`，推荐同时提供：
  - `references/stages/00_STAGE_INDEX.md`
  - `assets/templates/stages/`
  - `assets/templates/stages/STAGE_TEMPLATE/`
- 若技能需要真实项目上下文才能生成某些命令或边界，必须在文档中区分：
  - static authoring contract
  - dynamic runtime contract

## 验收清单
- frontmatter 中存在 `name` 与 `description` 字段。
- `1-7` 章节标题完整存在且可读。
- `1/6/7` 内容必须可执行或可验证。
- `2/3/4/5` 内容可执行/可验证，或明确标注 `N/A`（允许占位，不允许缺失条目）。
- `2.可用工具` 章节必须存在：有工具时需显式声明 `Cli_Toolbox` 命名规则；无工具时写 `N/A`。
- `3/4/5/6` 章节必须采用“抽象层 + 业务需求层”分域写法，不得混写。
- 若技能包含工具，必须存在 `references/tooling/Cli_Toolbox_USAGE.md` 与 `references/tooling/Cli_Toolbox_DEVELOPMENT.md`。
- `Cli_Toolbox_USAGE.md` 必须包含“示例命令（强制）”章节：`cd` 开头、一行可复制、包含管道、附最小用途描述。
- 若 Toolbox 涉及多模块，必须存在开发分类索引与模块目录（`20_CATEGORY_INDEX.md` + `10_MODULE_CATALOG.yaml`）。
- 若技能存在运行态规则，必须存在 CLI 输出入口、machine-readable 合同与 markdown 审计版三者闭环。
- 若技能属于 `staged_cli_first`，必须能明确指出：
  - 阶段顺序或阶段集合
  - resident docs
  - stage switch discard policy
  - stage templates 或 stage references 的固定入口
- 必需文件中不存在未替换占位符（如 `[TODO]`、`<...>`、`TBD`）。
- 接口元数据与技能目标一致。
- 创建或更新的文件以明确路径形式输出。
