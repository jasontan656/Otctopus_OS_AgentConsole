---
doc_id: skillsmanager_doc_structure.path.primary_flow.execution
doc_type: topic_atom
topic: Execution sequence for the primary doc-structure governance flow
reading_chain:
- key: target_shape
  target: 21_TARGET_SHAPE.md
  hop: next
  reason: Execution starts from target-shape resolution.
---

# 主治理链路执行

## 当前动作
1. 先读取目标技能 `SKILL.md` 顶层 `skill_mode`，或从实际根形态推断组织形态。
2. 再检查目标技能根目录是否只保留目标态允许的根节点。
3. 再检查 `SKILL.md` 是否只保留门面职责，并把读者送向唯一的下一级。
4. 再检查 `path/` 内部是否按物理目录逐级下沉，而不是把后续文件平铺后靠内联硬控读序。
5. 最后检查 reading-chain 是否只指向存在的必要节点。

## 下一跳列表
- [目标技能形态判定]：`21_TARGET_SHAPE.md`
