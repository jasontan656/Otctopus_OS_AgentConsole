---
name: Workflow-CentralFlow2-OctppusOS
description: 开发闭环 workflow 技能；以 mother_doc、construction_plan、implementation、acceptance 组成复合阶段闭环。
skill_mode: executable_workflow_skill
metadata:
  doc_structure:
    doc_id: workflow_centralflow2_octppusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-CentralFlow2-OctppusOS skill
---

# Workflow-CentralFlow2-OctppusOS

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能负责把开发任务收敛到统一闭环：`mother_doc -> construction_plan -> implementation -> acceptance`。
- 当前技能属于复合 workflow skill；主入口下仍会继续下沉到阶段索引与子工作流。
- 文档链是真源；CLI 负责编译文档链、执行辅助动作与补充动态运行态。

### 2. 技能约束
- `SKILL.md` 只暴露功能入口，不平铺阶段正文、模板树或旧式运行时合同。
- `target_root / docs_root / codebase_root / graph_runtime_root` 属于动态运行态；它们由 CLI 解析，不提前回流到门面。
- `mother_doc` 是当前闭环里最复杂的子 workflow；不能把它压扁成单步说明页。
- 现有 CLI 子命令在治理过程中保持兼容；重构重点是承载方式，不是先删命令。

### 3. 顶层常驻合同
- 进入本技能后，先选功能入口，再沿当前入口继续下沉。
- `read-contract-context` 用于快速编译当前入口的完整上下文；逐文件阅读与 CLI 编译阅读等价。

## 2. 功能入口
- [development_loop]：`path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md`
  - 作用：开发闭环主入口；进入后按主 workflow 继续下沉到各阶段。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry development_loop --json`

## 3. 目录结构图
```text
Workflow-CentralFlow2-OctppusOS/
├── SKILL.md
├── agents/
├── path/
└── scripts/
```
