---
doc_id: skillsmanager_mirror_to_codex.path.auto_routing.execution
doc_type: execution_doc
topic: Auto routing execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate that auto routing selected the correct mode.
---

# 自动导航实施

## 执行顺序
1. 解析 codex root 与 mirror root。
2. 归一化 `skill_name`，并在 skills 边界内锁定源目录与目标目录。
3. 若显式指定 `rename`，走 rename 闭环并停止自动判断。
4. 若显式指定 `push` 或 `install`，直接进入指定模式。
5. 若仍为 `auto`，根据目标目录是否已存在，在 `push` 与 `install` 之间收敛。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
