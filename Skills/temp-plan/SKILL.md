---
name: "temp-plan"
description: 用于绑定长期任务、维护极简任务日志，并把协同方式、偏好、目标与任务心智模型持续注入到后续回合。
---

# Temp-Plan

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：为需要长期对齐的任务建立稳定任务目录，并把当前有效的任务语义压缩成可持续复用的最小快照。
- 本技能默认把任务日志写到 `/home/jasontan656/AI_Projects/Codex_Skills_Result/temp-plan`。
- 本技能不提供本地 `Cli_Toolbox.py`；任务日志由 AI 直接维护为 markdown。
- 本技能不是 repo 运行合同，也不替代具体领域技能。

## 2. 必读顺序
1. 先读取 `references/current_intent.md`。
2. 再读取 `references/application_contract.md`。
3. 再读取 `references/task_log_contract.md`。
4. 需要具体文件结构时，再读取 `references/task_log_schema.md`。
5. 若当前任务是创建、改造或安装新的开发技能，转入 `$SkillsManager-Creation-Template` 作为具体模板治理入口。
6. 一旦任务目录被绑定，本回合后续动作与后续相关回合都必须服从该任务快照，直到用户显式切换、拆分、归档或结束任务。

## 3. 分类入口
- 意图背景层：
  - `references/current_intent.md`
- 使用合同层：
  - `references/application_contract.md`
- 任务日志层：
  - `references/task_log_contract.md`
  - `references/task_log_schema.md`
- 治理说明层：
  - `references/tooling/`
- 模板资产层：
  - `assets/templates/`
- 运行边界层：
  - workspace/root `AGENTS.md`
  - concrete repo local `AGENTS.md`
  - `$SkillsManager-Creation-Template`

## 4. 适用域
- 适用于：任何需要跨回合持续对齐的任务，尤其是需要沉淀协同方式、偏好、目标与边界的长期任务。
- 适用于：用户希望 AI 自己维护任务日志，而不是每轮重复补充同样背景。
- 适用于：技能建设、架构整理、长期开发主题、复杂文档治理等需要持续注入上下文的任务。
- 不适用于：只做一次、无需长期状态的短平快任务。
- 不适用于：替代具体技术域技能、repo-specific 合同或脚本型工作流。

## 5. 执行入口
- 统一入口：
  - 触发本技能后，按 `references/current_intent.md -> references/application_contract.md -> references/task_log_contract.md` 的顺序读取。
- 任务绑定入口：
  - 先识别用户是在描述 `new_task` 还是 `continue_task`。
  - 任务名必须来自用户自然语言；若当前上下文已足够明确，可直接归一化为 slug；若不明确且风险高，再补问。
  - 绑定后必须创建或更新 `ACTIVE_TASK.md`、任务目录内 `TASK.md`、`TURN_LOG.md`。
- 对齐入口：
  - 进入具体任务后，先更新任务快照，再执行真实工作。
  - 若任务是新技能建设，先用本技能固化长期任务背景，再转入 `$SkillsManager-Creation-Template`。
- 合同入口：
  - 无 runtime contract；本技能的有效内容来自静态参考文档与受管结果目录。
- 资产入口：
  - `assets/templates/` 提供 `ACTIVE_TASK.md`、`TASK.md`、`TURN_LOG.md` 的最小模板。

## 6. 读取原则
- 门面只做路由，正文下沉到 `references/`。
- `TASK.md` 记录“当前仍然有效的真相”，优先替换旧语义，不堆积历史废话。
- `TURN_LOG.md` 只记录回合级增量，不重复整份快照。
- 记录风格必须最小语义、短句、关键词优先；允许中英混合，禁止长篇大论。
- 需要什么读什么，不要把所有引用文档一次性展开成新的门面正文。
- 当用户纠正偏好、边界或目标时，必须先更新任务日志，再继续执行。
- 若本技能的意图、边界、日志结构或 OK 定义变化，同步更新门面、参考文档、模板资产与 tooling 说明。

## 7. 结构索引
```text
temp-plan/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── current_intent.md
│   ├── application_contract.md
│   ├── task_log_contract.md
│   ├── task_log_schema.md
│   └── tooling/
└── assets/
    └── templates/
```
