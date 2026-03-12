---
name: "SkillsManager-Tooling-CheckUp"
description: "治理已安装 skills 内部工具代码是否绕开 repo 既定依赖栈，并通过语义审查覆盖日志落盘、产物落点与迁移责任的技能。"
metadata:
  doc_structure:
    doc_id: "SkillsManager-Tooling-CheckUp.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the skills tooling checkup skill"
    anchors:
      - target: "references/routing/TASK_ROUTING.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The human facade still keeps a routing mirror for audit readability."
      - target: "references/governance/SKILL_DOCSTRUCTURE_POLICY.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Doc-structure policy remains a mandatory governance branch."
---

# SkillsManager-Tooling-CheckUp

## 1. 工具入口
- 本技能提供本地 CLI：
  - `contract`
  - `directive`
  - `govern-target`
- 运行时统一入口：
  - `python3 scripts/Cli_Toolbox.py contract --json`
  - `python3 scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `python3 scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
- 模型读取合同、workflow、instruction、guide 时必须走 CLI JSON；human markdown 只作为人类叙事镜像。

## 2. 适用域
- 适用于：已安装或已镜像 skill 内部的 Python / TypeScript / Vue tooling code、文档解析代码、schema 校验代码、CLI glue code、lint/test/helper code 的轮子重复实现检查与修正。
- 适用于：根据 repo 当前 `skills_required_techstacks` 基线，判断某段自实现逻辑是否应该优先替换为现有依赖能力。
- 适用于：通过代码语义检查目标技能的日志可观测性落盘、默认产物落盘、定向产物落点约束、相关文档声明与历史落盘迁移责任。
- 不适用于：新增 repo 依赖、发明新的治理工具、替代目标 skill 的 domain 规则源、在证据不足时臆断“所有自写代码都应该被库替换”。
- 若修正落在 Python 代码，仍要遵守 `Dev-PythonCode-Constitution-Backend`；若修正落在 Vue3 / TypeScript tooling code，仍要遵守目标前端 skill 的既有合同。

## 3. 必读顺序
1. 先执行 `python3 scripts/Cli_Toolbox.py contract --json`。
2. 按任务意图选择 directive：
   - 只读检查：`--topic read-audit`
   - 进入修正：`--topic remediation`
   - 日志/产物治理：`--topic output-governance`
   - 依赖基线判断：`--topic techstack-baseline`
   - 本技能工具面：`--topic tooling-entry`
   - 目标技能形态治理：`--topic target-shape-governance`
3. 真正进入目标 skill 前，再按目标 skill 自己的 CLI-first/runtime contract 入口补齐其局部合同。
4. 只有当 CLI JSON 仍留下真实语义缺口时，才打开 human markdown mirror 或 legacy reference docs。

## 4. 运行时资产治理模型
- 所有面向模型运行时的 contract/workflow/instruction/guide 资产，必须同时存在：
  - `*_human.md`
  - 同名 `.json`
- `*_human.md` 必须使用：
  - `<part_A> ... </part_A>` 作为人类叙事层
  - `<part_B> ... </part_B>` 作为 JSON payload 镜像层
- CLI 输出必须直接返回 payload 本体，而不是仅返回“去读哪个文件”的路径元数据。

## 5. 维护入口
- 门面不再把模型主入口路由为 markdown 文件链。
- 若任务目标是治理某个具体 skill 的运行时形态，必须优先使用 `govern-target --target-skill-root <path> --json` 获取目标感知审计结果。
- 真正的改写、测试与 lint 仍通过目标 skill 已有命令完成，而不是把本技能扩张成目标 skill 的替代执行器。
- 若任务涉及 Python 代码修改，回合末必须对具体 Python 目标范围执行 `Dev-PythonCode-Constitution-Backend` lint。

## 6. 参考入口
- Runtime 合同：`references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
- Directive 索引：`references/runtime_contracts/DIRECTIVE_INDEX.json`
- Human mirrors：`references/runtime_contracts/*_human.md`
- Legacy reference docs：`references/routing/`、`references/governance/`、`references/tooling/`

## 7. 约束
- `SkillsManager-Doc-Structure` 仍是创建与治理本技能时必须应用的显式规则。
- 本技能判断“是否自造轮子”时必须基于语义与依赖能力边界，而不是只凭函数名或文件名做机械替换。
- 若某段实现是否可被既有依赖替换仍然未知，应保持未知，不进行脑补式整改。
- 新增任何 runtime-facing contract/workflow/instruction/guide 时，必须继续遵守 `*_human.md + same-name .json` 双文件形态。

## 8. 结构索引
```text
SkillsManager-Tooling-CheckUp/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── Cli_Toolbox.py
├── references/
│   ├── runtime_contracts/
│   ├── governance/
│   ├── routing/
│   └── tooling/
├── assets/
└── tests/
```
