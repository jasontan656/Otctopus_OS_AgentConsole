---
doc_id: skills_tooling_checkup.routing.task_routing
doc_type: routing_doc
topic: Task routing for skills tooling dependency-baseline review and remediation
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The facade still exposes a human-readable routing mirror.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: routes_to
  direction: downstream
  reason: Task routing must still pass through execution rules.
---

# Task Routing

## CLI-first 入口
- 本路由文档保留为 human reference。
- 模型运行时应先执行：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - 当目标是审计某个具体 skill 的 tooling surface 时：`./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`

## 当前分叉轴线
- 本文件只按一个语义轴线分流：当前任务是在做只读定位、实改修正，还是要求变更 repo 技术栈基线本身。

## 分支一：只读检查与问题定位
- 先用 `directive --topic read-audit`。
- 若任务涉及运行时日志、调试痕迹、默认产物或定向产物落点，再补 `directive --topic output-governance`。
- 若需要判断现有依赖是否已覆盖目标能力，再补 `directive --topic techstack-baseline`。
- 若需要典型命中样式，再读 `../governance/COMMON_REDUNDANT_WHEEL_PATTERNS.md`。
- 输出应聚焦于：哪些实现是“可能重复造轮子”、日志与产物落盘治理是否闭合、证据是什么、哪些结论仍然未知。

## 分支二：进入目标 skill 做修正
- 若当前任务首先是在审计“目标 skill 的 tooling surface”，先用 `govern-target --target-skill-root <path> --json` 拿到目标感知审计结果。
- 先用 `directive --topic remediation`。
- 再按任务需要补 `directive --topic output-governance` 与 `directive --topic techstack-baseline`。
- 若需要典型命中样式或 gates 细节，再读 `../governance/COMMON_REDUNDANT_WHEEL_PATTERNS.md` 与 `../governance/REMEDIATION_GATES.md`。
- 然后进入目标 skill 自己的 `SKILL.md -> routing -> execution/tooling docs`，按其局部合同执行改写、测试和 lint。
- 若改动落在 Python，额外纳入 `Dev-PythonCode-Constitution` 的阅读与 lint；若落在 Vue3 / TS tooling，额外纳入目标前端 skill 的既有合同。

## 分支三：用户要改 repo 必用依赖栈
- 这不是本技能单独决策的范围。
- 此分支先用 `directive --topic techstack-baseline` 对齐现有基线，再回退到 repo 合同治理链，不能在本技能内部私自新增、删除或重命名 tech stack 基线。
