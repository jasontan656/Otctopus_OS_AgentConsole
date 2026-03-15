---
doc_id: skillsmanager_tooling_checkup.path.techstack_baseline.contract
doc_type: topic_atom
topic: Contract for techstack baseline checking
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: baseline contract is followed by the applicable tooling surface.
---

# 依赖基线检查合同

## 当前动作要完成什么
- 判定目标技能的自实现是否与 repo 既定依赖栈能力重叠。
- 只处理“已有依赖已能覆盖，却仍手写通用能力”的情况。

## 当前动作必须满足什么
- 唯一强制基线是 repo 的 `skills_required_techstacks`。
- 不能因为某个库“更标准”就自行新增依赖要求。
- 只有在替换后不丢失目标技能现有行为语义时，才允许进入整改。
- 若自实现仍承载 repo-specific orchestration、兼容语义或域内规则，则只能缩小通用部分，不能整体抽空。

## 下一跳列表
- [tools]：`15_TOOLS.md`
