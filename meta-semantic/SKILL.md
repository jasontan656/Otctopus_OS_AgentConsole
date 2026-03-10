---
name: "meta-semantic"
description: "语义集合收敛与用户表达归一化。用于当用户希望模型长期维护一组稳定的术语映射、动作边界、禁止误解规则和 prompt 翻译约定时；尤其适用于先把口语化指令翻译成精确执行语义，再继续执行，例如把“清理掉”解释为删除且不留痕，而不是备份、注释或保留兼容残留。"
---

# meta-semantic

## 1. 目标
- 让模型先读取用户约定的语义集合，再把当前 prompt 中的自然语言表达翻译成可执行意图。
- 降低“模型默认常识”对用户自定义语义的覆盖，长期收敛同一套词义、动作边界与禁忌解释。

## 2. 可用工具
- 抽象层：
  - 本技能当前不提供 CLI，不提供脚本入口，不提供 machine runtime contract。
  - 运行时依据 `SKILL.md` 与 `references/` 中的语义规范执行。
- 业务需求层：
  - `semantic-normalization`：
    - 读取 [references/semantic-canon.md](references/semantic-canon.md) 中的术语映射、动作拆解、非等价解释与冲突优先级。
  - `prompt-translation`：
    - 读取 [references/prompt-translation.md](references/prompt-translation.md) 中的翻译流程，把用户原话改写为精确执行语义。

## 3. 工作流约束
- 抽象层：
  - 先识别用户是否显式提到本技能，或当前任务是否明显在建立、对齐、修正语义集合。
  - 一旦触发，先归一化语义，再进入后续分析、编码、评审或执行动作。
- 业务需求层：
  - `semantic-normalization`：
    - 提取 prompt 中的关键词、动作词、边界词和否定词。
    - 优先匹配已有语义条目；若匹配成功，采用用户定义含义覆盖模型默认含义。
    - 若未命中现有条目，只做最小保守推断，不自行扩展为“看起来更安全”的替代动作。
  - `prompt-translation`：
    - 把原始表达翻译为简明的执行语义。
    - 显式保留禁止项，例如“不备份”“不注释”“不保留兼容层”“不留痕”。
    - 仅在语义仍存在实质性歧义时才向用户追问。

## 4. 规则约束
- 抽象层：
  - 用户语义优先级高于模型默认 best practice、高于常见工程习惯、高于“保守解释”。
  - 不得把“清理掉”“删掉”“去掉”“移除掉”自动翻译成“备份后删除”“注释替代删除”或“先保留兼容残留”。
  - 不得因为害怕破坏而擅自引入用户未要求的缓冲层、兼容层、临时别名或旁路实现。
  - 若用户显式给出语义映射，应按映射执行；若现有语义库与本轮 prompt 冲突，应以本轮更具体的约束为准。
- 业务需求层：
  - `semantic-normalization`：
    - 语义条目必须至少写清楚：原始表达、归一化意图、必须包含、明确排除。
    - 遇到近义词时，先判断是否 truly equivalent；不能因为“差不多”就合并。
  - `prompt-translation`：
    - 翻译后的执行语义应尽量短句化、动作化、约束可检查。
    - 若需要补充假设，必须把假设标成推断，不能伪装成用户原意。

## 5. 方法论约束
- 抽象层：
  - 先对齐词义，再执行动作；不要先执行再事后解释。
  - 用“显式包含 + 显式排除”的方式定义术语，避免只写正向含义。
  - 默认怀疑模型自己的惯性解释，而不是怀疑用户词义。
- 业务需求层：
  - `semantic-normalization`：
    - 优先收敛高频、易误解、易造成错误执行的词。
    - 每个条目尽量附一个反例，明确什么不算。
  - `prompt-translation`：
    - 把用户原句翻译成“动作 + 范围 + 保留项/删除项 + 禁止项”的结构。
    - 若用户句子包含情绪化或口语化表达，只提炼其执行含义，不模仿情绪。

## 6. 内联导航索引
- 抽象层：
  - [语义总表] -> [references/semantic-canon.md]
  - [Prompt 翻译协议] -> [references/prompt-translation.md]
- 业务需求层：
  - `semantic-normalization` -> [references/semantic-canon.md]
  - `prompt-translation` -> [references/prompt-translation.md]

## 7. 架构契约
```text
meta-semantic/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── semantic-canon.md
    └── prompt-translation.md
```
