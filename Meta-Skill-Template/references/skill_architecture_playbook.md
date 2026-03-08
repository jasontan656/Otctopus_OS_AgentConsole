# 技能架构手册

## 设计目标
构建便于模型路由、执行与验证的技能，同时避免加载不必要上下文。

## Profile 选择
- `basic`
  - 单目标技能。
  - 规则边界较少。
  - 不需要阶段化 contract。
- `staged_cli_first`
  - 多阶段技能。
  - 当前阶段的运行时指引、门禁与可读域需要强控制。
  - 适合复杂流程、强治理、强模板依赖的技能。

## 推荐模式
- 轻量 `SKILL.md`：仅保留路由、契约、流程。
- 深度细节按需放在 `references/`。
- 确定性动作放在 `scripts/`。
- 描述结构统一为 1-7 章节且条目必须完整存在；`1/6/7` 必须填充，`2/3/4/5` 可按任务复杂度选择填充，若不适用写 `N/A`（不可删节）。
- “必须/可选”语义仅用于模板填充阶段，不应出现在生成技能的章节标题中。
- 工具统一采用 `Cli_Toolbox.<tool_name>` 命名，避免跨技能命名漂移。
- 每个工具同步维护“使用文档 + 开发文档”，避免只改代码导致知识断层。
- 开发文档应按“入口索引 + 分类索引 + 模块目录 + 模块文档”组织，避免单文件持续膨胀。
- 若技能存在运行态规则、约束、指引，优先采用 CLI-first 模式：
  - machine-readable 合同作为运行时真实规则源
  - markdown 作为审计镜像
  - 模型通过 CLI 获取指引，不直接读 markdown

## staged_cli_first 复杂技能模式
- 把 `SKILL.md` 当门面，不当规则正文。
- 将常驻文档限制在极少、固定的一组入口，避免阶段切换时上下文漂移。
- 将每个阶段的运行信息至少拆成：
  - checklist
  - doc contract
  - command contract
  - graph contract
- 阶段切换时显式丢弃上一阶段 focus，只保留 resident docs。
- 模板不能只是一份 `SKILL_TEMPLATE.md`；复杂技能需要模板簇。
- 模板簇应分离：
  - 人类阅读 markdown anchors
  - machine-readable json/yaml contracts
  - 脚本入口
- 目录深度越深，单个文档的适用域越窄，模型越容易遵守边界。

## static / dynamic contract 区分
- static authoring contract
  - 与具体项目状态无关。
  - 可直接从模板或 skill 自身输出。
- dynamic runtime contract
  - 依赖真实项目路径、现有产物、当前运行态。
  - 允许由 CLI 计算后输出。
  - 必须在文档中显式声明其前置条件，避免在空环境下误判为脚本损坏。

## 反模式
- 巨型单体 SKILL 文档，混入多个无关目标。
- 触发描述过宽，导致路由失真。
- 没有完成标准或校验门禁。
- 一个技能里塞入多个独立目标。
- 把“创建技能本身”写进被创建技能的 `1.目标` 章节，导致运行态目标漂移。
- 让模型直接读取 markdown 作为运行规则源，却没有 machine-readable 合同与 CLI 输出入口。
- 让复杂技能只靠单层 references 承载全部阶段规则。
- 把 markdown anchors 和 machine files 混写为一个万能模板。

## 规范化步骤
1. 识别技能唯一主决策目标。
2. 先判定使用 `basic` 还是 `staged_cli_first` profile。
3. 将非路由细节从 SKILL 下沉到 references。
4. 为重复初始化或检查动作补充脚本锚点。
5. 若为复杂技能，建立阶段目录与阶段合同出口。
6. 增加最小验收清单。
7. 保持输出契约显式且可测试。
8. 若存在运行态规则，补齐 machine-readable 合同、markdown 审计版与 CLI 输出入口。
