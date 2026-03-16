---
name: SkillsManager-GovTargetSkill
description: 接收一个目标技能并依托 Functional-Analysis-Runtask 完成轻量 analysis_loop 治理闭环，用于把目标技能收敛到稳定 profile、结构、tooling 与验证状态。
metadata:
  skill_profile:
    doc_topology: workflow_path
    tooling_surface: none
    workflow_control: compiled
  doc_structure:
    doc_id: skillsmanager_govtargetskill.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-GovTargetSkill skill
    anchors:
    - target: ./path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: The facade routes execution into the only analysis_loop workflow.
---

# SkillsManager-GovTargetSkill

## Runtime Entry
- Primary runtime entry: `path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md`
- Routing note: `references/routing/TASK_ROUTING.md`
- 本技能是轻量 prompt workflow skill，不提供独立 CLI；运行时入口就是文档链本身。

## 1. 技能定位
### 1. 总览
- 本技能是一个轻量 workflow prompt skill。
- 本技能不自带重型模板机、独立治理壳或自有 CLI；它只负责把“治理某个目标技能”的任务收敛到一个固定闭环。
- 主执行闭环依托 `Functional-Analysis-Runtask` 的 `analysis_loop`，阶段顺序固定为：
  - `research_baseline`
  - `architecture_convergence`
  - `plan`
  - `implementation`
  - `validation`

### 2. 核心职责边界
- 本技能负责：
  - 接收一个明确的治理目标技能
  - 组织治理闭环的读序、阶段边界与阶段产物
  - 强制把下游治理技能作为约束源显式纳入
- 本技能不负责：
  - 替代 `Functional-Analysis-Runtask` 成为新的主方法论
  - 自己承载一套独立的 Python tooling 或 contract runtime
  - 在没有目标技能的情况下做泛化技能理论讨论

### 3. 触发方式
- 当用户要“治理一个已有技能”“把一个技能收敛到更标准的工程形态”“对某个技能做完整规范化闭环改造”时触发本技能。
- 输入里应至少出现：
  - 目标技能名或目标技能路径
  - 当前希望治理的问题或改造目标
- 典型触发句式：
  - `用 SkillsManager-GovTargetSkill 治理 <TargetSkill>`
  - `让 SkillsManager-GovTargetSkill 对 <TargetSkill> 跑完整 analysis_loop`
  - `把 <TargetSkill> 收敛成稳定 profile，并按治理链完成调研、实施与验证`

### 4. 下游治理链
- `Functional-Analysis-Runtask`：主执行闭环与阶段节奏真源。
- `SkillsManager-Creation-Template`：判断目标技能应收敛成什么 profile 与骨架形态。
- `Dev-ProjectStructure-Constitution`：约束项目级结构、目录定位、上下游归属与对象落点。
- `SkillsManager-Tooling-CheckUp`：当目标技能含 CLI、runtime contract 或 tooling surface 时，执行 contract-first 审计与整改门禁。
- `Dev-PythonCode-Constitution`：当目标技能涉及 Python 脚本或 CLI 时，约束代码拆分、lint、pytest、runtime safety 与 tooling 文档同步。
- `Meta-keyword-first-edit`：约束真实治理动作遵循 `删掉重写 > keyword first 替换 > 新增`，避免留下 patch 痕迹。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`，确认这个技能只服务“治理单个目标技能”的 analysis_loop 场景。
2. 再进入 `path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md`。
3. 进入闭环后，固定按 `contract -> workflow_index -> stages -> global_validation` 下沉。
4. 真正执行阶段动作时，把 `Functional-Analysis-Runtask` 作为主闭环，并按当前阶段显式启用相关治理技能。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- workflow 入口：
  - `path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md`

## 4. 唯一功能入口
- [analysis_loop]：`path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md`
  - 作用：对单个目标技能执行标准化治理闭环。

## 5. 读取原则
- 始终先识别目标技能当前真实状态，再进入目标态收敛；不能把现状直接覆盖成目标态描述。
- 始终以 `Functional-Analysis-Runtask` 为主闭环，以其余治理技能为约束源，而不是并列拼接多个独立闭环。
- 若目标技能不涉及 Python 或 CLI，不应强行扩张到 tooling-heavy 改造。
- 若目标技能需要重写，应优先朝最终形态一次性收敛，而不是叠兼容层或 legacy wrapper。

## 6. 结构索引
```text
SkillsManager-GovTargetSkill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── governance/
│   └── routing/
└── path/
    └── analysis_loop/
        ├── 00_ANALYSIS_LOOP_ENTRY.md
        ├── 10_CONTRACT.md
        ├── 20_WORKFLOW_INDEX.md
        ├── 30_VALIDATION.md
        └── steps/
```
