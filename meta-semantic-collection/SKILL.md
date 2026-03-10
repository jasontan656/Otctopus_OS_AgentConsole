---
name: "meta-semantic-collection"
description: "runtime 必须维护的语义词池。用于让模型在每个 turn start 自动加载用户常用词与动作语义映射，并在用户澄清语义、纠正误解或补充真实意图时自动触发本技能；必要时在 turn end 可选更新词池。"
---

# meta-semantic-collection

## 1. 目标
- 本技能是 runtime 必须维护的语义词池，负责整合用户常用词与 AI 易偏差理解之间的翻译和映射。
- 每个 turn start 默认加载词池，再进入当轮理解和执行。
- 当用户在多轮交互中补充澄清语义、纠正 AI 误解、停止当前动作并重新解释真实意图时，自动触发本技能。

## 2. 集合（json payload structure）
- 词池 payload 不直接写在 `SKILL.md` 里，真实内容固定存放在：
  - `assets/runtime/semantic_pool_payload.json`
- 模型在正常执行中不得直接阅读 payload 文件本体；必须通过 CLI 打印 runtime contract 到 console 后再遵守。
- 统一 CLI 入口：
  - `python3 scripts/Cli_Toolbox.py runtime-contract --json`
- 该命令会把 payload 包进 runtime contract 外壳，输出“本 turn 必须遵守的翻译合同”。
- payload entry schema 固定为：
  - `collection: list[str]`
  - `action_semantic_description: str`
- 硬约束：
  - 多个词可以指向一个 `action_semantic_description`
  - 一个词不能同时指向多个 `action_semantic_description`
  - prompt 命中词池后，词池语义优先覆盖模型默认理解
- 维护入口：
  - `python3 scripts/Cli_Toolbox.py upsert-payload --term "<term>" --term "<term>" --description "<semantic>" --dry-run --json`
  - `python3 scripts/Cli_Toolbox.py upsert-payload --term "<term>" --term "<term>" --description "<semantic>" --json`
- `dry-run` 只预览 diff 与 runtime contract 结果，不实际回写 JSON。
- 非 `dry-run` 模式才真正写回 payload 文件，并由脚本保证 JSON 结构合法。

## 3. 维护规则
- `turn start`：默认加载当前语义词池。
- `turn end`：若本轮出现新的有效澄清语义，可选更新词池。
- 词池本体只落在 `assets/runtime/semantic_pool_payload.json`。
- `SKILL.md` 只保留入口、规则与 CLI 用法，不再承载完整 payload。
- 当用户澄清“不是这个意思”“我的意思是……”“这里应该理解成……”这类内容时，提取：
  - 用户原词
  - 争议内容
  - 最终澄清后的动作语义
- 若澄清后的动作语义已存在，则把新的用户原词并入已有 `collection`。
- 若澄清后的动作语义不存在，则新建一个新的集合条目。
- 同一语义的不同描述方式，应收入同一个 `collection` 并指向同一个 `action_semantic_description`。
- 若一个用户原词与已有集合发生语义冲突，必须先更新映射归属，再删除旧归属，不能让一个词同时挂到多个描述下。
- 新增或更新时，优先处理“模型最容易误译”的高频词和高频澄清场景。
