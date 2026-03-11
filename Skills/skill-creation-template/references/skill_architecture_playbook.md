# 技能架构手册

## 设计目标
- 让未来技能从第一版开始就拥有可路由、可执行、可治理的稳定骨架。
- 将已验证的技能治理结构抽象为通用模板，而不是把来源技能的领域语义打包复制。
- 让 `SKILL.md` 回到门面职责，把运行细节下沉到 contracts、references、assets 和脚本。

## 设计来源
- 模板吸收的是可复用的治理形状，而不是来源技能的项目语义。
- 被证明有效的是这些结构特征：
  - 轻量门面
  - 明确读序
  - 极少 resident docs
  - CLI-first 阶段合同
  - 阶段切换丢弃策略
  - 模板簇与 lint/测试闭环

## 统一门面模式
- 默认门面采用固定 7 章结构：
  1. `技能定位`
  2. `适用域`
  3. `可用工具简述&入口`
  4. `文档指引&入口`
  5. `工作流指引`
  6. `顶层常驻通用规则`
  7. `结构索引`
- 这 7 章的职责是路由，不是正文。
- 模板门面的信息分配应稳定：
  - 技能定位负责定义主轴与模板身份
  - 工具入口与文档入口分开陈述
  - 工作流只写顺序，不回填规则正文
  - 顶层常驻通用规则负责 entry-only 与 CLI-first 之类硬约束

## Profile 选择
- `basic`
  - 单主轴技能。
  - 无需阶段合同或只存在极少运行态规则。
  - 可选 runtime contract，但若有运行规则就必须补齐。
- `staged_cli_first`
  - 多阶段、多门禁、强窄域读取技能。
  - 当前阶段该读什么、能做什么、能看什么必须由 CLI 合同给出。
  - 适合复杂流程、强治理、模板簇依赖重的技能。

## staged_cli_first 设计骨架
- `SKILL.md` 只做门面。
- top-level resident docs 必须极少且固定。
- 每个阶段至少要有：
  - checklist
  - doc contract
  - command contract
  - graph contract
- 阶段切换时显式丢弃上一阶段 focus。
- 阶段模板簇必须分离：
  - markdown anchors
  - machine-readable contracts
  - 统一 CLI 入口

## static / dynamic contract 区分
- static authoring contract
  - 与真实项目状态无关。
  - 适合作为模板资产与固定规则。
- dynamic runtime contract
  - 依赖真实项目路径、已有产物或运行态。
  - 只能由 CLI 计算输出。
  - 必须声明前置条件和失败口径。

## 模板作者方法论
1. 先识别技能唯一主轴，而不是先套文件树。
2. 决定它是 `basic` 还是 `staged_cli_first`。
3. 先写门面，再下沉细节到 contracts/references/assets。
4. 若需要运行态规则，优先设计 machine-readable contract，再补审计版 markdown。
5. 若为 staged skill，先定义 resident docs、stage order 和 discard policy，再写阶段模板。
6. 模板升级时优先整体重构，不做 patch stacking。

## 反模式
- 继续使用“大而全 SKILL.md”承载所有规则。
- 把来源技能的项目路径、项目术语或验收口径直接复制进模板。
- 把 `basic` 生成为半成品，再靠大量手改补成 staged。
- 只有 markdown，没有 machine-readable contracts。
- 阶段切换没有 discard policy，导致上一阶段上下文残留。
- 模板改了但生成器、tooling 文档、测试没更新。

## 规范化步骤
1. 识别技能主轴与 profile。
2. 用 7 章门面结构搭门面。
3. 决定需要哪些 contracts。
4. 决定需要哪些模板资产。
5. 用 `create-skill-from-template` 生成骨架。
6. 回填真实语义，去掉占位符。
7. 运行最小回归，确认生成骨架与 contracts 没漂移。
