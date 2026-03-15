---
doc_id: skillsmanager_mirror_to_codex.path.auto_routing.entry
doc_type: path_doc
topic: Auto routing entry
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: Auto routing starts from its contract.
---

# 自动导航入口

## 这个入口是干什么的
- 本入口用于定义 `auto` 模式如何在 `push` 与 `install` 之间收敛。
- 当前线路也约束 `rename` 只能显式进入，不参与自动猜测。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
