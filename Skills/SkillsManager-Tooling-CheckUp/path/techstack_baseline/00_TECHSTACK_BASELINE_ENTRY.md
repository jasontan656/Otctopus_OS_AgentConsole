---
doc_id: skillsmanager_tooling_checkup.path.techstack_baseline.entry
doc_type: path_doc
topic: Action-loop entry for techstack baseline checking
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: baseline checking starts from the contract doc.
---

# 依赖基线检查入口

## 这个入口是干什么的
- 本入口只服务目标技能的依赖基线检查。
- 当前线路用于判断：目标技能是否在 repo 已声明依赖已经覆盖的范围内，继续手写通用能力。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
