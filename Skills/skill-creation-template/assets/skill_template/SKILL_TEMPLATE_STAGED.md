---
name: "${skill_name}"
description: ${description}
---

# ${skill_name}

## 1. 技能定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：`[stage_1] -> [stage_2] -> [stage_3] -> [stage_4]`。
- 各阶段的细节规则、读取边界、命令入口与 graph 角色以下沉 contracts 为准，不得只凭本门面自行发挥。
- 固定输出根与运行边界请在 runtime contract 或 stage contracts 中显式声明，不要把真实项目路径硬编码进模板。

## 2. 适用域
- 适用于：[明确该 staged skill 负责的 staged workflow]
- 不适用于：[明确排除域]
- companion skills 只负责其自身能力；本技能只消费其输出，不在门面里重复造规则正文。

## 3. 可用工具简述&入口
- 统一工具入口：
  - `scripts/Cli_Toolbox.py`
- 阶段合同工具：
  - `stage-checklist --stage <stage>`
  - `stage-doc-contract --stage <stage>`
  - `stage-command-contract --stage <stage>`
  - `stage-graph-contract --stage <stage>`
- 顶层合同工具：
  - `runtime-contract --json`
- 其他 profile-specific init/lint/archive/template 命令以 `stage-command-contract` 与 runtime contract 输出为准。

## 4. 文档指引&入口
- 顶层常驻文档：
  - [rules/...]
  - [references/tooling/...]
  - [workspace root AGENTS]
  - [companion repo AGENTS，如适用]
- 运行合同层：
  - `references/runtime/`
- 阶段层：
  - `references/stages/`
- 模板层：
  - `assets/templates/`
- 外部辅助层：
  - [companion skills / control plane / external validators]

## 5. 工作流指引
1. 先读取 `runtime-contract --json`，确认 top-level resident docs 与整体阶段边界。
2. 进入任一阶段前，固定先读 `stage-checklist --stage <stage>`。
3. 当前阶段的读物边界只从 `stage-doc-contract --stage <stage>` 获取。
4. 当前阶段的入口、门禁和动作只从 `stage-command-contract --stage <stage>` 获取。
5. 当前阶段的 graph/context 角色只从 `stage-graph-contract --stage <stage>` 获取。
6. 阶段切换时，显式丢弃上一阶段 checklist、阶段文档与临时 focus，只保留顶层常驻文档。

## 6. 顶层常驻通用规则
- 门面只做阶段入口、适用域提示与顶层规则，不回填阶段正文。
- 顶层常驻文档必须少且固定；阶段细节不得塞回常驻文档。
- 单阶段执行时，只读当前阶段 checklist 与当前阶段直接需要的合同、模板和文档。
- 多阶段连续执行时，阶段切换后必须重新读取当前阶段 checklist，并丢弃上一阶段 focus。
- 若技能存在运行态规则，模型禁止直接阅读 markdown 获取运行指引；必须通过 CLI 读取 machine-readable contracts。
- 模板簇应分离 markdown anchors 与 machine-readable contracts，不要把二者混成一个巨型模板。

## 7. 结构索引
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
