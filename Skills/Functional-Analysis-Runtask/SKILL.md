---
name: Functional-Analysis-Runtask
description: 围绕明确目标意图或目标项目做分析、方案收敛、最小切片施工规划与实施验证证据沉淀的单技能多阶段 workflow。
skill_mode: executable_workflow_skill
metadata:
  doc_structure:
    doc_id: functional_analysis_runtask.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Functional-Analysis-Runtask skill
---

# Functional-Analysis-Runtask

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能不再停留在“只分析目标项目并偏向单份正式输出”的单层门面，而是升级为面向明确目标意图或目标项目的单技能多阶段 workflow。
- 固定主闭环为：`research -> design -> plan -> implementation -> validation`。
- 主入口统一保持为 `analysis_loop`；调用者既可连续执行，也可只进入某一个阶段单独收口。

### 2. 技能约束
- 本技能的真相源优先级为：小型对象 > 阶段合同 > 阶段沉淀文档。
- 旧资产必须继承，不得绕开当前已落盘的两份分析方法论文档另起平行方法论。
- plan 阶段必须收敛为最小切片施工合同，不能退回泛泛计划。
- implementation 阶段一旦发生真实实现、验证、状态裁决或关键判断更新，必须同回合写回证据对象。
- 任何调研报告、撰写计划、施工计划、阶段沉淀文档与类似任务产物，都必须先联动 `Functional-HumenWorkZone-Manager` 解析 `Human_Work_Zone` 受管路径，再允许落盘。
- 技能目录只承载 skill 本体所需的 facade、workflow、scripts、references 与实现资产；不得继续承载任务执行产物。

### 3. 顶层常驻合同
- 先选择功能入口，再沿当前入口下沉，不把阶段正文回填到门面。
- `read-contract-context` 与逐文档阅读等价；`read-path-context` 保持等价别名。
- CLI 至少负责提供：运行时合同、文档链编译、阶段 checklist、workspace scaffold、task runtime scaffold、新任务门禁与 stage-specific lint。
- `workspace-scaffold` 与 `stage-lint` 必须拒绝技能目录内落盘；task artifact root 必须位于 `Human_Work_Zone` 受管根下。

## 2. 功能入口
- [analysis_loop]：`path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md`
  - 作用：进入 `Functional-Analysis-Runtask` 的单技能多阶段主闭环。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry analysis_loop --json`

## 3. 目录结构图
```text
Functional-Analysis-Runtask/
├── SKILL.md
├── agents/
├── path/
│   └── analysis_loop/
└── scripts/
```
