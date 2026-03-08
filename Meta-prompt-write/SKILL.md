---
name: "Meta-prompt-write"
description: "将用户提示词强化为固定模板的结构化执行合同。先完整调研当前 repo 与用户目标的关系、影响面与覆盖面，再补足目标、输入、输出、边界与验证，最后仅通过固定 CLI tool 输出最终 prompt。Manual invoke: $Meta-prompt-write."
---

# Meta Prompt Write

## Overview

这个技能只有一个目的：
理解用户目标后，把用户原始 prompt 强化成**结构化执行合同**，让 agent 不需要依赖一句碎片化的“是的 / ok / 继续”去猜当前到底要做什么。

它负责补足的核心信息只有这些：
- 目标
- repo 上下文与影响面
- 输入
- 输出
- 边界
- 验证方式

## Two Uses

1. AGENTS / runtime 自动强化用户需求  
2. 手动 `$Meta-prompt-write`，要求强化某段 prompt

无论是哪一种，都必须遵守同一条主链路：
- 先调研当前 repo
- 再补足结构化执行合同
- 最后通过固定 CLI tool 输出稳定模板

## Hard Contract

- 本技能只处理 prompt / instruction / workflow 文本强化，不输出方法论报告。
- 每次输出强化后的 prompt 之前，必须先完整调研当前 repo：
  - 先看全 repo 文件清单
  - 再定位与用户目标相关的文件、模块、文档、脚本、工作流
  - 再读取与当前 prompt 真正相关的对象，补足用户没明说但 repo 已经隐含的上下文
- 必须显式判断用户 prompt 在 repo 中影响哪些面：
  - 哪些模块会被触达
  - 哪些边界需要被写进 prompt
  - 哪些输出形态需要固定
  - 哪些验证条件必须提前声明
- 最终输出必须是结构化执行合同，而不是自由发挥的 prompt 文案。
- 最终输出必须经过固定 CLI tool 限形，禁止输出形态漂移。

## Fixed Output Shape

最终 prompt 固定为 6 段：
- `GOAL:`
- `REPO_CONTEXT_AND_IMPACT:`
- `INPUTS:`
- `OUTPUTS:`
- `BOUNDARIES:`
- `VALIDATION:`

不允许再输出：
- methodology mode
- impact matrix
- rollback narrative
- evaluation witness
- edit override
- 任意临时自创键名

## Workflow

1. 读取用户原始目标或原始 prompt。
2. 完整调研当前 repo，判断它与用户目标的关系、影响面、覆盖面。
3. 补足用户未明说但执行所必须的：
   - 真实目标
   - 相关输入
   - 预期输出
   - 执行边界
   - 验证方法
4. 先写出 `raw_prompt_output`。
5. 必须调用 `scripts/filter_active_invoke_output.py` 生成固定模板最终稿。
6. 只发布 tool 过滤后的最终 prompt。

## CLI Tool

- Script: `scripts/filter_active_invoke_output.py`
- 支持两种模式：
  - `active_invoke`
  - `skill_directive`

`active_invoke` 用途：
- 把已经补足的 `raw_prompt_output` 固定成稳定模板

`skill_directive` 用途：
- 仅给 AGENTS / runtime 打印“去读哪个 skill”的轻量指引

## Manual Invoke

手动强化 prompt：
```bash
python3 /home/jasontan656/.codex/skills/Meta-prompt-write/scripts/filter_active_invoke_output.py \
  --mode active_invoke \
  --input-text "<RAW_PROMPT_OUTPUT>"
```

其中 `<RAW_PROMPT_OUTPUT>` 必须已经包含 repo 调研后的合同信息，而不是只有一句原始用户话术。

## Runtime Helper

给 AGENTS / runtime 使用：
```bash
python3 /home/jasontan656/.codex/skills/Meta-prompt-write/scripts/filter_active_invoke_output.py \
  --mode skill_directive \
  --input-text "<USER_INTENT_TEXT>"
```

## Guardrails

- 不要跳过 repo 调研。
- 不要只根据用户一句短话术直接拼 prompt。
- 不要输出自由形态结构。
- 不要发明临时键名。
- 不要把技能写成 prompt 工程理论课。

## References

- `references/active-invoke-filter-contract.md`
- `references/templates/active_invoke_prompt_template_v1.txt`
