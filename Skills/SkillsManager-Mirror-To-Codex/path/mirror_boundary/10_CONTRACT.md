---
doc_id: skillsmanager_mirror_to_codex.path.mirror_boundary.contract
doc_type: contract_doc
topic: Mirror boundary contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the boundary contract, read the resolution commands and helper behavior.
---

# 镜像边界合同

## 当前动作的目标
- 统一 mirror 根、codex 根和 skills 容器的解析方式。
- 只发现真正可同步的技能根。

## 当前动作必须满足的约束
- mirror 根优先使用当前 repo，再退回受管环境变量与可见工程路径。
- 若存在 `Skills/` 子目录，则只从该容器中发现同步根；否则直接以 mirror 根为 skills 容器。
- `.system/` 只有存在受管标记时才视为可同步根。
- codex 根不允许保留 `AGENTS.md` 这类禁留项。

## 下一跳列表
- [tools]：`15_TOOLS.md`
