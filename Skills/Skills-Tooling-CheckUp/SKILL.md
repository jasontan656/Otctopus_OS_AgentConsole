---
name: "Skills-Tooling-CheckUp"
description: "治理已安装 skills 内部工具代码是否绕开 repo 既定依赖栈并通过语义审查推动修正的技能。"
metadata:
  doc_structure:
    doc_id: "Skills-Tooling-CheckUp.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the skills tooling checkup skill"
    anchors:
      - target: "references/routing/TASK_ROUTING.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The facade must route readers into the first task branch."
      - target: "references/governance/SKILL_DOCSTRUCTURE_POLICY.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Doc-structure policy is a mandatory governance branch."
---

# Skills-Tooling-CheckUp

## 1. 技能定位
- 本文件只做门面入口，不承载深规则正文。
- 本技能唯一主轴是：检查当前已安装或已镜像的 skills 内部工具代码，识别哪些实现绕开了 repo 已声明的必用依赖栈而重复自造轮子，并推动代码修正。
- 本技能不提供本地 `Cli_Toolbox.py`、不提供独立运行时合同；它依赖语义阅读、目标 skill 现有工具链，以及 repo 已治理的依赖基线来完成判断与修正。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`。
2. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
3. 再读取 `references/governance/SKILL_EXECUTION_RULES.md`。
4. 若任务需要确认 repo 已声明的必用依赖栈，再读取 `references/governance/MANDATORY_TECHSTACK_BASELINE.md`。
5. 若任务需要真正改写目标 skill 内部 tooling code，再读取 `references/governance/TOOLING_REMEDIATION_PROTOCOL.md`。
6. 真正进入目标 skill 之前，再按目标 skill 自己的 `SKILL.md -> routing -> execution/tooling docs` 顺序补齐其局部合同。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
  - `references/governance/MANDATORY_TECHSTACK_BASELINE.md`
  - `references/governance/TOOLING_REMEDIATION_PROTOCOL.md`
  - `references/governance/COMMON_REDUNDANT_WHEEL_PATTERNS.md`
  - `references/governance/REMEDIATION_GATES.md`
- 工具层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：已安装或已镜像 skill 内部的 Python / TypeScript / Vue tooling code、文档解析代码、schema 校验代码、CLI glue code、lint/test/helper code 的轮子重复实现检查与修正。
- 适用于：根据 repo 当前 `skills_required_techstacks` 基线，判断某段自实现逻辑是否应该优先替换为现有依赖能力。
- 不适用于：新增 repo 依赖、发明新的治理工具、替代目标 skill 的 domain 规则源、在证据不足时臆断“所有自写代码都应该被库替换”。
- 若修正落在 Python 代码，仍要遵守 `Dev-PythonCode-Constitution-Backend`；若修正落在 Vue3 / TypeScript tooling code，仍要遵守目标前端 skill 的既有合同。

## 5. 执行入口
- 本技能无本地 CLI 入口；执行入口固定为：
  - `SKILL.md -> references/routing/TASK_ROUTING.md -> references/governance/*`
- 真正的改写、测试与 lint 必须通过目标 skill 已有命令完成，而不是为本技能再造一套工具。
- 若任务涉及 Python 代码修改，回合末必须对具体 Python 目标范围执行 `Dev-PythonCode-Constitution-Backend` lint。

## 6. 读取原则
- 门面只负责路由，不重新长回规则正文。
- `skill-doc-structure` 是创建与治理本技能时必须应用的显式规则。
- 若某条规则只属于单一 topic，应下沉到原子文档；不要继续堆在门面里。
- 本技能判断“是否自造轮子”时必须基于语义与依赖能力边界，而不是只凭函数名或文件名做机械替换。
- 若某段实现是否可被既有依赖替换仍然未知，应保持未知，不进行脑补式整改。

## 7. 结构索引
```text
Skills-Tooling-CheckUp/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── governance/
│   ├── routing/
│   └── tooling/
├── assets/
└── tests/
```
