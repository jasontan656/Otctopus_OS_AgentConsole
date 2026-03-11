---
name: "${skill_name}"
description: ${description}
---

# ${skill_name}

## 1. 技能定位
- 本文件只做门面入口，不承载规则正文。
- [写明该技能在运行态的唯一主轴；禁止写“创建本技能/生成模板”之类 authoring 目标。]
- [若该技能本身也是模板或治理技能，明确“本结构即为模板 / 门面基线”。]
- [若技能存在运行态规则，写明运行指引由 CLI 输出的 machine-readable contract 决定。]

## 2. 适用域
- 适用于：[明确此技能负责的任务类型]
- 不适用于：[明确排除域]
- [若依赖外部 companion skill，只写职责边界，不复制对方规则。]

## 3. 可用工具简述&入口
- 统一工具入口：
  - [scripts/Cli_Toolbox.py 或其他统一入口]
- 核心工具：
  - [Cli_Toolbox.<tool_name> -> 用途 -> 命令]
- 合同/门禁工具：
  - [runtime contract / lint / gate command]
- [若没有工具，明确写“本技能无专属 CLI tool，入口即门面与固定文档”。]

## 4. 文档指引&入口
- 规则层：
  - [rules/...]
- 工作流/合同层：
  - [references/...]
- 模板或资产层：
  - [assets/...]
- 运行边界层：
  - [root AGENTS / companion AGENTS / 外部控制平面]

## 5. 工作流指引
1. [先读取本技能的 runtime contract 或统一入口命令。]
2. [若无 runtime contract，列出固定文档读取顺序。]
3. [列出进入具体执行前必须拿到的 checklist、合同或门禁命令。]
4. [列出主执行步骤与收口条件。]
5. [若存在多域流程，写明切换时要丢弃哪些 focus。]

## 6. 顶层常驻通用规则
- 门面只做路由，规则正文下沉到 `references/`、contracts 与脚本。
- 当前 7 章结构本身就是门面合同，不要在其他地方再复制一份平行门面说明。
- 需要什么读什么，不要把所有引用文档一次性展开成新的门面正文。
- 若存在运行态规则，模型禁止直接把 markdown 当运行规则源；必须通过 CLI 读取 machine-readable contract。
- 单域技能也要保持窄域读取，不要把无关 sibling 文档带入运行 focus。
- 若治理规则变化，同步更新门面、contracts、assets、scripts 与 tooling 文档。

## 7. 结构索引
```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
├── assets/
└── tests/
```
