---
name: "2-Task-runtime-selfcheck"
description: "Manual-invoke-only post-task runtime selfcheck. 在任务运行结束后，分析上一回合中的犹豫、工具失败、脚本失败、引导不足、模型 confused 与迷宫式流程，并输出完整痛点报告和整改方案。"
---

# 2-Task-runtime-selfcheck

用于任务结束后的运行过程复盘。
它的目标不是经营一套批处理回写系统，而是直接分析上一回合运行中哪里卡住、为什么卡住、应该改哪里。

## 主轴

本技能专门处理这些运行痛点：
- 模型犹豫、来回试探、重复尝试
- 工具调用失败
- 脚本使用失败
- CLI 指引不足
- 文档缺失或说明不够
- prompt / workflow 引导不足
- 模型 confused
- 迷宫式流程：步骤过绕、分叉过多、回退路径不清

本技能要回答的核心问题只有四个：
1. 上一回合到底卡在了哪里
2. 为什么会卡
3. 应该改哪一层
4. 下一次怎样避免再次发生

## Execution Contract (Hard)

- 仅手动触发：只有用户明确输入 `$2-Task-runtime-selfcheck` 或明确点名此技能时才允许执行。
- 默认使用场景是某次任务或某一回合运行结束后，立刻复盘刚刚那次过程。
- 默认目标是输出痛点报告和完整整改方案，而不是直接进入大规模 repair orchestration。
- 数据源来自外部 pain provider；本技能把它当证据来源，不把 provider 协议本身当技能主叙事。
- 分析必须面向“上一回合运行过程”组织，不要把回答写成抽象框架说明书。
- 整改方案必须落到具体改动对象：文档、脚本代码、CLI 指引、prompt、workflow、tool wrapper、约束文本。
- 如果某痛点的根因是引导不足、说明缺失、脚本设计不清、流程过绕，必须明确指出应该补哪一处，而不是泛泛说“加强鲁棒性”。
- 代码落盘修改不由本技能脚本自动完成；若后续真的要改文件，执行者仍需自己落盘。

## Trigger

- 默认诊断：`$2-Task-runtime-selfcheck` 或 `$2-Task-runtime-selfcheck >`
- 显式修复回写：`$2-Task-runtime-selfcheck 修复`

解释：
- 默认关注点是诊断上一回合痛点并给出完整解决方案。
- 只有用户明确要求“修复”且前置改动已经落盘时，才进入修复回写路径。

## 工作流

1. 锁定上一回合或刚结束的那次任务运行。
2. 提取其中的痛点证据：失败、犹豫、重复尝试、困惑、错误分流、无效回环。
3. 判断痛点属于哪一层：
   - 文档层
   - 脚本/代码层
   - CLI 指引层
   - prompt / instruction 层
   - workflow / routing 层
4. 输出完整痛点报告。
5. 给出完整整改方案，说明应该改哪里、改成什么、为什么这样改。
6. 若用户明确要求 `修复`，再进入修复回写路径。

## 输出要求

输出必须直接服务于“下次不再卡住”。

至少要包含：
- `发生了什么`：上一回合在哪一步卡住
- `为什么会卡`：根因，不要只复述表面报错
- `应该改哪里`：文档 / 脚本 / CLI / prompt / workflow / tool wrapper
- `怎么改`：完整整改方案
- `预期改善`：改完后下一次运行会少掉什么犹豫或失败

如果需要给结构化报告，优先保证以下信息密度：
- 痛点摘要
- 关键证据
- 根因判断
- 改动目标
- 整改步骤
- 验证方式

## Script Entrypoint

- Script: `scripts/runtime_pain_batch.py`

默认诊断：
```bash
python3 /home/jasontan656/.codex/skills/2-Task-runtime-selfcheck/scripts/runtime_pain_batch.py \
  ">" \
  --session-scope-mode all_threads \
  --max-results 200
```

显式修复回写：
```bash
python3 /home/jasontan656/.codex/skills/2-Task-runtime-selfcheck/scripts/runtime_pain_batch.py \
  修复 \
  --manual-repair-applied \
  --manual-repair-path /abs/path/to/changed_file.py \
  --verify-cmd "<verify_cmd>"
```

## Guardrails

- 不要把技能重点写成字段清单、聚类统计清单、批处理运营说明。
- 不要把回答写成抽象治理语言；必须围绕刚结束的那次运行来写。
- 不要只说“工具失败了”，必须说明为什么失败、应该补什么。
- 不要只给方向，必须给可执行整改方案。
- 未明确要求 `修复` 时，不进入修复回写叙事。

## 语言规则

- 对话输出必须使用**中文**。
- 起草文档时默认使用**中文**，除非用户另有指定。
- 代码块、代码注释和代码文件必须使用**English**；不要在代码中引入中文。
