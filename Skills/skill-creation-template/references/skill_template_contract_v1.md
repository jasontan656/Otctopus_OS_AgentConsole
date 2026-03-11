# 技能模板契约 v2

## Contract Header
- `contract_name`: `meta_skill_template_references_skill_template_contract_v2`
- `contract_version`: `2.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

## 目标
使用标准化技能门面结构，创建或改造可长期治理的 Codex 技能。这里约束的是技能运行态骨架，不是一次性写作格式。

## 核心升级
- 不再把模板核心寄托在“抽象层 + 业务层”标题堆叠上。
- 通用门面采用标准 7 段 façade：
  1. `定位`
  2. `必读顺序`
  3. `分类入口`
  4. `适用域`
  5. `执行入口`
  6. `读取原则`
  7. `结构索引`
- 抽象层与业务层仍然存在，但它们应体现在：
  - facade 的读序与分类
  - references/contracts 的拆分
  - profile-specific assets
  - CLI-first runtime surfaces

## 必需文件
- `SKILL.md`
- `agents/openai.yaml`

## 推荐目录
- `scripts/`
- `references/`
- `assets/`
- `tests/`

## Profile 契约
- `basic`
  - 适用于单主轴、低阶段复杂度技能。
  - 仍必须使用 7 段 façade。
  - 默认不强制阶段目录。
  - 若存在运行态规则，必须补齐 runtime contract。
- `staged_cli_first`
  - 适用于多阶段、多合同、强读取边界技能。
  - 必须使用 7 段 façade。
  - 必须显式建模：
    - top-level resident docs
    - stage order
    - stage checklist
    - stage doc contract
    - stage command contract
    - stage graph contract
    - stage-switch discard policy
  - 必须提供 `references/stages/` 或等价阶段目录体系。

## 门面契约
- `SKILL.md` 必须是 entry-only facade。
- 门面只做：
  - 运行定位
  - 必读顺序
  - 入口分类
  - 适用域提示
  - 执行入口
  - 读取原则
  - 结构索引
- 门面不得承担：
  - 长篇规则正文
  - 多阶段细节全集
  - 模板资产逐条解释
  - 重复的 authoring 历史说明

## 运行合同契约
- 若技能存在运行态规则、约束或门禁：
  - 必须提供 CLI 输出入口。
  - 必须提供 machine-readable `json/yaml` 合同。
  - 必须提供 markdown 审计版。
  - 必须在门面中写明：模型不能直接把 markdown 当运行规则源。
- 若规则依赖真实项目状态：
  - 必须显式标记为 dynamic runtime contract。
  - 不能伪装成纯静态模板。

## staged_cli_first 阶段合同契约
- 当前阶段至少应暴露以下合同中的适用子集：
  - `stage-checklist`
  - `stage-doc-contract`
  - `stage-command-contract`
  - `stage-graph-contract`
- 阶段切换后必须显式丢弃上一阶段 focus，仅保留 resident docs。
- 阶段域规则不得混写在单个胖文档中。
- 阶段模板簇必须分离：
  - 人类叙事 markdown
  - machine-readable contracts
  - 脚本入口或统一 CLI 入口

## 工具与文档契约
- 工具命名统一使用 `Cli_Toolbox.<tool_name>`。
- 工具入口允许统一为 `scripts/Cli_Toolbox.py`。
- 工具变更时必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - 受影响模块文档
- 示例命令必须是一行可复制命令。

## 模板簇契约
- `basic` 至少要提供：
  - 门面模板
  - `openai.yaml` 模板
- `staged_cli_first` 至少要提供：
  - staged 门面模板
  - runtime contract 模板
  - stage system 模板
  - stage checklist 模板
  - stage doc/command/graph contract 模板
- 不允许只有一份“大而全”的总模板。

## 回归与治理契约
- 模板升级时必须同时检查：
  - 生成器是否仍能生成 profile 对应目录
  - staged 输出是否包含 stage checklist 与合同四件套
  - tooling 文档是否同步
- 推荐提供最小回归测试覆盖模板生成行为。

## 验收清单
- frontmatter 包含 `name` 与 `description`。
- `SKILL.md` 使用 7 段 façade，标题完整存在。
- `SKILL.md` 为 entry-only，不承载规则正文。
- 若技能存在运行态规则，存在 CLI 输出入口、machine-readable 合同、markdown 审计版三者闭环。
- `basic` 与 `staged_cli_first` 的目录结构与资产深度符合各自 profile，不靠后补丁硬凑。
- `staged_cli_first` 能明确指出：
  - resident docs
  - stage order
  - stage checklist
  - stage doc contract
  - stage command contract
  - stage graph contract
  - stage-switch discard policy
- 模板与脚本变更已同步到 tooling 文档。
- 必需文件不存在未替换占位符。
