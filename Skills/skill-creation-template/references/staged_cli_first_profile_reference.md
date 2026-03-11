# staged_cli_first 复杂技能 profile 提炼参考

来源母本：`3-Octupos-OS-Backend`

## 目标
- 抽取 backend skill 成功的运行结构，作为复杂 staged 技能的通用模板。
- 这里沉淀的是治理形状，不是后端业务内容。

## 从母本中提炼出的稳定结构
- `SKILL.md` 只做门面，不做正文。
- 门面采用固定 façade：
  - `定位`
  - `必读顺序`
  - `分类入口`
  - `适用域`
  - `执行入口`
  - `读取原则`
  - `结构索引`
- 运行态规则优先由 CLI 输出，而不是让模型直接通读 markdown。
- 顶层常驻文档极少且固定。
- 进入阶段前必须先拿到当前阶段 checklist。
- 当前阶段的读物边界、命令边界、graph 角色分别独立暴露。
- 阶段切换时，显式丢弃上一阶段 focus。
- 模板簇分离人类叙事模板与 machine files。
- 工作流变更要有 lint/测试闭环，而不是只改说明文字。

## staged_cli_first 必需治理面
- stage order
- top-level resident docs
- stage checklist
- stage doc contract
- stage command contract
- stage graph contract
- stage-switch discard policy
- runtime contract
- stage template kit

## 泛化后应该保留什么
- 单一主轴驱动的 staged workflow
- entry-only facade
- CLI-first runtime contracts
- 极少 resident docs
- stage-specific narrow reading
- discard policy
- template cluster
- validation closure

## 泛化后必须去掉什么
- 后端专有目录名
- 固定项目路径
- `mother_doc`、`construction_plan`、`acceptance` 等业务命名
- 针对某个项目的 env、graph、acceptance 口径
- 任何依赖单一仓库现实的 hard-coded 语义

## 推荐目录形状
```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── rules/
├── scripts/
│   └── Cli_Toolbox.py
├── references/
│   ├── runtime/
│   ├── stages/
│   └── tooling/
├── assets/
│   └── templates/
│       └── stages/
└── tests/
```

## 推荐阶段合同面
- `stage-checklist`
  - 输出阶段目标、required outputs、resident docs、stage docs、entry actions、exit gate、drop policy。
- `stage-doc-contract`
  - 输出当前阶段允许读取的文档边界。
- `stage-command-contract`
  - 输出当前阶段入口命令、门禁命令、可选命令与必要动作。
- `stage-graph-contract`
  - 输出当前阶段对 graph/context 的角色定义。

## 模板治理建议
- `skill-creation-template` 的 staged profile 至少生成：
  - staged façade `SKILL.md`
  - runtime contract skeleton
  - `references/stages/00_STAGE_INDEX.md`
  - stage system README
  - `CHECKLIST.json`
  - `DOC_CONTRACT.json`
  - `COMMAND_CONTRACT.json`
  - `GRAPH_CONTRACT.json`
- 若 staged skill 存在 companion skill 或外部 control plane，应在门面 `分类入口` 中显式指向，但不要把 companion 规则抄进本技能。

## 作者检查清单
- 这个技能真的需要 staged，而不是 basic 吗？
- 门面是否仍然是 entry-only？
- resident docs 是否少而固定？
- 阶段合同是否分开，而不是混成一个大文档？
- 阶段切换是否写清 discard policy？
- 模板资产是否区分 markdown 与 machine contracts？
- 生成器、tooling 文档和回归检查是否同步？
