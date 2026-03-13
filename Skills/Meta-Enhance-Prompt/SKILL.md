---
name: Meta-Enhance-Prompt
description: '将用户提示词强化为固定模板的结构化执行合同。先完整调研当前 repo 与用户目标的关系、影响面与覆盖面，再补足目标、输入、输出、边界与验证，最后仅通过固定 CLI tool 输出最终 prompt。Manual invoke: $Meta-Enhance-Prompt.'
metadata:
  doc_structure:
    doc_id: meta_enhance_prompt.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Meta-Enhance-Prompt skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Meta Enhance Prompt

## 1. 定位
- 本技能用于把用户原始 prompt 强化成固定六段的结构化执行合同。
- 本技能只治理 prompt / instruction / workflow 的强化输出，不承担 repo 调研的替代执行，也不输出方法论报告。
- 本技能的模型运行时入口已经切换为 CLI-first；`SKILL.md` 只保留人类门面与路由叙事。

## 2. 工具入口
- 统一 runtime 入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py directive --topic <topic> --json`
- 结构化合同过滤入口：
  - `python3 scripts/filter_active_invoke_output.py --mode active_invoke --input-text "<RAW_PROMPT_OUTPUT>" --json`
  - `python3 scripts/filter_active_invoke_output.py --mode skill_directive --input-text "<USER_INTENT_TEXT>" --json`
- 模型读取合同、workflow、instruction、guide 时必须优先消费 CLI JSON；human markdown 只作为叙事镜像。

## 3. 必读顺序
1. 先执行 `scripts/Cli_Toolbox.py contract --json`。
2. 再按任务意图读取 directive：
   - 强化结构化合同：`--topic active-invoke`
   - 运行时入口提示：`--topic skill-directive`
   - 日志与结果治理：`--topic output-governance`
3. 真正执行 `filter_active_invoke_output.py` 前，必须先完成 repo 调研并产出包含六段信息的 `raw_prompt_output`。
4. 只有当 CLI JSON 仍留有真实语义缺口时，才打开 human mirror 或模板文件。

## 4. 运行时约束
- 最终合同固定为 6 段：
  - `GOAL:`
  - `REPO_CONTEXT_AND_IMPACT:`
  - `INPUTS:`
  - `OUTPUTS:`
  - `BOUNDARIES:`
  - `VALIDATION:`
- `active_invoke` 不允许用默认占位文案伪造缺失段落；缺段必须失败。
- `skill_directive` 不再把模型路由回 `SKILL.md`，而是返回 CLI-first 入口指引。
- 运行时日志默认治理到受管 runtime root；结果文件默认治理到受管 result root，并支持显式 `--output-path`。

## 5. 参考入口
- Runtime 合同：`references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
- Directive 索引：`references/runtime_contracts/DIRECTIVE_INDEX.json`
- Human mirrors：`references/runtime_contracts/*_human.md`
- 模板：`references/templates/active_invoke_prompt_template_v1.txt`

## 6. 结构索引
```text
Meta-Enhance-Prompt/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── runtime_contracts/
│   └── templates/
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── filter_active_invoke_output.py
│   ├── filter_prompt_shape_helper.py
│   ├── filter_runtime_governance.py
│   └── filter_skill_directive_support.py
└── tests/
```
