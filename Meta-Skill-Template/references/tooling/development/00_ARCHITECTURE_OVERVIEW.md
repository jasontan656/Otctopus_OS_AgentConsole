# Cli_Toolbox 开发文档架构总览

## 目标
- 支撑复杂 Toolbox 的开发文档扩展，不依赖单一文档承载全部信息。
- 通过“入口 + 分类 + 模块”结构降低认知负担与维护成本。
- 保证 `SKILL.md` 维持纯入口式，而不是继续堆积治理细节。

## 分层结构
0. 技能入口层：`SKILL.md`
1. 工具入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：
   - `references/tooling/development/10_MODULE_CATALOG.yaml`
   - `references/tooling/development/20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`references/tooling/development/90_CHANGELOG.md`

## 维护原则
- 先更新模块目录，再更新模块文档，再更新入口索引。
- 每次工具改动至少触达一个模块文档或模块目录字段。
- 入口文档只做导航与规则，不承载大量实现细节。
- 若模板规则影响运行态合同模式，必须同步更新：
  - 技能模板合同
  - 技能架构手册
  - `SKILL_TEMPLATE.md`
  - 使用文档中的模板行为描述
