---
doc_id: skillsmanager_python_subagentgov.references.policies.skill_execution_rules
doc_type: policy
topic: Execution rules for the Python subagent governance controller
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The execution policy explains the controller boundary promised by the facade.
---

# Skill Execution Rules

## 1. 主控与 subagent 分工
- 主控负责：
  - 发现目标技能
  - 维持最多 4 个并发 subagent
  - 轮询完成状态
  - 串行执行 `verify -> commit-and-push -> mirror sync -> session closeout`
  - 写入 `controller_status.json` 与单技能 `closure.json`
- 单技能 subagent 负责：
  - 只修改一个目标技能目录
  - 按 `Meta-refactor-behavior` 先定义 OEC
  - 仅依据 `Dev-PythonCode-Constitution` 审查和修复 Python 代码规范问题
  - 把结果写入 `result.json` 与 `result.md`

## 2. 行为保持边界
- 只允许对目标技能做行为保持型重构，不新增未经批准的语义，不丢失既有语义。
- 至少要取得一个明确的代码质量增益；若无须改动，也必须产出 `success_no_change` 证据。
- 若验证发现必须改动目标技能之外的文件才能收敛，单技能 subagent 必须返回失败，而不是扩散修改。

## 3. Runtime 边界
- 所有临时文件、prompt、日志、结果、closeout 证据都只能写入 `Codex_Skill_Runtime/SkillsManager-Python-SubAgentGov/`。
- 单技能 runtime 目录是：
  - `Codex_Skill_Runtime/SkillsManager-Python-SubAgentGov/<skill_name>/`
- 严禁把已安装的 `~/.codex/skills/<skill_name>` 当作治理源。

## 4. Git 与 Mirror 边界
- Git traceability 必须通过 `Meta-github-operation` 的受管 CLI 完成。
- mirror sync 必须通过 `SkillsManager-Mirror-To-Codex` 的受管 CLI 完成。
- remote write 只能串行执行；主控不得并行 push。
- 本技能默认只允许写 repo truth source，并在 closeout 阶段再同步安装镜像。

## 5. 自治理边界
- 在 `list-targets` 与 `govern` 的 all-scope 默认发现中，本技能自身会被排除。
- 若用户显式要求治理本技能自身，必须走单技能模式，避免运行中的控制器被批处理中途改写。
